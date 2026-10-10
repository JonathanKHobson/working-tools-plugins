#!/usr/bin/env python3
"""Read-only plugin and MCPB launcher for Oppia Research Compass."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> None:
    bundle_root = Path(__file__).resolve().parent
    os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    os.environ.setdefault(
        "OPPIA_RESEARCH_DB_PATH",
        str(bundle_root / "data" / "oppia_research.sqlite"),
    )
    if str(bundle_root) not in sys.path:
        sys.path.insert(0, str(bundle_root))
    sys.argv = [str(bundle_root / "server.py"), *sys.argv[1:]]
    from server import main as server_main  # pylint: disable=import-outside-toplevel

    server_main()


if __name__ == "__main__":
    main()

