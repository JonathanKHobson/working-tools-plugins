#!/usr/bin/env python3
"""Launch the locally bound Compass backend without bundling personal data."""
import argparse
import json
import os
from pathlib import Path
import sys

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", choices=["critical-compass"])
    parser.add_argument("--binding", type=Path, default=Path.home() / ".config/studio-tools/compass.json", help="Operator-selected JSON runtime binding; defaults to the current user's studio-tools file")
    options = parser.parse_args()
    binding = options.binding.expanduser()
    name = options.name
    if name not in {"critical-compass"}:
        raise ValueError("Unknown Compass integration")
    config = json.loads(binding.read_text())[name]
    interpreter = Path(config["interpreter"]).expanduser().absolute()
    # Preserve the venv entrypoint: resolving its Python symlink loses site-packages.
    server = Path(config["server"]).expanduser().resolve(strict=True)
    if not interpreter.is_file() or not os.access(interpreter, os.X_OK) or not server.is_file():
        raise ValueError("Compass runtime unavailable; verify the selected binding and mounted source")
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
        print("Compass runtime binding unavailable. Check the supplied --binding file; no backend was installed or downloaded.", file=sys.stderr)
        raise SystemExit(1)
