#!/usr/bin/env python3
"""Maintain an explicitly selected project-owned design source record. No network."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from datetime import datetime, timezone
from urllib.parse import urlsplit, parse_qsl

CATEGORIES = ('product-url', 'figma', 'screenshot', 'codebase', 'component-docs', 'tokens', 'brand-assets', 'context')
STATUSES = ('current', 'proposed', 'historical')
MAX_RECORD_BYTES = 2_000_000
MAX_IMAGE_BYTES = 20_000_000


def timestamp():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[a-z][a-z0-9-]{0,63}', value):
        raise ValueError('ID must start with a lowercase letter and contain only lowercase letters, digits and hyphens (1-64 characters).')
    return value


def validate(record):
    if not isinstance(record, dict) or record.get('schema_version') != 1:
        raise ValueError('Unsupported or malformed design source record.')
    if not isinstance(record.get('sources'), list) or not isinstance(record.get('preferences'), dict):
        raise ValueError('Record needs sources list and preferences object.')
    seen = set()
    for source in record['sources']:
        if not isinstance(source, dict):
            raise ValueError('Each source must be an object.')
        ident = identifier(source.get('id', ''))
        if ident in seen:
            raise ValueError('Duplicate source ID: ' + ident)
        seen.add(ident)
        if source.get('category') not in CATEGORIES or source.get('status') not in STATUSES:
            raise ValueError('Invalid source category or status: ' + ident)
        for key in ('label', 'target', 'added_utc', 'note'):
            if not isinstance(source.get(key), str):
                raise ValueError('Invalid source field: ' + key)
    if any(not isinstance(k, str) or not isinstance(v, str) for k, v in record['preferences'].items()):
        raise ValueError('Preferences must use text keys and values.')
    return record


def read_record(path):
    if path.is_symlink():
        raise ValueError('Record may not be a symlink.')
    if not path.exists():
        return None, None
    if not path.is_file():
        raise ValueError('Record must be a regular, non-symlink file.')
    raw = path.read_bytes()
    if len(raw) > MAX_RECORD_BYTES:
        raise ValueError('Record exceeds the 2 MB read limit.')
    return validate(json.loads(raw.decode('utf-8'))), raw


def atomic_bytes(path, data):
    name = None
    try:
        with tempfile.NamedTemporaryFile(prefix='.' + path.name + '.', dir=path.parent, delete=False) as temp:
            name = Path(temp.name)
            temp.write(data)
            temp.flush()
            os.fsync(temp.fileno())
        os.replace(name, path)
    finally:
        if name and name.exists():
            name.unlink()


def write_record(path, record, previous):
    validate(record)
    encoded = (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if len(encoded) > MAX_RECORD_BYTES:
        raise ValueError('Updated record exceeds the 2 MB limit.')
    if previous is not None:
        backup = path.with_name(path.name + '.previous')
        if backup.is_symlink():
            raise ValueError('Previous-record backup may not be a symlink.')
        atomic_bytes(backup, previous)
    atomic_bytes(path, encoded)


def safe_target(target):
    if not target.strip():
        raise ValueError('Source target cannot be empty.')
    if target.startswith(('http://', 'https://')):
        parsed = urlsplit(target)
        if parsed.username or parsed.password:
            raise ValueError('Do not save URL credentials in a source record.')
        sensitive = {'access_token', 'token', 'api_key', 'apikey', 'password', 'secret', 'authorization'}
        if any(k.lower() in sensitive for k, _ in parse_qsl(parsed.query)):
            raise ValueError('Do not save token/credential query parameters in a source record.')
    return target


def add_source(record, args, target, category, digest=None):
    ident = identifier(args.id)
    existing = next((x for x in record['sources'] if x['id'] == ident), None)
    if existing and not args.replace:
        raise ValueError('Source ID exists; use --replace only for an authorized replacement: ' + ident)
    source = dict(id=ident, category=category, label=args.label, target=safe_target(target), note=args.note, status=args.status, added_utc=timestamp())
    if digest:
        source['sha256'] = digest
    if existing:
        record['sources'][record['sources'].index(existing)] = source
    else:
        record['sources'].append(source)


def image_kind(path):
    with path.open('rb') as image:
        head = image.read(12)
    if head.startswith(b'\x89PNG\r\n\x1a\n'):
        return '.png'
    if head.startswith(b'\xff\xd8\xff'):
        return '.jpg'
    if head[:6] in (b'GIF87a', b'GIF89a'):
        return '.gif'
    if head.startswith(b'RIFF') and head[8:12] == b'WEBP':
        return '.webp'
    raise ValueError('Image import supports PNG, JPEG, GIF or WebP file signatures; no active SVG/HTML content.')


def parser():
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument('--record', type=Path, required=True, help='Explicit project JSON record path. No global state is used.')
    sub = command.add_subparsers(dest='operation', required=True)
    sub.add_parser('init')
    sub.add_parser('list')
    for name in ('add', 'import-image'):
        item = sub.add_parser(name)
        item.add_argument('--id', required=True)
        item.add_argument('--label', required=True)
        item.add_argument('--note', default='')
        item.add_argument('--status', choices=STATUSES, default='current')
        item.add_argument('--replace', action='store_true')
        if name == 'add':
            item.add_argument('--category', choices=CATEGORIES, required=True)
            item.add_argument('--target', required=True)
        else:
            item.add_argument('--source', type=Path, required=True)
    remove = sub.add_parser('remove')
    remove.add_argument('--id', required=True)
    pref = sub.add_parser('set-preference')
    pref.add_argument('--key', required=True)
    pref.add_argument('--value', required=True)
    return command


def main():
    args = parser().parse_args()
    # Make relative paths explicit without resolving a potentially unsafe file symlink.
    path = Path(os.path.abspath(args.record.expanduser()))
    if args.operation == 'list':
        record, _ = read_record(path)
        print(json.dumps({'status': 'present' if record else 'missing', 'record': str(path), 'sources': record['sources'] if record else [], 'preferences': record['preferences'] if record else {}}, ensure_ascii=False, indent=2))
        return
    if args.operation == 'init':
        path.parent.mkdir(parents=True, exist_ok=True)
    if not path.parent.is_dir():
        raise ValueError('Record directory is missing; init the explicitly selected project record first.')
    lock = path.with_name(path.name + '.lock')
    imported = None
    imported_owned = False
    saved = False
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError('Record is locked by another mutation. Inspect that owner; do not remove its lock automatically.')
    try:
        os.close(descriptor)
        record, previous = read_record(path)
        if args.operation == 'init':
            if record is not None:
                print(json.dumps({'status': 'preserved', 'record': str(path)}))
                return
            record = {'schema_version': 1, 'sources': [], 'preferences': {}, 'created_utc': timestamp()}
        elif record is None:
            raise ValueError('Record is missing; init it first. Nothing was saved.')
        if args.operation == 'add':
            add_source(record, args, args.target, args.category)
        elif args.operation == 'import-image':
            source = args.source.expanduser().resolve(strict=True)
            if not source.is_file() or source.stat().st_size > MAX_IMAGE_BYTES:
                raise ValueError('Image must be a regular file no larger than 20 MB.')
            suffix = image_kind(source)
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            folder = path.parent / (path.stem + '-assets')
            if folder.is_symlink():
                raise ValueError('Image asset directory may not be a symlink.')
            folder.mkdir(exist_ok=True)
            imported = folder / (identifier(args.id) + '-' + digest[:12] + suffix)
            add_source(record, args, str(imported.relative_to(path.parent)), 'screenshot', digest)
            # Never overwrite bytes. An existing identical asset can be deliberately reused.
            if imported.exists():
                if imported.is_symlink() or hashlib.sha256(imported.read_bytes()).hexdigest() != digest:
                    raise ValueError('Asset collision; existing bytes were preserved.')
                imported = None
            else:
                with imported.open('xb') as dest:
                    imported_owned = True
                    with source.open('rb') as origin:
                        shutil.copyfileobj(origin, dest)
        elif args.operation == 'remove':
            ident = identifier(args.id)
            if not any(x['id'] == ident for x in record['sources']):
                raise ValueError('No such source ID: ' + ident)
            record['sources'] = [x for x in record['sources'] if x['id'] != ident]
        elif args.operation == 'set-preference':
            if not re.fullmatch(r'[a-z][a-z0-9_-]{0,63}', args.key):
                raise ValueError('Invalid preference key.')
            record['preferences'][args.key] = args.value
        record['updated_utc'] = timestamp()
        write_record(path, record, previous)
        saved = True
        print(json.dumps({'status': 'saved', 'record': str(path), 'source_count': len(record['sources']), 'operation': args.operation}))
    finally:
        if imported_owned and imported is not None and not saved and imported.exists():
            imported.unlink()
        lock.unlink()


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({'status': 'error', 'detail': str(exc)}))
        raise SystemExit(1)
