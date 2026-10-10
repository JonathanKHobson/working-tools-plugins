#!/usr/bin/env python3
"""Compute descriptive LinkedIn ratios from supplied JSON. No network or writes."""
import argparse
from datetime import datetime
import json
import math
from pathlib import Path
import statistics
import sys

COUNTS = ('impressions', 'members_reached', 'followers_at_posting', 'reactions',
          'comments', 'reposts', 'saves', 'sends', 'clicks')
RANKS = ('interaction_rate_pct', 'impression_follower_multiple')
MAX_BYTES = 5_000_000


def count(row, key):
    value = row.get(key)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{row["id"]}: {key} must be a nonnegative number or null')
    try:
        valid = math.isfinite(value) and value >= 0
    except (OverflowError, TypeError):
        valid = False
    if not valid:
        raise ValueError(f'{row["id"]}: invalid {key}')
    return value


def ratio(numerator, denominator, percent=False):
    if numerator is None or denominator is None or denominator == 0:
        return None
    value = numerator / denominator * (100 if percent else 1)
    return round(value, 6) if math.isfinite(value) else None


def timestamp(row, key):
    value = row.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f'{row["id"]}: {key} must be an ISO timestamp')
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        raise ValueError(f'{row["id"]}: invalid {key}') from None
    if result.utcoffset() is None:
        raise ValueError(f'{row["id"]}: {key} needs a timezone')
    return result


def analyze(rows, rank=None):
    if not isinstance(rows, list) or len(rows) > 10000:
        raise ValueError('Expected an array of at most 10000 post records')
    if rank is not None and rank not in RANKS:
        raise ValueError('Unsupported rank metric')
    seen, output, warnings = set(), [], []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('id'), str) or not row['id'].strip():
            raise ValueError('Every row needs a nonempty string id')
        if row['id'] in seen:
            raise ValueError('Duplicate post id: ' + row['id'])
        seen.add(row['id'])
        values = {key: count(row, key) for key in COUNTS}
        p, o = timestamp(row, 'published_at'), timestamp(row, 'observed_at')
        age = (o - p).total_seconds() / 86400 if p and o else None
        if age is not None and age < 0:
            raise ValueError(row['id'] + ': observed_at precedes published_at')
        parts = [values[k] for k in ('reactions', 'comments', 'reposts')]
        numerator = sum(parts) if all(x is not None for x in parts) else None
        if numerator is not None and not math.isfinite(numerator):
            raise ValueError(row['id'] + ': interaction sum overflows')
        metrics = {
            'visible_interactions': numerator,
            'interaction_rate_pct': ratio(numerator, values['impressions'], True),
            'comment_reaction_ratio': ratio(values['comments'], values['reactions']),
            'impression_follower_multiple': ratio(values['impressions'], values['followers_at_posting']),
            'members_reached': values['members_reached'],
        }
        for key in ('saves', 'sends', 'clicks'):
            metrics[key + '_rate_pct'] = ratio(values[key], values['impressions'], True)
        missing = [key for key in COUNTS if values[key] is None]
        row_warnings = []
        if values['impressions'] == 0:
            row_warnings.append('Zero impressions: impression-based rates undefined')
        if age is None:
            row_warnings.append('Post age unknown: comparison unverified')
        if values['members_reached'] is not None and values['impressions'] is not None and values['members_reached'] > values['impressions']:
            row_warnings.append('Members reached exceeds impressions: inspect source/window mismatch')
        if row.get('scope') not in ('organic', 'paid'):
            row_warnings.append('Organic/paid scope unverified')
        output.append({'id': row['id'], 'scope': row.get('scope'),
                       'published_at': row.get('published_at'), 'observed_at': row.get('observed_at'),
                       'post_age_days': round(age, 6) if age is not None else None,
                       'inputs': values, 'metrics': metrics, 'missing': missing, 'warnings': row_warnings})
    ages = [x['post_age_days'] for x in output if x['post_age_days'] is not None]
    if len(set(ages)) > 1:
        warnings.append('Different post ages: rank only within an explicitly comparable observation window')
    if len({x['scope'] for x in output if isinstance(x['scope'], str)}) > 1:
        warnings.append('Mixed organic/paid/other scopes: split cohorts before interpretation')
    if any(x['warnings'] for x in output):
        warnings.append('Some records have missing or questionable comparison context; read row warnings')
    if len(output) < 10:
        warnings.append('Small descriptive sample; no winner or causal inference is established')
    medians = {}
    for key in RANKS:
        vals = [x['metrics'][key] for x in output if x['metrics'][key] is not None]
        medians[key] = {'value': statistics.median(vals) if vals else None, 'n': len(vals)}
    ranked = None
    if rank:
        ranked = [{'id': x['id'], 'value': x['metrics'][rank]} for x in sorted(
            (x for x in output if x['metrics'][rank] is not None),
            key=lambda x: x['metrics'][rank], reverse=True)]
    return {'schema_version': 1, 'claim_boundary': 'Descriptive local arithmetic only; impressions are not unique reach; missing is not zero; no causal or algorithm claims.',
            'post_count': len(output), 'records': output, 'medians': medians,
            'rank_metric': rank, 'ranking': ranked, 'warnings': warnings}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', help='JSON file or - for stdin')
    ap.add_argument('--rank', choices=RANKS)
    args = ap.parse_args()
    try:
        if args.input == '-':
            raw = sys.stdin.buffer.read(MAX_BYTES + 1)
        else:
            with Path(args.input).open('rb') as handle:
                raw = handle.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError('Input exceeds 5 MB')
        rows = json.loads(raw.decode('utf-8-sig'))
        print(json.dumps(analyze(rows, args.rank), ensure_ascii=False, indent=2, allow_nan=False))
    except (OSError, ValueError, TypeError, OverflowError) as exc:
        print('Input error: ' + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
