#!/usr/bin/env python3
"""Compare a candidate draft with an authentic author or destination baseline."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'])")
CONTRACTION_RE = re.compile(r"\b\w+(?:n't|'re|'ve|'ll|'d|'m|'s)\b", re.IGNORECASE)
FIRST_PERSON = {"i", "me", "my", "mine", "we", "us", "our", "ours"}
US_WORDS = {"color", "center", "organize", "analyze", "behavior", "favorite", "meter"}
UK_WORDS = {"colour", "centre", "organise", "analyse", "behaviour", "favourite", "metre"}


def metrics(text: str) -> dict[str, object]:
    words = [word.lower() for word in WORD_RE.findall(text)]
    sentences = [item.strip() for item in SENTENCE_RE.split(text.strip()) if item.strip()]
    lengths = [len(WORD_RE.findall(item)) for item in sentences]
    starts = Counter(" ".join(WORD_RE.findall(item)[:2]).lower() for item in sentences if WORD_RE.findall(item))
    total = max(len(words), 1)
    return {
        "words": len(words),
        "sentences": len(sentences),
        "average_sentence_words": round(sum(lengths) / len(lengths), 2) if lengths else 0,
        "sentence_length_sd": round((sum((value - (sum(lengths) / len(lengths))) ** 2 for value in lengths) / len(lengths)) ** 0.5, 2) if lengths else 0,
        "type_token_ratio": round(len(set(words)) / total, 4),
        "first_person_per_1000": round(1000 * sum(word in FIRST_PERSON for word in words) / total, 2),
        "contractions_per_1000": round(1000 * len(CONTRACTION_RE.findall(text)) / total, 2),
        "em_dashes_per_1000": round(1000 * text.count("—") / total, 2),
        "question_marks_per_1000": round(1000 * text.count("?") / total, 2),
        "top_sentence_starts": starts.most_common(8),
        "us_variant_hits": sum(word in US_WORDS for word in words),
        "uk_variant_hits": sum(word in UK_WORDS for word in words),
    }


def comparisons(base: dict[str, object], candidate: dict[str, object]) -> list[dict[str, object]]:
    rows = []
    thresholds = {
        "average_sentence_words": 5.0,
        "sentence_length_sd": 4.0,
        "type_token_ratio": 0.12,
        "first_person_per_1000": 12.0,
        "contractions_per_1000": 8.0,
        "em_dashes_per_1000": 5.0,
        "question_marks_per_1000": 5.0,
    }
    for key, threshold in thresholds.items():
        delta = round(float(candidate[key]) - float(base[key]), 2)
        rows.append({"metric": key, "baseline": base[key], "candidate": candidate[key], "delta": delta, "review": abs(delta) >= threshold})
    variant_shift = (int(base["us_variant_hits"]) > int(base["uk_variant_hits"]) and int(candidate["uk_variant_hits"]) > int(candidate["us_variant_hits"])) or (int(base["uk_variant_hits"]) > int(base["us_variant_hits"]) and int(candidate["us_variant_hits"]) > int(candidate["uk_variant_hits"]))
    rows.append({"metric": "english_variant_shift", "baseline": f"US {base['us_variant_hits']} / UK {base['uk_variant_hits']}", "candidate": f"US {candidate['us_variant_hits']} / UK {candidate['uk_variant_hits']}", "delta": "", "review": variant_shift})
    return rows


def render_markdown(base_path: str, candidate_path: str, base: dict[str, object], candidate: dict[str, object], rows: list[dict[str, object]]) -> str:
    lines = ["# Style drift comparison", "", f"Baseline: `{base_path}` ({base['words']} words)", f"Candidate: `{candidate_path}` ({candidate['words']} words)", "", "Differences are review cues, not authorship evidence.", "", "| Metric | Baseline | Candidate | Delta | Review |", "| --- | ---: | ---: | ---: | --- |"]
    for row in rows:
        lines.append(f"| {row['metric']} | {row['baseline']} | {row['candidate']} | {row['delta']} | {'yes' if row['review'] else 'no'} |")
    if int(base["words"]) < 200:
        lines += ["", "Baseline warning: fewer than 200 words; style estimates are unstable."]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare a draft with an authentic writing baseline.")
    parser.add_argument("baseline")
    parser.add_argument("candidate")
    parser.add_argument("--format", choices=("text", "markdown", "json"), default="text")
    args = parser.parse_args()
    base_text = Path(args.baseline).read_text(encoding="utf-8")
    candidate_text = Path(args.candidate).read_text(encoding="utf-8")
    base = metrics(base_text)
    candidate = metrics(candidate_text)
    rows = comparisons(base, candidate)
    payload = {"baseline": args.baseline, "candidate": args.candidate, "disclaimer": "Review cues only; not authorship evidence.", "baseline_metrics": base, "candidate_metrics": candidate, "comparisons": rows}
    if args.format == "json":
        print(json.dumps(payload, indent=2))
    elif args.format == "markdown":
        print(render_markdown(args.baseline, args.candidate, base, candidate, rows))
    else:
        print(f"Baseline {base['words']} words; candidate {candidate['words']} words. Review cues only.")
        for row in rows:
            marker = "REVIEW" if row["review"] else "ok"
            print(f"[{marker}] {row['metric']}: {row['baseline']} -> {row['candidate']} (delta {row['delta']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
