#!/usr/bin/env python3
"""Launch a fixed Atlas view through its automatically shared domain backend."""
import os
import json
from pathlib import Path
import sys

RUNTIME = Path(__file__).resolve().parents[1] / 'runtime/studio_library'
sys.path.insert(0, str(RUNTIME))
from binding import load_binding
DOMAINS = json.loads((RUNTIME / 'domains.json').read_text(encoding='utf-8'))


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in DOMAINS:
        raise ValueError('Supply exactly one registered domain; MCP tools cannot override it')
    binding = load_binding()
    env = dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['ACTIVITIES_SEARCH_MISSES_DB'] = str(binding['search_misses_database'])
    interpreter = str(binding['interpreter'])
    if os.name != 'posix' or os.environ.get('ACTIVITIES_TRANSPORT') == 'direct':
        # Compatibility/rollback path. Normal use needs no operator switching.
        command = [interpreter, str(binding['server']), '--db', str(binding['database']), '--domain', sys.argv[1]]
    else:
        command = [interpreter, '-B', str(RUNTIME / 'stdio_proxy.py'),
                   '--db', str(binding['database']), '--domain', sys.argv[1],
                   '--misses', str(binding['search_misses_database']), '--interpreter', interpreter]
    os.execve(interpreter, command, env)


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError):
        print('Activities Templates unavailable: supply the external atlas-library.json binding, a Python environment with mcp and PyYAML, and the mounted Atlas catalog. No download or repair was attempted.', file=sys.stderr)
        raise SystemExit(1)
