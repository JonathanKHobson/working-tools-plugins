#!/usr/bin/env python3
"""Validate a contiguous agenda in elapsed minutes, including closeout."""
import argparse
import json
import math
from pathlib import Path


def number(value):
    return type(value) in (int, float) and math.isfinite(value)


def validate(data):
    if not isinstance(data, dict):
        return ['agenda must be an object']
    errors = []
    duration = data.get('duration_minutes')
    if not number(duration) or duration <= 0:
        errors.append('duration_minutes must be positive and finite')
    segments = data.get('segments')
    if not isinstance(segments, list) or not segments:
        return errors + ['segments must be a nonempty list']
    cursor, seen, closeouts = 0, set(), 0
    for row in segments:
        if not isinstance(row, dict):
            errors.append('each segment must be an object')
            continue
        key = row.get('id')
        if not isinstance(key, str) or not key.strip():
            errors.append('segment id required')
        elif key in seen:
            errors.append(f'duplicate segment id {key}')
        else:
            seen.add(key)
        for field in ('title', 'purpose', 'output', 'instructions', 'fallback'):
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f'{key}: {field} required')
        kind = row.get('kind')
        if kind not in ('opening', 'activity', 'transition', 'break', 'debrief', 'closeout'):
            errors.append(f'{key}: unsupported kind')
        if kind == 'closeout':
            closeouts += 1
        start, end = row.get('start'), row.get('end')
        if not number(start) or not number(end) or start < 0 or end <= start:
            errors.append(f'{key}: invalid start/end minutes')
            continue
        if not math.isclose(start, cursor, abs_tol=1e-8):
            errors.append(f'{key}: gap or overlap; expected start {cursor}, got {start}')
        cursor = end
    if number(duration) and not math.isclose(cursor, duration, abs_tol=1e-8):
        errors.append(f'agenda ends at {cursor}, expected {duration}')
    if not closeouts or not isinstance(segments[-1], dict) or segments[-1].get('kind') != 'closeout':
        errors.append('last segment must be an explicit closeout')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    args = parser.parse_args()
    try:
        errors = validate(json.loads(args.path.read_text()))
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    print(json.dumps({'ok': not errors, 'errors': errors,
                      'limit': 'Timing and completeness only; rehearse instructions and inspect group fit.'}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
