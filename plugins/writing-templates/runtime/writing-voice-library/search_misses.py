"""Explicit, sanitized library search feedback; no automatic search telemetry."""
from __future__ import annotations

import argparse
from collections import Counter
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import uuid

DEFAULT_DB = Path(os.environ.get('ACTIVITIES_SEARCH_MISSES_DB', Path.home() / '.local/share/studio-tools/library-search-misses.sqlite'))
LIBRARIES = {'writing', 'design', 'activity-atlas'}
DIAGNOSES = {'unknown', 'possible_content_gap', 'retrieval_taxonomy', 'restrictive_filters', 'technical_access'}
STATUSES = {'open', 'resolved', 'dismissed'}
FILTERS = {'type', 'category', 'domain', 'collection', 'status', 'participants', 'minutes', 'mode', 'include_unknown', 'limit', 'offset'}
SCHEMA = '''CREATE TABLE IF NOT EXISTS library_search_misses (
 id TEXT PRIMARY KEY, library TEXT NOT NULL, task_key TEXT NOT NULL, need_key TEXT NOT NULL,
 first_seen TEXT NOT NULL, last_seen TEXT NOT NULL, first_observation TEXT NOT NULL,
 observation TEXT NOT NULL, UNIQUE(library, task_key, need_key))'''


def safe_text(value, label, maximum=240, allow_empty=False):
    if not isinstance(value, str) or len(value) > maximum or (not value.strip() and not allow_empty):
        raise ValueError(f'{label}: supply concise sanitized text within {maximum} characters')
    # Defense in depth only: caller must remove names and private task details too.
    if re.search(r'[\x00-\x1f\x7f]|https?://|www\.|\S+@\S+|(?:^|\s)(?:/|~/|[A-Za-z]:\\)|(?:sk-|ghp_|github_pat_|Bearer\s)|\d{7,}|[A-Za-z0-9_+=/-]{48,}', value, re.I):
        raise ValueError(f'{label}: remove sensitive identifiers, paths, URLs, secrets or multiline text')
    return ' '.join(value.split())


def validate(payload):
    allowed = {'library', 'task_key', 'need_key', 'route', 'intent', 'search_terms', 'result_count', 'evidence', 'filters', 'diagnosis', 'diagnosis_evidence', 'reviewed', 'status', 'evidence_source'}
    if not isinstance(payload, dict) or set(payload) - allowed:
        raise ValueError('Unknown feedback fields; never pass the full prompt or tool response')
    p = dict(payload)
    if p.get('library') not in LIBRARIES:
        raise ValueError('Unknown library')
    p['task_key'] = str(uuid.UUID(p['task_key']))
    need = p.get('need_key', '')
    if not isinstance(need, str) or not re.fullmatch(r'[a-z][a-z0-9-]{2,79}', need):
        raise ValueError('need_key must be a stable, nonpersonal lowercase topic slug; reuse across reformulations')
    p['need_key'] = safe_text(need, 'need_key', 80)
    p['route'] = safe_text(p.get('route'), 'route', 120)
    p['intent'] = safe_text(p.get('intent'), 'intent', 180)
    p['search_terms'] = safe_text(p.get('search_terms', ''), 'search_terms', 160, True)
    p['evidence'] = safe_text(p.get('evidence'), 'evidence', 400)
    p['diagnosis'] = p.get('diagnosis', 'unknown')
    p['status'] = p.get('status', 'open')
    p['evidence_source'] = p.get('evidence_source', 'observed')
    p['reviewed'] = p.get('reviewed', False)
    if p['diagnosis'] not in DIAGNOSES or p['status'] not in STATUSES or p['evidence_source'] not in {'observed', 'user_report'} or type(p['reviewed']) is not bool:
        raise ValueError('Invalid diagnosis, status, review flag or evidence source')
    p['diagnosis_evidence'] = safe_text(p.get('diagnosis_evidence', ''), 'diagnosis_evidence', 400, True)
    count = p.get('result_count')
    if count is not None and (type(count) is not int or count < 0):
        raise ValueError('result_count must be an observed nonnegative count or null')
    if count is None and p['diagnosis'] != 'technical_access' and p['evidence_source'] != 'user_report':
        raise ValueError('An observed search needs a result count; do not turn an error into zero results')
    p['result_count'] = count
    if count and len(p['evidence']) < 20:
        raise ValueError('Nonzero poor fit requires a concrete mismatch explanation')
    if (p['reviewed'] or p['status'] != 'open' or p['diagnosis'] != 'unknown') and len(p['diagnosis_evidence']) < 20:
        raise ValueError('Diagnosis or status changes require supporting inspection evidence')
    filters = p.get('filters', {})
    if not isinstance(filters, dict) or set(filters) - FILTERS:
        raise ValueError('Only safe library filter keys are accepted')
    p['filters'] = {}
    for key, value in filters.items():
        if type(value) in (int, bool) or value is None:
            p['filters'][key] = value
        else:
            p['filters'][key] = safe_text(value, 'filter ' + key, 80, True)
    if p['diagnosis'] == 'restrictive_filters' and not p['filters']:
        raise ValueError('Restrictive-filter diagnosis needs the applied filters')
    return p


def unavailable(operation, exc):
    # Never echo the rejected payload or OS exception (which can include private paths).
    return {'ok': False, 'logged': False, 'operation': operation, 'error': type(exc).__name__,
            'message': 'Feedback unavailable or invalid; continue the search/task. Do not claim it was logged.'}


