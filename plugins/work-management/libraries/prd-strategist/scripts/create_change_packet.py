#!/usr/bin/env python3
"""Create a lightweight local change packet.

This recreates the useful OpenSpec pattern without requiring the OpenSpec CLI:
one folder per change, behavior-first spec deltas, design notes, tasks, and a
verification record. It writes only under the requested output root.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "change"


def split_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def checkbox_lines(items: list[str], prefix: str) -> str:
    if not items:
        items = ["Confirm scope and write the first implementation slice"]
    return "\n".join(f"- [ ] {prefix}.{index} {item}" for index, item in enumerate(items, start=1))


def write_if_allowed(path: Path, content: str, overwrite: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def build_packet(args: argparse.Namespace) -> dict[str, str]:
    change_slug = slugify(args.name)
    capability_slug = slugify(args.capability or args.name)
    root = Path(args.output_root).expanduser().resolve()
    packet_root = root / change_slug
    created_at = datetime.now(timezone.utc).isoformat()
    tasks = split_csv(args.tasks)
    scenarios = split_csv(args.scenarios)
    if not scenarios:
        scenarios = ["Primary happy path", "Important failure or edge path"]

    metadata = {
        "schema_version": "jonathan.change_packet.v1",
        "source_inspiration": "Fission-AI/OpenSpec@1.4.1",
        "created_at": created_at,
        "change": change_slug,
        "capability": capability_slug,
        "status": "proposed",
        "telemetry": "none",
        "runtime_dependency": "none",
    }

    proposal = f"""# Proposal: {args.name}

## Why

{args.why or "Explain the problem, opportunity, or delivery reason this change matters now."}

## What Changes

- {args.what or "Describe the behavior or capability that changes."}

## Capabilities

### New Capabilities

- `{capability_slug}`: {args.capability_description or "Behavior covered by this change."}

### Modified Capabilities

- None listed.

## Scope

In scope:
- {args.in_scope or "Smallest useful implementation slice."}

Out of scope:
- {args.out_of_scope or "Follow-on polish, expansion, or speculative automation."}

## Impact

- Affected surfaces: {args.impact or "TBD"}
- Rollback/reversal note: {args.rollback or "Remove the change slice or revert the commit."}
"""

    scenario_blocks = []
    for scenario in scenarios:
        scenario_blocks.append(
            f"""#### Scenario: {scenario}
- **GIVEN** the user or system is in the relevant starting state
- **WHEN** the change is exercised
- **THEN** the expected observable behavior occurs
"""
        )
    spec = f"""# Delta for {capability_slug}

## ADDED Requirements

### Requirement: {args.requirement or args.name}
The system SHALL support {args.requirement_text or args.what or "the requested behavior"}.

{chr(10).join(scenario_blocks)}
"""

    design = f"""# Design Notes: {args.name}

## Context

{args.context or "Summarize current state, constraints, and known dependencies."}

## Goals / Non-Goals

**Goals:**
- {args.goal or "Ship the smallest behaviorally complete slice."}

**Non-Goals:**
- {args.non_goal or args.out_of_scope or "Avoid broad refactors or speculative expansion."}

## Decisions

### Decision: Implementation shape

{args.decision or "Prefer existing project patterns and keep the change reversible."}

Alternative considered: {args.alternative or "A broader rewrite; rejected unless the current code makes the small slice impossible."}

## Risks / Trade-offs

- {args.risk or "Risk TBD"} -> {args.mitigation or "Mitigation TBD"}

## Open Questions

- {args.open_question or "None yet."}
"""

    task_doc = f"""# Tasks: {args.name}

## 1. Prepare

{checkbox_lines(split_csv(args.prepare_tasks) or ["Confirm affected files and existing tests"], "1")}

## 2. Implement

{checkbox_lines(tasks, "2")}

## 3. Verify

{checkbox_lines(split_csv(args.verify_tasks) or ["Run targeted tests and record the result"], "3")}
"""

    verification = f"""# Verification: {args.name}

## Acceptance Checks

- [ ] Every requirement scenario has either a test, a manual check, or a documented reason it is deferred.
- [ ] Existing behavior that shares the touched surface still works.
- [ ] User-facing changes were visually or manually checked when relevant.
- [ ] Rollback or reversal path is known.

## Evidence Log

| Check | Command or Evidence | Result | Notes |
|---|---|---|---|
| TBD | TBD | pending | Fill during implementation. |

## Archive Decision

Status: proposed

Decision note: record shipped, deferred, rejected, or superseded when this packet closes.
"""

    write_if_allowed(packet_root / ".change-packet.json", json.dumps(metadata, indent=2), args.overwrite)
    write_if_allowed(packet_root / "proposal.md", proposal, args.overwrite)
    write_if_allowed(packet_root / "specs" / capability_slug / "spec.md", spec, args.overwrite)
    write_if_allowed(packet_root / "design.md", design, args.overwrite)
    write_if_allowed(packet_root / "tasks.md", task_doc, args.overwrite)
    write_if_allowed(packet_root / "verification.md", verification, args.overwrite)

    return {
        "schema_version": "jonathan.change_packet.created.v1",
        "change": change_slug,
        "capability": capability_slug,
        "root": str(packet_root),
        "files": [
            str(packet_root / ".change-packet.json"),
            str(packet_root / "proposal.md"),
            str(packet_root / "specs" / capability_slug / "spec.md"),
            str(packet_root / "design.md"),
            str(packet_root / "tasks.md"),
            str(packet_root / "verification.md"),
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a local proposal/spec/design/tasks/verification packet.")
    parser.add_argument("name", help="Human-readable change name")
    parser.add_argument("--output-root", default="changes", help="Directory where the change folder should be created")
    parser.add_argument("--capability", default="", help="Capability/spec folder name")
    parser.add_argument("--why", default="")
    parser.add_argument("--what", default="")
    parser.add_argument("--capability-description", default="")
    parser.add_argument("--in-scope", default="")
    parser.add_argument("--out-of-scope", default="")
    parser.add_argument("--impact", default="")
    parser.add_argument("--rollback", default="")
    parser.add_argument("--requirement", default="")
    parser.add_argument("--requirement-text", default="")
    parser.add_argument("--scenarios", default="")
    parser.add_argument("--context", default="")
    parser.add_argument("--goal", default="")
    parser.add_argument("--non-goal", default="")
    parser.add_argument("--decision", default="")
    parser.add_argument("--alternative", default="")
    parser.add_argument("--risk", default="")
    parser.add_argument("--mitigation", default="")
    parser.add_argument("--open-question", default="")
    parser.add_argument("--prepare-tasks", default="")
    parser.add_argument("--tasks", default="")
    parser.add_argument("--verify-tasks", default="")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing packet")
    return parser.parse_args()


def main() -> int:
    result = build_packet(parse_args())
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
