#!/usr/bin/env python3
"""Launch only this plugin's fixed Atlas domain from a recipient-owned binding."""
import argparse
import json
import os
from pathlib import Path
import sys

DOMAIN = 'instructional'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--binding', type=Path,
                        default=Path.home() / '.config/studio-tools/atlas-library.json',
                        help='Recipient-owned Atlas JSON binding')
    options = parser.parse_args()
    config = json.loads(options.binding.expanduser().read_text())
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
        print('Atlas library unavailable: check the selected recipient binding and mounted Atlas source. No download or repair was attempted.', file=sys.stderr)
        raise SystemExit(1)
