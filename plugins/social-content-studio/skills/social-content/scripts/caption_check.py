#!/usr/bin/env python3
"""Inspect caption limits and a codepoint preview without rewriting content.

The original Unicode string is returned byte-for-byte as decoded input. The
preview is a codepoint window, not a render or an AI score. Platform is only a
caller-supplied label; hashtag limits are checked only when an explicit limit
is supplied. No readiness, reach, or performance claim is made.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

HASHTAG_RE = re.compile(r"(?<!\w)#[\w]+", re.UNICODE)

def analyse(text, limit=None, preview_budget=125, max_hashtags=None, platform=None, keywords=None):
    if not isinstance(text, str): raise ValueError("text must be a string")
    if limit is not None and (isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0): raise ValueError("limit must be a positive integer")
    if isinstance(preview_budget, bool) or not isinstance(preview_budget, int) or preview_budget < 0: raise ValueError("preview_budget must be a nonnegative integer")
    if max_hashtags is not None and (isinstance(max_hashtags, bool) or not isinstance(max_hashtags, int) or max_hashtags < 0): raise ValueError("max_hashtags must be a nonnegative integer")
    hashtags = HASHTAG_RE.findall(text)
    found = [k for k in (keywords or []) if isinstance(k, str) and k and k.casefold() in text.casefold()]
    missing = [k for k in (keywords or []) if isinstance(k, str) and k and k.casefold() not in text.casefold()]
    warnings = []
    if limit is not None and len(text) > limit: warnings.append("caption exceeds supplied limit")
    if max_hashtags is not None and len(hashtags) > max_hashtags: warnings.append("hashtag count exceeds supplied platform limit")
    return {"schema_version": 1, "claim_boundary": "Codepoint counts and approximate preview only; no render, AI score, readiness, reach, or performance claim.", "text": text, "characters": len(text), "limit": limit, "preview_budget": preview_budget, "preview": text[:preview_budget], "truncated": len(text) > preview_budget, "hashtags": hashtags, "max_hashtags": max_hashtags, "platform": platform, "keywords": {"found": found, "missing": missing} if keywords is not None else None, "warnings": warnings}

def _read_input(path):
    """Decode UTF-8 bytes without universal-newline conversion or BOM removal."""
    raw = sys.stdin.buffer.read() if path == "-" else Path(path).read_bytes()
    return raw.decode("utf-8")

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument("input", nargs="?", default="-"); ap.add_argument("--limit", type=int); ap.add_argument("--preview-budget", type=int, default=125); ap.add_argument("--max-hashtags", type=int); ap.add_argument("--platform"); ap.add_argument("--keywords", default=""); args = ap.parse_args(argv)
    try:
        text = _read_input(args.input)
        result = analyse(text, args.limit, args.preview_budget, args.max_hashtags, args.platform, args.keywords.split(",") if args.keywords else None)
        print(json.dumps(result, ensure_ascii=False, allow_nan=False)); return 0
    except (OSError, ValueError, TypeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr); return 2
if __name__ == "__main__": raise SystemExit(main())
