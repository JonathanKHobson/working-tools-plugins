#!/usr/bin/env python3
"""Launch the selected critical review without installing or repairing dependencies."""
import argparse
import json
import os
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binding", type=Path, required=True, help="Operator-selected JSON runtime binding")
    options = parser.parse_args()
    config = json.loads(options.binding.expanduser().read_text())
    interpreter = Path(config["interpreter"]).expanduser().absolute()
    server = Path(config["server"]).expanduser().resolve(strict=True)
    data_dir = Path(config["data_dir"]).expanduser().absolute()
    if not interpreter.is_file() or not os.access(interpreter, os.X_OK) or not server.is_file():
        raise ValueError("Critical review runtime unavailable")
    os.chdir(server.parent)
    os.execve(str(interpreter), [str(interpreter), str(server), "--data-dir", str(data_dir)],
              dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError):
        print("Critical review unavailable: check the supplied --binding file and mounted runtime. No repair was attempted.", file=sys.stderr)
        raise SystemExit(1)
