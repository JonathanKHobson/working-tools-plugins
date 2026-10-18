#!/usr/bin/env python3
"""Offline byte-level journal for canonical plugin sources.

This observes source trees and may refresh a local review queue. It never builds,
installs, publishes, or authorizes a release.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import time
import uuid


SKIP_DIRS = {'.git', 'node_modules', '.venv', 'venv', '__pycache__', '.pytest_cache'}
MANIFESTS = ('.codex-plugin/plugin.json', '.claude-plugin/plugin.json',
             'plugin.portable.json', 'plugin.json')
SCHEMA = 1


def _now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def _atomic_json(path: Path, value: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            os.fchmod(stream.fileno(), 0o600)
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def _load(path: Path):
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
        if (not isinstance(value, dict) or value.get('schema_version') != SCHEMA
                or not isinstance(value.get('revision'), int)
                or value['revision'] < 0 or not isinstance(value.get('products'), dict)
                or not isinstance(value.get('events'), list)
                or not isinstance(value.get('pending_refresh_ids', []), list)
                or not isinstance(value.get('initialized_at'), str)
                or not isinstance(value.get('observed_at'), str)):
            raise ValueError('invalid schema')
        for product in value['products'].values():
            if not isinstance(product, dict) or not isinstance(product.get('files'), dict):
                raise ValueError('invalid product')
            for entry in product['files'].values():
                if (not isinstance(entry, dict) or not isinstance(entry.get('sha256'), str)
                        or not isinstance(entry.get('size'), int)
                        or not isinstance(entry.get('mtime_ns'), int)):
                    raise ValueError('invalid file')
        if any(not isinstance(ident, str) or not ident for ident in value.get('pending_refresh_ids', [])):
            raise ValueError('invalid pending refresh IDs')
        for event in value['events']:
            if (not isinstance(event, dict)
                    or any(not isinstance(event.get(key), str) or not event[key]
                           for key in ('id', 'at', 'origin'))
                    or not isinstance(event.get('changes'), list) or not event['changes']):
                raise ValueError('invalid event')
            for change in event['changes']:
                if (not isinstance(change, dict)
                        or any(not isinstance(change.get(key), str) or not change[key]
                               for key in ('plugin', 'path'))
                        or change.get('operation') not in {'added', 'edited', 'deleted'}
                        or any(change.get(key) is not None and not isinstance(change[key], str)
                               for key in ('before_sha256', 'after_sha256'))):
                    raise ValueError('invalid change')
        return value
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, TypeError) as exc:
        raise ValueError('Change journal is corrupt; original bytes preserved') from exc


def _excluded(name: str):
    return (name == '.DS_Store' or name.startswith('._') or name.endswith(('.pyc', '.pyo'))
            or name.endswith(('~', '.swp', '.swo', '.tmp', '.temp')))


def _file_entry(path: Path, previous: dict | None):
    before = path.lstat()
    if stat.S_ISLNK(before.st_mode):
        target = os.readlink(path)
        digest = hashlib.sha256(b'link\0' + os.fsencode(target)).hexdigest()
        after = path.lstat()
        if before.st_mtime_ns != after.st_mtime_ns or before.st_size != after.st_size:
            raise OSError('link changed during scan')
        return {'sha256': digest, 'size': before.st_size, 'mtime_ns': before.st_mtime_ns,
                'kind': 'symlink', 'target': target}
    if not stat.S_ISREG(before.st_mode):
        return None
    if (previous and previous.get('kind', 'file') == 'file'
            and previous.get('size') == before.st_size
            and previous.get('mtime_ns') == before.st_mtime_ns
            and previous.get('ctime_ns') == before.st_ctime_ns
            and previous.get('dev') == before.st_dev
            and previous.get('ino') == before.st_ino):
        return previous
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        opened = os.fstat(stream.fileno())
        if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            raise OSError('file replaced during scan')
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
        after = os.fstat(stream.fileno())
    if ((before.st_size, before.st_mtime_ns, before.st_ctime_ns) !=
            (after.st_size, after.st_mtime_ns, after.st_ctime_ns)):
        raise OSError('file changed during scan')
    return {'sha256': digest.hexdigest(), 'size': before.st_size,
            'mtime_ns': before.st_mtime_ns, 'ctime_ns': before.st_ctime_ns,
            'dev': before.st_dev, 'ino': before.st_ino, 'kind': 'file'}


def _scan_product(root: Path, previous: dict):
    files = {}
    prior = previous.get('files', {})
    for directory, dirs, names in os.walk(root, followlinks=False, onerror=lambda e: (_ for _ in ()).throw(e)):
        base = Path(directory)
        kept = []
        for name in sorted(dirs):
            if name in SKIP_DIRS:
                continue
            path = base / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                files[rel] = _file_entry(path, prior.get(rel))
            else:
                kept.append(name)
        dirs[:] = kept
        for name in sorted(names):
            if _excluded(name):
                continue
            path = base / name
            rel = path.relative_to(root).as_posix()
            item = _file_entry(path, prior.get(rel))
            if item is not None:
                files[rel] = item
    return {'files': files}


def _is_product(path: Path):
    return path.is_dir() and ((path / 'skills').is_dir()
                              or any((path / manifest).is_file() for manifest in MANIFESTS))


def _sources(config: dict, known=()):
    root = Path(config['canonical_root']).expanduser()
    if not root.is_dir():
        return None, set()
    sources = {}
    unavailable = set()
    for path in sorted(root.iterdir(), key=lambda p: p.name):
        if path.name.startswith('.') or path.name in SKIP_DIRS:
            continue
        if path.is_symlink() and not path.exists():
            unavailable.add(path.name)
        elif _is_product(path) or (path.name in known and path.is_dir()):
            sources[path.name] = path
    overrides = config.get('canonical_sources', {})
    if not isinstance(overrides, dict):
        raise ValueError('canonical_sources must be an object')
    for ident, raw in overrides.items():
        if not isinstance(ident, str) or not ident or '/' in ident or not isinstance(raw, str):
            raise ValueError('invalid canonical source mapping')
        path = Path(raw).expanduser()
        if path.is_dir() and (_is_product(path) or ident in known):
            sources[ident] = path
            unavailable.discard(ident)
        else:
            sources.pop(ident, None)
            unavailable.add(ident)
    return sources, unavailable


def _changes(before: dict, after: dict, ident: str):
    old = before.get('files', {})
    new = after.get('files', {})
    result = []
    for rel in sorted(old.keys() | new.keys()):
        a = old.get(rel, {}).get('sha256')
        b = new.get(rel, {}).get('sha256')
        if a == b:
            continue
        result.append({'plugin': ident, 'path': rel,
                       'operation': 'added' if a is None else 'deleted' if b is None else 'edited',
                       'before_sha256': a, 'after_sha256': b})
    return result


def _public_ids(release_root: Path):
    path = release_root / 'catalog/packages.json'
    value = json.loads(path.read_text(encoding='utf-8'))
    return {row['id'] for row in value['packages']}


def _refresh_pending(document: dict, config: dict, baseline: bool):
    release_config = config.get('release_config')
    if not release_config:
        return None
    release_config = Path(release_config).expanduser()
    release = json.loads(release_config.read_text(encoding='utf-8'))
    root = Path(release['public_source']).expanduser()
    if not root.is_dir():
        return 'public source unavailable'
    ids = _public_ids(root)
    selected = set(document.get('pending_refresh_ids', [])) & ids
    if baseline:
        selected |= set(document['products']) & ids
    if not selected:
        document['pending_refresh_ids'] = []
        return None
    lock_path = root / 'dist/release-manager/completion.lock'
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return 'release completion busy'
        # Import only the reviewed local release package. Never call complete_update.
        sys.path.insert(0, str(root / 'scripts'))
        try:
            from release_manager import pending
            pending.refresh(root, release, sorted(selected))
        finally:
            sys.path.remove(str(root / 'scripts'))
            for name in list(sys.modules):
                if name == 'release_manager' or name.startswith('release_manager.'):
                    module = sys.modules[name]
                    if str(root / 'scripts') in str(getattr(module, '__file__', '')):
                        del sys.modules[name]
    document['pending_refresh_ids'] = []
    return None


def record(config: dict, origin: str = 'manual') -> dict:
    """Observe available canonical products and persist one atomic material batch.

    An unavailable product remains in its last known state. A corrupt journal is
    never overwritten. Queue errors are returned and retained for the next run.
    """
    if not isinstance(config, dict) or not config.get('canonical_root') or not config.get('state_dir'):
        raise ValueError('canonical_root and state_dir are required')
    if not isinstance(origin, str) or not origin or len(origin) > 120:
        raise ValueError('invalid origin')
    state = Path(config['state_dir']).expanduser()
    state.mkdir(parents=True, exist_ok=True)
    lock_path = state / 'journal.lock'
    with lock_path.open('a') as lock:
        os.fchmod(lock.fileno(), 0o600)
        deadline = time.monotonic() + 0.5
        while True:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    return {'status': 'busy', 'changed': 0, 'revision': None}
                time.sleep(0.025)
        journal_path = state / 'journal.json'
        previous = _load(journal_path)
        sources, unavailable = _sources(config, previous['products'] if previous else ())
        if sources is None:
            return {'status': 'unavailable', 'changed': 0,
                    'revision': previous['revision'] if previous else None,
                    'unavailable': ['canonical_root']}
        now = _now()
        baseline = previous is None
        document = previous or {'schema_version': SCHEMA, 'revision': 0,
                                'initialized_at': now, 'observed_at': now,
                                'products': {}, 'events': [], 'pending_refresh_ids': []}
        products = dict(document['products'])
        changes = []
        for ident, path in sorted(sources.items()):
            try:
                current = _scan_product(path, products.get(ident, {}))
            except (OSError, UnicodeError, ValueError):
                unavailable.add(ident)
                continue
            if not baseline:
                changes.extend(_changes(products.get(ident, {}), current, ident))
            products[ident] = current
        for ident in sorted(set(products) - set(sources) - unavailable):
            if not baseline:
                changes.extend(_changes(products[ident], {'files': {}}, ident))
            del products[ident]
        material = bool(changes)
        if baseline or material or products != document['products']:
            document['products'] = products
            if baseline and config.get('release_config'):
                document['pending_refresh_ids'] = sorted(products)
            if material:
                document['revision'] += 1
                document['observed_at'] = now
                document['events'].append({'id': uuid.uuid4().hex, 'at': now,
                                           'origin': origin, 'changes': changes})
                document['pending_refresh_ids'] = sorted(set(document['pending_refresh_ids']) |
                                                        {item['plugin'] for item in changes})
            _atomic_json(journal_path, document)
        queue_error = None
        if config.get('release_config') and (baseline or document['pending_refresh_ids']):
            try:
                queue_error = _refresh_pending(document, config, baseline)
                if queue_error is None:
                    _atomic_json(journal_path, document)
            except (OSError, ValueError, KeyError, ImportError, TypeError) as exc:
                queue_error = str(exc)
        return {'status': 'recorded' if baseline else 'changed' if material else 'unchanged',
                'changed': len(changes), 'revision': document['revision'],
                'unavailable': sorted(unavailable), 'queue_error': queue_error}


def _private_error(config_path: Path, message: str, config: dict | None = None):
    if isinstance(config, dict) and isinstance(config.get('state_dir'), str) and config['state_dir']:
        path = Path(config['state_dir']).expanduser() / 'errors.log'
    else:
        path = Path.home() / '.local/state/plugin-change-tracking/errors.log'
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_APPEND | os.O_WRONLY, 0o600)
    with os.fdopen(fd, 'w') as stream:
        stream.write(f'{_now()} {config_path}: {message}\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path,
                        default=Path.home() / '.config/studio-tools/plugin-change-tracking.json')
    parser.add_argument('--origin', default='manual')
    parser.add_argument('--quiet', action='store_true')
    args = parser.parse_args()
    config = None
    try:
        config = json.loads(args.config.expanduser().read_text(encoding='utf-8'))
        result = record(config, args.origin)
        # Activity capture is a separate, explicitly opted-in observer. Its
        # failure must never change the established plugin journal result.
        activity_error = None
        activity_config = config.get('work_activity_config') if isinstance(config, dict) else None
        if activity_config:
            try:
                activity_path = Path(activity_config).expanduser()
                activity_config_value = json.loads(activity_path.read_text(encoding='utf-8'))
                activity_module_path = Path(__file__).with_name('work_activity_record.py')
                activity_spec = importlib.util.spec_from_file_location(
                    'work_management_work_activity_record', activity_module_path)
                if activity_spec is None or activity_spec.loader is None:
                    raise ImportError('work activity recorder unavailable')
                activity_module = importlib.util.module_from_spec(activity_spec)
                activity_spec.loader.exec_module(activity_module)
                scan_work_activity = activity_module.scan
                scan_work_activity(activity_config_value)
            except Exception as exc:
                activity_error = str(exc)
                if args.quiet:
                    _private_error(args.config, f'work activity capture: {activity_error}', config)
        if args.quiet and result.get('queue_error'):
            _private_error(args.config, result['queue_error'], config)
        elif not args.quiet:
            if activity_error:
                result['activity_error'] = activity_error
            print(json.dumps(result, sort_keys=True))
        return 0
    except Exception as exc:
        if args.quiet:
            try:
                _private_error(args.config, str(exc), config)
            except OSError:
                pass
            return 0
        print(f'plugin change recorder: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
