"""Read-only YouTube chapter export from an existing course-media package.

Validates declared timing and hashes; never probes, edits, uploads or approves media.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from decimal import Decimal
from pathlib import Path
from typing import Any


class ChapterExportError(ValueError):
    """Invalid chapters or stale package/delivery evidence."""


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _number(value: Any, where: str) -> Decimal:
    try:
        valid = not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)
    except OverflowError:
        valid = False
    if not valid:
        raise ChapterExportError(f"{where} must be a finite number")
    return Decimal(str(value))


def _hash(value: Any, where: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise ChapterExportError(f"{where} must be a lowercase SHA-256")
    return value


def _stamp(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}" if hours else f"{minutes:02d}:{seconds:02d}"


def export_youtube_chapters(chapters_path: str | Path, receipt_path: str | Path,
                            render_path: str | Path) -> dict[str, Any]:
    """Validate real package inputs and render bytes, then return text and hash proof."""
    chapters_path, receipt_path, render_path = map(Path, (chapters_path, receipt_path, render_path))
    if any(not path.is_file() or path.stat().st_size == 0 for path in (chapters_path, receipt_path, render_path)):
        raise ChapterExportError("chapter, receipt and render inputs must be nonempty files")
    try:
        chapters = json.loads(chapters_path.read_text(encoding="utf-8"))
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise ChapterExportError("chapter/receipt input is not valid JSON") from exc
    if not isinstance(receipt, dict) or type(receipt.get("schemaVersion")) is not int or receipt["schemaVersion"] != 1:
        raise ChapterExportError("receipt schemaVersion must be 1")
    if not isinstance(receipt.get("id"), str) or chapters_path.name != f"{receipt['id']}.chapters.json":
        raise ChapterExportError("chapter filename does not match package ID")
    files = receipt.get("files")
    chapter_proof = files.get(chapters_path.name) if isinstance(files, dict) else None
    chapter_hash = _digest(chapters_path)
    if not isinstance(chapter_proof, dict) or _hash(chapter_proof.get("sha256"), "chapter hash") != chapter_hash:
        raise ChapterExportError("chapter hash differs from the package receipt; regenerate after edits")
    duration = _number(receipt.get("durationSeconds"), "package duration")
    if duration <= 0:
        raise ChapterExportError("duration must be positive")
    delivery = receipt.get("delivery")
    if not isinstance(delivery, dict):
        raise ChapterExportError("receipt needs final delivery hash/duration; package with delivery proof")
    render_hash = _digest(render_path)
    if _hash(delivery.get("sha256"), "delivery hash") != render_hash:
        raise ChapterExportError("render hash differs from receipt; recompute sidecars after edits")
    delivery_duration = _number(delivery.get("declaredDurationSeconds"), "delivery duration")
    if delivery_duration <= 0 or abs(delivery_duration - duration) > Decimal("0.250"):
        raise ChapterExportError("delivery and package durations disagree")
    if type(delivery.get("bytes")) is not int or delivery["bytes"] != render_path.stat().st_size:
        raise ChapterExportError("render byte size differs from receipt")
    if not isinstance(chapters, list) or len(chapters) < 3:
        raise ChapterExportError("YouTube needs at least three chapters")
    starts, titles, ids = [], [], set()
    for index, chapter in enumerate(chapters):
        if not isinstance(chapter, dict) or set(chapter) != {"id", "title", "startSeconds"}:
            raise ChapterExportError(f"chapter {index} must contain id, title and startSeconds")
        ident = chapter["id"]
        if not isinstance(ident, str) or not ident.strip() or ident in ids:
            raise ChapterExportError(f"chapter {index} needs a unique nonblank ID")
        ids.add(ident)
        title = chapter["title"]
        if not isinstance(title, str) or not title.strip() or any(ord(c) < 32 or ord(c) == 127 or c in "\u2028\u2029" for c in title):
            raise ChapterExportError(f"chapter {index} title must be one nonblank line without control characters")
        titles.append(" ".join(title.split()))
        starts.append(_number(chapter["startSeconds"], f"chapter {index} start"))
    if starts[0] != 0:
        raise ChapterExportError("first chapter must begin at 00:00")
    ends = starts[1:] + [delivery_duration]
    if any(start < 0 or end - start < 10 for start, end in zip(starts, ends)):
        raise ChapterExportError("every chapter must be ascending and at least ten seconds, including the last")
    exported = [int(value) for value in starts]
    exported_ends = exported[1:] + [delivery_duration]
    if any(end - start < 10 for start, end in zip(exported, exported_ends)):
        raise ChapterExportError("whole-second exported chapters would be shorter than ten seconds")
    description = "\n".join(f"{_stamp(start)} {title}" for start, title in zip(exported, titles)) + "\n"
    return {"schemaVersion": 1, "id": receipt["id"], "description": description,
            "chapterCount": len(chapters), "durationSeconds": float(delivery_duration),
            "chaptersSha256": chapter_hash, "packageReceiptSha256": _digest(receipt_path),
            "renderSha256": render_hash,
            "descriptionSha256": hashlib.sha256(description.encode("utf-8")).hexdigest(),
            "validation": "hashes and declared timing only; no probing, rendered QA or publication"}
