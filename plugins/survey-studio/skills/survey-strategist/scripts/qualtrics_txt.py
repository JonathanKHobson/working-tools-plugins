#!/usr/bin/env python3
"""Conservative Qualtrics Simple and Advanced TXT exporters.

The exporter uses only documented text-import constructs. Features that the
TXT format cannot represent are surfaced as warnings rather than encoded with
invented tags. QSF generation is intentionally out of scope.
"""

from __future__ import annotations

import json
import math
from decimal import Decimal
from typing import Any, Iterable, Mapping

from survey_io import iter_question_contexts, validate_survey

MATRIX_TYPES = {"matrix", "likert_matrix", "bipolar_matrix"}
SCALE_TYPES = {"likert", "rating", "nps", "slider", "number_scale"}
CHOICE_TYPES = {"single_choice", "multi_choice", "dropdown", "yes_no"}


def _warn(warnings: list[str], message: str) -> None:
    if message not in warnings:
        warnings.append(message)


def _multiline(value: Any) -> list[str]:
    text = str(value).replace("\r\n", "\n").replace("\r", "\n").strip()
    return text.split("\n") if text else [""]


def _numeric_recode(value: Any, fallback: int, warnings: list[str], context: str) -> str:
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    if isinstance(value, str) and value.strip().lstrip("-").isdigit():
        return value.strip()
    _warn(
        warnings,
        f"{context}: Qualtrics TXT recodes are emitted as integers; nonnumeric value {value!r} was assigned deterministic recode {fallback}. Preserve the original value in the codebook.",
    )
    return str(fallback)


def _scale_values(scale: Mapping[str, Any]) -> list[Decimal]:
    minimum = Decimal(str(scale.get("min", 1)))
    maximum = Decimal(str(scale.get("max", 5)))
    step = Decimal(str(scale.get("step", 1)))
    if step <= 0 or maximum < minimum:
        return []
    values: list[Decimal] = []
    value = minimum
    guard = 0
    while value <= maximum and guard < 1000:
        values.append(value)
        value += step
        guard += 1
    return values


def _decimal_label(value: Decimal) -> str:
    return str(int(value)) if value == value.to_integral_value() else format(value.normalize(), "f")


def _scale_choices(question: Mapping[str, Any]) -> list[dict[str, Any]]:
    scale = question.get("scale", {})
    anchors = {str(k): str(v) for k, v in scale.get("anchors", {}).items()} if isinstance(scale, Mapping) else {}
    choices: list[dict[str, Any]] = []
    for value in _scale_values(scale if isinstance(scale, Mapping) else {}):
        numeric = _decimal_label(value)
        label = anchors.get(numeric, numeric)
        if label != numeric:
            label = f"{numeric} — {label}"
        choices.append({"id": f"v_{numeric.replace('.', '_').replace('-', 'm')}", "label": label, "value": numeric})
    if isinstance(scale, Mapping) and scale.get("include_not_applicable"):
        choices.append({"id": "not_applicable", "label": scale.get("not_applicable_label", "Not applicable"), "value": 99})
    return choices


def _advanced_options(tag: str, items: Iterable[Mapping[str, Any]], warnings: list[str], context: str) -> list[str]:
    marker = "Choice" if tag == "AdvancedChoices" else "Answer"
    lines = [f"[[{tag}]]"]
    for index, item in enumerate(items, 1):
        recode = _numeric_recode(item.get("value"), index, warnings, context)
        lines.append(f"[[{marker}:{recode}]]")
        lines.extend(_multiline(item.get("label", "")))
    return lines


def _unsupported_advanced(question: Mapping[str, Any], warnings: list[str]) -> list[str]:
    qid = str(question.get("id", "unknown"))
    qtype = str(question.get("type", "unknown"))
    _warn(
        warnings,
        f"{qid}: question type '{qtype}' is not representable in documented Qualtrics Advanced TXT and was emitted as a Text/Graphic programming marker. Replace it in Survey Builder after import.",
    )
    return [
        "[[Question:DB]]",
        f"[[ID:{question.get('export_tag', qid)}]]",
        f"[Manual programming required — original type: {qtype}]",
        *_multiline(question.get("text", "")),
    ]


