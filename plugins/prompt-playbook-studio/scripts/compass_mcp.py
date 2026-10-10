#!/usr/bin/env python3
"""Launch the locally bound Compass backend without bundling personal data."""
import json
import os
from pathlib import Path
import sys

def main():
    binding = Path.home() / ".config/studio-tools/compass.json"
    name = sys.argv[1] if len(sys.argv) == 2 else ""
    if name not in {"prompt-compass", "knowledge_atlas"}:
        raise ValueError("Unknown Compass integration")
    config = json.loads(binding.read_text())[name]
    interpreter = Path(config["interpreter"]).expanduser().absolute()
    # Preserve the venv entrypoint: resolving its Python symlink loses site-packages.
    server = Path(config["server"]).expanduser().resolve(strict=True)
    if not interpreter.is_file() or not os.access(interpreter, os.X_OK) or not server.is_file():
        raise ValueError("Compass runtime unavailable; verify the private binding and mounted source")
    extra = config.get("args", [])
    if not isinstance(extra, list) or not all(isinstance(v, str) for v in extra):
        raise ValueError("Invalid Compass launch arguments")
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    additions = config.get("env", {})
    if not isinstance(additions, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in additions.items()):
        raise ValueError("Invalid Compass environment settings")
    env.update(additions)
    os.chdir(server.parent)
    os.execve(str(interpreter), [str(interpreter), str(server), *extra], env)

if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("Compass runtime binding unavailable. Check ~/.config/studio-tools/compass.json; no backend was installed or downloaded.", file=sys.stderr)
        raise SystemExit(1)
