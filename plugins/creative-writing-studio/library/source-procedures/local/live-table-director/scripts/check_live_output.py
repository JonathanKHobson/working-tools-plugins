#!/usr/bin/env python3
"""Check live-table-director output contract from stdin."""

from __future__ import annotations

import re
import sys


REQUIRED = [
    "CLOCK | SCENE | ENERGY | SPOTLIGHT",
    "NOW:",
    "SAY:",
    "ASK:",
    "WATCH:",
    "CUT WHEN:",
    "NEXT:",
]

FORBIDDEN = re.compile(
    r"\b(shy|anxious|adhd|autistic|bored|bully|problem player|power gamer|diagnose|diagnosis)\b",
    re.IGNORECASE,
)


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def main() -> int:
    text = sys.stdin.read()
    errors: list[str] = []
    for marker in REQUIRED:
        if marker not in text:
            errors.append(f"missing marker: {marker}")
    words = word_count(text)
    if words > 140:
        errors.append(f"word count {words} exceeds 140")
    if FORBIDDEN.search(text):
        errors.append("contains diagnostic or shaming label")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"ok: {words} words")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
