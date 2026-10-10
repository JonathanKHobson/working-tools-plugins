#!/usr/bin/env python3
"""Summarize repetition and sentence shape for a human editorial review."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'])")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")


def read_text(path: str) -> tuple[str, str]:
    if path == "-":
        return sys.stdin.read(), "stdin"
    source = Path(path)
    return source.read_text(encoding="utf-8"), str(source)


def ngrams(words: list[str], size: int) -> Counter[str]:
    return Counter(" ".join(words[index:index + size]) for index in range(len(words) - size + 1))


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize style patterns without scoring authorship.")
    parser.add_argument("path", help="UTF-8 text file, or - for stdin")
    parser.add_argument("--top", type=int, default=10, help="Maximum repeated phrases to report")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    text, source = read_text(args.path)
    sentences = [sentence.strip() for sentence in SENTENCE_RE.split(text.strip()) if sentence.strip()]
    words = [word.lower() for word in WORD_RE.findall(text)]
    lengths = [len(WORD_RE.findall(sentence)) for sentence in sentences]
    starts = Counter(" ".join(WORD_RE.findall(sentence)[:2]).lower() for sentence in sentences if WORD_RE.findall(sentence))
    repeated = []
    for size in (4, 3):
        repeated.extend((phrase, count, size) for phrase, count in ngrams(words, size).items() if count > 1)
    repeated.sort(key=lambda item: (-item[1], -item[2], item[0]))
    payload = {
        "source": source,
        "disclaimer": "Style observations only; repetition can be intentional and this is not an authorship score.",
        "sentences": len(sentences),
        "words": len(words),
        "average_sentence_words": round(sum(lengths) / len(lengths), 1) if lengths else 0,
        "sentence_word_range": [min(lengths), max(lengths)] if lengths else [0, 0],
        "repeated_sentence_starts": [{"start": start, "count": count} for start, count in starts.most_common() if count > 1][:args.top],
        "repeated_phrases": [{"phrase": phrase, "count": count, "words": size} for phrase, count, size in repeated[:args.top]],
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2))
        return 0
    print(f"{source}: {payload['words']} words, {payload['sentences']} sentences, average {payload['average_sentence_words']} words/sentence.")
    print(payload["disclaimer"])
    if payload["repeated_sentence_starts"]:
        print("Repeated sentence starts:")
        for item in payload["repeated_sentence_starts"]:
            print(f"- {item['start']!r}: {item['count']}")
    if payload["repeated_phrases"]:
        print("Repeated phrases:")
        for item in payload["repeated_phrases"]:
            print(f"- {item['phrase']!r}: {item['count']} occurrences")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
