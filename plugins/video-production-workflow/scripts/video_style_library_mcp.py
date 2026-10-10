#!/usr/bin/env python3
"""Optional compatibility route to a separately installed Video Templates package."""
import json
import os
from pathlib import Path
import runpy
import sys


def main() -> None:
    binding = Path(os.environ.get("VIDEO_TEMPLATES_BINDINGS", Path.home() / ".config/video-templates/bindings.json")).expanduser()
    config = json.loads(binding.read_text()) if binding.is_file() else {}
    root = Path(os.environ.get("VIDEO_TEMPLATES_ROOT", config.get("templates_root", Path(__file__).resolve().parents[2] / "video-templates"))).expanduser()
    launcher = root / "scripts/video_style_library_mcp.py"
    if not launcher.is_file():
        raise ValueError("Install Video Templates and set VIDEO_TEMPLATES_ROOT or external templates_root binding")
    runpy.run_path(str(launcher), run_name="__main__")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Video Templates compatibility route: {exc}", file=sys.stderr)
        raise SystemExit(1)
