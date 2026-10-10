#!/usr/bin/env python3
"""Print YouTube description chapters from a course package; all inputs are read-only."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from video_workflow.youtube_chapters import ChapterExportError, export_youtube_chapters


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("chapters", type=Path)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("render", type=Path)
    parser.add_argument("--json", action="store_true", help="include hashes and validation boundary")
    args = parser.parse_args()
    try:
        result = export_youtube_chapters(args.chapters, args.receipt, args.render)
    except (ChapterExportError, OSError, UnicodeError) as exc:
        print(f"YouTube chapters: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True) if args.json else result["description"],
          end="\n" if args.json else "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