def _advanced_question(question: Mapping[str, Any], warnings: list[str]) -> list[str]:
    qid = str(question["id"])
    export_tag = str(question.get("export_tag", qid))
    qtype = str(question["type"])
    lines: list[str]

    if qtype == "single_choice" or qtype == "yes_no":
        lines = ["[[Question:MC:SingleAnswer:Vertical]]", f"[[ID:{export_tag}]]", *_multiline(question["text"])]
        lines.extend(_advanced_options("AdvancedChoices", question.get("choices", []), warnings, qid))
    elif qtype == "multi_choice":
        lines = ["[[Question:MC:MultipleAnswer:Vertical]]", f"[[ID:{export_tag}]]", *_multiline(question["text"])]
        lines.extend(_advanced_options("AdvancedChoices", question.get("choices", []), warnings, qid))
    elif qtype == "dropdown":
        lines = ["[[Question:MC:Dropdown]]", f"[[ID:{export_tag}]]", *_multiline(question["text"])]
        lines.extend(_advanced_options("AdvancedChoices", question.get("choices", []), warnings, qid))
    elif qtype in SCALE_TYPES:
        choices = _scale_choices(question)
        lines = ["[[Question:MC:SingleAnswer:Horizontal]]", f"[[ID:{export_tag}]]", *_multiline(question["text"])]
        lines.extend(_advanced_options("AdvancedChoices", choices, warnings, qid))
        _warn(
            warnings,
            f"{qid}: native '{qtype}' was mapped to a multiple-choice horizontal scale because Advanced TXT documents MC but not this native question type. Confirm display, labels, scoring, and analytics after import.",
        )
    elif qtype in MATRIX_TYPES:
        lines = ["[[Question:Matrix:SingleAnswer]]", f"[[ID:{export_tag}]]", *_multiline(question["text"])]
        lines.extend(_advanced_options("AdvancedChoices", question.get("rows", []), warnings, f"{qid} row"))
        lines.extend(_advanced_options("AdvancedAnswers", question.get("columns", []), warnings, f"{qid} column"))
    elif qtype == "text":
        lines = ["[[Question:TE:SingleLine]]", f"[[ID:{export_tag}]]", *_multiline(question["text"])]
    elif qtype == "textarea":
        lines = ["[[Question:TE:Essay]]", f"[[ID:{export_tag}]]", *_multiline(question["text"])]
    elif qtype in {"numeric", "date", "calendar"}:
        lines = ["[[Question:TE:SingleLine]]", f"[[ID:{export_tag}]]", *_multiline(question["text"])]
        _warn(
            warnings,
            f"{qid}: '{qtype}' was imported as single-line Text Entry. Configure content type, date handling, and validation in Survey Builder.",
        )
    elif qtype == "form":
        lines = ["[[Question:TE:Form]]", f"[[ID:{export_tag}]]", *_multiline(question["text"]), "[[Choices]]"]
        for field in question.get("fields", []):
            lines.extend(_multiline(field.get("text", field.get("id", "Field"))))
        _warn(warnings, f"{qid}: form field validation and PII handling must be configured after import.")
    elif qtype == "constant_sum":
        lines = ["[[Question:CS]]", f"[[ID:{export_tag}]]", *_multiline(question["text"])]
        lines.extend(_advanced_options("AdvancedChoices", question.get("choices", []), warnings, qid))
        _warn(warnings, f"{qid}: verify the required total and validation after import.")
    elif qtype == "rank":
        lines = ["[[Question:RO]]", f"[[ID:{export_tag}]]", *_multiline(question["text"])]
        lines.extend(_advanced_options("AdvancedChoices", question.get("choices", []), warnings, qid))
    elif qtype == "descriptive":
        lines = ["[[Question:DB]]", f"[[ID:{export_tag}]]", *_multiline(question["text"])]
    else:
        lines = _unsupported_advanced(question, warnings)

    if question.get("display_if"):
        _warn(warnings, f"{qid}: display logic is not encoded by this TXT exporter; program it after import from the canonical display_if metadata.")
    if question.get("skip_to"):
        _warn(warnings, f"{qid}: skip logic is not encoded by this TXT exporter; program it after import from the canonical skip_to metadata.")
    if question.get("randomize_choices"):
        _warn(warnings, f"{qid}: choice randomization is not encoded in Advanced TXT by this conservative exporter; configure it after import.")
    if question.get("required") or question.get("validation"):
        _warn(warnings, "Required-response and validation settings need a post-import Survey Builder review because they are not represented by the documented tags used here.")
    return lines


