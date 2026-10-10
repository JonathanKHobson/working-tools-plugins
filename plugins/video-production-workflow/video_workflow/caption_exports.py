"""Local, hash-bound caption variants from an existing reviewed cue timeline.

This is timing arithmetic, not transcription, audio alignment or editorial QA.
It refuses partial source cues rather than guessing which words a cut removed.
"""

from __future__ import annotations

import hashlib
import json
import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Any


class CaptionExportError(ValueError):
    """A caption export contract or destination failed validation."""


def _object(value: Any, required: set[str], optional: set[str], where: str) -> dict:
    if not isinstance(value, dict) or required - value.keys() or value.keys() - required - optional:
        raise CaptionExportError(f"{where}: expected fields {sorted(required)}; optional {sorted(optional)}")
    return value


def _number(value: Any, where: str, *, positive: bool = False) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CaptionExportError(f"{where}: expected a finite number")
    number = Decimal(str(value))
    if not number.is_finite() or number < 0 or (positive and number == 0):
        raise CaptionExportError(f"{where}: expected a finite {'positive' if positive else 'nonnegative'} number")
    return number


def _millis(seconds: Decimal) -> int:
    return int((seconds * 1000).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def _stamp(millis: int) -> str:
    hours, remainder = divmod(millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, ms = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{ms:03}"


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def _read(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as exc:
        raise CaptionExportError(f"cannot read {path.name}: {exc}") from exc


def _parse(raw: bytes, where: str) -> Any:
    try:
        return json.loads(raw)
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise CaptionExportError(f"{where}: invalid JSON") from exc


def _build(manifest_path: Path) -> tuple[dict, dict[str, bytes], set[Path]]:
    raw_manifest = _read(manifest_path)
    manifest = _object(_parse(raw_manifest, "manifest"), {"schemaVersion", "cues", "outputs"}, set(), "manifest")
    if type(manifest["schemaVersion"]) is not int or manifest["schemaVersion"] != 1:
        raise CaptionExportError("schemaVersion must be 1")
    source = _object(manifest["cues"], {"path", "sha256"}, set(), "cues")
    name, expected = source["path"], source["sha256"]
    if not isinstance(name, str) or not name or Path(name).is_absolute():
        raise CaptionExportError("cues.path must be a manifest-relative file path")
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
        raise CaptionExportError("cues.sha256 must be lowercase SHA-256")
    cue_path = (manifest_path.parent / name).resolve()
    raw_cues = _read(cue_path)
    if hashlib.sha256(raw_cues).hexdigest() != expected:
        raise CaptionExportError("cues sha256 mismatch")
    data = _parse(raw_cues, "cues")
    if not isinstance(data, list) or not data:
        raise CaptionExportError("cues must be a nonempty array")
    cues: list[tuple[Decimal, Decimal, str]] = []
    previous_start = Decimal(-1)
    for index, raw in enumerate(data):
        where = f"cue {index + 1}"
        cue = _object(raw, {"startSeconds", "endSeconds", "text"}, {"id"}, where)
        start = _number(cue["startSeconds"], where)
        end = _number(cue["endSeconds"], where, positive=True)
        text = cue["text"]
        if end <= start or start < previous_start:
            raise CaptionExportError(f"{where}: nonpositive or unordered timing")
        if not isinstance(text, str) or not text.strip() or "\r" in text or re.search(r"\n[ \t]*\n", text):
            raise CaptionExportError(f"{where}: expected nonempty text without blank paragraphs or carriage returns")
        cues.append((start, end, text))
        previous_start = start
    outputs = manifest["outputs"]
    if not isinstance(outputs, list) or not outputs:
        raise CaptionExportError("outputs must be a nonempty array")
    ids: set[str] = set()
    files: dict[str, bytes] = {}
    proofs: list[dict] = []
    for index, raw in enumerate(outputs):
        item = _object(raw, {"id", "segments"}, set(), f"outputs[{index}]")
        item_id = item["id"]
        if not isinstance(item_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", item_id):
            raise CaptionExportError("output id must be a lowercase safe slug")
        if item_id in ids:
            raise CaptionExportError(f"duplicate output id: {item_id}")
        ids.add(item_id)
        segments = item["segments"]
        if not isinstance(segments, list) or not segments:
            raise CaptionExportError(f"{item_id}: segments must be a nonempty array")
        offset, previous_out = Decimal(0), Decimal(0)
        result: list[str] = []
        cue_count = 0
        for segment_index, raw_segment in enumerate(segments):
            segment = _object(raw_segment, {"sourceIn", "sourceOut"}, {"speed"}, f"{item_id} segment {segment_index + 1}")
            start = _number(segment["sourceIn"], "sourceIn")
            end = _number(segment["sourceOut"], "sourceOut", positive=True)
            speed = _number(segment.get("speed", 1), "speed", positive=True)
            if end <= start or start < previous_out:
                raise CaptionExportError(f"{item_id}: segments must have positive durations and be ordered without overlap")
            for cue_index, (cue_in, cue_out, text) in enumerate(cues):
                if cue_out <= start or cue_in >= end:
                    continue
                if cue_in < start or cue_out > end:
                    raise CaptionExportError(f"{item_id} segment {segment_index + 1} cuts through cue {cue_index + 1}; review the boundary or supply reviewed split cues")
                output_in = _millis(offset + (cue_in - start) / speed)
                output_out = _millis(offset + (cue_out - start) / speed)
                if output_out <= output_in:
                    raise CaptionExportError(f"{item_id}: cue {cue_index + 1} collapses at millisecond precision")
                cue_count += 1
                result.append(f"{cue_count}\n{_stamp(output_in)} --> {_stamp(output_out)}\n{text}\n\n")
            offset += (end - start) / speed
            previous_out = end
        if not cue_count:
            raise CaptionExportError(f"{item_id}: no retained caption cues")
        filename = f"{item_id}.srt"
        encoded = "".join(result).encode("utf-8")
        files[filename] = encoded
        proofs.append({"id": item_id, "file": filename, "cueCount": cue_count,
                       "durationSeconds": float(offset.quantize(Decimal("0.000001"))),
                       "segments": segments, "sha256": hashlib.sha256(encoded).hexdigest(), "bytes": len(encoded)})
    receipt = {"schemaVersion": 1, "manifestSha256": hashlib.sha256(raw_manifest).hexdigest(),
               "cues": source, "outputs": proofs,
               "validation": "Hash-bound, verbatim whole-cue mapping for ordered constant-speed segments; no transcription, boundary listening, render alignment, or editorial approval."}
    files["caption-export-receipt.json"] = _json_bytes(receipt)
    return receipt, files, {manifest_path, cue_path}


def export_caption_variants(manifest_path: str | Path, output_dir: str | Path | None = None) -> dict:
    """Dry-run by default; refuse changed existing files and source overwrites."""
    try:
        receipt, files, inputs = _build(Path(manifest_path).resolve())
    except ArithmeticError as exc:
        raise CaptionExportError("timing or speed exceeds supported decimal precision") from exc
    if output_dir is None:
        return {**receipt, "status": "validated", "filesWritten": 0}
    out = Path(output_dir).resolve()
    if out.exists() and not out.is_dir():
        raise CaptionExportError("output must be a directory")
    for name, content in files.items():
        target = out / name
        if target.is_symlink() or target.resolve() in inputs:
            raise CaptionExportError(f"output would overwrite an input or symbolic link: {name}")
        if target.exists() and (not target.is_file() or target.read_bytes() != content):
            raise CaptionExportError(f"existing output differs: {name}")
    out.mkdir(parents=True, exist_ok=True)
    written = 0
    try:
        for name, content in files.items():
            target = out / name
            if not target.exists():
                with target.open("xb") as stream:
                    stream.write(content)
                written += 1
    except OSError as exc:
        raise CaptionExportError(f"cannot write output: {exc}") from exc
    return {**receipt, "status": "exported", "filesWritten": written}
