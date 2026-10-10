"""Optional private feedback using the bundled, complete first-party helper."""
import json
import os
from pathlib import Path
import sys
from search_misses import register_tools


def register_feedback(server, library):
    try:
        explicit = os.environ.get('WRITING_LIBRARY_FEEDBACK_DB')
        if explicit:
            database = Path(explicit).expanduser().resolve()
        else:
            binding = json.loads((Path.home() / '.config/studio-tools/atlas-library.json').read_text())
            database = Path(binding.get('search_misses_database', Path(binding['database']).parent / 'observability/library-search-misses.sqlite')).expanduser().resolve()
        package = Path(__file__).resolve().parents[2]
        if database.is_relative_to(package):
            raise ValueError('Private feedback must remain outside the package')
        register_tools(server, library, db=database)
    except Exception:
        print('Optional private search feedback unavailable; search remains usable. Do not claim misses are logged.', file=sys.stderr)
