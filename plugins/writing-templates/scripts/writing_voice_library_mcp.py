#!/usr/bin/env python3
"""Select the documented existing Python before importing the MCP SDK."""
import json, os, sys
from pathlib import Path

def main():
    binding = Path.home() / '.config/studio-tools/design-library.json'
    complete_environment = bool(os.environ.get('WRITING_TEMPLATES_PYTHON') and os.environ.get('WRITING_TEMPLATES_DATA_ROOT'))
    config = json.loads(binding.read_text()) if binding.is_file() and not complete_environment else {}
    collection = config.get('collections', {}).get('writing-templates', {})
    if not isinstance(collection, dict):
        raise ValueError('Writing collection binding must be an object')
    python = Path(os.environ.get('WRITING_TEMPLATES_PYTHON') or config.get('interpreter') or sys.executable).expanduser().absolute()
    if not python.is_file() or not os.access(python, os.X_OK):
        raise ValueError('Selected Python is unavailable')
    server = Path(__file__).resolve().parents[1] / 'runtime/writing-voice-library/server.py'
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    if 'WRITING_TEMPLATES_DATA_ROOT' not in env:
        for key, variable in [('data_root', 'WRITING_TEMPLATES_DATA_ROOT'), ('approved_sources', 'WRITING_TEMPLATES_APPROVED_SOURCES')]:
            if key in collection:
                env.setdefault(variable, str(Path(collection[key]).expanduser().absolute()))
        if 'public_base' in collection:
            env.setdefault('WRITING_TEMPLATES_PUBLIC_BASE', collection['public_base'])
    os.execve(str(python), [str(python), str(server), *sys.argv[1:]], env)

if __name__ == '__main__':
    try: main()
    except (OSError, ValueError, TypeError, KeyError):
        print('Set WRITING_TEMPLATES_PYTHON to an existing Python 3.10+ with requirements.txt installed. Startup never downloads dependencies.', file=sys.stderr)
        raise SystemExit(1)
