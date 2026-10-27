#!/usr/bin/env python3
"""Select the documented existing Python before importing the MCP SDK."""
import json, os, sys
from pathlib import Path

def main():
    binding = Path.home() / '.config/studio-tools/design-library.json'
    complete_environment = bool(os.environ.get('BRAND_TEMPLATES_PYTHON') and os.environ.get('BRAND_TEMPLATES_DATA_ROOT'))
    config = json.loads(binding.read_text()) if binding.is_file() and not complete_environment else {}
    collection = config.get('collections', {}).get('brand-templates', {})
    if not isinstance(collection, dict):
        raise ValueError('Brand collection binding must be an object')
    python = Path(os.environ.get('BRAND_TEMPLATES_PYTHON') or config.get('interpreter') or sys.executable).expanduser().absolute()
    if not python.is_file() or not os.access(python, os.X_OK):
        raise ValueError('Selected Python is unavailable')
    server = Path(__file__).resolve().parents[1] / 'runtime/brand-library/server.py'
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    if 'BRAND_TEMPLATES_DATA_ROOT' not in env:
        for key, variable in [('catalog', 'BRAND_TEMPLATES_CATALOG'), ('source_manifest', 'BRAND_TEMPLATES_SOURCE_MANIFEST'), ('data_root', 'BRAND_TEMPLATES_DATA_ROOT')]:
            if key in collection:
                env.setdefault(variable, str(Path(collection[key]).expanduser().absolute()))
    # Preserve direct CLI/export behavior and an explicit rollback path.
    if os.name != 'posix' or sys.argv[1:] or os.environ.get('BRAND_TEMPLATES_TRANSPORT') == 'direct':
        command = [str(python), str(server), *sys.argv[1:]]
    else:
        command = [str(python), '-B', str(server.with_name('stdio_proxy.py')), '--interpreter', str(python)]
    os.execve(str(python), command, env)

if __name__ == '__main__':
    try: main()
    except (OSError, ValueError, TypeError, KeyError):
        print('Set BRAND_TEMPLATES_PYTHON to an existing Python 3.10+ with requirements.txt installed. Startup never downloads dependencies.', file=sys.stderr)
        raise SystemExit(1)
