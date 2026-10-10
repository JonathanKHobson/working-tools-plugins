#!/usr/bin/env python3
"""Read-only entrypoint for the pinned, vendored agent-skillguard scanner."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

VENDOR = Path(__file__).resolve().parents[1] / "vendor" / "agent-skillguard"
MODULE = VENDOR / "scripts" / "skillguard.py"
spec = importlib.util.spec_from_file_location("vendored_skillguard", MODULE)
if spec is None or spec.loader is None:
    raise SystemExit("vendored skillguard module unavailable")
skillguard = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = skillguard
spec.loader.exec_module(skillguard)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Local file or directory to scan")
    parser.add_argument("--format", choices=("json", "markdown", "sarif"), default="json")
    parser.add_argument("--suppressions", type=Path, help="Reviewed exact-match suppressions file")
    parser.add_argument("--max-files", type=int, default=5000)
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    parser.add_argument("--version", action="version", version=f"agent-skillguard {skillguard.VERSION} (vendored)")
    args = parser.parse_args()
    if not 1 <= args.max_files <= 5000 or not 1 <= args.max_bytes <= 1_000_000:
        parser.error("limits must be positive and no greater than the reviewed defaults")
    try:
        report = skillguard.scan_path(
            args.path,
            rules_path=VENDOR / "rules" / "default-rules.json",
            suppressions_path=args.suppressions,
            max_files=args.max_files,
            max_bytes=args.max_bytes,
        )
        if args.format == "markdown":
            output = skillguard.render_markdown(report)
        elif args.format == "sarif":
            output = json.dumps(
                skillguard.render_sarif(report, skillguard.load_rules(VENDOR / "rules" / "default-rules.json")),
                indent=2,
            ) + "\n"
        else:
            output = json.dumps(report, indent=2) + "\n"
        sys.stdout.write(output)
        return skillguard.EXIT_FINDINGS if report["summary"]["active_findings"] else skillguard.EXIT_PASS
    except (skillguard.SkillGuardError, OSError) as exc:
        print(f"skillguard: {exc}", file=sys.stderr)
        return skillguard.EXIT_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
