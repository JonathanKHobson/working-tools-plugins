#!/usr/bin/env python3
"""Small, local Reel planning helpers.

Contracts: ``beats`` estimates beat durations from a supplied script using a
positive finite words-per-minute value. ``hooks`` performs optional literal
cue matching against a caller-supplied JSON file. Both commands read a file or
stdin and emit JSON only; they never write, call a network, score virality, or
declare a winner. Timing and feature notes are planning diagnostics, not reach
or readiness claims.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

WORD_RE = re.compile(r"(?:\$\s*)?\b[\w]+(?:['’][\w]+)?(?:[.,][\w]+)*\b", re.UNICODE)
UNSUPPORTED_SCRIPT_RE = re.compile(r"[\u0e00-\u0e7f\u1780-\u17ff\u1000-\u109f\u3040-\u30ff\uac00-\ud7af\u4e00-\u9fff]")
SENT_RE = re.compile(r"[^.!?]+[.!?]*")
CONCRETE_RE = re.compile(r"\$\s?\d|\b\d[\d,.]*\b|(?<!^)\b[A-Z][\w-]{2,}\b")
STOPWORDS = {"the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "for", "with", "that", "this", "it", "is", "are", "you", "your", "i", "my", "me", "we", "our"}


def _positive(value, name):
    try:
        finite = math.isfinite(value)
    except (OverflowError, TypeError):
        finite = False
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not finite or value <= 0:
        raise ValueError(f"{name} must be a positive finite number")
    return float(value)


def words(text):
    return WORD_RE.findall(text)


def _beats(raw, wpm=165, target=None):
    rate = _positive(wpm, "wpm")
    if target is not None:
        target = _positive(target, "target")
    wps = rate / 60.0
    if not math.isfinite(wps) or wps <= 0:
        raise ValueError("wpm produces an unavailable words-per-second rate")
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if not lines:
        return {"schema_version": 1, "claim_boundary": "Timing estimate only; no reach or readiness claim.", "wpm": rate, "target": target, "total_seconds": 0.0, "total_words": 0, "beats": [], "diagnostics": ["empty script"]}
    if UNSUPPORTED_SCRIPT_RE.search(raw) and not re.search(r"\s", raw):
        return {"schema_version": 1, "claim_boundary": "No timing estimate is provided for non-space-delimited scripts.", "unsupported": True, "wpm": rate, "target": target, "total_seconds": None, "total_words": None, "beats": [], "diagnostics": [{"kind": "unsupported_language", "message": "Use a recorded read-through or supply an externally measured duration for this script."}]}
    beat_text = []
    for line in lines:
        if len(words(line)) / wps <= 6:
            beat_text.append(line)
            continue
        buf = ""
        for part in (p.strip() for p in SENT_RE.findall(line) if p.strip()):
            candidate = (buf + " " + part).strip()
            if buf and len(words(candidate)) / wps > 4:
                beat_text.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beat_text.append(buf)
    rows, clock = [], 0.0
    for number, text in enumerate(beat_text, 1):
        count = len(words(text))
        try:
            duration = count / wps
        except (OverflowError, ZeroDivisionError):
            raise ValueError("beat duration is unavailable due to numeric overflow") from None
        if not math.isfinite(duration):
            raise ValueError("beat duration is unavailable due to numeric overflow")
        rows.append({"number": number, "start_seconds": round(clock, 3), "duration_seconds": round(duration, 3), "words": count, "text": text, "concrete_feature_count": len(CONCRETE_RE.findall(text)), "labels": ["hook"] if number == 1 else []})
        clock += duration
        if not math.isfinite(clock):
            raise ValueError("total duration is unavailable due to numeric overflow")
    diagnostics = []
    if rows[0]["duration_seconds"] > 3:
        diagnostics.append({"kind": "timing", "beat": 1, "message": "first beat estimate exceeds three seconds"})
    if rows[0]["concrete_feature_count"] == 0:
        diagnostics.append({"kind": "literal_feature", "beat": 1, "message": "first beat contains no detected number or capitalized name"})
    if target is not None:
        diagnostics.append({"kind": "target_delta", "seconds": round(clock - target, 3), "message": "estimated duration compared with supplied target"})
    return {"schema_version": 1, "claim_boundary": "Timing estimate and literal feature diagnostics only; no reach, readiness, score, winner, or virality claim.", "wpm": rate, "target": target, "total_seconds": round(clock, 3), "total_words": sum(row["words"] for row in rows), "beats": rows, "diagnostics": diagnostics}


def _load_formulas(path):
    if not path:
        return []
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    formulas = data.get("hooks", data) if isinstance(data, dict) else data
    if not isinstance(formulas, list):
        raise ValueError("formula file must contain a hooks array")
    return formulas


DEFAULT_FORMULAS = Path(__file__).resolve().parents[2] / "../references/social-methods/reel-hook-formulas.json"

def _hooks(raw, path=None):
    selected = Path(path) if path else DEFAULT_FORMULAS
    formulas = _load_formulas(selected) if selected.exists() else []
    if not formulas:
        return {"schema_version": 1, "claim_boundary": "Literal matching only; no formula, score, winner, or virality conclusion.", "matches": [], "abstained": True, "reason": "no formula source supplied"}
    lowered = raw.casefold()
    matches = []
    for formula in formulas:
        if not isinstance(formula, dict):
            continue
        cues = formula.get("literal_matches") or formula.get("cue_phrases") or formula.get("keywords") or []
        if isinstance(cues, str):
            cues = [cues]
        cues = [cue for cue in cues if isinstance(cue, str) and cue]
        found = [cue for cue in cues if re.search(r"(?<!\w)" + re.escape(cue) + r"(?!\w)", raw, re.IGNORECASE)]
        if found:
            matches.append({"id": formula.get("id"), "name": formula.get("name"), "matched_literals": found})
    reason = None if matches else "formula source contains no literal cue fields or no literal cue matched"
    return {"schema_version": 1, "claim_boundary": "Literal matching only; a match is a prompt for human review, not a classification, score, winner, or virality conclusion.", "matches": matches, "abstained": not bool(matches), "reason": reason}


def _read(path):
    return sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    beat = sub.add_parser("beats"); beat.add_argument("input", nargs="?", default="-"); beat.add_argument("--wpm", type=float, default=165); beat.add_argument("--target", type=float)
    hook = sub.add_parser("hooks"); hook.add_argument("input", nargs="?", default="-"); hook.add_argument("--formulas", default=str(DEFAULT_FORMULAS))
    args = parser.parse_args(argv)
    try:
        result = _beats(_read(args.input), args.wpm, args.target) if args.command == "beats" else _hooks(_read(args.input), args.formulas)
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
