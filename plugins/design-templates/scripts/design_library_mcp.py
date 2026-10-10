#!/usr/bin/env python3
"""Portable launcher. Reuse a host-provided MCP Python; never install at launch."""
import importlib.util
import json
import os
from pathlib import Path
import sys


def interpreter():
    explicit = os.environ.get('DESIGN_LIBRARY_PYTHON')
    if explicit:
        candidate = Path(explicit).expanduser().absolute()
    else:
        binding = Path.home() / '.config/studio-tools/design-library.json'
        if binding.is_file():
            candidate = Path(json.loads(binding.read_text())['interpreter']).expanduser().absolute()
        elif importlib.util.find_spec('mcp'):
            candidate = Path(sys.executable).absolute()
        else:
            raise ValueError('MCP SDK runtime required')
    # Do not resolve Python venv symlinks; preserve site-packages identity.
    if not candidate.is_file() or not os.access(candidate, os.X_OK):
        raise ValueError('MCP Python is unavailable')
    return candidate


def main():
    python = interpreter()
    server = Path(__file__).resolve().parents[1] / 'runtime/design-library/server.py'
    if not server.is_file():
        raise ValueError('Packaged server is missing')
    os.execve(str(python), [str(python), str(server), *sys.argv[1:]],
              dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError):
        print('Design Library requires an existing Python with the MCP SDK. See docs/setup.md. No runtime was downloaded.', file=sys.stderr)
        raise SystemExit(1)
