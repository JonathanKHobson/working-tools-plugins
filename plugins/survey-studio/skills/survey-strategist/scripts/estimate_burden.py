#!/usr/bin/env python3
"""Estimate respondent effort and identify burden hotspots in a canonical survey."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

from survey_io import iter_question_contexts, load_survey

BASE_SECONDS = {
    "single_choice": 4.0,
    "multi_choice": 6.0,
    "dropdown": 5.0,
    "yes_no": 3.0,
    "likert": 4.0,
    "rating": 4.5,
    "nps": 4.5,
    "slider": 6.0,
    "number_scale": 4.5,
    "matrix": 5.0,
    "likert_matrix": 5.0,
    "bipolar_matrix": 6.0,
    "rank_order_matrix": 8.0,
    "constant_sum_matrix": 10.0,
    "text_entry_matrix": 12.0,
    "side_by_side": 8.0,
    "text": 12.0,
    "textarea": 35.0,
    "numeric": 5.0,
    "date": 6.0,
    "calendar": 7.0,
    "rank": 8.0,
    "constant_sum": 10.0,
    "maxdiff": 10.0,
    "pick_group_rank": 18.0,
    "drilldown": 8.0,
    "form": 10.0,
    "file_upload": 45.0,
    "signature": 30.0,
    "heatmap": 12.0,
    "hotspot": 12.0,
    "highlight": 18.0,
    "video": 90.0,
    "descriptive": 2.0,
    "timing": 0.0,
    "captcha": 12.0,
}


def _word_seconds(text: str) -> float:
    # 200 words/minute is a neutral planning assumption, not a promise about completion time.
    return len(text.split()) * 0.3


def estimate_question_seconds(question: Mapping[str, Any]) -> float:
    qtype = str(question.get("type", ""))
    seconds = BASE_SECONDS.get(qtype, 6.0)
    seconds += _word_seconds(str(question.get("text", "")))
    seconds += _word_seconds(str(question.get("help_text", "")))
    choices = question.get("choices", []) if isinstance(question.get("choices"), list) else []
    rows = question.get("rows", []) if isinstance(question.get("rows"), list) else []
    columns = question.get("columns", []) if isinstance(question.get("columns"), list) else []
    fields = question.get("fields", []) if isinstance(question.get("fields"), list) else []

    if qtype in {"single_choice", "multi_choice", "dropdown", "rank", "constant_sum", "maxdiff", "pick_group_rank", "drilldown"}:
        seconds += len(choices) * (0.6 if qtype in {"single_choice", "dropdown"} else 1.4)
    if qtype in {"matrix", "likert_matrix", "bipolar_matrix", "side_by_side"}:
        seconds += len(rows) * 2.5 + len(columns) * 0.4
    elif qtype in {"rank_order_matrix", "constant_sum_matrix", "text_entry_matrix"}:
        seconds += len(rows) * 4.0 + len(columns) * 0.8
    if qtype == "form":
        seconds += sum(estimate_question_seconds(field) for field in fields)
    if question.get("sensitive"):
        seconds *= 1.20
    if question.get("required"):
        seconds += 0.5
    return round(seconds, 1)


def estimate_burden(data: Mapping[str, Any]) -> dict[str, Any]:
    question_rows: list[dict[str, Any]] = []
    for context in iter_question_contexts(data):
        seconds = estimate_question_seconds(context.question)
        question_rows.append(
            {
                "block_id": context.block_id,
                "question_id": context.question.get("id"),
                "type": context.question.get("type"),
                "seconds": seconds,
            }
        )
    intro = 10.0 + len(data.get("blocks", [])) * 2.0
    estimated_seconds = round(intro + sum(row["seconds"] for row in question_rows), 1)
    hotspots = sorted(question_rows, key=lambda row: row["seconds"], reverse=True)[:5]
    return {
        "assumption": "Planning heuristic based on reading load, interaction type, option count, sensitivity, and open-response effort; validate with pilot completion-time data.",
        "estimated_seconds": estimated_seconds,
        "estimated_minutes": round(estimated_seconds / 60.0, 1),
        "plausible_range_minutes": [round(estimated_seconds * 0.7 / 60.0, 1), round(estimated_seconds * 1.6 / 60.0, 1)],
        "questions": question_rows,
        "hotspots": hotspots,
    }


def _text_report(report: Mapping[str, Any]) -> str:
    low, high = report["plausible_range_minutes"]
    lines = [
        "Respondent burden estimate",
        f"Estimated median: {report['estimated_minutes']:.1f} minutes",
        f"Planning range: {low:.1f}–{high:.1f} minutes",
        "",
        "Largest estimated contributors:",
    ]
    for row in report["hotspots"]:
        lines.append(f"- {row['question_id']} ({row['type']}): {row['seconds']:.1f} seconds")
    lines.extend(["", f"Caveat: {report['assumption']}"])
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Estimate survey completion burden and list the highest-effort questions.")
    parser.add_argument("survey", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    args = parser.parse_args(argv)
    data = load_survey(args.survey)
    report = estimate_burden(data)
    if args.output_format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(_text_report(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
