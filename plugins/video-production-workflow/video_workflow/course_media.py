"""Deterministic, local sidecar packaging for ordered course clips.

This module validates declared media hashes and caption timing. It does not
probe, edit, render, or approve the audiovisual content.
"""

from __future__ import annotations

import hashlib
import html
import json
import math
import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any


class CourseMediaError(ValueError):
    """A manifest, caption, or output preflight failed."""


_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
_SHA256 = re.compile(r"[0-9a-f]{64}\Z")
_STAMP = re.compile(r"(\d{2,}):(\d{2}):(\d{2}),(\d{3})\Z")
_TIMING = re.compile(r"(\S+)\s+-->\s+(\S+)\Z")
_STYLE = re.compile(r"</?(?:b|i|u|font|c|v|ruby|rt|lang)(?:\s+[^<>]*)?>", re.I)
_MS = Decimal("0.001")
_BOUND_TOLERANCE = Decimal("0.050")


def _require_keys(value: Any, required: set[str], optional: set[str], where: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CourseMediaError(f"{where} must be an object")
    missing = required - value.keys()
    unexpected = value.keys() - required - optional
    if missing or unexpected:
        raise CourseMediaError(f"{where}: missing {sorted(missing)}; unexpected {sorted(unexpected)}")
    return value


def _slug(value: Any, where: str) -> str:
    if not isinstance(value, str) or not _SLUG.fullmatch(value):
        raise CourseMediaError(f"{where} must be a lowercase safe slug")
    return value


def _nonblank(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CourseMediaError(f"{where} must be nonblank text")
    return value


def _duration(value: Any, where: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise CourseMediaError(f"{where} must be a finite positive number")
    return Decimal(str(value))


def _digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def _declared_file(
    base: Path, name: Any, where: str, expected_hash: Any = None, *, nonempty: bool = False
) -> tuple[Path, str]:
    if not isinstance(name, str) or not name or Path(name).is_absolute():
        raise CourseMediaError(f"{where} must be a relative file path")
    path = (base / name).resolve()
    if not path.is_file():
        raise CourseMediaError(f"{where} is missing: {name}")
    if nonempty and path.stat().st_size == 0:
        raise CourseMediaError(f"{where} is empty: {name}")
    actual = _digest(path)
    if expected_hash is not None:
        if not isinstance(expected_hash, str) or not _SHA256.fullmatch(expected_hash):
            raise CourseMediaError(f"{where} sha256 must be lowercase hex")
        if actual != expected_hash:
            raise CourseMediaError(f"{where} sha256 mismatch: {name}")
    return path, actual


def _seconds(stamp: str, where: str) -> Decimal:
    match = _STAMP.fullmatch(stamp)
    if not match:
        raise CourseMediaError(f"{where}: invalid SRT timestamp {stamp!r}")
    hours, minutes, seconds, millis = map(int, match.groups())
    if minutes >= 60 or seconds >= 60:
        raise CourseMediaError(f"{where}: invalid SRT timestamp {stamp!r}")
    return Decimal(((hours * 60 + minutes) * 60 + seconds) * 1000 + millis) / 1000


def _caption_text(lines: list[str], where: str) -> str:
    text = "\n".join(_STYLE.sub("", line) for line in lines)
    if not text.strip():
        raise CourseMediaError(f"{where}: empty caption cue")
    return text


def parse_strict_srt(path: Path, duration: Decimal) -> list[dict[str, Any]]:
    """Parse every SRT block, retaining cue line breaks and spoken repetition."""
    raw = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    blocks = re.split(r"\n[ \t]*\n", raw.strip()) if raw.strip() else []
    if not blocks:
        raise CourseMediaError(f"{path.name}: no caption cues")
    cues: list[dict[str, Any]] = []
    previous_start = Decimal("-1")
    for index, block in enumerate(blocks):
        where = f"{path.name} cue {index + 1}"
        lines = block.split("\n")
        if len(lines) < 3 or lines[0].strip() != str(index + 1):
            raise CourseMediaError(f"{where}: expected sequential cue number, timing, and text")
        match = _TIMING.fullmatch(lines[1].strip())
        if not match:
            raise CourseMediaError(f"{where}: malformed timing line")
        start = _seconds(match.group(1), where)
        end = _seconds(match.group(2), where)
        if end <= start or start < previous_start:
            raise CourseMediaError(f"{where}: timing is nonpositive or out of order")
        if end > duration + _BOUND_TOLERANCE:
            raise CourseMediaError(f"{where}: caption extends beyond clip duration")
        previous_start = start
        cues.append({"start": start, "end": end, "text": _caption_text(lines[2:], where)})
    return cues


def _number(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))


def _stamp(value: Decimal) -> str:
    millis = int((value * 1000).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    seconds, millis = divmod(millis, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{millis:03}"


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def build_package(manifest_path: str | Path) -> tuple[dict[str, Any], dict[str, bytes], set[Path]]:
    """Validate all inputs and construct output bytes without writing anything."""
    manifest_path = Path(manifest_path).resolve()
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CourseMediaError(f"cannot read manifest: {exc}") from exc
    obj = _require_keys(manifest, {"schemaVersion", "id", "clips"}, {"corrections", "delivery"}, "manifest")
    if type(obj["schemaVersion"]) is not int or obj["schemaVersion"] != 1:
        raise CourseMediaError("schemaVersion must be 1")
    package_id = _slug(obj["id"], "manifest id")
    clips = obj["clips"]
    if not isinstance(clips, list) or not clips:
        raise CourseMediaError("clips must be a nonempty ordered array")
    base = manifest_path.parent
    input_paths = {manifest_path}
    clip_ids: set[str] = set()
    source_paths: set[Path] = set()
    caption_paths: set[Path] = set()
    sources: list[dict[str, Any]] = []
    chapters: list[dict[str, Any]] = []
    cues: list[dict[str, Any]] = []
    clip_cues: dict[str, list[dict[str, Any]]] = {}
    offset = Decimal(0)
    for index, raw_clip in enumerate(clips):
        where = f"clips[{index}]"
        clip = _require_keys(raw_clip, {"id", "title", "source", "sha256", "durationSeconds", "captions"}, set(), where)
        clip_id = _slug(clip["id"], f"{where}.id")
        if clip_id in clip_ids:
            raise CourseMediaError(f"duplicate clip id: {clip_id}")
        clip_ids.add(clip_id)
        title = _nonblank(clip["title"], f"{where}.title")
        duration = _duration(clip["durationSeconds"], f"{where}.durationSeconds")
        source_path, source_hash = _declared_file(base, clip["source"], f"{where}.source", clip["sha256"], nonempty=True)
        caption_path, caption_hash = _declared_file(base, clip["captions"], f"{where}.captions")
        if source_path in source_paths:
            raise CourseMediaError(f"duplicate clip source: {clip['source']}")
        if caption_path in caption_paths:
            raise CourseMediaError(f"duplicate caption source: {clip['captions']}")
        source_paths.add(source_path)
        caption_paths.add(caption_path)
        input_paths.update((source_path, caption_path))
        parsed = parse_strict_srt(caption_path, duration)
        clip_cues[clip_id] = parsed
        chapters.append({"id": clip_id, "title": title, "startSeconds": _number(offset)})
        for cue in parsed:
            cues.append({"id": clip_id, "startSeconds": _number(offset + cue["start"]),
                         "endSeconds": _number(offset + cue["end"]), "text": cue["text"]})
        sources.append({"id": clip_id, "source": clip["source"], "sha256": source_hash,
                        "captions": clip["captions"], "captionsSha256": caption_hash,
                        "durationSeconds": _number(duration)})
        offset += duration

    corrections = obj.get("corrections", [])
    if not isinstance(corrections, list):
        raise CourseMediaError("corrections must be an array")
    seen_corrections: set[tuple[str, int]] = set()
    for index, raw_correction in enumerate(corrections):
        where = f"corrections[{index}]"
        correction = _require_keys(raw_correction, {"clipId", "cueIndex", "before", "after", "reason"}, set(), where)
        clip_id = correction["clipId"]
        cue_index = correction["cueIndex"]
        if clip_id not in clip_cues or type(cue_index) is not int or not 0 <= cue_index < len(clip_cues[clip_id]):
            raise CourseMediaError(f"{where}: unknown clip or cue index")
        key = (clip_id, cue_index)
        if key in seen_corrections:
            raise CourseMediaError(f"{where}: duplicate correction")
        seen_corrections.add(key)
        _nonblank(correction["before"], f"{where}.before")
        _nonblank(correction["after"], f"{where}.after")
        _nonblank(correction["reason"], f"{where}.reason")
        if "\r" in correction["after"] or re.search(r"\n[ \t]*\n", correction["after"]):
            raise CourseMediaError(f"{where}.after contains a blank paragraph or carriage return")
        original = clip_cues[clip_id][cue_index]["text"]
        if original != correction["before"]:
            raise CourseMediaError(f"{where}: before does not exactly match source cue")
        clip_cues[clip_id][cue_index]["text"] = correction["after"]
        matching = [cue for cue in cues if cue["id"] == clip_id]
        matching[cue_index]["text"] = correction["after"]

    delivery_proof = None
    if "delivery" in obj:
        delivery = _require_keys(obj["delivery"], {"path", "sha256", "maxBytes", "durationSeconds"}, set(), "delivery")
        delivery_path, delivery_hash = _declared_file(base, delivery["path"], "delivery.path", delivery["sha256"], nonempty=True)
        input_paths.add(delivery_path)
        if type(delivery["maxBytes"]) is not int or delivery["maxBytes"] <= 0:
            raise CourseMediaError("delivery.maxBytes must be a positive integer")
        byte_size = delivery_path.stat().st_size
        if byte_size > delivery["maxBytes"]:
            raise CourseMediaError("delivery exceeds maxBytes")
        delivery_duration = _duration(delivery["durationSeconds"], "delivery.durationSeconds")
        if abs(delivery_duration - offset) > Decimal("0.250"):
            raise CourseMediaError("delivery duration differs from source-duration total by more than 250ms")
        delivery_proof = {"path": delivery["path"], "sha256": delivery_hash,
                          "bytes": byte_size, "maxBytes": delivery["maxBytes"],
                          "declaredDurationSeconds": _number(delivery_duration)}

    for previous, current in zip(cues, cues[1:]):
        if current["startSeconds"] < previous["startSeconds"]:
            raise CourseMediaError("combined cue start times are out of order across clip boundaries")

    vtt = ["WEBVTT", ""]
    for cue in cues:
        vtt.extend((f"{_stamp(Decimal(str(cue['startSeconds'])))} --> {_stamp(Decimal(str(cue['endSeconds'])))}",
                    html.escape(cue["text"], quote=False), ""))
    transcript: list[str] = []
    for chapter in chapters:
        transcript.append(f"{chapter['title']} ({_stamp(Decimal(str(chapter['startSeconds'])))})")
        transcript.append(" ".join(cue["text"].replace("\n", " ") for cue in cues if cue["id"] == chapter["id"]))
        transcript.append("")
    files = {
        f"{package_id}.cues.json": _json_bytes(cues),
        f"{package_id}.chapters.json": _json_bytes(chapters),
        f"{package_id}.vtt": ("\n".join(vtt) + "\n").encode("utf-8"),
        f"{package_id}.txt": ("\n".join(transcript) + "\n").encode("utf-8"),
    }
    receipt = {"schemaVersion": 1, "id": package_id, "manifestSha256": _digest(manifest_path),
               "validation": "mechanical hashes, declared durations, caption structure, and timing only; no transcript, content, or visual approval",
               "sources": sources, "corrections": corrections, "durationSeconds": _number(offset), "cueCount": len(cues),
               "files": {name: {"sha256": hashlib.sha256(content).hexdigest()} for name, content in files.items()}}
    if delivery_proof is not None:
        receipt["delivery"] = delivery_proof
    files["package-receipt.json"] = _json_bytes(receipt)
    summary = {"id": package_id, "clips": len(clips), "cues": len(cues),
               "sourceDurationSeconds": _number(offset), "deliveryValidated": delivery_proof is not None,
               "validation": "mechanical only"}
    return summary, files, input_paths


def package_course_media(manifest_path: str | Path, output_dir: str | Path | None = None) -> dict[str, Any]:
    """Dry-run by default; write complete deterministic sidecars when output is set."""
    summary, files, inputs = build_package(manifest_path)
    if output_dir is None:
        return {**summary, "status": "validated", "filesWritten": 0}
    out = Path(output_dir).resolve()
    if out.exists() and not out.is_dir():
        raise CourseMediaError("output must be a directory")
    destinations = {name: out / name for name in files}
    for name, target in destinations.items():
        if target.resolve() in inputs:
            raise CourseMediaError(f"output would overwrite input: {name}")
        if target.exists() and target.read_bytes() != files[name]:
            raise CourseMediaError(f"existing output differs: {name}")
    out.mkdir(parents=True, exist_ok=True)
    written = 0
    for name, target in destinations.items():
        if not target.exists():
            with target.open("xb") as stream:
                stream.write(files[name])
            written += 1
    return {**summary, "status": "packaged", "filesWritten": written}
