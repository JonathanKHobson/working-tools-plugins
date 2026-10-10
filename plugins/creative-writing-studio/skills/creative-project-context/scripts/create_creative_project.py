#!/usr/bin/env python3
"""Create a small plain-text Creative Studio project scaffold."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path


VALID_TYPES = {
    "book",
    "story",
    "screenplay",
    "interactive-fiction",
    "ttrpg-campaign",
    "ttrpg-system",
    "board-game",
    "card-game",
    "video-game-concept",
    "publishing-project",
    "other",
}

VALID_PRIVACY = {"public", "internal", "confidential", "sensitive-personal", "licensed-restricted"}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "creative-project"


def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Approved parent directory for the project.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--type", default="other", choices=sorted(VALID_TYPES))
    parser.add_argument("--privacy", default="confidential", choices=sorted(VALID_PRIVACY))
    parser.add_argument("--owner", default="Project Owner")
    parser.add_argument("--status", default="planning")
    parser.add_argument("--force", action="store_true", help="Allow creating inside an existing empty directory.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    project = root / slugify(args.title)
    if project.exists() and any(project.iterdir()) and not args.force:
        raise SystemExit(f"Refusing to write into non-empty project directory: {project}")
    project.mkdir(parents=True, exist_ok=True)

    for rel in [
        "canon/entities",
        "canon/timeline",
        "canon/locations",
        "canon/relationships",
        "drafts",
        "research/sources",
        "feedback",
        "provenance",
        "playtests",
        "builds",
        "releases",
        "logs",
        "tests",
        "archive",
    ]:
        (project / rel).mkdir(parents=True, exist_ok=True)

    project_id = slugify(args.title)
    yaml = f"""id: {project_id}
title: {args.title}
project_type: {args.type}
status: {args.status}
privacy: {args.privacy}
canonical_source: creative-project.yaml
owners:
  - {args.owner}
collaborators: []
audience: ""
format: ""
intent: ""
promise: ""
constraints: []
anti_goals: []
definition_of_done: ""
rights:
  license: ""
  attribution_required: []
  restricted_sources: []
privacy_boundaries:
  pii_allowed: false
  external_upload_allowed: false
  notes: ""
accessibility:
  known_needs: []
  review_required: true
provenance:
  ledger: provenance/provenance-ledger.jsonl
logs:
  decisions: logs/decisions.jsonl
  assumptions: logs/assumptions.jsonl
  questions: logs/questions.jsonl
  risks: logs/risks.jsonl
release:
  requires_hash_approval: true
  ledger: releases/release-ledger.jsonl
"""
    (project / "creative-project.yaml").write_text(yaml, encoding="utf-8")
    (project / "brief.md").write_text(
        f"# {args.title}\n\n## Intent\n\n## Audience\n\n## Promise\n\n## Constraints\n\n## Definition Of Done\n",
        encoding="utf-8",
    )
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    append_jsonl(project / "logs/decisions.jsonl", {"timestamp": now, "decision": "project scaffold created", "source": "creative-project-context"})
    append_jsonl(project / "logs/assumptions.jsonl", {"timestamp": now, "assumption": "plain-text source of truth is canonical until changed"})
    append_jsonl(project / "logs/questions.jsonl", {"timestamp": now, "question": "what is the first concrete deliverable?"})
    append_jsonl(project / "provenance/provenance-ledger.jsonl", {"timestamp": now, "artifact": "creative-project.yaml", "source_type": "original", "source": "local scaffold", "use": "project source of truth"})

    print(project)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
