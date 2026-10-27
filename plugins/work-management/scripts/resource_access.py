#!/usr/bin/env python3
"""Offline resource lookup and explicit installation of reviewed API Anything recipes."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'references/operations/resource-directory.json'
RECIPES = ROOT / 'references/operations/api-anything-recipes'
TOKEN = re.compile(r'^[a-z0-9][a-z0-9-]*$')
SHA256 = re.compile(r'^[0-9a-f]{64}$')


def _json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def _regular_file(path: Path) -> bool:
    return path.is_file() and not path.is_symlink()


def _no_symlink_ancestors(path: Path) -> None:
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError(f'Symlink path refused: {part}')


def resources():
    data = _json(DIRECTORY)
    if data.get('schema_version') != 1 or not isinstance(data.get('resources'), list):
        raise ValueError('Invalid resource directory schema')
    seen = set()
    for item in data['resources']:
        if not isinstance(item, dict) or not isinstance(item.get('id'), str) or not TOKEN.fullmatch(item['id']):
            raise ValueError('Invalid resource ID')
        if item['id'] in seen:
            raise ValueError('Duplicate resource ID')
        seen.add(item['id'])
        if not isinstance(item.get('name'), str):
            raise ValueError('Invalid resource record')
        url = item.get('url')
        unresolved = str(item.get('identity_status', '')).startswith('unresolved')
        if url is None and unresolved:
            pass  # Preserve unresolved identities without substituting a guessed site.
        elif not isinstance(url, str) or not url.startswith('https://'):
            raise ValueError('Resource URL must use HTTPS or remain unresolved')
        if not isinstance(item.get('owner_plugins'), list) or not all(isinstance(x, str) for x in item['owner_plugins']):
            raise ValueError('Invalid resource owners')
    return data['resources']


def _summary(item):
    return {key: item.get(key) for key in ('id', 'name', 'url', 'category', 'owner_plugins', 'identity_status', 'access_route')}


def list_resources(items, owner=None, category=None):
    return [_summary(x) for x in items if (owner is None or owner in x['owner_plugins']) and
            (category is None or x.get('category') == category)]


def search(items, query):
    words = re.findall(r'[a-z0-9]+', query.lower())
    if not words:
        raise ValueError('Search query must contain a word')
    matches = []
    for item in items:
        haystack = ' '.join(str(item.get(k, '')) for k in ('id', 'name', 'url', 'category', 'purpose', 'access_route')).lower()
        haystack += ' ' + ' '.join(item['owner_plugins']).lower()
        if all(word in haystack for word in words):
            matches.append(_summary(item))
    return matches


def show(items, ident):
    return next((x for x in items if x['id'] == ident), None)


def _recipe_bytes(site):
    if not TOKEN.fullmatch(site):
        raise ValueError('Invalid site ID')
    manifest_path = RECIPES / 'manifest.json'
    if not _regular_file(manifest_path):
        raise ValueError('Recipe manifest unavailable')
    manifest = _json(manifest_path)
    files = manifest.get('files')
    if not isinstance(files, dict):
        raise ValueError('Invalid recipe manifest')
    selected = {}
    for suffix in ('.json', '.md'):
        name = site + suffix
        expected = files.get(name)
        source = RECIPES / name
        if not isinstance(expected, str) or not SHA256.fullmatch(expected):
            raise ValueError(f'Recipe not allowlisted: {name}')
        _no_symlink_ancestors(source)
        if not _regular_file(source):
            raise ValueError(f'Recipe unavailable: {name}')
        content = source.read_bytes()
        if hashlib.sha256(content).hexdigest() != expected:
            raise ValueError(f'Recipe hash mismatch: {name}')
        selected[name] = content
    spec = json.loads(selected[site + '.json'])
    operations = spec.get('operations') if isinstance(spec, dict) else None
    if not isinstance(operations, list) or not operations:
        raise ValueError('Recipe has no operations')
    if spec.get('name') != site:
        raise ValueError('Recipe site name mismatch')
    for operation in operations:
        if (not isinstance(operation, dict) or operation.get('readOnly') is not True or
                not isinstance(operation.get('request'), dict) or
                operation['request'].get('method') != 'GET'):
            raise ValueError('Only read-only GET operations can be installed')
    return selected


def install_api(site, state, items=None):
    if not isinstance(site, str) or not TOKEN.fullmatch(site):
        raise ValueError('Invalid site ID')
    if state is None:
        raise ValueError('Explicit --state PATH is required')
    raw_target = Path(state).expanduser().absolute()
    _no_symlink_ancestors(raw_target)
    # Normalize dot segments before comparing containment. Path.absolute() retains '..'.
    target = Path(os.path.abspath(str(raw_target)))
    _no_symlink_ancestors(target)
    plugin = ROOT.resolve()
    if target == plugin or plugin in target.parents:
        raise ValueError('State must be outside the plugin')
    if target.exists() and not target.is_dir():
        raise ValueError('State path is not a directory')
    if items is None:
        items = resources()
    matches = [x for x in items if isinstance(x.get('api_anything'), dict) and x['api_anything'].get('site') == site]
    if not matches:
        raise ValueError('Site is not listed in the resource directory')
    selected = _recipe_bytes(site)
    dest_dir = target / 'sites'
    _no_symlink_ancestors(dest_dir)
    if dest_dir.exists() and not dest_dir.is_dir():
        raise ValueError('sites destination is not a directory')
    changed = {}
    for name, content in selected.items():
        dest = dest_dir / name
        _no_symlink_ancestors(dest)
        if dest.exists():
            if not _regular_file(dest):
                raise ValueError(f'Non-regular destination refused: {name}')
            if dest.read_bytes() != content:
                raise ValueError(f'Existing recipe differs: {name}')
        else:
            changed[name] = content
    if not changed:
        return {'site': site, 'status': 'already-installed', 'files': sorted(selected)}
    dest_dir.mkdir(parents=True, exist_ok=True)
    staged = []
    published = []
    try:
        for name, content in changed.items():
            with tempfile.NamedTemporaryFile(prefix='.resource-access-', dir=dest_dir, delete=False) as tmp:
                tmp.write(content)
                tmp.flush()
                os.fsync(tmp.fileno())
                staged.append((Path(tmp.name), dest_dir / name))
        # Every destination is checked before either reviewed file is published.
        for _, dest in staged:
            if dest.exists() or dest.is_symlink():
                raise ValueError(f'Destination appeared during staging: {dest.name}')
        for tmp, dest in staged:
            # Hard-link creation fails if another writer created the destination.
            os.link(tmp, dest)
            published.append(dest)
    except Exception:
        for dest in published:
            dest.unlink(missing_ok=True)
        raise
    finally:
        for tmp, _ in staged:
            tmp.unlink(missing_ok=True)
    return {'site': site, 'status': 'installed', 'files': sorted(selected)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    listing = sub.add_parser('list')
    listing.add_argument('--owner')
    listing.add_argument('--category')
    searching = sub.add_parser('search')
    searching.add_argument('query')
    showing = sub.add_parser('show')
    showing.add_argument('id')
    installing = sub.add_parser('install-api')
    installing.add_argument('site')
    installing.add_argument('--state', required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        items = resources()
        if args.command == 'list': result = list_resources(items, args.owner, args.category)
        elif args.command == 'search': result = search(items, args.query)
        elif args.command == 'show':
            result = show(items, args.id)
            if result is None: raise ValueError(f'Unknown resource ID: {args.id}')
        else: result = install_api(args.site, args.state, items)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f'resource-access: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
