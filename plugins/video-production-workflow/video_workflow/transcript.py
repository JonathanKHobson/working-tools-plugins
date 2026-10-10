from __future__ import annotations

from copy import deepcopy
from typing import Any, Iterable


def words_from_transcript(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize common transcript JSON shapes into sorted word dictionaries."""
    candidates: list[dict[str, Any]] = []
    if isinstance(data.get("words"), list):
        candidates.extend(data["words"])
    for segment in data.get("segments", []) if isinstance(data.get("segments"), list) else []:
        if isinstance(segment, dict) and isinstance(segment.get("words"), list):
            for word in segment["words"]:
                if isinstance(word, dict):
                    merged = dict(word)
                    merged.setdefault("speaker", segment.get("speaker"))
                    candidates.append(merged)
    out = []
    for raw in candidates:
        if not isinstance(raw, dict):
            continue
        if raw.get("type") not in {None, "word"}:
            continue
        text = str(raw.get("text", raw.get("word", ""))).strip()
        start, end = raw.get("start"), raw.get("end")
        if not text or start is None or end is None:
            continue
        start_f, end_f = float(start), float(end)
        if end_f <= start_f:
            continue
        out.append({**raw, "text": text, "start": start_f, "end": end_f})
    return sorted(out, key=lambda w: (w["start"], w["end"]))


def pack_phrases(
    data: dict[str, Any],
    *,
    silence_threshold: float = 0.65,
    max_duration: float = 12.0,
    max_words: int = 40,
) -> list[dict[str, Any]]:
    """Pack word timestamps into readable phrases without discarding source words."""
    words = words_from_transcript(data)
    phrases: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []

    def flush() -> None:
        nonlocal current
        if not current:
            return
        phrases.append({
            "start": round(float(current[0]["start"]), 4),
            "end": round(float(current[-1]["end"]), 4),
            "speaker": current[0].get("speaker"),
            "text": " ".join(str(w["text"]).strip() for w in current).replace("  ", " "),
            "words": deepcopy(current),
        })
        current = []

    for word in words:
        if current:
            gap = float(word["start"]) - float(current[-1]["end"])
            speaker_changed = word.get("speaker") != current[0].get("speaker") and (
                word.get("speaker") is not None or current[0].get("speaker") is not None
            )
            too_long = float(word["end"]) - float(current[0]["start"]) > max_duration
            too_many = len(current) >= max_words
            sentence_end = str(current[-1]["text"]).rstrip().endswith((".", "?", "!")) and gap >= 0.18
            if gap >= silence_threshold or speaker_changed or too_long or too_many or sentence_end:
                flush()
        current.append(word)
    flush()
    return phrases


def snap_ranges(
    ranges: Iterable[dict[str, Any]],
    transcript: dict[str, Any],
    *,
    pad_before: float = 0.08,
    pad_after: float = 0.12,
    max_snap_distance: float = 1.5,
) -> list[dict[str, Any]]:
    """Snap approved rough ranges outward to complete intersecting word boundaries."""
    words = words_from_transcript(transcript)
    if not words:
        return [dict(item) for item in ranges]
    result: list[dict[str, Any]] = []
    for raw in ranges:
        item = dict(raw)
        rough_start = float(item["start"])
        rough_end = float(item["end"])
        intersecting = [w for w in words if w["end"] > rough_start and w["start"] < rough_end]
        if intersecting:
            candidate_start = float(intersecting[0]["start"])
            candidate_end = float(intersecting[-1]["end"])
            if abs(candidate_start - rough_start) <= max_snap_distance:
                item["start"] = round(max(0.0, candidate_start - pad_before), 4)
            if abs(candidate_end - rough_end) <= max_snap_distance:
                item["end"] = round(candidate_end + pad_after, 4)
            item["snap"] = {
                "rough_start": rough_start,
                "rough_end": rough_end,
                "first_word": intersecting[0]["text"],
                "last_word": intersecting[-1]["text"],
            }
        result.append(item)
    return result
