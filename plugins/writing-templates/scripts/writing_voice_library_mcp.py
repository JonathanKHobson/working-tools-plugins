#!/usr/bin/env python3
"""Select the documented existing Python before importing the MCP SDK."""
import os, sys
from pathlib import Path

def main():
    python = Path(os.environ.get('WRITING_TEMPLATES_PYTHON') or sys.executable).expanduser().absolute()
    if not python.is_file() or not os.access(python, os.X_OK):
        raise ValueError('Selected Python is unavailable')
    server = Path(__file__).resolve().parents[1] / 'runtime/writing-voice-library/server.py'
    os.execve(str(python), [str(python), str(server), *sys.argv[1:]], dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))

if __name__ == '__main__':
    try: main()
    except (OSError, ValueError):
        print('Set WRITING_TEMPLATES_PYTHON to an existing Python 3.10+ with requirements.txt installed. Startup never downloads dependencies.', file=sys.stderr)
        raise SystemExit(1)
