#!/usr/bin/env python3
"""Portable stdlib launcher for the Writing Voice Library validator."""

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    node = os.environ.get("NODE_BIN") or "node"
    script = Path(__file__).with_suffix(".cjs")
    try:
        return subprocess.call([node, str(script), *sys.argv[1:]])
    except FileNotFoundError:
        print(f"voice validation: Node executable unavailable: {node}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"voice validation: cannot launch Node: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
