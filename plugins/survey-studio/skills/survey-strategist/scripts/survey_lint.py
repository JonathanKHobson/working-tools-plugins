#!/usr/bin/env python3
"""Heuristic and structural quality audit for canonical survey files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from survey_io import SurveyValidationError, iter_question_contexts, load_survey, validate_survey

SEVERITY_ORDER = {"info": 0, "warning": 1, "error": 2}
CLOSED_TYPES = {
    "single_choice", "multi_choice", "dropdown", "yes_no", "likert", "rating", "nps", "slider", "number_scale",
    "matrix", "likert_matrix", "bipolar_matrix", "rank_order_matrix", "constant_sum_matrix", "side_by_side",
    "rank", "constant_sum", "maxdiff", "pick_group_rank", "drilldown",
}
OPEN_TYPES = {"text", "textarea", "text_entry_matrix", "video"}
MATRIX_TYPES = {
    "matrix", "likert_matrix", "bipolar_matrix", "rank_order_matrix", "constant_sum_matrix", "text_entry_matrix", "side_by_side"
}
DEMOGRAPHIC_MARKERS = {
    "age", "gender", "sex", "race", "ethnicity", "income", "education", "marital", "household", "demographic",
    "religion", "disability", "nationality", "postcode", "zip", "socioeconomic", "employment status",
}
SENSITIVE_MARKERS = {
    "health", "diagnosis", "disability", "income", "salary", "debt", "religion", "political", "sexual", "race", "ethnicity",
    "criminal", "immigration", "biometric", "genetic", "pregnancy", "trauma", "abuse", "mental health",
}
VAGUE_TIME = re.compile(r"\b(recently|often|regularly|usually|frequently|sometimes|occasionally|a while ago)\b", re.I)
LEADING = re.compile(
    r"\b(don['’]t you agree|wouldn['’]t you say|isn['’]t it true|obviously|clearly|of course|how great|how helpful|shouldn['’]t)\b",
    re.I,
)
DOUBLE_NEGATIVE = re.compile(
    r"\b(not\b.{0,35}\b(?:never|not|disagree|unlikely)|don['’]t\b.{0,35}\bnot|isn['’]t\b.{0,35}\bnot)\b",
    re.I,
)
DOUBLE_BARREL = re.compile(
    r"\b(?:and|or)\s+(?:how|whether|why|easy|difficult|clear|useful|helpful|fast|reliable|satisfied|confident|comfortable)\b",
    re.I,
)
BALANCED_BIPOLAR = re.compile(
    r"\b(?:easy or difficult|difficult or easy|clear or unclear|unclear or clear|helpful or unhelpful|unhelpful or helpful|"
    r"satisfied or dissatisfied|dissatisfied or satisfied|likely or unlikely|unlikely or likely|relevant or irrelevant|"
    r"irrelevant or relevant|comfortable or uncomfortable|uncomfortable or comfortable)\b",
    re.I,
)
RANGE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*(?:-|–|—|to)\s*(-?\d+(?:\.\d+)?)\s*$", re.I)


@dataclass(frozen=True)
class Issue:
    severity: str
    code: str
    message: str
    question_id: str | None = None
    block_id: str | None = None
    suggestion: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {key: value for key, value in asdict(self).items() if value is not None}


def _issue(
    severity: str,
    code: str,
    message: str,
    *,
    question: Mapping[str, Any] | None = None,
    block_id: str | None = None,
    suggestion: str | None = None,
) -> Issue:
    return Issue(
        severity=severity,
        code=code,
        message=message,
        question_id=str(question.get("id")) if question and question.get("id") else None,
        block_id=block_id,
        suggestion=suggestion,
    )


def _question_position(data: Mapping[str, Any]) -> dict[str, int]:
    return {str(context.question.get("id")): index for index, context in enumerate(iter_question_contexts(data))}


def _contains_marker(text: str, markers: Iterable[str]) -> bool:
    """Match whole words/phrases rather than accidental substrings such as age in manageable."""
    return any(re.search(rf"(?<!\w){re.escape(marker)}(?!\w)", text, re.I) for marker in markers)


def _numeric_ranges(choices: Sequence[Mapping[str, Any]]) -> list[tuple[float, float, str]]:
    ranges: list[tuple[float, float, str]] = []
    for choice in choices:
        label = str(choice.get("label", ""))
        match = RANGE.match(label)
        if match:
            low, high = float(match.group(1)), float(match.group(2))
            ranges.append((min(low, high), max(low, high), label))
    return ranges


def _scale_anchor_issue(question: Mapping[str, Any], block_id: str) -> list[Issue]:
    issues: list[Issue] = []
    scale = question.get("scale")
    if not isinstance(scale, Mapping):
        return issues
    minimum = scale.get("min")
    maximum = scale.get("max")
    anchors = scale.get("anchors", {})
    if isinstance(minimum, (int, float)) and isinstance(maximum, (int, float)):
        if maximum <= minimum:
            issues.append(_issue("error", "SCALE_DIRECTION", "Scale maximum must be greater than its minimum.", question=question, block_id=block_id))
        if isinstance(anchors, Mapping):
            keys = {str(key) for key in anchors}
            if str(minimum) not in keys or str(maximum) not in keys:
                issues.append(
                    _issue(
                        "warning",
                        "SCALE_ENDPOINTS_UNLABELED",
                        "Scale does not explicitly label both endpoints.",
                        question=question,
                        block_id=block_id,
                        suggestion="Label the minimum and maximum with construct-specific, symmetric anchors.",
                    )
                )
    return issues


def lint_survey(data: Mapping[str, Any], *, include_info: bool = False) -> list[Issue]:
    """Return structural, methodological, privacy, accessibility, and burden diagnostics."""
    issues: list[Issue] = []
    try:
        validate_survey(data)
    except SurveyValidationError as exc:
        for message in exc.messages:
            issues.append(Issue("error", "STRUCTURE", message))
        # Continue where possible so one run gives a useful audit rather than a single failure.

    contexts = list(iter_question_contexts(data))
    positions = _question_position(data)
    privacy = data.get("survey", {}).get("privacy", {}) if isinstance(data.get("survey"), Mapping) else {}
    collects_pii = bool(privacy.get("collects_pii")) if isinstance(privacy, Mapping) else False
    open_count = 0
    required_count = 0
    sensitive_count = 0

    for position, context in enumerate(contexts):
        question = context.question
        qid = str(question.get("id", ""))
        qtype = str(question.get("type", ""))
        text = str(question.get("text", "")).strip()
        lower = f"{qid} {question.get('construct', '')} {text}".lower()
        word_count = len(re.findall(r"\b[\w'’.-]+\b", text))
        sentence_count = len(re.findall(r"[.!?](?:\s|$)", text))

        if qtype in OPEN_TYPES:
            open_count += 1
        if question.get("required"):
            required_count += 1
        is_sensitive = bool(question.get("sensitive")) or _contains_marker(lower, SENSITIVE_MARKERS)
        if is_sensitive:
            sensitive_count += 1

        if word_count > 30 and qtype != "descriptive":
            issues.append(
                _issue(
                    "warning",
                    "WORDING_LONG",
                    f"Question has {word_count} words; long items increase reading effort and ambiguity.",
                    question=question,
                    block_id=context.block_id,
                    suggestion="Move context to help text and keep the actual question to one focused sentence.",
                )
            )
        if sentence_count > 1 and qtype != "descriptive":
            issues.append(
                _issue(
                    "warning",
                    "WORDING_MULTI_SENTENCE",
                    "Question text contains more than one sentence.",
                    question=question,
                    block_id=context.block_id,
                    suggestion="Ask one thing in one sentence; move instructions into help text.",
                )
            )
        if LEADING.search(text):
            issues.append(
                _issue(
                    "warning",
                    "WORDING_LEADING",
                    "Question uses leading or evaluative language that can cue a preferred answer.",
                    question=question,
                    block_id=context.block_id,
                    suggestion="Use neutral, descriptive wording without agreement cues or praise.",
                )
            )
        if DOUBLE_BARREL.search(text) and not BALANCED_BIPOLAR.search(text):
            issues.append(
                _issue(
                    "warning",
                    "WORDING_DOUBLE_BARRELED",
                    "Question may ask about more than one construct in the same response.",
                    question=question,
                    block_id=context.block_id,
                    suggestion="Split the item unless one combined construct is explicitly intended and validated.",
                )
            )
        if DOUBLE_NEGATIVE.search(text):
            issues.append(
                _issue(
                    "warning",
                    "WORDING_DOUBLE_NEGATIVE",
                    "Question contains a likely double negative.",
                    question=question,
                    block_id=context.block_id,
                    suggestion="Rewrite positively and keep scale direction consistent.",
                )
            )
        if VAGUE_TIME.search(text) and not re.search(r"\b(past|last|within)\s+\d+\s+(day|week|month|year)s?\b", text, re.I):
            issues.append(
                _issue(
                    "warning",
                    "WORDING_VAGUE_TIMEFRAME",
                    "Question uses a vague recall period.",
                    question=question,
                    block_id=context.block_id,
                    suggestion="Use a concrete reference period that respondents can remember reliably.",
                )
            )

        if is_sensitive and question.get("required"):
            justification = str(question.get("required_justification", "")).strip()
            if len(justification) >= 20:
                issues.append(
                    _issue(
                        "warning",
                        "SENSITIVE_REQUIRED_JUSTIFIED",
                        "Sensitive question is required with an explicit necessity justification; confirm proportionality and an alternate path.",
                        question=question,
                        block_id=context.block_id,
                        suggestion="Verify the justification with the responsible privacy/ethics owner and state why the service or study cannot proceed without the field.",
                    )
                )
            else:
                issues.append(
                    _issue(
                        "error",
                        "SENSITIVE_REQUIRED",
                        "Sensitive question is required without an explicit necessity justification.",
                        question=question,
                        block_id=context.block_id,
                        suggestion="Make it optional, or add a specific required_justification and confirm proportionality, notice, safeguards, and an alternate path.",
                    )
                )
        if question.get("pii") and not collects_pii:
            issues.append(
                _issue(
                    "error",
                    "PII_PRIVACY_MISMATCH",
                    "Question is marked as collecting personally identifiable information, but survey privacy metadata says PII is not collected.",
                    question=question,
                    block_id=context.block_id,
                    suggestion="Remove the field or update the privacy, consent, security, and retention plan.",
                )
            )
        if is_sensitive and not question.get("sensitive"):
            issues.append(
                _issue(
                    "info",
                    "SENSITIVE_REVIEW",
                    "Question content may be sensitive even though the canonical flag is not set.",
                    question=question,
                    block_id=context.block_id,
                    suggestion="Confirm sensitivity, necessity, consent language, optionality, and access controls.",
                )
            )

        demographic = _contains_marker(lower, DEMOGRAPHIC_MARKERS)
        if demographic and position < max(1, len(contexts) // 2) and not question.get("screening"):
            issues.append(
                _issue(
                    "warning",
                    "DEMOGRAPHIC_EARLY",
                    "Demographic or identity question appears early in the instrument.",
                    question=question,
                    block_id=context.block_id,
                    suggestion="Move it later unless needed for eligibility or immediate routing.",
                )
            )

        choices = question.get("choices", [])
        if isinstance(choices, list) and choices:
            typed_choices = [choice for choice in choices if isinstance(choice, Mapping)]
            ranges = _numeric_ranges(typed_choices)
            for left, right in zip(ranges, ranges[1:]):
                if right[0] <= left[1]:
                    issues.append(
                        _issue(
                            "error",
                            "OPTIONS_OVERLAP",
                            f"Numeric response ranges overlap: '{left[2]}' and '{right[2]}'.",
                            question=question,
                            block_id=context.block_id,
                            suggestion="Use mutually exclusive boundaries such as 18–24 and 25–34.",
                        )
                    )
                    break
            exclusive_labels = [
                str(choice.get("label", ""))
                for choice in typed_choices
                if re.search(r"\b(none|not applicable|prefer not|don['’]t know|no experience)\b", str(choice.get("label", "")), re.I)
                and not choice.get("exclusive")
            ]
            if qtype == "multi_choice" and exclusive_labels:
                issues.append(
                    _issue(
                        "error",
                        "OPTIONS_EXCLUSIVE_NOT_MARKED",
                        f"Mutually exclusive multi-select choice is not marked exclusive: {exclusive_labels[0]!r}.",
                        question=question,
                        block_id=context.block_id,
                    )
                )
            if qtype in {"single_choice", "multi_choice", "dropdown"} and len(typed_choices) >= 3:
                labels = " ".join(str(choice.get("label", "")) for choice in typed_choices)
                if not re.search(r"\b(other|none|not applicable|don['’]t know|not sure|prefer not)\b", labels, re.I):
                    issues.append(
                        _issue(
                            "info",
                            "OPTIONS_EXHAUSTIVENESS_REVIEW",
                            "Closed response set has no explicit catch-all, uncertainty, or non-applicability option.",
                            question=question,
                            block_id=context.block_id,
                            suggestion="Confirm the list is genuinely exhaustive; add an option only when conceptually valid.",
                        )
                    )
            if qtype == "rank" and len(typed_choices) > 7:
                issues.append(
                    _issue(
                        "warning",
                        "RANKING_OVERLOAD",
                        f"Ranking asks respondents to order {len(typed_choices)} items.",
                        question=question,
                        block_id=context.block_id,
                        suggestion="Limit the list, rank only a selected subset, or use MaxDiff/conjoint when justified.",
                    )
                )
            if qtype == "maxdiff" and len(typed_choices) < 4:
                issues.append(_issue("error", "MAXDIFF_TOO_FEW_ITEMS", "MaxDiff requires a sufficiently large item set to create meaningful best–worst tasks.", question=question, block_id=context.block_id))

        issues.extend(_scale_anchor_issue(question, context.block_id))
        scale = question.get("scale", {})
        if qtype == "nps" and isinstance(scale, Mapping) and (scale.get("min"), scale.get("max")) != (0, 10):
            issues.append(
                _issue(
                    "error",
                    "NPS_SCALE",
                    "An item labeled NPS must use the standardized 0–10 response scale; otherwise call it a recommendation rating.",
                    question=question,
                    block_id=context.block_id,
                )
            )
        if qtype == "slider":
            issues.append(
                _issue(
                    "warning",
                    "SLIDER_ACCESSIBILITY",
                    "Slider interaction can create precision and accessibility problems, especially on mobile or with assistive technology.",
                    question=question,
                    block_id=context.block_id,
                    suggestion="Provide keyboard support, visible numeric value, endpoint labels, and a discrete alternative when possible.",
                )
            )
        if qtype in MATRIX_TYPES:
            rows = question.get("rows", []) if isinstance(question.get("rows"), list) else []
            columns = question.get("columns", []) if isinstance(question.get("columns"), list) else []
            if len(rows) > 7 or len(columns) > 7 or len(rows) * len(columns) > 35:
                issues.append(
                    _issue(
                        "warning",
                        "MATRIX_OVERLOAD",
                        f"Matrix has {len(rows)} rows × {len(columns)} columns.",
                        question=question,
                        block_id=context.block_id,
                        suggestion="Split the matrix, shorten it, or use one item per page for mobile and accessibility.",
                    )
                )
            issues.append(
                _issue(
                    "info",
                    "MATRIX_MOBILE_REVIEW",
                    "Matrix questions need explicit mobile, keyboard, screen-reader, and straightlining review.",
                    question=question,
                    block_id=context.block_id,
                )
            )
        if qtype == "constant_sum":
            validation = question.get("validation", {})
            if not isinstance(validation, Mapping) or "total" not in validation:
                issues.append(
                    _issue(
                        "warning",
                        "CONSTANT_SUM_TOTAL",
                        "Constant-sum question does not declare the required total.",
                        question=question,
                        block_id=context.block_id,
                    )
                )
        if qtype in {"file_upload", "signature", "video", "heatmap", "hotspot"}:
            issues.append(
                _issue(
                    "warning",
                    "RICH_RESPONSE_RISK",
                    "Rich response type can increase burden, privacy risk, moderation needs, and platform dependence.",
                    question=question,
                    block_id=context.block_id,
                    suggestion="Collect it only when necessary and document file limits, consent, retention, accessibility, and fallback paths.",
                )
            )

        logic = question.get("display_if")
        if isinstance(logic, Mapping):
            dependency = str(logic.get("question_id", ""))
            if dependency in positions and positions[dependency] >= position:
                issues.append(
                    _issue(
                        "error",
                        "LOGIC_FORWARD_REFERENCE",
                        f"Display logic depends on '{dependency}', which appears at or after this question.",
                        question=question,
                        block_id=context.block_id,
                        suggestion="Move the dependency earlier or revise the logic path.",
                    )
                )
        if question.get("skip_to") == qid:
            issues.append(_issue("error", "LOGIC_SELF_LOOP", "Question skips to itself.", question=question, block_id=context.block_id))

    total = len(contexts)
    if total:
        open_share = open_count / total
        required_share = required_count / total
        if open_count > 3 or open_share > 0.30:
            issues.append(
                Issue(
                    "warning",
                    "OPEN_TEXT_BURDEN",
                    f"Instrument contains {open_count} open-response items ({open_share:.0%} of questions).",
                    suggestion="Keep only open questions that serve a defined qualitative coding plan; place the broadest one near the end.",
                )
            )
        if required_share > 0.80:
            issues.append(
                Issue(
                    "warning",
                    "REQUIRED_SHARE",
                    f"{required_share:.0%} of questions are required.",
                    suggestion="Require only fields necessary for eligibility, safety, core measurement, or transaction completion.",
                )
            )
        if include_info:
            issues.append(Issue("info", "INSTRUMENT_SIZE", f"Instrument contains {total} questions across {len(data.get('blocks', []))} blocks."))
    if sensitive_count and not privacy.get("sensitive_data"):
        issues.append(
            Issue(
                "warning",
                "SENSITIVE_METADATA_MISSING",
                "Potentially sensitive questions are present, but privacy metadata does not list sensitive data categories.",
                suggestion="Document categories, lawful basis/consent, access controls, retention, and disclosure risks.",
            )
        )

    if not include_info:
        issues = [issue for issue in issues if issue.severity != "info"]
    return sorted(issues, key=lambda issue: (-SEVERITY_ORDER[issue.severity], issue.block_id or "", issue.question_id or "", issue.code))


def _text_report(issues: Iterable[Issue]) -> str:
    rows = list(issues)
    if not rows:
        return "Survey quality audit: PASS — no findings.\n"
    counts = {severity: sum(issue.severity == severity for issue in rows) for severity in ("error", "warning", "info")}
    lines = [
        "Survey quality audit",
        f"Errors: {counts['error']} | Warnings: {counts['warning']} | Info: {counts['info']}",
        "",
    ]
    for issue in rows:
        location = ""
        if issue.question_id:
            location = f" [{issue.question_id}]"
        lines.append(f"{issue.severity.upper():7} {issue.code}{location}: {issue.message}")
        if issue.suggestion:
            lines.append(f"         Fix: {issue.suggestion}")
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit a canonical JSON/YAML survey for structural and methodological quality risks.")
    parser.add_argument("survey", type=Path, help="Path to a canonical .json, .yaml, or .yml survey file")
    parser.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    parser.add_argument("--include-info", action="store_true", help="Include informational diagnostics")
    parser.add_argument("--fail-on", choices=("error", "warning", "never"), default="error", help="Lowest severity that produces exit code 1")
    args = parser.parse_args(argv)

    try:
        data = load_survey(args.survey, validate=False)
    except (FileNotFoundError, SurveyValidationError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    issues = lint_survey(data, include_info=args.include_info)
    if args.output_format == "json":
        print(json.dumps({"issues": [issue.to_dict() for issue in issues]}, indent=2, ensure_ascii=False))
    else:
        print(_text_report(issues), end="")

    if args.fail_on == "never":
        return 0
    threshold = SEVERITY_ORDER[args.fail_on]
    return 1 if any(SEVERITY_ORDER[issue.severity] >= threshold for issue in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
