#!/usr/bin/env python3
"""Compatibility entrypoint for an explicitly configured external closeout helper."""
import json
import os
from pathlib import Path
import runpy
import sys

def main():
    helper = os.environ.get("WORK_MANAGEMENT_CLOSEOUT_HELPER")
    if not helper:
        config = Path.home() / ".config/studio-tools/work-management-host-hooks.json"
        try:
            helper = json.loads(config.read_text()).get("closeout")
        except (OSError, ValueError, TypeError):
            return
    if not isinstance(helper, str) or not helper:
        return
    path = Path(helper).expanduser().resolve()
    if path == Path(__file__).resolve() or not path.is_file():
        return
    sys.path.insert(0, str(path.parent))
    try:
        runpy.run_path(str(path), run_name="__main__")
    finally:
        sys.path.pop(0)

if __name__ == "__main__":
    main()
