#!/usr/bin/env python3
"""Check references and evidence coverage, not instructional validity."""
import argparse
import json
import math
from pathlib import Path


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ['alignment must be an object']
    groups = {}
    for group in ('outcomes', 'practice', 'assessments', 'rubric'):
        rows = data.get(group)
        if not isinstance(rows, list) or not rows:
            errors.append(f'{group}: nonempty list required')
            groups[group] = {}
            continue
        indexed = {}
        for row in rows:
            if not isinstance(row, dict):
                errors.append(f'{group}: each row must be an object')
                continue
            key = row.get('id')
            if not isinstance(key, str) or not key.strip():
                errors.append(f'{group}: nonempty string id required')
            elif key in indexed:
                errors.append(f'{group}: duplicate id {key}')
            else:
                indexed[key] = row
            if not isinstance(row.get('description'), str) or not row['description'].strip():
                errors.append(f'{group}/{key}: description required')
        groups[group] = indexed
    outcomes = set(groups['outcomes'])
    coverage = {'practice': set(), 'assessments': set(), 'rubric': set()}
    for group in ('practice', 'assessments'):
        for key, row in groups[group].items():
            ids = row.get('outcome_ids')
            if not isinstance(ids, list) or not ids or not all(isinstance(x, str) for x in ids):
                errors.append(f'{group}/{key}: outcome_ids must be nonempty strings')
                continue
            if len(ids) != len(set(ids)):
                errors.append(f'{group}/{key}: repeated outcome id')
            if set(ids) - outcomes:
                errors.append(f'{group}/{key}: unknown outcomes {sorted(set(ids) - outcomes)}')
            coverage[group].update(ids)
    total = 0
    scored = set()
    for key, row in groups['rubric'].items():
        oid, aid, points = row.get('outcome_id'), row.get('assessment_id'), row.get('points')
        if not isinstance(oid, str) or oid not in outcomes:
            errors.append(f'rubric/{key}: unknown outcome')
        else:
            coverage['rubric'].add(oid)
        assessment = groups['assessments'].get(aid) if isinstance(aid, str) else None
        if assessment is None:
            errors.append(f'rubric/{key}: unknown assessment')
        else:
            scored.add(aid)
            aligned = assessment.get('outcome_ids')
            if not isinstance(aligned, list) or oid not in aligned:
                errors.append(f'rubric/{key}: outcome not assessed by {aid}')
        if type(points) not in (int, float) or not math.isfinite(points) or points <= 0:
            errors.append(f'rubric/{key}: positive finite points required')
        else:
            total += points
    for group, covered in coverage.items():
        if outcomes - covered:
            errors.append(f'{group}: uncovered outcomes {sorted(outcomes - covered)}')
    if set(groups['assessments']) - scored:
        errors.append('each assessment needs at least one rubric criterion')
    maximum = data.get('max_points')
    if type(maximum) not in (int, float) or not math.isfinite(maximum) or maximum <= 0:
        errors.append('max_points must be positive and finite')
    elif not math.isclose(total, maximum):
        errors.append(f'rubric total {total} differs from max_points {maximum}')
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
                      'limit': 'Coverage and reference check only; inspect actual cognitive alignment.'}, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
