"""Validate assistant-supplied values before opening the human framework editor."""

import json


MAX_SCALAR = 8000
MAX_TOTAL = 100000
_TEXT_TYPES = {'text', 'textarea', 'typeahead'}


def _error(key, detail):
    raise ValueError(f'Invalid prefill for {key}: {detail}.')


def _text(key, value):
    if type(value) is not str:
        _error(key, 'expected text')
    if len(value) > MAX_SCALAR:
        _error(key, 'text exceeds 8000 characters')
    return value


def _options(field):
    return {str(option.get('value', option.get('label', '')))
            if isinstance(option, dict) else str(option)
            for option in field.get('options', [])}


def _max_rows(field):
    try:
        maximum = int(field.get('max', 20))
    except (ValueError, TypeError):
        maximum = 20
    return max(0, maximum)


def _field_value(field, value, key):
    kind = field.get('type') or 'text'
    if kind in _TEXT_TYPES:
        return _text(key, value)
    if kind == 'checkbox':
        if type(value) is not bool:
            _error(key, 'expected true or false')
        return value
    if kind == 'select':
        selected = _text(key, value)
        if selected and selected not in _options(field):
            _error(key, 'value is not an authored option')
        return selected
    if kind == 'multiselect':
        if not isinstance(value, list):
            _error(key, 'expected a list of authored options')
        allowed = _options(field)
        selected = []
        for entry in value:
            entry = _text(key, entry)
            if entry not in allowed:
                _error(key, 'value is not an authored option')
            if entry not in selected:
                selected.append(entry)
        return selected
    if kind == 'repeater':
        grouped = field.get('itemType') == 'group' and bool(field.get('fields'))
        if grouped:
            if not isinstance(value, list) or any(not isinstance(row, dict) for row in value):
                _error(key, 'expected a list of group rows')
            if len(value) > _max_rows(field):
                _error(key, 'too many rows')
            subfields = {sub['key']: sub for sub in field['fields']}
            rows = []
            for row in value:
                if any(type(subkey) is not str or subkey not in subfields for subkey in row):
                    _error(key, 'unknown group field')
                rows.append({subkey: _field_value(subfields[subkey], entry, key + '.' + subkey)
                             for subkey, entry in row.items()})
            return rows
        if type(value) is str:
            rows = value.splitlines()
        elif isinstance(value, list):
            rows = value
        else:
            _error(key, 'expected text or a list of text rows')
        if len(rows) > _max_rows(field):
            _error(key, 'too many rows')
        return _text(key, '\n'.join(_text(key, row) for row in rows))
    _error(key, 'unsupported field type')


def validate_prefill(item: dict, values: dict):
    """Return a new partial values object matching this catalog item's fields.

    No defaults or required-field completion are inferred. The human editor
    remains responsible for completing and reviewing the assembled prompt.
    """
    if not isinstance(item, dict) or not isinstance(item.get('fields'), list):
        raise ValueError('Invalid framework schema: fields are unavailable.')
    if not isinstance(values, dict):
        raise ValueError('Invalid prefill: expected an object of field values.')
    fields = {field['key']: field for field in item['fields']}
    if any(type(key) is not str or key not in fields and key != 'ctx' for key in values):
        raise ValueError('Invalid prefill: unknown framework field.')
    try:
        size = len(json.dumps(values, ensure_ascii=False))
    except (TypeError, ValueError) as exc:
        raise ValueError('Invalid prefill: values must be JSON-compatible.') from exc
    if size > MAX_TOTAL:
        raise ValueError('Invalid prefill: total input exceeds 100000 characters.')
    return {key: _text('ctx', value) if key == 'ctx' else _field_value(fields[key], value, key)
            for key, value in values.items()}
