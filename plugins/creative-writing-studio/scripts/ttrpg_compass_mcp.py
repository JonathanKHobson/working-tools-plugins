#!/usr/bin/env python3
"""Launch the separately installed TTRPG Compass from a private host binding."""

import json
import os
from pathlib import Path
import sys


def main():
    if len(sys.argv) != 1:
        raise ValueError("This launcher accepts no arguments")
    binding = Path.home() / ".config/studio-tools/compass.json"
    config = json.loads(binding.read_text())["ttrpg-compass"]
    interpreter = Path(config["interpreter"]).expanduser().absolute()
    # Keep the venv entrypoint; resolving its Python symlink loses site-packages.
    server = Path(config["server"]).expanduser().resolve(strict=True)
    if not interpreter.is_file() or not os.access(interpreter, os.X_OK) or not server.is_file():
        raise ValueError("TTRPG Compass runtime unavailable")
    extra = config.get("args", [])
    if not isinstance(extra, list) or not all(isinstance(value, str) for value in extra):
        raise ValueError("Invalid TTRPG Compass launch arguments")
    additions = config.get("env", {})
    if not isinstance(additions, dict) or not all(isinstance(key, str) and isinstance(value, str) for key, value in additions.items()):
        raise ValueError("Invalid TTRPG Compass environment settings")
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # A parent process must not activate the private campaign slot by accident.
    env.pop("TTRPG_COMPASS_PERSONAL_CAMPAIGN_CONFIG", None)
    env.update(additions)
    os.chdir(server.parent)
    os.execve(str(interpreter), [str(interpreter), str(server), *extra], env)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        print("TTRPG Compass unavailable: check the private studio-tools/compass.json binding and mounted runtime. No install or repair was attempted.", file=sys.stderr)
        raise SystemExit(1)
