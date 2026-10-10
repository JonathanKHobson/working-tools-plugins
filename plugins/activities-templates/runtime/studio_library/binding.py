"""Operator-supplied external data and Python bindings. No automatic setup."""
import json
import os
from pathlib import Path

DEFAULT_CONFIG = Path.home() / '.config/studio-tools/atlas-library.json'
RUNTIME = Path(__file__).resolve().parent


def load_binding(config_path=None):
    path = Path(config_path or os.environ.get('ACTIVITIES_ATLAS_CONFIG') or DEFAULT_CONFIG).expanduser()
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict):
        raise ValueError('Binding must be a JSON object')
    interpreter = Path(data['interpreter']).expanduser().absolute()
    database = Path(data['database']).expanduser().resolve(strict=True)
    if not interpreter.is_file() or not os.access(interpreter, os.X_OK) or not database.is_file():
        raise ValueError('External Python or catalog is unavailable')
    package = RUNTIME.parents[1]
    if database.is_relative_to(package):
        raise ValueError('The private database must stay outside the package')
    misses = Path(data.get('search_misses_database', database.parent / 'observability/library-search-misses.sqlite')).expanduser().absolute()
    if misses.resolve().is_relative_to(package):
        raise ValueError('Private feedback must stay outside the package')
    return {'interpreter': interpreter, 'database': database,
            'search_misses_database': misses, 'server': RUNTIME / 'server.py'}
