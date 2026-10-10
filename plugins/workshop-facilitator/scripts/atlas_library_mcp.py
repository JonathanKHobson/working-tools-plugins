#!/usr/bin/env python3
"""Launch this plugin's fixed Atlas domain from a recipient-owned binding."""
import argparse
import json
import os
from pathlib import Path
import sys

DOMAIN = 'facilitation'

def main():
    parser = argparse.ArgumentParser(description='Launch the fixed facilitation Atlas view.')
    parser.add_argument('--binding', type=Path,
                        help='Private JSON binding; defaults to ~/.config/studio-tools/atlas-library.json')
    args = parser.parse_args()
    binding = args.binding.expanduser() if args.binding else Path.home() / '.config/studio-tools/atlas-library.json'
    config = json.loads(binding.read_text())
    interpreter = Path(config['interpreter']).expanduser().absolute()
    server = Path(config['server']).expanduser().resolve(strict=True)
    database = Path(config['database']).expanduser().resolve(strict=True)
    if not interpreter.is_file() or not os.access(interpreter, os.X_OK) or not server.is_file() or not database.is_file():
        raise ValueError('Local Atlas runtime or database is unavailable.')
    env = dict(os.environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    os.execve(str(interpreter), [str(interpreter), str(server), '--db', str(database), '--domain', DOMAIN], env)

if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError):
        print('Atlas library unavailable: check the selected private binding, compatible server and catalog. No download or repair was attempted.', file=sys.stderr)
        raise SystemExit(1)
