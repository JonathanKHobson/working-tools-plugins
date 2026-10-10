#!/usr/bin/env python3
"""Validate AI Workshop Studio outlines against the portable studio-v3-1 contract."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
CONTRACT_PATH = ROOT / "references" / "ai-workshop-studio-v3-template.json"
PROVENANCE_PATH = ROOT / "references" / "ai-workshop-studio-v3-template.provenance.json"
VALID_REVIEW_STATES = {"approved", "proposed", "rejected", "unresolved", "needs-review"}


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        return None
    return float(value)


def word_count(value: Any) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text(value)))


def validate(outline: Any, contract: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    def add(code: str, location: str, message: str) -> None:
        errors.append({"code": code, "location": location, "message": message})

    if not isinstance(outline, dict):
        return [{"code": "outline_type", "location": "$", "message": "Outline must be a JSON object."}]

    if outline.get("templateVersion") != contract.get("version"):
        add("template_version", "templateVersion", f"Expected {contract.get('version')!r}.")

    contract_sections = contract.get("sections", [])
    expected_steps = [section.get("step") for section in contract_sections]
    sections = outline.get("sections")
    if not isinstance(sections, list):
        add("sections_type", "sections", "Sections must be an ordered list.")
        sections = []
    actual_steps = [section.get("step") for section in sections if isinstance(section, dict)]
    if actual_steps != expected_steps:
        add("section_order", "sections", f"Expected exact order {expected_steps}; got {actual_steps}.")

    by_step = {section.get("step"): section for section in sections if isinstance(section, dict)}
    for source in contract_sections:
        step = source.get("step")
        section = by_step.get(step)
        if not isinstance(section, dict):
            add("missing_section", f"sections.{step}", f"Missing section {step!r}.")
            continue
        if section.get("sourceStep") != source.get("sourceStep"):
            add("source_step", f"sections.{step}.sourceStep", f"Expected source step {source.get('sourceStep')!r}.")
        if "originalFields" in source:
            fields = section.get("fields")
            if not isinstance(fields, dict):
                add("fields_type", f"sections.{step}.fields", "Fields must be an object.")
                fields = {}
            for field in source["originalFields"]:
                if not text(fields.get(field)):
                    add("missing_field", f"sections.{step}.fields.{field}", "Required source field is empty.")
        if "originalColumns" in source:
            columns = section.get("columns")
            if columns != source["originalColumns"]:
                add("column_order", f"sections.{step}.columns", f"Expected exact columns {source['originalColumns']}.")

    overview = by_step.get("overview", {})
    overview_fields = overview.get("fields", {}) if isinstance(overview, dict) else {}
    title = text(overview_fields.get("Project Title")) if isinstance(overview_fields, dict) else ""
    difficulty = text(overview_fields.get("Difficulty Level")).lower() if isinstance(overview_fields, dict) else ""
    max_title = contract.get("rules", {}).get("beginnerTitleCharacters", 59)
    if "foundational" in difficulty or difficulty == "l1":
        if len(title) > max_title or not re.fullmatch(r".+ for Beginners: .+", title):
            add("title_rule", "sections.overview.fields.Project Title", f"Foundational title must match 'Tool for Beginners: Focus' and be at most {max_title} characters.")
    elif "intermediate" in difficulty or difficulty == "l2":
        if not re.fullmatch(r".+ with .+: .+", title):
            add("title_rule", "sections.overview.fields.Project Title", "Intermediate title must match 'Skill with Tool: Method/Output'.")

    goals = by_step.get("goals", {})
    goal_fields = goals.get("fields", {}) if isinstance(goals, dict) else {}
    extensions = goals.get("extensions", {}) if isinstance(goals, dict) else {}
    objective_ids = extensions.get("Stable Objective IDs", []) if isinstance(extensions, dict) else []
    expected_objectives = contract.get("rules", {}).get("objectives", 3)
    if not isinstance(objective_ids, list) or len(objective_ids) != expected_objectives or len(set(objective_ids)) != expected_objectives:
        add("objective_ids", "sections.goals.extensions.Stable Objective IDs", f"Expected {expected_objectives} unique objective IDs.")
        objective_ids = []
    for index in range(1, expected_objectives + 1):
        if not text(goal_fields.get(f"Learning Objective {index}")):
            add("objective_count", f"sections.goals.fields.Learning Objective {index}", "Exactly three nonempty objectives are required.")

    project = by_step.get("project", {})
    project_fields = project.get("fields", {}) if isinstance(project, dict) else {}
    artifact = text(project_fields.get("Project Artifact")) if isinstance(project_fields, dict) else ""
    outcome = text(goal_fields.get("Project Outcome")) if isinstance(goal_fields, dict) else ""
    if artifact and outcome and re.sub(r"\W+", " ", artifact.lower()).strip() == re.sub(r"\W+", " ", outcome.lower()).strip():
        add("outcome_as_artifact", "sections.project.fields.Project Artifact", "Artifact duplicates the outcome instead of naming a usable deliverable.")

    review = outline.get("review")
    if not isinstance(review, dict):
        add("review_metadata", "review", "Review metadata is required for substantive decisions.")
        review = {}
    for field_id, record in review.items():
        if not isinstance(record, dict) or record.get("status") not in VALID_REVIEW_STATES:
            add("review_state", f"review.{field_id}", f"Status must be one of {sorted(VALID_REVIEW_STATES)}.")
    artifact_review = review.get("project.Project Artifact", {})
    if not isinstance(artifact_review, dict) or artifact_review.get("status") != "approved" or not text(artifact_review.get("evidence/source")) or not text(artifact_review.get("reviewer decision")):
        add("unapproved_artifact", "review.project.Project Artifact", "Artifact needs explicit approval, source evidence, and reviewer decision before readiness.")

    tasks = by_step.get("tasks", {})
    rows = tasks.get("rows", []) if isinstance(tasks, dict) else []
    if not isinstance(rows, list):
        add("tasks_type", "sections.tasks.rows", "Task rows must be a list.")
        rows = []
    task_ids: set[str] = set()
    instructional_ids: set[str] = set()
    coverage = {objective_id: {"instructional": False, "practice": False, "assessment": False} for objective_id in objective_ids}
    scope_minutes: dict[str, float] = {}
    cumulative_rows: list[dict[str, Any]] = []
    allowed_task_types = set(contract.get("extensionCategories", {}).get("taskType", []))
    instruction_min, instruction_max = contract.get("rules", {}).get("instructionalTaskMinutes", [3, 7])
    for index, row in enumerate(rows):
        location = f"sections.tasks.rows[{index}]"
        if not isinstance(row, dict):
            add("task_type", location, "Task must be an object.")
            continue
        row_ext = row.get("_extensions", {})
        task_id = text(row_ext.get("Stable Task ID")) if isinstance(row_ext, dict) else ""
        if not task_id or task_id in task_ids:
            add("task_id", f"{location}._extensions.Stable Task ID", "Task ID must be nonempty and unique.")
        else:
            task_ids.add(task_id)
        task_type = text(row.get("Task Type")).lower()
        if task_type not in allowed_task_types:
            add("task_category", f"{location}.Task Type", f"Unknown task type {task_type!r}.")
        minutes = number(row.get("Estimated Time"))
        if task_type == "cumulative":
            if minutes is None or minutes < 0:
                add("task_minutes", f"{location}.Estimated Time", "Cumulative sequence-reference time must be a nonnegative finite number; it is ignored in arithmetic.")
                minutes = 0
        elif minutes is None or minutes <= 0:
            add("task_minutes", f"{location}.Estimated Time", "Estimated time must be a positive finite number.")
            minutes = 0
        if task_type == "instructional":
            instructional_ids.add(task_id)
            if minutes < instruction_min or minutes > instruction_max:
                add("instructional_duration", f"{location}.Estimated Time", f"Instructional task must be {instruction_min}-{instruction_max} minutes.")
        aligned = text(row.get("Aligned Learning Objective"))
        if aligned and aligned not in coverage:
            add("unknown_objective", f"{location}.Aligned Learning Objective", f"Unknown objective {aligned!r}.")
        elif aligned and task_type in {"instructional", "practice"}:
            coverage[aligned][task_type] = True
        scopes = row_ext.get("Delivery Scopes", []) if isinstance(row_ext, dict) else []
        if not isinstance(scopes, list) or not scopes:
            add("delivery_scope", f"{location}._extensions.Delivery Scopes", "Every activity needs at least one delivery scope.")
            scopes = []
        if task_type != "cumulative":
            for scope in scopes:
                scope_minutes[scope] = scope_minutes.get(scope, 0) + minutes
        if task_type == "cumulative":
            cumulative_rows.append(row)

    cumulative = by_step.get("cumulative", {})
    cumulative_ext = cumulative.get("extensions", {}) if isinstance(cumulative, dict) else {}
    cumulative_id = text(cumulative_ext.get("Stable Cumulative ID")) if isinstance(cumulative_ext, dict) else ""
    cumulative_minutes = number(cumulative_ext.get("Estimated Time")) if isinstance(cumulative_ext, dict) else None
    cumulative_min, cumulative_max = contract.get("rules", {}).get("cumulativeMinutes", [10, 20])
    if cumulative_minutes is None or not cumulative_min <= cumulative_minutes <= cumulative_max:
        add("cumulative_duration", "sections.cumulative.extensions.Estimated Time", f"Cumulative activity must be {cumulative_min}-{cumulative_max} minutes.")
    if cumulative_ext.get("Introduces New Required Material") is not False:
        add("cumulative_new_material", "sections.cumulative.extensions.Introduces New Required Material", "Cumulative activity must not introduce required new material.")
    mapped = cumulative_ext.get("Objective Alignment", []) if isinstance(cumulative_ext, dict) else []
    if set(mapped) != set(objective_ids):
        add("cumulative_alignment", "sections.cumulative.extensions.Objective Alignment", "Cumulative activity must map to all three objectives.")
    matching_rows = []
    for row in cumulative_rows:
        row_ext = row.get("_extensions", {}) if isinstance(row, dict) else {}
        if row_ext.get("Cumulative Reference") == cumulative_id:
            matching_rows.append(row)
    if len(matching_rows) != 1:
        add("cumulative_reference", "sections.tasks.rows", "Exactly one cumulative task row must link to the Step 4 cumulative ID.")
    if cumulative_minutes is not None:
        cumulative_scopes: set[str] = set()
        if matching_rows:
            for row in matching_rows:
                row_ext = row.get("_extensions", {}) if isinstance(row, dict) else {}
                scopes = row_ext.get("Delivery Scopes", []) if isinstance(row_ext, dict) else []
                if isinstance(scopes, list):
                    cumulative_scopes.update(scope for scope in scopes if isinstance(scope, str))
        else:
            declared_scopes = outline.get("deliveryScopes", [])
            if isinstance(declared_scopes, list):
                cumulative_scopes.update(
                    text(scope.get("id"))
                    for scope in declared_scopes
                    if isinstance(scope, dict) and text(scope.get("id"))
                )
        for scope in cumulative_scopes:
            scope_minutes[scope] = scope_minutes.get(scope, 0) + cumulative_minutes

    delivery_scopes = outline.get("deliveryScopes")
    if not isinstance(delivery_scopes, list) or not delivery_scopes:
        add("scope_budgets", "deliveryScopes", "Declare at least one delivery scope and budget.")
        delivery_scopes = []
    for index, scope in enumerate(delivery_scopes):
        location = f"deliveryScopes[{index}]"
        if not isinstance(scope, dict):
            add("scope_type", location, "Delivery scope must be an object.")
            continue
        scope_id = text(scope.get("id"))
        budget = number(scope.get("targetMinutes"))
        reported = number(scope.get("reportedTotalMinutes"))
        computed = scope_minutes.get(scope_id, 0)
        if budget is None or budget <= 0:
            add("scope_budget", f"{location}.targetMinutes", "Target minutes must be positive.")
        elif computed > budget:
            add("scope_over_budget", location, f"Computed {computed:g} minutes exceeds the {budget:g}-minute {scope_id!r} budget.")
        if reported is None or reported != computed:
            code = "timing_double_count" if cumulative_minutes and reported == computed + cumulative_minutes else "timing_total_mismatch"
            add(code, f"{location}.reportedTotalMinutes", f"Reported {reported!r}; canonical task-row total is {computed:g}. Count linked cumulative work once.")

    assessment = by_step.get("assessment", {})
    questions = assessment.get("questions", []) if isinstance(assessment, dict) else []
    if not isinstance(questions, list):
        add("questions_type", "sections.assessment.questions", "Questions must be a list.")
        questions = []
    assessed_tasks: set[str] = set()
    minimum_choices = contract.get("rules", {}).get("minimumAssessmentChoices", 4)
    for index, question in enumerate(questions):
        location = f"sections.assessment.questions[{index}]"
        if not isinstance(question, dict):
            add("question_type", location, "Question must be an object.")
            continue
        task_id = text(question.get("Task #"))
        if task_id not in instructional_ids:
            add("quiz_task_link", f"{location}.Task #", "Question must link to a known instructional task.")
        else:
            assessed_tasks.add(task_id)
        aligned = text(question.get("Aligned Learning Objective"))
        if aligned not in coverage:
            add("quiz_objective_link", f"{location}.Aligned Learning Objective", "Question must link to a known objective.")
        else:
            coverage[aligned]["assessment"] = True
        choices = question.get("Answer Choices")
        if not isinstance(choices, list) or len(choices) < minimum_choices:
            add("quiz_choices", f"{location}.Answer Choices", f"At least {minimum_choices} choices are required.")
            choices = []
        choice_ids = {text(choice.get("id")) for choice in choices if isinstance(choice, dict)}
        answer_keys = question.get("Answer Key")
        if not isinstance(answer_keys, list) or not answer_keys or not set(answer_keys).issubset(choice_ids):
            add("quiz_answer_key", f"{location}.Answer Key", "Answer key must name one or more existing choice IDs.")
        if not text(question.get("Feedback")):
            add("quiz_feedback", f"{location}.Feedback", "Author planning requires feedback for likely mistakes.")
        if question.get("Format") == "multiple-select":
            if not text(question.get("Selection Instructions")) or not text(question.get("Scoring Instructions")):
                add("quiz_multiple_select_instructions", location, "Multiple-select items require selection and scoring instructions.")
    for task_id in sorted(instructional_ids - assessed_tasks):
        add("quiz_task_coverage", "sections.assessment.questions", f"Instructional task {task_id!r} has no linked question.")

    for objective_id, states in coverage.items():
        for state, covered in states.items():
            if not covered:
                add("objective_misalignment", f"objective.{objective_id}", f"Objective {objective_id!r} lacks {state} evidence.")

    description = by_step.get("description", {})
    description_fields = description.get("fields", {}) if isinstance(description, dict) else {}
    description_text = description_fields.get("Guided Project Description") if isinstance(description_fields, dict) else ""
    description_min, description_max = contract.get("rules", {}).get("descriptionWords", [150, 250])
    words = word_count(description_text)
    if words < description_min or words > description_max:
        add("description_length", "sections.description.fields.Guided Project Description", f"Description has {words} words; expected {description_min}-{description_max}.")

    root_extensions = outline.get("extensions", {})
    dependencies = root_extensions.get("accessDependencies", []) if isinstance(root_extensions, dict) else []
    if not isinstance(dependencies, list):
        add("dependencies_type", "extensions.accessDependencies", "Access dependencies must be a list.")
        dependencies = []
    for index, dependency in enumerate(dependencies):
        location = f"extensions.accessDependencies[{index}]"
        if not isinstance(dependency, dict):
            add("dependency_type", location, "Dependency must be an object.")
            continue
        product = text(dependency.get("product"))
        if product not in {"ChatGPT Desktop", "Codex Desktop", "Claude", "Manual/Supplied Export"}:
            add("dependency_product", f"{location}.product", "Name the exact product or manual route.")
        if dependency.get("availabilityClaim") == "available" and dependency.get("verificationStatus") != "verified-current":
            add("dependency_false_claim", location, "A current availability claim requires verified-current evidence.")

    return errors


def check_contract_source(source: Path, portable: Path, provenance: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    portable_hash = sha256(portable)
    if portable_hash != provenance.get("sha256"):
        errors.append({"code": "portable_contract_hash", "location": str(portable), "message": "Portable contract differs from its provenance hash."})
    source_hash = sha256(source)
    if source_hash != portable_hash:
        errors.append({"code": "contract_drift", "location": str(source), "message": f"Source hash {source_hash} differs from portable hash {portable_hash}."})
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outline", type=Path)
    parser.add_argument("--source-contract", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        contract = load_json(CONTRACT_PATH)
        provenance = load_json(PROVENANCE_PATH)
        outline = load_json(args.outline)
        errors = validate(outline, contract)
        if args.source_contract:
            errors.extend(check_contract_source(args.source_contract, CONTRACT_PATH, provenance))
    except (OSError, json.JSONDecodeError) as exc:
        errors = [{"code": "input_error", "location": str(args.outline), "message": str(exc)}]

    result = {"valid": not errors, "errorCount": len(errors), "errors": errors}
    if args.json:
        print(json.dumps(result, indent=2))
    elif errors:
        for error in errors:
            print(f"{error['code']}: {error['location']}: {error['message']}")
    else:
        print("valid studio-v3-1 outline")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
