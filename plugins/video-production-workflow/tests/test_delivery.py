import hashlib
import json
from pathlib import Path

import pytest
from PIL import Image

from video_workflow.delivery import DeliveryError, preflight_delivery


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture
def delivery(tmp_path, monkeypatch):
    from video_workflow import delivery as module
    render = tmp_path / "render.mp4"
    render.write_bytes(b"synthetic render")
    (tmp_path / "captions.srt").write_text("1\n00:00:00,000 --> 00:00:01,000\nHello\n")
    (tmp_path / "transcript.txt").write_text("Hello")
    Image.new("RGB", (90, 160)).save(tmp_path / "cover.png")
    monkeypatch.setattr(module, "probe_media", lambda path: {
        "video": {"width": 1080, "height": 1920}, "format": {"duration": 30.0}})
    item = {"id": "short-one", "format": "portrait", "files": {
        role: {"path": name, "sha256": digest(tmp_path / name)}
        for role, name in {"render": "render.mp4", "captions": "captions.srt",
                           "transcript": "transcript.txt", "cover": "cover.png"}.items()}}
    item["files"]["render"].update(width=1080, height=1920, durationSeconds=30)
    item["files"]["captions"]["renderSha256"] = digest(render)
    item["files"]["transcript"]["renderSha256"] = digest(render)
    item["reviews"] = {}
    for kind, roles in {"visual": ["render"], "captions": ["render", "captions"],
                        "transcript": ["render", "transcript"],
                        "cover": ["cover"], "audio": ["render"]}.items():
        item["reviews"][kind] = {"status": "passed", "evidence": "Reviewed synthetic fixture",
                                "hashes": {role: item["files"][role]["sha256"] for role in roles}}
    manifest = {"schemaVersion": 1, "items": [item]}
    path = tmp_path / "delivery.json"
    def check():
        path.write_text(json.dumps(manifest))
        before = {p: p.read_bytes() for p in tmp_path.iterdir() if p.is_file()}
        result = preflight_delivery(path)
        assert before == {p: p.read_bytes() for p in tmp_path.iterdir() if p.is_file()}
        return result
    return manifest, item, tmp_path, check


def codes(report):
    return {issue["code"] for issue in report["items"][0]["issues"]}


def test_complete_delivery_is_read_only_and_deterministic(delivery):
    _, _, _, check = delivery
    first = check()
    assert first == check()
    assert first["passed"] and first["items"][0]["localHandoffReady"]
    assert first["summary"]["ready"] == 1
    assert first["items"][0]["nextActions"] == []
    assert "publication" in first["boundary"]


def test_portrait_cover_cannot_be_a_landscape_image(delivery):
    _, item, root, check = delivery
    Image.new("RGB", (160, 90)).save(root / "cover.png")
    item["files"]["cover"]["sha256"] = digest(root / "cover.png")
    assert "aspect-mismatch" in codes(check())


def test_missing_assets_are_reported_together(delivery):
    _, _, root, check = delivery
    (root / "cover.png").unlink()
    (root / "transcript.txt").unlink()
    result = check()
    assert sum(i["code"] == "missing-file" for i in result["items"][0]["issues"]) == 2
    assert not result["passed"]


def test_changed_bytes_invalidate_review_even_at_same_path(delivery):
    _, _, root, check = delivery
    (root / "render.mp4").write_bytes(b"new render")
    report = check()
    assert {"hash-mismatch", "stale-review", "caption-render-mismatch"} <= codes(report)


def test_declared_duration_and_size_use_actual_files(delivery):
    _, item, _, check = delivery
    item["files"]["render"].update(durationSeconds=45, maxBytes=1)
    assert {"duration-mismatch", "size-exceeded"} <= codes(check())


def test_review_without_hash_binding_is_pending(delivery):
    _, item, _, check = delivery
    item["reviews"]["cover"]["hashes"] = {}
    result = check()
    assert "stale-review" in codes(result)
    assert result["items"][0]["filesPassed"]
    assert not result["items"][0]["localHandoffReady"]


def test_optional_square_course_card_and_explicit_limits(delivery):
    _, item, root, check = delivery
    Image.new("RGB", (100, 80)).save(root / "card.png")
    item["files"]["courseCard"] = {"path": "card.png", "sha256": digest(root / "card.png"),
                                  "minWidth": 128, "minHeight": 128}
    assert {"aspect-mismatch", "dimensions-too-small"} <= codes(check())


