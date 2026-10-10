from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from video_workflow.course_media import CourseMediaError, package_course_media


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "package_course_media.py"


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _fixture(root: Path) -> tuple[Path, dict]:
    (root / "first.mp4").write_bytes(b"first source")
    (root / "second.mp4").write_bytes(b"second source")
    (root / "first.srt").write_text(
        "1\n00:00:00,100 --> 00:00:00,500\n<b>Hello</b> & again again\nsecond line\n\n"
        "2\n00:00:01,200 --> 00:00:01,250\nLast word\n", encoding="utf-8"
    )
    (root / "second.srt").write_text(
        "1\n00:00:00,100 --> 00:00:00,400\nWelcome back\n", encoding="utf-8"
    )
    manifest = {
        "schemaVersion": 1,
        "id": "lesson-demo",
        "clips": [
            {"id": "part-a", "title": "Part A", "source": "first.mp4", "sha256": _hash(root / "first.mp4"),
             "durationSeconds": 1.25, "captions": "first.srt"},
            {"id": "part-b", "title": "Part B", "source": "second.mp4", "sha256": _hash(root / "second.mp4"),
             "durationSeconds": 2.5, "captions": "second.srt"},
        ],
    }
    path = root / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path, manifest


def _save(path: Path, manifest: dict) -> None:
    path.write_text(json.dumps(manifest), encoding="utf-8")


def test_offsets_corrections_and_receipt(tmp_path: Path) -> None:
    path, manifest = _fixture(tmp_path)
    manifest["corrections"] = [{"clipId": "part-b", "cueIndex": 0, "before": "Welcome back",
                                 "after": "Welcome, back", "reason": "Reviewed against recording"}]
    (tmp_path / "delivery.mp4").write_bytes(b"delivery")
    manifest["delivery"] = {"path": "delivery.mp4", "sha256": _hash(tmp_path / "delivery.mp4"),
                            "maxBytes": 100, "durationSeconds": 3.75}
    _save(path, manifest)
    out = tmp_path / "package"
    summary = package_course_media(path, out)
    assert summary["filesWritten"] == 5
    cues = json.loads((out / "lesson-demo.cues.json").read_text())
    chapters = json.loads((out / "lesson-demo.chapters.json").read_text())
    receipt = json.loads((out / "package-receipt.json").read_text())
    assert chapters == [{"id": "part-a", "title": "Part A", "startSeconds": 0.0},
                        {"id": "part-b", "title": "Part B", "startSeconds": 1.25}]
    assert cues == [
        {"id": "part-a", "startSeconds": 0.1, "endSeconds": 0.5,
         "text": "Hello & again again\nsecond line"},
        {"id": "part-a", "startSeconds": 1.2, "endSeconds": 1.25, "text": "Last word"},
        {"id": "part-b", "startSeconds": 1.35, "endSeconds": 1.65, "text": "Welcome, back"},
    ]
    vtt = (out / "lesson-demo.vtt").read_text()
    assert "00:00:01.350 --> 00:00:01.650" in vtt
    assert "Hello &amp; again again\nsecond line" in vtt
    assert "<b>" not in vtt
    assert "again again" in (out / "lesson-demo.txt").read_text()
    assert receipt["durationSeconds"] == 3.75
    assert receipt["cueCount"] == 3
    assert receipt["manifestSha256"] == _hash(path)
    assert receipt["corrections"] == manifest["corrections"]
    assert receipt["sources"][0]["captionsSha256"] == _hash(tmp_path / "first.srt")
    assert receipt["delivery"]["sha256"] == _hash(tmp_path / "delivery.mp4")
    for name, proof in receipt["files"].items():
        assert proof["sha256"] == _hash(out / name)
    assert "no transcript, content, or visual approval" in receipt["validation"]


