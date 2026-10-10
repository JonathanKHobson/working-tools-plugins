"""Real course-package interoperability and unsafe/stale chapter rejection."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from video_workflow.course_media import package_course_media
from video_workflow.youtube_chapters import ChapterExportError, export_youtube_chapters


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture
def package(tmp_path):
    clips = []
    for index in range(3):
        source = tmp_path / f"part-{index}.mp4"
        source.write_bytes(f"synthetic media {index}".encode())
        caption = tmp_path / f"part-{index}.srt"
        caption.write_text("1\n00:00:00,000 --> 00:00:01,000\nA demonstrated action.\n")
        clips.append({"id": f"part-{index}", "title": f"Action {index}", "source": source.name,
                      "sha256": digest(source), "durationSeconds": 35.25, "captions": caption.name})
    render = tmp_path / "delivery.mp4"
    render.write_bytes(b"synthetic final render, not playable media")
    manifest = tmp_path / "package.json"
    manifest.write_text(json.dumps({"schemaVersion": 1, "id": "lesson", "clips": clips,
        "delivery": {"path": render.name, "sha256": digest(render), "maxBytes": 1000,
                     "durationSeconds": 105.75}}))
    output = tmp_path / "sidecars"
    package_course_media(manifest, output)
    return output / "lesson.chapters.json", output / "package-receipt.json", render


def change_chapters(package, chapters):
    path, receipt_path, _ = package
    path.write_text(json.dumps(chapters))
    receipt = json.loads(receipt_path.read_text())
    receipt["files"][path.name]["sha256"] = digest(path)
    receipt_path.write_text(json.dumps(receipt))


def test_real_package_readonly_cli_and_hash_proof(package):
    before = {path: path.read_bytes() for path in package}
    result = export_youtube_chapters(*package)
    assert result["description"] == "00:00 Action 0\n00:35 Action 1\n01:10 Action 2\n"
    assert result["renderSha256"] == digest(package[2])
    assert result["descriptionSha256"] == hashlib.sha256(result["description"].encode()).hexdigest()
    script = Path(__file__).resolve().parents[1] / "scripts/export_youtube_chapters.py"
    command = [sys.executable, str(script), *(str(path) for path in package)]
    proc = subprocess.run(command, capture_output=True, text=True)
    assert proc.returncode == 0 and proc.stdout == result["description"]
    proc = subprocess.run(command + ["--json"], capture_output=True, text=True)
    assert proc.returncode == 0 and json.loads(proc.stdout) == result
    assert all(path.read_bytes() == content for path, content in before.items())


@pytest.mark.parametrize("starts", [[0, 35], [1, 35, 70], [0, 35, 30], [0, 9.9, 70],
    [0, 35, 96], [0, 35, 106], [0, True, 70], [0, float("nan"), 70], [0, -1, 70], [0, 10**400, 70]])
def test_reject_invalid_boundaries_and_last_chapter(package, starts):
    change_chapters(package, [{"id": f"p-{i}", "title": "Useful action", "startSeconds": start}
                              for i, start in enumerate(starts)])
    with pytest.raises(ChapterExportError):
        export_youtube_chapters(*package)


@pytest.mark.parametrize("target", [0, 2])
def test_stale_chapters_or_render_rejected(package, target):
    package[target].write_bytes(package[target].read_bytes() + b" ")
    with pytest.raises(ChapterExportError, match="hash"):
        export_youtube_chapters(*package)


@pytest.mark.parametrize("title", ["", "Claim\n00:10 injected chapter", "Bad\x00 title", "Bad\u2028line"])
def test_reject_blank_or_multiline_titles(package, title):
    chapters = json.loads(package[0].read_text())
    chapters[1]["title"] = title
    change_chapters(package, chapters)
    with pytest.raises(ChapterExportError, match="title"):
        export_youtube_chapters(*package)


def test_missing_delivery_proof_rejected(package):
    receipt = json.loads(package[1].read_text())
    del receipt["delivery"]
    package[1].write_text(json.dumps(receipt))
    with pytest.raises(ChapterExportError, match="delivery"):
        export_youtube_chapters(*package)


def test_hour_timestamps(package):
    change_chapters(package, [{"id": f"p-{i}", "title": "Topic", "startSeconds": start}
                              for i, start in enumerate([0, 3500, 3600])])
    receipt = json.loads(package[1].read_text())
    receipt["durationSeconds"] = receipt["delivery"]["declaredDurationSeconds"] = 3620
    package[1].write_text(json.dumps(receipt))
    assert export_youtube_chapters(*package)["description"] == "00:00 Topic\n58:20 Topic\n1:00:00 Topic\n"


@pytest.mark.parametrize("field,value", [("declaredDurationSeconds", 200), ("bytes", 1), ("sha256", "bad")])
def test_bad_receipt_delivery_rejected(package, field, value):
    receipt = json.loads(package[1].read_text())
    receipt["delivery"][field] = value
    package[1].write_text(json.dumps(receipt))
    with pytest.raises(ChapterExportError):
        export_youtube_chapters(*package)
