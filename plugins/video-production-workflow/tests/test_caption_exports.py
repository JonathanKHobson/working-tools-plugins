from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from video_workflow.caption_exports import CaptionExportError, export_caption_variants
from video_workflow.cli import main


def fixture(root: Path) -> tuple[Path, dict]:
    cues = [
        {"id": "part-1", "startSeconds": 0.1, "endSeconds": 1.0, "text": "Try first.\nExplain why."},
        {"id": "part-1", "startSeconds": 1.5, "endSeconds": 2.0, "text": "Ask for a hint."},
        {"id": "part-2", "startSeconds": 5.1, "endSeconds": 6.0, "text": "Check the source & again again."},
    ]
    cue_path = root / "reviewed.cues.json"
    cue_path.write_text(json.dumps(cues))
    manifest = {"schemaVersion": 1, "cues": {"path": cue_path.name, "sha256": digest(cue_path)},
                "outputs": [
                    {"id": "part-2", "segments": [{"sourceIn": 5, "sourceOut": 7}]},
                    {"id": "full", "segments": [{"sourceIn": 0, "sourceOut": 7}]},
                    {"id": "short", "segments": [{"sourceIn": 0, "sourceOut": 1.1, "speed": 1.1},
                                                    {"sourceIn": 5, "sourceOut": 6.1, "speed": 1.1}]},
                ]}
    path = root / "exports.json"
    path.write_text(json.dumps(manifest))
    return path, manifest


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path: Path, manifest: dict) -> None:
    path.write_text(json.dumps(manifest))


def test_batch_offsets_speed_join_and_verbatim_text(tmp_path: Path) -> None:
    path, _ = fixture(tmp_path)
    out = tmp_path / "captions"
    report = export_caption_variants(path, out)
    assert report["filesWritten"] == 4
    assert (out / "part-2.srt").read_text() == "1\n00:00:00,100 --> 00:00:01,000\nCheck the source & again again.\n\n"
    assert "00:00:05,100 --> 00:00:06,000" in (out / "full.srt").read_text()
    assert (out / "short.srt").read_text() == (
        "1\n00:00:00,091 --> 00:00:00,909\nTry first.\nExplain why.\n\n"
        "2\n00:00:01,091 --> 00:00:01,909\nCheck the source & again again.\n\n")
    receipt = json.loads((out / "caption-export-receipt.json").read_text())
    assert receipt["manifestSha256"] == digest(path)
    assert receipt["cues"]["sha256"] == digest(tmp_path / "reviewed.cues.json")
    assert receipt["outputs"][2]["durationSeconds"] == 2.0
    assert receipt["outputs"][2]["sha256"] == digest(out / "short.srt")
    assert export_caption_variants(path, out)["filesWritten"] == 0


@pytest.mark.parametrize("start,end", [(0.5, 1.1), (0, 0.8)])
def test_reject_partial_cues_before_any_write(tmp_path: Path, start: float, end: float) -> None:
    path, manifest = fixture(tmp_path)
    manifest["outputs"][2]["segments"][0].update(sourceIn=start, sourceOut=end)
    save(path, manifest)
    with pytest.raises(CaptionExportError, match="cuts through cue"):
        export_caption_variants(path, tmp_path / "out")
    assert not (tmp_path / "out").exists()


def test_hash_change_and_dry_run_preserve_sources(tmp_path: Path) -> None:
    path, _ = fixture(tmp_path)
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    report = export_caption_variants(path)
    assert report["status"] == "validated" and report["filesWritten"] == 0
    assert before == {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    (tmp_path / "reviewed.cues.json").write_text("[]")
    with pytest.raises(CaptionExportError, match="sha256 mismatch"):
        export_caption_variants(path)


@pytest.mark.parametrize("value", [0, -1, True, float("nan"), float("inf")])
def test_reject_invalid_speed(tmp_path: Path, value: float) -> None:
    path, manifest = fixture(tmp_path)
    manifest["outputs"][0]["segments"][0]["speed"] = value
    save(path, manifest)
    with pytest.raises(CaptionExportError):
        export_caption_variants(path)


def test_duplicate_id_reverse_or_overlapping_segments_rejected(tmp_path: Path) -> None:
    path, manifest = fixture(tmp_path)
    manifest["outputs"][1]["id"] = "part-2"
    save(path, manifest)
    with pytest.raises(CaptionExportError, match="duplicate"):
        export_caption_variants(path)
    manifest["outputs"][1]["id"] = "full"
    manifest["outputs"][2]["segments"] = [{"sourceIn": 5, "sourceOut": 7}, {"sourceIn": 0, "sourceOut": 1.1}]
    save(path, manifest)
    with pytest.raises(CaptionExportError, match="ordered"):
        export_caption_variants(path)


def test_existing_different_output_not_overwritten(tmp_path: Path) -> None:
    path, _ = fixture(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "short.srt").write_text("approved older artifact")
    with pytest.raises(CaptionExportError, match="existing output differs"):
        export_caption_variants(path, out)
    assert sorted(p.name for p in out.iterdir()) == ["short.srt"]


def test_submillisecond_cue_cannot_collapse_at_srt_precision(tmp_path: Path) -> None:
    path, manifest = fixture(tmp_path)
    cue_path = tmp_path / "reviewed.cues.json"
    cues = json.loads(cue_path.read_text())
    cues[0].update(startSeconds=0.1001, endSeconds=0.1002)
    cue_path.write_text(json.dumps(cues))
    manifest["cues"]["sha256"] = digest(cue_path)
    save(path, manifest)
    with pytest.raises(CaptionExportError, match="millisecond"):
        export_caption_variants(path)


def test_cli_default_read_only_and_explicit_output(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    path, _ = fixture(tmp_path)
    assert main(["export-captions", str(path)]) == 0
    assert json.loads(capsys.readouterr().out)["filesWritten"] == 0
    assert main(["export-captions", str(path), "--output", str(tmp_path / "out")]) == 0
    assert json.loads(capsys.readouterr().out)["filesWritten"] == 4


def test_reject_symlink_destination_and_source_collision(tmp_path: Path) -> None:
    path, manifest = fixture(tmp_path)
    out = tmp_path / "out"
    out.mkdir()
    (out / "part-2.srt").symlink_to(tmp_path / "reviewed.cues.json")
    with pytest.raises(CaptionExportError, match="symbolic link"):
        export_caption_variants(path, out)
    before = path.read_bytes()
    collision = tmp_path / "full.srt"
    collision.write_bytes(before)
    with pytest.raises(CaptionExportError, match="overwrite"):
        export_caption_variants(collision, tmp_path)
    assert collision.read_bytes() == before


@pytest.mark.parametrize("changes", [{"startSeconds": -1}, {"endSeconds": 0.05},
                                     {"text": " "}, {"text": "two\n\nparagraphs"}])
def test_reject_invalid_reviewed_cues(tmp_path: Path, changes: dict) -> None:
    path, manifest = fixture(tmp_path)
    cue_path = tmp_path / "reviewed.cues.json"
    cues = json.loads(cue_path.read_text())
    cues[0].update(changes)
    cue_path.write_text(json.dumps(cues))
    manifest["cues"]["sha256"] = digest(cue_path)
    save(path, manifest)
    with pytest.raises(CaptionExportError):
        export_caption_variants(path)


def test_unsupported_extreme_timing_returns_actionable_cli_error(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    path, manifest = fixture(tmp_path)
    manifest["outputs"][0]["segments"][0]["speed"] = 1e-300
    save(path, manifest)
    assert main(["export-captions", str(path)]) == 1
    assert "decimal precision" in capsys.readouterr().err
