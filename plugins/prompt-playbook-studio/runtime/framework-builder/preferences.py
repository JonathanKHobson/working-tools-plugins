"""Private, local preferences for the Prompt Framework Builder."""

import json
import os
from pathlib import Path
import tempfile


PREFERENCES_PATH = Path.home() / '.config/studio-tools/prompt-framework-preferences.json'
LENS_IDS = frozenset({
    '',
    'analytical-algorithmic',
    'divergent-inventive',
    'skeptical-verifier',
    'systems-integrator',
    'human-centered-mediator',
})
_FIELDS = frozenset({'version', 'lensId', 'instructions', 'keepOpen'})


def _defaults():
    return {'version': 1, 'lensId': '', 'instructions': '', 'keepOpen': False}


def _validate(data):
    if not isinstance(data, dict) or data.keys() != _FIELDS:
        raise ValueError('Invalid framework preferences: expected only version, lensId, instructions, and keepOpen.')
    if type(data['version']) is not int or data['version'] != 1:
        raise ValueError('Invalid framework preferences: unsupported version.')
    if type(data['lensId']) is not str or data['lensId'] not in LENS_IDS:
        raise ValueError('Invalid framework preferences: unknown lens ID.')
    if type(data['instructions']) is not str or len(data['instructions']) > 8000:
        raise ValueError('Invalid framework preferences: instructions must be text of at most 8000 characters.')
    if type(data['keepOpen']) is not bool:
        raise ValueError('Invalid framework preferences: keepOpen must be true or false.')
    return data


def load_preferences(*, _path=None):
    """Return the saved preference object, or defaults when no file exists.

    ``_path`` is an internal override for isolated tests; the MCP tool must not
    expose it to callers.
    """
    path = Path(_path) if _path is not None else PREFERENCES_PATH
    try:
        raw = path.read_text(encoding='utf-8')
    except FileNotFoundError:
        return _defaults()
    except UnicodeDecodeError as exc:
        raise ValueError('Invalid framework preferences: file is not UTF-8 text.') from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError('Invalid framework preferences: file is not valid JSON.') from exc
    return _validate(data)


def save_preferences(lens_id: str, instructions: str, keep_open: bool, *, _path=None):
    """Validate and atomically save preferences, returning the saved object."""
    data = _validate({
        'version': 1,
        'lensId': lens_id,
        'instructions': instructions,
        'keepOpen': keep_open,
    })
    path = Path(_path) if _path is not None else PREFERENCES_PATH
    if path.exists():
        load_preferences(_path=path)  # Refuse to replace malformed existing state.
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                         prefix='.prompt-framework-preferences-',
                                         suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            os.chmod(temporary, 0o600)
            json.dump(data, stream, ensure_ascii=False, separators=(',', ':'))
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return data
