#!/usr/bin/env python3
"""Route Design Library to the separately installed design-templates owner."""
import os
from pathlib import Path
import sys


def main():
    owner = Path(os.environ.get("DESIGN_TEMPLATES_ROOT") or
                 Path(__file__).resolve().parents[1].parent / "design-templates").expanduser()
    launcher = owner / "scripts/design_library_mcp.py"
    if launcher.is_file():
        os.execve(sys.executable, [sys.executable, str(launcher), *sys.argv[1:]],
                  dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    raise FileNotFoundError(f"Design Library owner missing: {launcher}. Install design-templates or set DESIGN_TEMPLATES_ROOT to its root.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Design Library unavailable: {exc}", file=sys.stderr)
        raise SystemExit(1)
