#!/usr/bin/env python3
"""Run the pinned local prompt-packet compiler without installing a package."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    runtime = Path(__file__).resolve().parents[1] / "runtime" / "prompt_optimizer.py"
    spec = importlib.util.spec_from_file_location("prompt_playbook_compiler_runtime", runtime)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load bundled prompt compiler: {runtime}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return int(module.main(argv))


if __name__ == "__main__":
    raise SystemExit(main())
