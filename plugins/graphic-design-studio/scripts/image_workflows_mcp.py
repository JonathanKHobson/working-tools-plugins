#!/usr/bin/env python3
"""Launch the bundled image workflow server with a recipient-prepared runtime."""

import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def interpreter_path() -> Path:
    declared = os.environ.get('IMAGE_WORKFLOWS_PYTHON')
    if declared:
        return Path(declared).expanduser().absolute()
    packaged = ROOT / ('.runtime/venv/Scripts/python.exe' if os.name == 'nt' else '.runtime/venv/bin/python')
    if packaged.is_file():
        return packaged
    # Preserve the existing local studio-tools binding without distributing it.
    binding = Path.home() / '.config/studio-tools/design-library.json'
    if binding.is_file():
        config = json.loads(binding.read_text(encoding='utf-8'))
        return Path(config['interpreter']).expanduser().absolute()
    return packaged


def main() -> None:
    interpreter = interpreter_path()
    if not interpreter.is_file() or not os.access(interpreter, os.X_OK):
        raise ValueError('Prepare the documented runtime or set IMAGE_WORKFLOWS_PYTHON to a suitable venv interpreter')
    server = ROOT / 'runtime/image-workflows/server.py'
    if not server.is_file():
        raise ValueError('Image Workflows server missing')
    os.execve(str(interpreter), [str(interpreter), str(server), *sys.argv[1:]],
              dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Image Workflows unavailable: {exc}', file=sys.stderr)
        raise SystemExit(1)