def test_review_hold_is_preserved_and_not_called_passed(delivery):
    _, item, _, check = delivery
    item["reviews"]["audio"]["status"] = "not-performed"
    assert "review-pending" in codes(check())


@pytest.mark.parametrize("bad_value", [0, -1, True, float("nan")])
def test_invalid_numeric_expectations_fail(delivery, bad_value):
    _, item, _, check = delivery
    item["files"]["render"]["width"] = bad_value
    assert "invalid-expectation" in codes(check())


def test_duplicate_local_id_is_rejected(delivery):
    manifest, item, _, check = delivery
    manifest["items"].append(item)
    with pytest.raises(DeliveryError, match="duplicate"):
        check()


def test_cache_reuses_hash_and_probe_within_one_batch(delivery, monkeypatch):
    from video_workflow import delivery as module
    manifest, item, _, check = delivery
    other = json.loads(json.dumps(item))
    other["id"] = "short-two"
    manifest["items"].append(other)
    counts = {"probe": 0, "hash": 0}
    real_hash = module.sha256_file
    def counted_probe(path):
        counts["probe"] += 1
        return {"video": {"width": 1080, "height": 1920}, "format": {"duration": 30.0}}
    def counted_hash(path):
        counts["hash"] += 1
        return real_hash(path)
    monkeypatch.setattr(module, "probe_media", counted_probe)
    monkeypatch.setattr(module, "sha256_file", counted_hash)
    assert check()["passed"]
    assert counts == {"probe": 1, "hash": 4}


def test_updated_transcript_hash_does_not_reuse_old_review(delivery):
    _, item, root, check = delivery
    (root / "transcript.txt").write_text("A different transcript")
    item["files"]["transcript"]["sha256"] = digest(root / "transcript.txt")
    assert "stale-review" in codes(check())


def test_optional_card_requires_review_of_its_exact_bytes(delivery):
    _, item, root, check = delivery
    Image.new("RGB", (100, 100)).save(root / "card.png")
    item["files"]["courseCard"] = {"path": "card.png", "sha256": digest(root / "card.png")}
    assert "stale-review" in codes(check())
    item["reviews"]["cover"]["hashes"]["courseCard"] = digest(root / "card.png")
    assert check()["passed"]


def test_same_size_change_during_batch_is_detected(delivery, monkeypatch):
    from video_workflow import delivery as module
    manifest, item, root, check = delivery
    other = json.loads(json.dumps(item))
    other["id"] = "short-two"
    manifest["items"].append(other)
    real_hash = module.sha256_file
    def change_previous_file(path):
        value = real_hash(path)
        if Path(path).name == "transcript.txt":
            (root / "render.mp4").write_bytes(b"Synthetic render")
        return value
    monkeypatch.setattr(module, "sha256_file", change_previous_file)
    path = root / "delivery.json"
    path.write_text(json.dumps(manifest))
    result = preflight_delivery(path)
    assert not result["passed"]
    assert any(i["code"] == "inspection-failed" for i in result["items"][1]["issues"])


def test_expected_audio_is_not_assumed_from_video_extension(delivery):
    _, item, _, check = delivery
    item["files"]["render"]["requireAudio"] = True
    assert "missing-audio" in codes(check())


def test_misspelled_constraint_is_not_silently_ignored(delivery):
    _, item, _, check = delivery
    item["files"]["cover"]["maxByets"] = 1
    assert "unknown-field" in codes(check())


def test_unbound_transcript_is_not_ready(delivery):
    _, item, _, check = delivery
    item["files"]["transcript"].pop("renderSha256")
    assert "transcript-render-mismatch" in codes(check())


def test_cli_probes_real_media_without_writing(tmp_path, capsys):
    from video_workflow.cli import main
    from video_workflow.probe import probe_media
    render = Path(__file__).resolve().parents[1] / "examples/multi-aspect-variants/output/vertical/preview.mp4"
    probe = probe_media(render)
    spec = {"schemaVersion": 1, "items": [{"id": "real-probe", "format": "portrait", "files": {
        "render": {"path": str(render), "sha256": digest(render),
                   "width": probe["video"]["width"], "height": probe["video"]["height"],
                   "durationSeconds": probe["format"]["duration"]}}}]}
    manifest = tmp_path / "delivery.json"
    manifest.write_text(json.dumps(spec))
    before = digest(render)
    assert main(["preflight-delivery", str(manifest)]) == 2
    result = json.loads(capsys.readouterr().out)
    assert result["items"][0]["files"]["render"]["height"] == 640
    assert digest(render) == before
    assert list(tmp_path.iterdir()) == [manifest]
