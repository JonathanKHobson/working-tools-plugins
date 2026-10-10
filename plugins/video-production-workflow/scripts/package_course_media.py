#!/usr/bin/env python3
"""Validate or package local course video sidecars from a JSON manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from video_workflow.course_media import CourseMediaError, package_course_media


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="JSON course media manifest")
    parser.add_argument("--output", type=Path, help="directory for deterministic sidecars")
    args = parser.parse_args()
    try:
        result = package_course_media(args.manifest, args.output)
    except (CourseMediaError, OSError, UnicodeError) as exc:
        print(f"course media: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
