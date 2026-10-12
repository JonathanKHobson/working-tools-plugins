"""Validate reviewed source coverage; optionally compare the live canonical source.

Public CI checks package bytes against a locked, reviewed source snapshot. Only
--canonical-root enables live local-source verification. --canonical-package
limits that live comparison to named packages while retaining the full public
inventory and baseline checks. This module never
refreshes either inventory or coverage baseline from the current filesystem.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import unicodedata
from typing import Iterable, Mapping

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {'.git', '.venv', '__pycache__', '.pytest_cache'}
DIGEST = re.compile(r'[0-9a-f]{64}\Z')
PACKAGE_ID = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
DISPOSITIONS = {'included', 'external', 'private', 'retired', 'blocked'}
REVISION_KIND = 'sha256-distributable-tree-v1'


def files(root: Path, *, excluded_aliases: set[str] | None = None) -> Iterable[Path]:
    """Match packages.py exclusions; skip only verified canonical aliases.

    The default public scan rejects every symlink. A canonical caller may pass
    exact excluded link paths after checking their declarations and target hashes.
    No symlink destination is traversed, including those explicitly excluded.
    """
    root = Path(root)
    if root.is_symlink():
        raise ValueError('symlink package root')
    excluded_aliases = excluded_aliases or set()

    def walk(directory: Path):
        for path in sorted(directory.iterdir()):
            if path.is_symlink():
                relative = path.relative_to(root).as_posix()
                if relative in excluded_aliases:
                    continue
                raise ValueError(f'symlink is not distributable: {relative}')
            if path.is_dir():
                yield from walk(path)
            elif (path.is_file() and not EXCLUDED_DIRS.intersection(path.parts)
                  and path.name != '.DS_Store' and path.suffix not in {'.pyc', '.pyo'}):
                yield path

    yield from walk(root)


def tree_digest(hashes: Mapping[str, str]) -> str:
    """Hash sorted UTF-8 'sha256  relative/path\n' records (empty tree allowed)."""
    records = ''.join(f'{hashes[path]}  {path}\n' for path in sorted(hashes))
    return hashlib.sha256(records.encode('utf-8')).hexdigest()


def _text(value: object) -> bool:
    return (isinstance(value, str) and bool(value.strip())
            and not any(unicodedata.category(char) in {'Cc', 'Cf', 'Cs'} for char in value))


def _relative(value: object) -> bool:
    return (_text(value) and not value.startswith('/') and '\\' not in value
            and not re.match(r'^[A-Za-z]:', value)
            and all(part not in {'', '.', '..'} for part in value.split('/')))


def _digest(value: object) -> bool:
    return isinstance(value, str) and DIGEST.fullmatch(value) is not None


def _scope(value: object) -> bool:
    return isinstance(value, str) and _relative(value.removesuffix('/'))


def _covered_by_scope(path: str, scope: str) -> bool:
    prefix = scope.removesuffix('/')
    return path == prefix or path.startswith(prefix + '/')


def _no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def _load(path: Path, errors: list[str]):
    try:
        if path.is_symlink():
            raise ValueError('symlink document')
        return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=_no_duplicate_keys)
    except (OSError, ValueError, UnicodeError):
        errors.append(f'{path.name}: missing or invalid JSON document')
        return None


def _document_rows(document, field: str, label: str, errors: list[str]):
    if not isinstance(document, dict):
        return []
    if type(document.get('schema_version')) is not int or document['schema_version'] != 1:
        errors.append(f'{label}: schema_version must be 1')
    if not isinstance(document.get(field), list):
        errors.append(f'{label}: {field} must be a list')
        return []
    return document[field]


def _index(rows, label: str, errors: list[str], *, package_ids: bool = True):
    indexed = {}
    for row in rows:
        if (not isinstance(row, dict) or not _text(row.get('id'))
                or package_ids and not PACKAGE_ID.fullmatch(row['id'])):
            errors.append(f'{label}: invalid package/entry ID')
            continue
        ident = row['id']
        if ident in indexed:
            errors.append(f'{label}: duplicate ID {ident}')
        else:
            indexed[ident] = row
    return indexed


def _physical(root: Path, label: str, errors: list[str], *, excluded_aliases: set[str] | None = None):
    if not root.is_dir():
        errors.append(f'{label}: missing package directory')
        return None
    try:
        return {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in files(root, excluded_aliases=excluded_aliases)}
    except (OSError, ValueError) as exc:
        # No absolute canonical path or private filename is emitted to CI logs.
        detail = str(exc) if label.startswith('public ') and isinstance(exc, ValueError) else 'unsafe or unreadable source tree'
        errors.append(f'{label}: {detail}')
        return None


def _compare(expected: dict, actual: dict, label: str, errors: list[str]):
    for path in sorted(expected.keys() - actual.keys()):
        errors.append(f'{label}: missing file {path}')
    for path in sorted(actual.keys() - expected.keys()):
        errors.append(f'{label}: unexpected file {path}')
    for path in sorted(expected.keys() & actual.keys()):
        if expected[path] != actual[path]:
            errors.append(f'{label}: changed file {path}')


def _dispositions(rows, label: str, errors: list[str], *, excluded: bool = False):
    if not isinstance(rows, list):
        errors.append(f'{label}: dispositions must be a list')
        return []
    for row in rows:
        if not isinstance(row, dict):
            errors.append(f'{label}: invalid disposition record')
            continue
        disposition = row.get('disposition')
        if not isinstance(disposition, str) or disposition not in DISPOSITIONS or (excluded and disposition == 'included'):
            errors.append(f'{label}: invalid disposition')
        if excluded and not _scope(row.get('scope')):
            errors.append(f'{label}: disposition scope must be a safe relative scope')
        if disposition != 'included':
            for field in (('reason', 'capability_effect') if excluded else ('capability_effect',)):
                if not _text(row.get(field)):
                    errors.append(f'{label}: nonincluded disposition requires {field}')
    return rows


def _aliases(rows, locked: dict, label: str, errors: list[str]) -> dict[str, str]:
    """Validate excluded link declarations; hashes lock raw UTF-8 readlink text."""
    if not isinstance(rows, list):
        errors.append(f'{label}: aliases must be a list')
        return {}
    aliases = {}
    for row in rows:
        if not isinstance(row, dict) or not _relative(row.get('path')):
            errors.append(f'{label}: malformed excluded alias path')
            continue
        path = row['path']
        if path in aliases:
            errors.append(f'{label}: duplicate excluded alias path')
        if any(included == path or included.startswith(path + '/') for included in locked):
            errors.append(f'{label}: excluded alias overlaps an included file')
            continue
        if not _digest(row.get('target_sha256')):
            errors.append(f'{label}: invalid excluded alias target_sha256')
            continue
        if not isinstance(row.get('disposition'), str) or row['disposition'] not in DISPOSITIONS - {'included'}:
            errors.append(f'{label}: invalid excluded alias disposition')
        for field in ('reason', 'capability_effect'):
            if not _text(row.get(field)):
                errors.append(f'{label}: excluded alias requires {field}')
        aliases[path] = row['target_sha256']
    if any(other.startswith(path + '/') for path in aliases for other in aliases):
        errors.append(f'{label}: excluded alias paths overlap')
    return aliases


def _verified_alias_paths(root: Path, aliases: dict[str, str], label: str, errors: list[str]) -> set[str]:
    """Verify links without traversing destinations or printing private targets."""
    verified = set()
    for relative, expected in aliases.items():
        path = root/relative
        try:
            # An undeclared parent link must not become a path to a private tree.
            parents = Path(relative).parents
            if any((root/parent).is_symlink() for parent in parents):
                raise ValueError('alias parent is a link')
            if not path.is_symlink():
                raise ValueError('alias missing')
            target_hash = hashlib.sha256(os.readlink(path).encode('utf-8')).hexdigest()
            # Even a changed target is never traversed; its mismatch fails validation.
            verified.add(relative)
            if target_hash != expected:
                errors.append(f'{label}: excluded alias target hash changed')
        except (OSError, ValueError, UnicodeError):
            errors.append(f'{label}: missing or unsafe excluded alias')
    return verified


def validate_inventory(repo_root: Path, records: list[dict], canonical_root: Path | None = None,
                       canonical_packages: Iterable[str] | None = None) -> list[str]:
    """Return all named coverage/hash errors; records are catalog package rows.

    Source and baseline documents come from repo_root/catalog. canonical_root
    contains directories named by canonical_source.id. Component IDs are global
    owner-prefixed IDs, e.g. owner:skills/example/SKILL.md. Baseline owner names
    refer to canonical_source.id, allowing a reviewed public package rename.
    Live comparison resolves the explicitly selected canonical owner directory
    once, allowing maintained top-level directory aliases. Missing/broken owner
    aliases and all public package symlinks remain invalid. Inner symlinks are
    rejected except exact excluded_source.aliases declarations with matching raw
    readlink target hashes, which are skipped without traversing destinations.
    These aliases cannot hide included files and are not regular excluded files.
    With canonical_packages, only those named products receive live source checks;
    the standalone default also audits the complete canonical namespace.
    """
    root = Path(repo_root)
    errors: list[str] = []
    inventory_doc = _load(root/'catalog/source-inventory.json', errors)
    baseline_doc = _load(root/'catalog/coverage-baseline.json', errors)
    inventory_rows = _document_rows(inventory_doc, 'packages', 'source-inventory', errors)
    baseline_rows = _document_rows(baseline_doc, 'entries', 'coverage-baseline', errors)
    if not isinstance(records, list):
        errors.append('catalog: package records must be a list')
        records = []
    registry = _index(records, 'catalog', errors)
    inventory = _index(inventory_rows, 'source-inventory', errors)
    baseline = _index(baseline_rows, 'coverage-baseline', errors, package_ids=False)
    selected = None
    if canonical_packages is not None:
        try:
            requested = list(canonical_packages) if not isinstance(canonical_packages, (str, bytes)) else []
        except TypeError:
            requested = []
        if canonical_root is None or not requested or any(not isinstance(ident, str) or
                not PACKAGE_ID.fullmatch(ident) for ident in requested):
            errors.append('canonical selection: requires a canonical root and nonempty valid package IDs')
        elif len(requested) != len(set(requested)):
            errors.append('canonical selection: duplicate package ID')
        else:
            unknown = set(requested) - (registry.keys() & inventory.keys())
            if unknown:
                errors.append('canonical selection: unknown package ID '+', '.join(sorted(unknown)))
            else:
                selected = set(requested)
    if canonical_root is not None:
        canonical = Path(canonical_root)
        baseline_owners = {row.get('canonical_owner') for row in baseline.values()
                           if isinstance(row.get('canonical_owner'), str)}
        try:
            if canonical.is_symlink() or not canonical.is_dir():
                raise ValueError('canonical root must be a real directory')
            if selected is None:
                for child in sorted(canonical.iterdir()):
                    if child.is_dir() and any((child/manifest).is_file() for manifest in
                                             ('plugin.json', '.codex-plugin/plugin.json', '.claude-plugin/plugin.json')):
                        if child.name not in baseline_owners:
                            safe_id = child.name if PACKAGE_ID.fullmatch(child.name) else '[unreviewed package ID]'
                            errors.append(f'canonical namespace: package ID without baseline owner: {safe_id}')
        except (OSError, ValueError):
            errors.append('canonical namespace: unsafe or unreadable canonical root')
    for ident in sorted(registry.keys() - inventory.keys()):
        errors.append(f'source-inventory: missing package ID {ident}')
    for ident in sorted(inventory.keys() - registry.keys()):
        errors.append(f'source-inventory: unexpected package ID {ident}')
    plugins = root/'plugins'
    if plugins.is_dir():
        for path in sorted(plugins.iterdir()):
            if path.is_symlink():
                errors.append(f'public package: symlink package ID {path.name}')
            elif path.is_dir() and path.name not in registry and path.name not in EXCLUDED_DIRS:
                errors.append(f'public package: unexpected package ID {path.name}')
    components_seen: dict[str, str] = {}
    owners: dict[str, set[str]] = {}
    for ident, row in inventory.items():
        label = f'source-inventory {ident}'
        version = row.get('version')
        if not _text(version):
            errors.append(f'{label}: version must be nonempty')
        if ident in registry and version != registry[ident].get('version'):
            errors.append(f'{label}: wrong version {version!r}; catalog has {registry[ident].get("version")!r}')
        locked = row.get('files')
        if not isinstance(locked, dict):
            errors.append(f'{label}: files must be a path-to-sha256 object')
            locked = {}
        valid_files = {}
        for path, digest in locked.items():
            if not _relative(path):
                errors.append(f'{label}: malformed relative file path')
            elif not _digest(digest):
                errors.append(f'{label}: invalid sha256 for {path}')
            else:
                valid_files[path] = digest
        # canonical_files is optional: it records the last-known canonical byte
        # hashes separately from the shipped public hashes (valid_files), since
        # publication only ever copies canonical -> public and never writes
        # canonical, so the two can legitimately diverge (e.g. a version bump).
        # Absent entirely, canonical is assumed to still mirror the public tree.
        canonical_locked = row.get('canonical_files')
        valid_canonical_files = valid_files
        if canonical_locked is not None:
            if not isinstance(canonical_locked, dict):
                errors.append(f'{label}: canonical_files must be a path-to-sha256 object')
            else:
                valid_canonical_files = {}
                for path, digest in canonical_locked.items():
                    if path not in valid_files:
                        errors.append(f'{label}: canonical_files path not in files: {path}')
                    elif not _digest(digest):
                        errors.append(f'{label}: invalid canonical sha256 for {path}')
                    else:
                        valid_canonical_files[path] = digest
        source = row.get('canonical_source')
        source = source if isinstance(source, dict) else {}
        owner = source.get('id')
        if not isinstance(owner, str) or not PACKAGE_ID.fullmatch(owner):
            errors.append(f'{label}: invalid canonical source ID')
            owner = None
        revision = source.get('revision')
        revision = revision if isinstance(revision, dict) else {}
        if revision.get('kind') != REVISION_KIND or not _digest(revision.get('sha256')):
            errors.append(f'{label}: invalid source revision')
        elif revision['sha256'] != tree_digest(valid_files):
            errors.append(f'{label}: source revision digest differs from locked files')
        components = row.get('components')
        if not isinstance(components, list):
            errors.append(f'{label}: components must be a list')
            components = []
        component_ids = set()
        component_paths = set()
        for component in components:
            if not isinstance(component, dict):
                errors.append(f'{label}: malformed component')
                continue
            cid, path = component.get('id'), component.get('path')
            if _text(cid):
                if cid in components_seen:
                    errors.append(f'{label}: duplicate component ID {cid} (also {components_seen[cid]})')
                components_seen[cid] = ident
            if not _text(cid) or not cid.startswith(ident + ':') or not _relative(cid[len(ident)+1:]):
                errors.append(f'{label}: component ID must use a safe owner-prefixed path')
            else:
                component_ids.add(cid)
            if not _text(component.get('kind')):
                errors.append(f'{label}: component kind must be nonempty')
            if not _relative(path):
                errors.append(f'{label}: malformed component path')
            elif path not in valid_files:
                errors.append(f'{label}: component path not included: {path}')
            else:
                component_paths.add(path)
        for path in sorted(valid_files):
            if Path(path).name == 'SKILL.md' and path not in component_paths:
                errors.append(f'{label}: SKILL.md lacks named component: {path}')
        if owner:
            owners.setdefault(owner, set()).update(component_ids)
        excluded = row.get('excluded_source')
        excluded = excluded if isinstance(excluded, dict) else {}
        count, extra_digest = excluded.get('files'), excluded.get('tree_sha256')
        if type(count) is not int or count < 0:
            errors.append(f'{label}: excluded source file count must be a nonnegative integer')
        if not _digest(extra_digest):
            errors.append(f'{label}: excluded source tree_sha256 is invalid')
        dispositions = _dispositions(excluded.get('dispositions'), label+' excluded source', errors, excluded=True)
        aliases = _aliases(excluded.get('aliases', []), valid_files, label+' excluded source', errors)
        if type(count) is int and count > 0 and not dispositions:
            errors.append(f'{label}: excluded source files require explicit dispositions')
        if count == 0 and _digest(extra_digest) and extra_digest != tree_digest({}):
            errors.append(f'{label}: empty excluded source tree digest is stale')
        actual = _physical(plugins/ident, 'public '+ident, errors)
        if actual is not None:
            _compare(valid_files, actual, 'public '+ident, errors)
            for manifest in ('plugin.json', '.codex-plugin/plugin.json', '.claude-plugin/plugin.json'):
                if manifest in actual:
                    document = _load(plugins/ident/manifest, errors)
                    if isinstance(document, dict) and document.get('version') != version:
                        errors.append(f'public {ident}: wrong version in {manifest}')
        if canonical_root is not None and owner and (selected is None or ident in selected):
            try:
                source_root = (Path(canonical_root)/owner).resolve(strict=True)
            except (OSError, RuntimeError):
                errors.append(f'canonical {owner}: missing or broken canonical owner directory')
                source_root = None
            alias_paths = _verified_alias_paths(source_root, aliases, 'canonical '+owner, errors) if source_root is not None else set()
            actual_source = _physical(source_root, 'canonical '+owner, errors, excluded_aliases=alias_paths) if source_root is not None else None
            if actual_source is not None:
                included_source = {path: digest for path, digest in actual_source.items() if path in valid_canonical_files}
                _compare(valid_canonical_files, included_source, 'canonical '+owner, errors)
                extras = {path: digest for path, digest in actual_source.items() if path not in valid_canonical_files}
                scopes = sorted({row['scope'] for row in dispositions
                                 if isinstance(row, dict) and _scope(row.get('scope'))})
                if any(not any(_covered_by_scope(path, scope) for scope in scopes) for path in extras):
                    errors.append(f'canonical {owner}: unreviewed excluded source scope; '
                                  'some excluded files have no matching declared scope')
                if len(extras) != count or tree_digest(extras) != extra_digest:
                    errors.append(f'canonical {owner}: unreviewed excluded source additions/removals/changes; '
                                  f'expected {count} files, observed {len(extras)}; reviewed scopes: {", ".join(scopes) or "none"}')
    included_owners = set()
    for ident, row in baseline.items():
        label = f'coverage-baseline {ident}'
        _dispositions([row], label, errors)
        expected = row.get('expected_components')
        if not isinstance(expected, list) or not all(_text(cid) for cid in expected):
            errors.append(f'{label}: expected_components must be a list of component IDs')
            expected = []
        elif len(expected) != len(set(expected)):
            errors.append(f'{label}: duplicate expected component IDs')
        evidence = row.get('evidence')
        if not isinstance(evidence, list) or not evidence or not all(_text(item) for item in evidence):
            errors.append(f'{label}: evidence must be a nonempty list of nonempty references')
        owner = row.get('canonical_owner')
        if not isinstance(owner, str) or not PACKAGE_ID.fullmatch(owner):
            errors.append(f'{label}: invalid canonical_owner')
            continue
        if row.get('disposition') == 'included':
            included_owners.add(owner)
            if owner not in owners:
                errors.append(f'{label}: included owner missing from source inventory: {owner}')
            for cid in expected:
                if cid not in owners.get(owner, set()):
                    errors.append(f'{label}: expected component missing for {owner}: {cid}')
    for owner in sorted(owners.keys() - included_owners):
        errors.append(f'coverage-baseline: inventory owner absent from included baseline: {owner}')
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT)
    parser.add_argument('--canonical-root', type=Path)
    parser.add_argument('--canonical-package', action='append', dest='canonical_packages',
                        help='Check live canonical bytes only for this reviewed product ID; repeat for multiple products')
    args = parser.parse_args(argv)
    errors: list[str] = []
    catalog = _load(args.root/'catalog/packages.json', errors)
    records = catalog.get('packages') if isinstance(catalog, dict) else None
    if not isinstance(records, list):
        errors.append('packages.json: packages must be a list')
        records = []
    errors.extend(validate_inventory(args.root, records, args.canonical_root, args.canonical_packages))
    coverage_errors: list[str] = []
    coverage = _load(args.root/'catalog/coverage-baseline.json', coverage_errors)
    entries = coverage.get('entries', []) if isinstance(coverage, dict) else []
    counts = {disposition: sum(isinstance(row, dict) and row.get('disposition') == disposition for row in entries)
              for disposition in sorted(DISPOSITIONS)} if isinstance(entries, list) else {}
    verification = ('reviewed public snapshot only; live canonical source not checked'
                    if args.canonical_root is None else
                    'live canonical source for selected packages and reviewed public snapshot; other canonical sources and namespace not checked'
                    if args.canonical_packages is not None else
                    'live canonical source and reviewed public snapshot')
    print(json.dumps({'status': 'failed' if errors else 'passed', 'packages': len(records),
                      'verification': verification,
                      'coverage_dispositions': counts,
                      'coverage_note': 'Validation success checks the inventory; blocked capabilities remain unresolved.',
                      'errors': errors}, indent=2))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
