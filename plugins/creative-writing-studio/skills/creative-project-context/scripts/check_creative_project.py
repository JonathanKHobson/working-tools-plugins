#!/usr/bin/env python3
"""Check a Creative Studio project scaffold without external dependencies."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_PATHS = [
    "creative-project.yaml",
    "brief.md",
    "canon",
    "drafts",
    "research",
    "feedback",
    "provenance/provenance-ledger.jsonl",
    "logs/decisions.jsonl",
    "logs/assumptions.jsonl",
    "logs/questions.jsonl",
    "releases",
]

REQUIRED_YAML_KEYS = [
    "id:",
    "title:",
    "project_type:",
    "status:",
    "privacy:",
    "canonical_source:",
    "rights:",
    "privacy_boundaries:",
    "provenance:",
    "release:",
]

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}"),
]


def check_project(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    for rel in REQUIRED_PATHS:
        if not (root / rel).exists():
            errors.append(f"missing required path: {rel}")
    yaml_path = root / "creative-project.yaml"
    text = yaml_path.read_text(encoding="utf-8", errors="replace") if yaml_path.exists() else ""
    for key in REQUIRED_YAML_KEYS:
        if key not in text:
            errors.append(f"creative-project.yaml missing key: {key}")
    for rel in ["brief.md", "creative-project.yaml"]:
        path = root / rel
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"\b(TODO|TBD|FIXME)\b", content):
            warnings.append(f"{rel} contains TODO/TBD/FIXME")
        for pattern in SECRET_PATTERNS:
            if pattern.search(content):
                errors.append(f"possible secret in {rel}")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root")
    args = parser.parse_args()
    root = Path(args.project_root).expanduser().resolve()
    errors, warnings = check_project(root)
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARN: {item}")
    if not errors and not warnings:
        print("OK: creative project scaffold looks structurally valid")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