def record(payload, db=DEFAULT_DB):
    try:
        p = validate(payload)
        path = Path(db)
        if path.is_symlink():
            raise ValueError('Symlink database rejected')
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        os.close(fd)
        path.chmod(0o600)
        stamp = datetime.now(timezone.utc).isoformat()
        key = hashlib.sha256((p['library'] + '\0' + p['task_key'] + '\0' + p['need_key']).encode()).hexdigest()[:24]
        observation = json.dumps(p, ensure_ascii=False, sort_keys=True)
        with closing(sqlite3.connect(path, timeout=0.2)) as con:
            with con:
                con.execute(SCHEMA)
                previous = con.execute('SELECT id FROM library_search_misses WHERE id=?', (key,)).fetchone()
                con.execute('''INSERT INTO library_search_misses VALUES (?,?,?,?,?,?,?,?)
                    ON CONFLICT(library,task_key,need_key) DO UPDATE SET
                    last_seen=excluded.last_seen, observation=excluded.observation''',
                    (key, p['library'], p['task_key'], p['need_key'], stamp, stamp, observation, observation))
            # Read after COMMIT: success is a persisted row, not an attempted write.
            row = con.execute('SELECT observation FROM library_search_misses WHERE id=?', (key,)).fetchone()
            if row is None or json.loads(row[0]) != p:
                raise RuntimeError('Readback mismatch')
        return {'ok': True, 'logged': True, 'id': key, 'deduplicated': previous is not None, 'record': p}
    except Exception as exc:
        return unavailable('record', exc)


def report(library='', need_key='', db=DEFAULT_DB):
    try:
        if library and library not in LIBRARIES:
            raise ValueError('Unknown library')
        path = Path(db)
        if path.is_symlink():
            raise ValueError('Symlink database rejected')
        if not path.exists():
            return {'ok': True, 'store_state': 'not_created', 'groups': [], 'records': [], 'note': 'No log exists; absence is not proof that searches succeeded.'}
        with closing(sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True, timeout=0.2)) as con:
            rows = con.execute('SELECT id,first_seen,last_seen,first_observation,observation FROM library_search_misses ORDER BY last_seen DESC').fetchall()
        records, buckets = [], {}
        for key, first, last, initial, encoded in rows:
            p = json.loads(encoded)
            if (library and p['library'] != library) or (need_key and p['need_key'] != need_key):
                continue
            records.append({'id': key, 'first_seen': first, 'last_seen': last, 'first_observation': json.loads(initial), **p})
            buckets.setdefault((p['library'], p['need_key']), []).append(p)
        groups = []
        for (lib, need), items in sorted(buckets.items()):
            groups.append({'library': lib, 'need_key': need,
                'distinct_tasks': len({p['task_key'] for p in items}),
                'observed_tasks': len({p['task_key'] for p in items if p['evidence_source'] == 'observed'}),
                'user_reported_tasks': len({p['task_key'] for p in items if p['evidence_source'] == 'user_report'}),
                'statuses': dict(Counter(p['status'] for p in items)),
                'diagnoses': dict(Counter(p['diagnosis'] for p in items)),
                'provisional': sum(not p['reviewed'] for p in items)})
        return {'ok': True, 'store_state': 'readable', 'groups': groups, 'records': records,
                'note': 'Distinct tasks are prioritization input, not popularity or proof of missing content. Semantic need keys require editorial grouping. Technical errors are not zero-result searches. Logging coverage is not automatic.'}
    except Exception as exc:
        return unavailable('report', exc)


def register_tools(server, library, route_hint='', db=DEFAULT_DB):
    from mcp.types import ToolAnnotations
    @server.tool(name='record_library_search_miss', description=f'Privately record or update one sanitized {library} AI search miss. Reuse one opaque UUID task_key and stable need_key across retries. Never send raw prompts, names, paths or secrets. Zero results do not prove missing content. Only logged=true confirms persistence. Diagnosis is provisional unless inspected and reviewed. Search itself stays read-only.', annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True, openWorldHint=False))
    def record_miss(task_key: str, need_key: str, route: str, intent: str, search_terms: str, evidence: str,
                    result_count: int | None = None, filters: dict | None = None, diagnosis: str = 'unknown',
                    diagnosis_evidence: str = '', reviewed: bool = False, status: str = 'open', evidence_source: str = 'observed') -> dict:
        return record(dict(library=library, task_key=task_key, need_key=need_key, route=route, intent=intent,
            search_terms=search_terms, evidence=evidence, result_count=result_count, filters=filters or {},
            diagnosis=diagnosis, diagnosis_evidence=diagnosis_evidence, reviewed=reviewed, status=status, evidence_source=evidence_source), db)

    @server.tool(name='review_library_search_misses', description=f'Inspect private {library} misses, distinct-task recurrence, provisional diagnoses and status. Reuse a returned need key when recording the same need; counts are not an automatic popularity score. {route_hint}', annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False))
    def review_misses(need_key: str = '') -> dict:
        return report(library, need_key, db)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--record', action='store_true', help='Read one sanitized JSON object from stdin')
    mode.add_argument('--report', action='store_true')
    parser.add_argument('--library', choices=sorted(LIBRARIES), default='')
    parser.add_argument('--need-key', default='')
    args = parser.parse_args()
    try:
        if args.record:
            raw = sys.stdin.read(8193)
            if len(raw) > 8192:
                raise ValueError('Payload too large')
            result = record(json.loads(raw))
        else:
            result = report(args.library, args.need_key)
    except Exception as exc:
        result = unavailable('cli', exc)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
