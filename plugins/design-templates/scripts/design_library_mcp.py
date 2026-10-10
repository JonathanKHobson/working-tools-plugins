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
    binding = Path.home() / '.config/studio-tools/design-library.json'
    complete_environment = bool(os.environ.get('DESIGN_LIBRARY_PYTHON') and os.environ.get('DESIGN_TEMPLATES_DATA_ROOT'))
    config = json.loads(binding.read_text()) if binding.is_file() and not complete_environment else {}
    collection = config.get('collections', {}).get('design-templates', {})
    if not isinstance(collection, dict):
        raise ValueError('Design collection binding must be an object')
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    # A caller-selected data root must not inherit a different collection's pins.
    if 'DESIGN_TEMPLATES_DATA_ROOT' not in env:
        for key, variable in [('catalog', 'DESIGN_LIBRARY_CATALOG'), ('data_root', 'DESIGN_TEMPLATES_DATA_ROOT'), ('asset_manifest', 'DESIGN_TEMPLATES_ASSET_MANIFEST')]:
            if key in collection:
                env.setdefault(variable, str(Path(collection[key]).expanduser().absolute()))
    os.execve(str(python), [str(python), str(server), *sys.argv[1:]],
              env)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError):
        print('Design Library requires an existing Python with the MCP SDK. See docs/setup.md. No runtime was downloaded.', file=sys.stderr)
        raise SystemExit(1)