def export_advanced_txt(data: Mapping[str, Any]) -> tuple[str, list[str]]:
    """Return documented Qualtrics Advanced TXT plus explicit compatibility warnings."""
    validate_survey(data)
    warnings: list[str] = []
    lines = ["[[AdvancedFormat]]", ""]

    embedded = data.get("metadata", {}).get("qualtrics", {}).get("embedded_data", {}) if isinstance(data.get("metadata"), Mapping) else {}
    if isinstance(embedded, Mapping):
        for field, value in embedded.items():
            if value in (None, ""):
                lines.append(f"[[ED:{field}]]")
            else:
                lines.append(f"[[ED:{field}:{value}]]")
        if embedded:
            lines.append("")

    for block_index, block in enumerate(data.get("blocks", [])):
        block_name = str(block.get("title") or block.get("id") or f"Block {block_index + 1}").replace("]]", "] ]")
        lines.extend([f"[[Block:{block_name}]]", ""])
        if block.get("randomize"):
            _warn(warnings, f"Block '{block.get('id')}': block randomization is not encoded; configure it after import.")
        if block.get("display_if"):
            _warn(warnings, f"Block '{block.get('id')}': block display logic is not encoded; configure it after import.")
        for question in block.get("questions", []):
            lines.extend(_advanced_question(question, warnings))
            lines.append("")
        if block.get("page_break_after"):
            lines.extend(["[[PageBreak]]", ""])
    return "\n".join(lines).rstrip() + "\n", warnings


def _simple_choice_label(label: Any, warnings: list[str], qid: str) -> str:
    text = str(label).replace("\r", " ").replace("\n", " ").strip()
    if ":" in text:
        _warn(warnings, f"{qid}: colons in Simple TXT choices were replaced with an em dash for import compatibility.")
        text = text.replace(":", " —")
    return text


def _simple_question(question: Mapping[str, Any], warnings: list[str]) -> list[str]:
    qid = str(question["id"])
    export_tag = str(question.get("export_tag", qid))
    qtype = str(question["type"])
    text = " ".join(_multiline(question["text"]))
    lines = [f"{export_tag}. {text}"]

    if qtype == "multi_choice":
        lines.extend(["[[MultipleAnswer]]", ""])
        if question.get("randomize_choices"):
            lines.append("[[Randomize]]")
        lines.extend(_simple_choice_label(choice.get("label", ""), warnings, qid) for choice in question.get("choices", []))
    elif qtype in {"single_choice", "yes_no", "dropdown"}:
        lines.append("")
        if question.get("randomize_choices"):
            lines.append("[[Randomize]]")
        lines.extend(_simple_choice_label(choice.get("label", ""), warnings, qid) for choice in question.get("choices", []))
        if qtype == "dropdown":
            _warn(warnings, f"{qid}: Simple TXT imports as multiple choice; set the dropdown display in Survey Builder after import.")
    elif qtype in SCALE_TYPES:
        lines.append("")
        lines.extend(_simple_choice_label(choice["label"], warnings, qid) for choice in _scale_choices(question))
        _warn(warnings, f"{qid}: native '{qtype}' was mapped to multiple choice in Simple TXT; verify scoring and display after import.")
    elif qtype in MATRIX_TYPES:
        lines.append("")
        lines.extend(_simple_choice_label(row.get("label", ""), warnings, qid) for row in question.get("rows", []))
        lines.append("")
        lines.extend(_simple_choice_label(column.get("label", ""), warnings, qid) for column in question.get("columns", []))
    elif qtype == "descriptive":
        pass
    else:
        lines[0] = f"{export_tag}. [Manual programming required — original type: {qtype}] {text}"
        _warn(
            warnings,
            f"{qid}: '{qtype}' is not safely representable in Simple TXT and was emitted as a Text/Graphic programming marker. Use Advanced TXT or replace it after import.",
        )

    if question.get("display_if") or question.get("skip_to"):
        _warn(warnings, f"{qid}: branching/display logic is not encoded in Simple TXT; configure it after import.")
    if question.get("required") or question.get("validation"):
        _warn(warnings, "Required-response and validation settings require a post-import Survey Builder review.")
    return lines


def export_simple_txt(data: Mapping[str, Any]) -> tuple[str, list[str]]:
    """Return Qualtrics Simple TXT for supported MC/matrix content plus warnings."""
    validate_survey(data)
    warnings: list[str] = []
    chunks: list[str] = []
    for block_index, block in enumerate(data.get("blocks", [])):
        block_name = str(block.get("title") or block.get("id") or f"Block {block_index + 1}").replace("]]", "] ]")
        chunks.append(f"[[Block:{block_name}]]")
        for question in block.get("questions", []):
            chunks.append("\n".join(_simple_question(question, warnings)))
        if block.get("page_break_after"):
            chunks.append("[[PageBreak]]")
        if block.get("randomize") or block.get("display_if"):
            _warn(warnings, f"Block '{block.get('id')}': block randomization/display logic is not encoded in Simple TXT.")
    return "\n\n\n".join(chunks).rstrip() + "\n", warnings