def test_cli_dry_run_writes_nothing(tmp_path: Path) -> None:
    manifest, _ = _fixture(tmp_path)
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    result = subprocess.run([sys.executable, str(SCRIPT), str(manifest)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["status"] == "validated"
    assert {p.name: p.read_bytes() for p in tmp_path.iterdir()} == before


def test_unchanged_rerun_has_no_writes_and_conflict_is_atomic(tmp_path: Path) -> None:
    manifest, _ = _fixture(tmp_path)
    out = tmp_path / "out"
    package_course_media(manifest, out)
    snapshot = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in out.iterdir()}
    assert package_course_media(manifest, out)["filesWritten"] == 0
    assert {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in out.iterdir()} == snapshot
    (out / "lesson-demo.vtt").write_text("different", encoding="utf-8")
    (out / "lesson-demo.txt").unlink()
    with pytest.raises(CourseMediaError, match="existing output differs"):
        package_course_media(manifest, out)
    assert not (out / "lesson-demo.txt").exists()
    assert (out / "lesson-demo.vtt").read_text() == "different"


@pytest.mark.parametrize("change,match", [
    (lambda m: m["clips"][0].update(durationSeconds=float("nan")), "finite positive"),
    (lambda m: m["clips"][0].update(durationSeconds=0), "finite positive"),
    (lambda m: m["clips"][1].update(source="first.mp4", sha256=m["clips"][0]["sha256"]), "duplicate clip source"),
    (lambda m: m["clips"][1].update(id="part-a"), "duplicate clip id"),
    (lambda m: m["clips"][0].update(sha256="0" * 64), "sha256 mismatch"),
    (lambda m: m["clips"][0].update(trimStart=1), "unexpected"),
    (lambda m: m["clips"][0].update(captions="absent.srt"), "missing"),
    (lambda m: m.update(corrections=[{"clipId": "part-a", "cueIndex": 0,
                                      "before": "wrong", "after": "right", "reason": "reviewed"}]), "exactly match"),
    (lambda m: m.update(corrections=[{"clipId": "part-a", "cueIndex": 0,
                                      "before": "Hello & again again\nsecond line", "after": "right", "reason": " "}]), "nonblank"),
    (lambda m: m.update(corrections=[{"clipId": "part-a", "cueIndex": 0,
                                      "before": "Hello & again again\nsecond line", "after": "right\n\nwrong", "reason": "reviewed"}]), "blank paragraph"),
])
def test_invalid_manifest_causes_no_writes(tmp_path: Path, change, match: str) -> None:
    manifest, obj = _fixture(tmp_path)
    change(obj)
    _save(manifest, obj)
    with pytest.raises(CourseMediaError, match=match):
        package_course_media(manifest, tmp_path / "out")
    assert not (tmp_path / "out").exists()


@pytest.mark.parametrize("srt,match", [
    ("1\n00:00:00,100 --> 00:00:01,301\nToo long\n", "beyond clip duration"),
    ("1\n00:00:00,500 --> 00:00:00,100\nBackward\n", "nonpositive"),
    ("1\n00:00:00,100 --> 00:00:00,500\nOkay\n\n2\nnot timing\nMissing\n", "malformed timing"),
    ("1\n00:00:00,100 --> 00:00:00,500\n<b></b>\n", "empty caption"),
    ("1\n00:00:00,100 --> 00:00:00,500\nOkay\n\n3\n00:00:00,600 --> 00:00:00,700\nSkipped\n", "sequential cue number"),
])
def test_bad_srt_fails_without_output(tmp_path: Path, srt: str, match: str) -> None:
    manifest, _ = _fixture(tmp_path)
    (tmp_path / "first.srt").write_text(srt, encoding="utf-8")
    with pytest.raises(CourseMediaError, match=match):
        package_course_media(manifest, tmp_path / "out")
    assert not (tmp_path / "out").exists()


def test_timing_tolerance_and_input_collision(tmp_path: Path) -> None:
    manifest, obj = _fixture(tmp_path)
    (tmp_path / "first.srt").write_text("1\n00:00:01,200 --> 00:00:01,300\nEdge\n", encoding="utf-8")
    assert package_course_media(manifest)["cues"] == 2
    obj["clips"][0]["source"] = "lesson-demo.cues.json"
    (tmp_path / "lesson-demo.cues.json").write_bytes(b"source")
    obj["clips"][0]["sha256"] = _hash(tmp_path / "lesson-demo.cues.json")
    _save(manifest, obj)
    with pytest.raises(CourseMediaError, match="overwrite input"):
        package_course_media(manifest, tmp_path)


def test_empty_media_and_delivery_are_rejected(tmp_path: Path) -> None:
    manifest, obj = _fixture(tmp_path)
    (tmp_path / "first.mp4").write_bytes(b"")
    obj["clips"][0]["sha256"] = _hash(tmp_path / "first.mp4")
    _save(manifest, obj)
    with pytest.raises(CourseMediaError, match="source is empty"):
        package_course_media(manifest, tmp_path / "out")
    (tmp_path / "first.mp4").write_bytes(b"first source")
    obj["clips"][0]["sha256"] = _hash(tmp_path / "first.mp4")
    (tmp_path / "delivery.mp4").write_bytes(b"")
    obj["delivery"] = {"path": "delivery.mp4", "sha256": _hash(tmp_path / "delivery.mp4"),
                       "maxBytes": 100, "durationSeconds": 3.75}
    _save(manifest, obj)
    with pytest.raises(CourseMediaError, match="delivery.path is empty"):
        package_course_media(manifest, tmp_path / "out")
    assert not (tmp_path / "out").exists()


def test_combined_cues_must_remain_start_ordered(tmp_path: Path) -> None:
    manifest, _ = _fixture(tmp_path)
    (tmp_path / "first.srt").write_text(
        "1\n00:00:01,260 --> 00:00:01,290\nEnd\n", encoding="utf-8"
    )
    (tmp_path / "second.srt").write_text(
        "1\n00:00:00,000 --> 00:00:00,100\nStart\n", encoding="utf-8"
    )
    with pytest.raises(CourseMediaError, match="combined cue start times"):
        package_course_media(manifest, tmp_path / "out")
    assert not (tmp_path / "out").exists()
