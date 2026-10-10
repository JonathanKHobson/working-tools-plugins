#!/usr/bin/env python3
"""Generate analysis-ready codebooks from a canonical survey specification."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from survey_io import iter_question_contexts, load_survey

FIELDS = [
    "survey_id",
    "block_id",
    "block_title",
    "record_type",
    "question_id",
    "export_tag",
    "question_type",
    "required",
    "question_text",
    "construct",
    "rationale",
    "analysis_use",
    "option_id",
    "option_value",
    "option_label",
    "exclusive",
    "open_text",
    "scale_min",
    "scale_max",
    "scale_step",
    "sensitive",
    "pii",
    "display_if",
    "skip_to",
]


def _base_row(data: Mapping[str, Any], context: Any) -> dict[str, Any]:
    question = context.question
    scale = question.get("scale", {}) if isinstance(question.get("scale"), Mapping) else {}
    return {
        "survey_id": data.get("survey", {}).get("id", ""),
        "block_id": context.block_id,
        "block_title": context.block_title,
        "record_type": "question",
        "question_id": question.get("id", ""),
        "export_tag": question.get("export_tag", question.get("id", "")),
        "question_type": question.get("type", ""),
        "required": bool(question.get("required")),
        "question_text": question.get("text", ""),
        "construct": question.get("construct", ""),
        "rationale": question.get("rationale", ""),
        "analysis_use": question.get("analysis_use", ""),
        "option_id": "",
        "option_value": "",
        "option_label": "",
        "exclusive": "",
        "open_text": "",
        "scale_min": scale.get("min", ""),
        "scale_max": scale.get("max", ""),
        "scale_step": scale.get("step", ""),
        "sensitive": bool(question.get("sensitive")),
        "pii": bool(question.get("pii")),
        "display_if": json.dumps(question.get("display_if", ""), ensure_ascii=False, sort_keys=True),
        "skip_to": question.get("skip_to", ""),
    }


def codebook_rows(data: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return one question row plus child rows for choices, matrix axes, and scale anchors."""
    rows: list[dict[str, Any]] = []
    for context in iter_question_contexts(data):
        base = _base_row(data, context)
        rows.append(dict(base))
        question = context.question
        for field_name, record_type in (("choices", "choice"), ("rows", "matrix_row"), ("columns", "matrix_column")):
            items = question.get(field_name, [])
            if not isinstance(items, list):
                continue
            for item in items:
                if not isinstance(item, Mapping):
                    continue
                row = dict(base)
                row.update(
                    {
                        "record_type": record_type,
                        "option_id": item.get("id", ""),
                        "option_value": item.get("value", ""),
                        "option_label": item.get("label", ""),
                        "exclusive": bool(item.get("exclusive")),
                        "open_text": bool(item.get("open_text")),
                    }
                )
                rows.append(row)
        scale = question.get("scale", {})
        anchors = scale.get("anchors", {}) if isinstance(scale, Mapping) else {}
        if isinstance(anchors, Mapping):
            def anchor_sort(item: tuple[Any, Any]) -> tuple[int, float | str]:
                try:
                    return (0, float(item[0]))
                except (TypeError, ValueError):
                    return (1, str(item[0]))
            for value, label in sorted(anchors.items(), key=anchor_sort):
                row = dict(base)
                row.update(
                    {
                        "record_type": "scale_anchor",
                        "option_id": f"anchor_{value}",
                        "option_value": value,
                        "option_label": label,
                    }
                )
                rows.append(row)
    return rows


def _cell(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return ""
    return str(value)


def write_codebook(data: Mapping[str, Any], output: str | Path, output_format: str = "csv") -> Path:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = codebook_rows(data)
    fmt = output_format.lower()
    if fmt == "csv":
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    elif fmt == "json":
        path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    elif fmt in {"markdown", "md"}:
        display_fields = [
            "record_type", "question_id", "export_tag", "question_type", "required", "question_text",
            "option_value", "option_label", "construct", "analysis_use",
        ]
        lines = [
            "| " + " | ".join(display_fields) + " |",
            "|" + "|".join("---" for _ in display_fields) + "|",
        ]
        for row in rows:
            values = [_cell(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in display_fields]
            lines.append("| " + " | ".join(values) + " |")
        path.write_text("# Survey codebook\n\n" + "\n".join(lines) + "\n", encoding="utf-8")
    else:
        raise ValueError(f"Unsupported codebook format: {output_format}")
    return path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a CSV, Markdown, or JSON survey codebook.")
    parser.add_argument("survey", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--format", choices=("csv", "markdown", "json"), default="csv", dest="output_format")
    args = parser.parse_args(argv)
    data = load_survey(args.survey)
    write_codebook(data, args.output, args.output_format)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
