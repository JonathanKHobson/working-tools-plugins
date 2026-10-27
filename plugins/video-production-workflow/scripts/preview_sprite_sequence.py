#!/usr/bin/env python3
"""Validate a sprite sequence and optionally write a GIF/still preview."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from video_workflow.sprite_sequence import SpriteSequenceError, load_manifest, render_sequence, validate_manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output-dir", type=Path, help="write GIF and stills here; omitted means validation only")
    args = parser.parse_args()
    try:
        manifest, root = load_manifest(args.manifest)
        result = render_sequence(manifest, root, args.output_dir) if args.output_dir else validate_manifest(manifest, root)
    except SpriteSequenceError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        return 2
    print(json.dumps({"ok": True, **result}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
