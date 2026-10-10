#!/usr/bin/env python3
"""Launch the packaged collaborative builder using the existing reviewed Atlas Python."""
import json
import os
from pathlib import Path
import sys

if len(sys.argv) != 1:
    raise SystemExit('This launcher accepts no arguments.')
try:
    binding = json.loads((Path.home() / '.config/studio-tools/atlas-library.json').read_text())
    python = Path(binding['interpreter']).expanduser().absolute()
    server = Path(__file__).resolve().parents[1] / 'runtime/framework-builder/server.py'
    if not python.is_file() or not os.access(python, os.X_OK) or not server.is_file():
        raise ValueError('Local runtime files unavailable')
except (OSError, ValueError, KeyError, TypeError):
    raise SystemExit('Framework Builder unavailable: check the recipient-owned Atlas Python binding; no installation or download was attempted.')
os.execve(str(python), [str(python), str(server)], dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
