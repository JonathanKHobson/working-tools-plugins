#!/usr/bin/env python3
"""Launch the shared private Draw and Think runtime; no install or repair side effects."""
import json
import os
from pathlib import Path
import sys

def main():
    if len(sys.argv) != 1:
        raise ValueError("This launcher accepts no arguments")
    config = json.loads((Path.home() / ".config/studio-tools/draw-think.json").read_text())
    interpreter = Path(config["interpreter"]).expanduser().absolute()
    server = Path(config["server"]).expanduser().resolve(strict=True)
    data_dir = Path(config["data_dir"]).expanduser().absolute()
    if not interpreter.is_file() or not os.access(interpreter, os.X_OK) or not server.is_file():
        raise ValueError("Drawing runtime unavailable")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    os.chdir(server.parent)
    os.execve(str(interpreter), [str(interpreter), str(server), "--data-dir", str(data_dir)], env)

if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        print("Draw and Think unavailable: check the private studio-tools/draw-think.json binding and mounted runtime. No repair was attempted.", file=sys.stderr)
        raise SystemExit(1)
