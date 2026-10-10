#!/usr/bin/env python3
"""Validate Qualtrics Simple or Advanced TXT structure and encoding."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

TAG = re.compile(r"^\[\[([^\]]+)\]\]$")
SIMPLE_QUESTION = re.compile(r"^([A-Za-z][A-Za-z0-9_.-]*)\.\s+\S")
ADVANCED_EXACT = {
    "AdvancedFormat", "SimpleFormat", "Choices", "Answers", "AdvancedChoices", "AdvancedAnswers",
    "MultipleAnswer", "PageBreak", "Randomize", "Block", "MC", "Matrix", "TextEntry", "TE",
    "SingleLine", "Essay", "Form", "ConstantSum", "CS", "RankOrder", "RO", "DB", "Vertical",
    "Horizontal", "DropDown", "Select", "MultiSelect", "SingleAnswer", "Question:Text",
}
SIMPLE_EXACT = {"SimpleFormat", "MultipleAnswer", "PageBreak", "Randomize", "Block"}


@dataclass(frozen=True)
class QualtricsIssue:
    severity: str
    code: str
    line: int
    message: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _recognized_advanced(content: str) -> bool:
    return content in ADVANCED_EXACT or any(
        content.startswith(prefix)
        for prefix in ("Block:", "ID:", "ED:", "Question:", "Choice:", "Answer:")
    ) or content in {"Choice", "Answer"}


def _recognized_simple(content: str) -> bool:
    return content in SIMPLE_EXACT or content.startswith("Block:")


def _finalize_question(state: dict[str, object], issues: list[QualtricsIssue], line: int) -> None:
    if not state.get("active"):
        return
    qtype = str(state.get("type", ""))
    if not state.get("has_text"):
        issues.append(QualtricsIssue("error", "QUESTION_TEXT_MISSING", int(state.get("line", line)), "Question has no text after its tags."))
    if qtype in {"MC", "CS", "RO"} and not state.get("has_choices"):
        issues.append(QualtricsIssue("error", "CHOICES_MISSING", int(state.get("line", line)), f"{qtype} question has no Choices/AdvancedChoices section."))
    if qtype == "Matrix":
        if not state.get("has_choices"):
            issues.append(QualtricsIssue("error", "MATRIX_ROWS_MISSING", int(state.get("line", line)), "Matrix question has no Choices/AdvancedChoices rows."))
        if not state.get("has_answers"):
            issues.append(QualtricsIssue("error", "MATRIX_COLUMNS_MISSING", int(state.get("line", line)), "Matrix question has no Answers/AdvancedAnswers columns."))


def _validate_advanced(lines: list[str]) -> list[QualtricsIssue]:
    issues: list[QualtricsIssue] = []
    ids: dict[str, int] = {}
    state: dict[str, object] = {"active": False}
    section: str | None = None

    for index, raw in enumerate(lines, 1):
        stripped = raw.strip()
        match = TAG.match(stripped)
        if match:
            content = match.group(1)
            if not _recognized_advanced(content):
                issues.append(QualtricsIssue("error", "UNKNOWN_TAG", index, f"Unknown or unsupported Advanced TXT tag: [[{content}]]"))
                continue
            if content.startswith("Question:") or content in {"MC", "Matrix", "TE", "TextEntry", "CS", "ConstantSum", "RO", "RankOrder", "DB", "Question:Text"}:
                _finalize_question(state, issues, index)
                if content.startswith("Question:"):
                    parts = content.split(":")
                    qtype = parts[1] if len(parts) > 1 else ""
                    qtype = {"Text": "DB", "TextEntry": "TE", "ConstantSum": "CS", "RankOrder": "RO"}.get(qtype, qtype)
                else:
                    qtype = {"TextEntry": "TE", "ConstantSum": "CS", "RankOrder": "RO", "Question:Text": "DB"}.get(content, content)
                state = {"active": True, "type": qtype, "line": index, "has_text": False, "has_choices": False, "has_answers": False}
                section = None
            elif content.startswith("ID:"):
                value = content[3:].strip()
                if not value:
                    issues.append(QualtricsIssue("error", "ID_EMPTY", index, "Question ID tag is empty."))
                elif value in ids:
                    issues.append(QualtricsIssue("error", "DUPLICATE_ID", index, f"Question ID '{value}' duplicates line {ids[value]}."))
                else:
                    ids[value] = index
            elif content in {"Choices", "AdvancedChoices"}:
                section = "choices"
                if state.get("active"):
                    state["has_choices"] = True
            elif content in {"Answers", "AdvancedAnswers"}:
                section = "answers"
                if state.get("active"):
                    state["has_answers"] = True
            elif content.startswith("Choice"):
                if section != "choices":
                    issues.append(QualtricsIssue("error", "CHOICE_OUTSIDE_SECTION", index, "Choice marker appears outside a Choices/AdvancedChoices section."))
            elif content.startswith("Answer"):
                if section != "answers":
                    issues.append(QualtricsIssue("error", "ANSWER_OUTSIDE_SECTION", index, "Answer marker appears outside an Answers/AdvancedAnswers section."))
            elif content.startswith("Block") or content == "PageBreak":
                section = None
            continue

        if stripped and state.get("active") and section is None:
            state["has_text"] = True
    _finalize_question(state, issues, len(lines) + 1)
    return issues


def _validate_simple(lines: list[str]) -> list[QualtricsIssue]:
    issues: list[QualtricsIssue] = []
    ids: dict[str, int] = {}
    in_question = False
    choices_started = False
    for index, raw in enumerate(lines, 1):
        stripped = raw.strip()
        tag = TAG.match(stripped)
        if tag:
            content = tag.group(1)
            if not _recognized_simple(content):
                issues.append(QualtricsIssue("error", "UNKNOWN_TAG", index, f"Unknown or unsupported Simple TXT tag: [[{content}]]"))
            continue
        match = SIMPLE_QUESTION.match(stripped)
        if match:
            export_tag = match.group(1)
            if export_tag in ids:
                issues.append(QualtricsIssue("error", "DUPLICATE_ID", index, f"Export tag '{export_tag}' duplicates line {ids[export_tag]}."))
            else:
                ids[export_tag] = index
            in_question = True
            choices_started = False
            continue
        if in_question and not stripped:
            choices_started = True
            continue
        if in_question and choices_started and stripped and ":" in stripped:
            issues.append(QualtricsIssue("warning", "SIMPLE_CHOICE_COLON", index, "Colon appears in a likely Simple TXT answer choice; add it after import or replace it."))
    if not ids:
        issues.append(QualtricsIssue("error", "NO_QUESTIONS", 1, "No Simple TXT questions with an export tag followed by a period were found."))
    return issues


def validate_text(text: str, *, encoding_name: str = "utf-8") -> list[QualtricsIssue]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")
    first = next((line.strip() for line in lines if line.strip()), "")
    mode = "advanced" if first == "[[AdvancedFormat]]" else "simple"
    issues = _validate_advanced(lines) if mode == "advanced" else _validate_simple(lines)
    if mode == "advanced" and first != "[[AdvancedFormat]]":
        issues.append(QualtricsIssue("error", "ADVANCED_HEADER", 1, "Advanced TXT must begin with [[AdvancedFormat]]."))
    if "utf-16" in encoding_name.lower():
        issues.insert(0, QualtricsIssue("error", "ENCODING_UTF16", 1, "Qualtrics TXT should be saved as UTF-8, not UTF-16."))
    if "\x00" in text:
        issues.insert(0, QualtricsIssue("error", "NUL_BYTES", 1, "NUL bytes suggest an incompatible encoding."))
    return sorted(issues, key=lambda issue: (0 if issue.severity == "error" else 1, issue.line, issue.code))


def validate_file(path: str | Path) -> list[QualtricsIssue]:
    source = Path(path)
    raw = source.read_bytes()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        try:
            text = raw.decode("utf-16")
        except UnicodeDecodeError:
            text = ""
        return validate_text(text, encoding_name="utf-16")
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        return [QualtricsIssue("error", "ENCODING_INVALID", 1, f"File is not valid UTF-8: {exc}")]
    issues = validate_text(text, encoding_name="utf-8")
    if raw.startswith(b"\xef\xbb\xbf"):
        issues.append(QualtricsIssue("warning", "UTF8_BOM", 1, "UTF-8 BOM detected; UTF-8 without BOM is the safest interchange form."))
    if b"\r\n" in raw:
        issues.append(QualtricsIssue("info", "CRLF", 1, "CRLF line endings detected; they are normalized by this validator."))
    return issues


def _text_report(issues: Iterable[QualtricsIssue]) -> str:
    rows = list(issues)
    if not rows:
        return "Qualtrics TXT validation: PASS\n"
    return "\n".join(f"{issue.severity.upper():7} line {issue.line}: {issue.code} — {issue.message}" for issue in rows) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Qualtrics Simple or Advanced TXT syntax and encoding.")
    parser.add_argument("file", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args(argv)
    try:
        issues = validate_file(args.file)
    except OSError as exc:
        print(f"Cannot read {args.file}: {exc}", file=sys.stderr)
        return 2
    if args.output_format == "json":
        print(json.dumps({"issues": [issue.to_dict() for issue in issues]}, indent=2, ensure_ascii=False))
    else:
        print(_text_report(issues), end="")
    if any(issue.severity == "error" for issue in issues):
        return 1
    if args.fail_on_warning and any(issue.severity == "warning" for issue in issues):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
