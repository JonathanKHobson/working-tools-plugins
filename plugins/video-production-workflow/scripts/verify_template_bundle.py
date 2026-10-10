#!/usr/bin/env python3
"""Verify a declared local bundle; write reports only outside its root."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from video_workflow.provenance import verify_relative_inventory


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    if args.output is not None:
        try:
            output = args.output.expanduser().resolve()
            root = args.root.expanduser().resolve()
            manifest = args.manifest.expanduser().resolve()
            if output == manifest:
                parser.error("Report output must not overwrite the input manifest")
            # Path spelling alone misses aliases on case-insensitive filesystems.
            # The parent must exist, and no ancestor may identify the bundle root.
            if output.is_relative_to(root) or any(
                parent.samefile(root) for parent in (output.parent, *output.parent.parents)
            ):
                parser.error("Report output must be outside the bundle root")
            if os.path.lexists(args.output.expanduser()):
                parser.error("Report output must be a new file; existing paths are refused")
        except (OSError, RuntimeError, ValueError) as exc:
            parser.error(f"Cannot resolve report output: {exc}")

    try:
        data = json.loads(args.manifest.expanduser().read_text(encoding="utf-8"))
        if not isinstance(data, dict) or "files" not in data:
            raise ValueError("Manifest must be an object with a files inventory")
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(f"Cannot read inventory manifest: {exc}")
    report = verify_relative_inventory(
        args.root, data["files"], required_paths=data.get("requiredPaths", [])
    )
    serialized = json.dumps(report, indent=2) + "\n"
    if args.output is not None:
        try:
            # Exclusive creation preserves existing files, including aliases to inputs.
            # Parent directories must already exist; reporting creates no directory tree.
            with args.output.expanduser().open("x", encoding="utf-8") as handle:
                handle.write(serialized)
        except OSError as exc:
            parser.error(f"Cannot create report output: {exc}")
    print(serialized, end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
