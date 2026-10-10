#!/usr/bin/env python3
"""Read-only local activity retrieval. Does not fetch sources or execute card text."""
import argparse
import json
from pathlib import Path

DEFAULT_LIBRARY = Path(__file__).resolve().parents[1] / 'assets/activity-library.json'


def load_library(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(data, dict) or data.get('schema_version') != 'learning-activity-library-1':
        raise ValueError('Expected learning-activity-library-1 object')
    rows = data.get('activities')
    if not isinstance(rows, list) or not rows:
        raise ValueError('Expected nonempty activities list')
    ids = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('Activity must be an object')
        for field in ('id', 'title', 'display_title', 'source_reference', 'source_sha256', 'readiness'):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError(f'Activity requires {field}')
        if row['id'] in ids:
            raise ValueError(f'Duplicate activity ID: {row["id"]}')
        ids.add(row['id'])
        for field in ('tags', 'modes', 'purposes'):
            if not isinstance(row.get(field), list) or not row[field] or not all(isinstance(x, str) for x in row[field]):
                raise ValueError(f'{row["id"]}: {field} requires nonempty string list')
        duration = row.get('duration_minutes')
        if not isinstance(duration, dict) or not all(type(duration.get(k)) is int for k in ('min', 'max')):
            raise ValueError(f'{row["id"]}: integer min/max duration required')
        if not 0 < duration['min'] <= duration['max']:
            raise ValueError(f'{row["id"]}: invalid duration range')
        adaptation = row.get('assessment_adaptation')
        fields = ('status', 'learner_prompt', 'observable_evidence', 'learner_artifact', 'success_criteria', 'debrief_and_retry', 'time_group_access_alternatives', 'individual_evidence_rule')
        if not isinstance(adaptation, dict) or not all(isinstance(adaptation.get(k), str) and adaptation[k].strip() for k in fields):
            raise ValueError(f'{row["id"]}: incomplete assessment adaptation')
    return rows


def search(rows, query='', max_minutes=None, mode=None, purpose=None, activity_id=None):
    terms = query.casefold().split()
    matches = []
    for row in rows:
        if activity_id and row['id'] != activity_id:
            continue
        if max_minutes is not None and row['duration_minutes']['max'] > max_minutes:
            continue
        if mode and mode not in row['modes']:
            continue
        if purpose and purpose not in row['purposes']:
            continue
        text = ' '.join([row['title'], row['display_title'], *row['tags'],
                         row['assessment_adaptation']['learner_prompt'],
                         row['assessment_adaptation']['observable_evidence']]).casefold()
        if not all(term in text for term in terms):
            continue
        score = sum(3 if term in ' '.join(row['tags']).casefold() else 1 for term in terms)
        matches.append((score, row))
    return [r for _, r in sorted(matches, key=lambda x: (-x[0], x[1]['duration_minutes']['max'], x[1]['id']))]


def positive(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError('Use a positive integer')
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--library', type=Path, default=DEFAULT_LIBRARY)
    parser.add_argument('--query', default='', help='Case-insensitive AND terms in title, tags, original prompt and evidence')
    parser.add_argument('--max-minutes', type=positive, help='Require upper planning estimate to fit; does not shorten an activity')
    parser.add_argument('--mode', choices=['solo', 'pair', 'group'])
    parser.add_argument('--purpose', choices=['diagnostic', 'formative'])
    parser.add_argument('--id', dest='activity_id', help='Exact stable source ID; returns full record')
    parser.add_argument('--limit', type=positive, default=5)
    parser.add_argument('--full', action='store_true')
    parser.add_argument('--list-tags', action='store_true')
    args = parser.parse_args()
    try:
        rows = load_library(args.library)
        if args.list_tags:
            result = {'tags': sorted({tag for row in rows for tag in row['tags']})}
        else:
            found = search(rows, args.query, args.max_minutes, args.mode, args.purpose, args.activity_id)
            chosen = found[:args.limit]
            if not (args.full or args.activity_id):
                chosen = [{k: row[k] for k in ('id', 'display_title', 'tags', 'duration_minutes', 'modes', 'purposes', 'readiness')} |
                          {'evidence': row['assessment_adaptation']['observable_evidence']} for row in chosen]
            result = {'matches': len(found), 'returned': len(chosen), 'activities': chosen,
                      'note': 'Proposed adaptations, not learner-validated. Inspect full card and author materials before use.'}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
