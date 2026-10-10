#!/usr/bin/env python3
"""Launch the user's existing general Research Compass MCP via a private binding."""

import json
import os
from pathlib import Path
import sys


def main() -> None:
    if len(sys.argv) != 1:
        raise ValueError("Research Compass launcher takes no arguments")
    binding = Path(os.environ.get("RESEARCH_COMPASS_BINDING", str(Path.home() / ".config/studio-tools/compass.json"))).expanduser()
    config = json.loads(binding.read_text())["research-compass"]
    interpreter = Path(config["interpreter"]).expanduser().absolute()
    # Keep the virtualenv entrypoint; resolving its symlink loses site-packages.
    server = Path(config["server"]).expanduser().resolve(strict=True)
    if not interpreter.is_file() or not os.access(interpreter, os.X_OK) or not server.is_file():
        raise ValueError("Research Compass runtime unavailable")
    extra = config.get("args", [])
    if not isinstance(extra, list) or not all(isinstance(value, str) for value in extra):
        raise ValueError("Invalid Research Compass launch arguments")
    additions = config.get("env", {})
    if not isinstance(additions, dict) or not all(
        isinstance(key, str) and isinstance(value, str)
        for key, value in additions.items()
    ):
        raise ValueError("Invalid Research Compass environment settings")
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    # Reality Check otherwise starts a uv subprocess that may download packages.
    # A deliberate private binding override is required to enable that adapter.
    env["IDEA_REALITY_ENABLED"] = "0"
    env["RESEARCH_COMPASS_DISCOURSE_ENABLED"] = "false"
    env.update(additions)
    os.chdir(server.parent)
    os.execve(str(interpreter), [str(interpreter), str(server), *extra], env)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        print(
            "Research Compass binding unavailable. Set RESEARCH_COMPASS_BINDING or check ~/.config/studio-tools/compass.json; "
            "no backend was installed or downloaded.",
            file=sys.stderr,
        )
        raise SystemExit(1)
