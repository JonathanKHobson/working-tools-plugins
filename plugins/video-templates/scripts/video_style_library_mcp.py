#!/usr/bin/env python3
"""Portable Video Templates launcher; host-specific bindings stay outside source."""
from __future__ import annotations
import json
import os
from pathlib import Path
import sys
import subprocess


def main() -> None:
    binding = Path(os.environ.get("VIDEO_TEMPLATES_BINDINGS", Path.home() / ".config/video-templates/bindings.json")).expanduser()
    complete_environment = bool(os.environ.get("VIDEO_TEMPLATES_PYTHON") and os.environ.get("VIDEO_LIBRARY_CATALOG")) and not os.environ.get("VIDEO_TEMPLATES_BINDINGS")
    config = json.loads(binding.read_text(encoding="utf-8")) if binding.is_file() and not complete_environment else {}
    if not isinstance(config, dict):
        raise ValueError("Bindings must be a JSON object")
    interpreter = Path(os.environ.get("VIDEO_TEMPLATES_PYTHON", config.get("interpreter", sys.executable))).expanduser().absolute()
    if not interpreter.is_file() or not os.access(interpreter, os.X_OK):
        raise ValueError("MCP Python interpreter unavailable")
    check = subprocess.run(
        [str(interpreter), "-c", "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('mcp') else 1)"],
        capture_output=True, timeout=10, check=False,
    )
    if check.returncode:
        raise ValueError("Selected Python lacks the MCP SDK; select an existing MCP environment with VIDEO_TEMPLATES_PYTHON or the external bindings file")
    root = Path(__file__).resolve().parents[1]
    server = root / "runtime/video-style-library/server.py"
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    for key, variable in (("catalog", "VIDEO_LIBRARY_CATALOG"), ("preview_root", "VIDEO_LIBRARY_PREVIEW_ROOT"), ("storyboard_db", "VIDEO_STORYBOARD_DB"), ("shared_ui", "VIDEO_TEMPLATES_CHOOSER")):
        if key in config and variable not in env:
            value = Path(config[key]).expanduser().resolve()
            if key == "storyboard_db" and value.is_relative_to(root):
                raise ValueError("Private storyboard state must remain outside the package")
            env[variable] = str(value)
    if "VIDEO_STORYBOARD_DB" in env and Path(env["VIDEO_STORYBOARD_DB"]).expanduser().resolve().is_relative_to(root):
        raise ValueError("Private storyboard state must remain outside the package")
    os.execve(str(interpreter), [str(interpreter), str(server), *sys.argv[1:]], env)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        print(f"Video Templates launcher: {exc}. See docs/onboarding.md.", file=sys.stderr)
        raise SystemExit(1)
