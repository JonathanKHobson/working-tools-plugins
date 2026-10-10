#!/usr/bin/env python3
"""Shared loading, schema validation, and traversal helpers for survey-strategist."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping

try:
    import yaml
except ImportError as exc:  # pragma: no cover - dependency error path
    raise SystemExit("PyYAML is required. Install it with: python -m pip install PyYAML") from exc

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover - dependency error path
    raise SystemExit("jsonschema is required. Install it with: python -m pip install jsonschema") from exc

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA_PATH = SKILL_ROOT / "assets" / "survey.schema.json"


class SurveyValidationError(ValueError):
    """Raised when the canonical survey structure is invalid."""

    def __init__(self, messages: Iterable[str]):
        self.messages = list(messages)
        super().__init__("Survey validation failed:\n- " + "\n- ".join(self.messages))


@dataclass(frozen=True)
class QuestionContext:
    block_id: str
    block_title: str
    question: dict[str, Any]


def load_survey(path: str | Path, *, validate: bool = True) -> dict[str, Any]:
    """Load a UTF-8 JSON or YAML survey and optionally validate it."""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Survey file not found: {source}")
    try:
        text = source.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise SurveyValidationError([f"{source.name} must be UTF-8 encoded: {exc}"]) from exc

    suffix = source.suffix.lower()
    try:
        if suffix == ".json":
            data = json.loads(text)
        elif suffix in {".yaml", ".yml"}:
            data = yaml.safe_load(text)
        else:
            # Be helpful for extensionless files while avoiding silent ambiguity.
            stripped = text.lstrip()
            data = json.loads(text) if stripped.startswith(("{", "[")) else yaml.safe_load(text)
    except (json.JSONDecodeError, yaml.YAMLError) as exc:
        raise SurveyValidationError([f"Cannot parse {source.name}: {exc}"]) from exc

    if not isinstance(data, dict):
        raise SurveyValidationError(["Survey root must be a mapping/object."])
    if validate:
        validate_survey(data)
    return data


def _load_schema(schema_path: str | Path | None = None) -> dict[str, Any]:
    path = Path(schema_path) if schema_path else DEFAULT_SCHEMA_PATH
    return json.loads(path.read_text(encoding="utf-8"))


def _format_jsonschema_error(error: Any) -> str:
    path = ".".join(str(part) for part in error.absolute_path)
    location = path or "<root>"
    return f"{location}: {error.message}"


def _duplicate_messages(items: list[Mapping[str, Any]], *, kind: str, container: str) -> list[str]:
    messages: list[str] = []
    seen_ids: dict[str, int] = {}
    seen_values: dict[str, int] = {}
    for index, item in enumerate(items):
        item_id = str(item.get("id", ""))
        if item_id:
            if item_id in seen_ids:
                messages.append(
                    f"{container}: duplicate {kind} id '{item_id}' at positions {seen_ids[item_id] + 1} and {index + 1}."
                )
            else:
                seen_ids[item_id] = index
        if "value" in item:
            value_key = json.dumps(item["value"], sort_keys=True, ensure_ascii=False)
            if value_key in seen_values:
                messages.append(
                    f"{container}: duplicate {kind} value {item['value']!r} at positions {seen_values[value_key] + 1} and {index + 1}."
                )
            else:
                seen_values[value_key] = index
    return messages


def validate_survey(data: Mapping[str, Any], schema_path: str | Path | None = None) -> None:
    """Validate schema plus cross-question invariants not expressible cleanly in JSON Schema."""
    schema = _load_schema(schema_path)
    validator = Draft202012Validator(schema)
    messages = [_format_jsonschema_error(error) for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path))]

    blocks = data.get("blocks", []) if isinstance(data, Mapping) else []
    block_ids: dict[str, int] = {}
    question_ids: dict[str, tuple[int, int]] = {}
    export_tags: dict[str, str] = {}

    if isinstance(blocks, list):
        for block_index, block in enumerate(blocks):
            if not isinstance(block, Mapping):
                continue
            block_id = str(block.get("id", ""))
            if block_id:
                if block_id in block_ids:
                    messages.append(
                        f"blocks: duplicate block id '{block_id}' at positions {block_ids[block_id] + 1} and {block_index + 1}."
                    )
                else:
                    block_ids[block_id] = block_index
            questions = block.get("questions", [])
            if not isinstance(questions, list):
                continue
            for question_index, question in enumerate(questions):
                if not isinstance(question, Mapping):
                    continue
                question_id = str(question.get("id", ""))
                if question_id:
                    if question_id in question_ids:
                        old_block, old_question = question_ids[question_id]
                        messages.append(
                            "duplicate question id "
                            f"'{question_id}' at blocks[{old_block}].questions[{old_question}] and "
                            f"blocks[{block_index}].questions[{question_index}]."
                        )
                    else:
                        question_ids[question_id] = (block_index, question_index)
                export_tag = str(question.get("export_tag", question_id))
                if export_tag:
                    if export_tag in export_tags and export_tags[export_tag] != question_id:
                        messages.append(
                            f"duplicate export tag '{export_tag}' used by '{export_tags[export_tag]}' and '{question_id}'."
                        )
                    else:
                        export_tags[export_tag] = question_id
                for field_name in ("choices", "rows", "columns"):
                    items = question.get(field_name, [])
                    if isinstance(items, list):
                        messages.extend(
                            _duplicate_messages(
                                [item for item in items if isinstance(item, Mapping)],
                                kind=field_name[:-1] if field_name.endswith("s") else field_name,
                                container=f"question '{question_id or question_index}' {field_name}",
                            )
                        )
                fields = question.get("fields", [])
                if isinstance(fields, list):
                    messages.extend(
                        _duplicate_messages(
                            [item for item in fields if isinstance(item, Mapping)],
                            kind="field",
                            container=f"question '{question_id or question_index}' fields",
                        )
                    )

    known_ids = set(question_ids)
    analysis_plan = data.get("analysis_plan", {}) if isinstance(data, Mapping) else {}
    if isinstance(analysis_plan, Mapping):
        for field_name in ("primary_metrics", "secondary_metrics", "segments"):
            for metric_id in analysis_plan.get(field_name, []) or []:
                if metric_id not in known_ids:
                    messages.append(f"analysis_plan.{field_name}: unknown question id '{metric_id}'.")

    for context in iter_question_contexts(data):
        question = context.question
        question_id = str(question.get("id", "<unknown>"))
        skip_to = question.get("skip_to")
        if skip_to and skip_to not in known_ids and skip_to not in block_ids and skip_to not in {"end", "terminate"}:
            messages.append(f"question '{question_id}': skip_to references unknown question or block '{skip_to}'.")
        logic = question.get("display_if")
        if isinstance(logic, Mapping):
            dependency = logic.get("question_id")
            if dependency and dependency not in known_ids:
                messages.append(f"question '{question_id}': display_if references unknown question '{dependency}'.")

    if messages:
        # Preserve order while eliminating duplicate schema/custom messages.
        unique = list(dict.fromkeys(messages))
        raise SurveyValidationError(unique)


def iter_question_contexts(data: Mapping[str, Any]) -> Iterator[QuestionContext]:
    for block in data.get("blocks", []) or []:
        if not isinstance(block, Mapping):
            continue
        block_id = str(block.get("id", ""))
        block_title = str(block.get("title", ""))
        for question in block.get("questions", []) or []:
            if isinstance(question, dict):
                yield QuestionContext(block_id=block_id, block_title=block_title, question=question)


def iter_questions(data: Mapping[str, Any]) -> Iterator[dict[str, Any]]:
    for context in iter_question_contexts(data):
        yield context.question


def question_map(data: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(question["id"]): question for question in iter_questions(data)}


def dump_json(data: Any, path: str | Path) -> None:
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
