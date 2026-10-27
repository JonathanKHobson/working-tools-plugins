"""Check license packaging and exact scope coverage, without inferring rights.

A passing result establishes document/metadata closure only. The maintainer must
still review provenance, upstream grant compatibility and authority to license.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

INVENTORY_FILES = frozenset({'LICENSE-SCOPE.json', 'PROVENANCE.json', 'PUBLIC_FILE_MANIFEST.json'})
REQUIRED_DOCUMENTS = ('LICENSE', 'LICENSING.md', 'THIRD_PARTY_NOTICES.md', 'LICENSE-SCOPE.json')
MANIFESTS = ('plugin.json', 'plugin.portable.json', '.codex-plugin/plugin.json', '.claude-plugin/plugin.json')


def package_files(root: Path):
    for path in sorted(root.rglob('*')):
        if any(part in ('__pycache__', '.pytest_cache', '.git', '.venv') for part in path.relative_to(root).parts):
            continue
        if path.name == '.DS_Store' or path.name.endswith(('.pyc', '.pyo')):
            continue
        if path.is_file() or path.is_symlink():
            yield path


def legal_errors(root: Path, record: dict) -> list[str]:
    """Return release-blocking missing/stale license packaging diagnostics."""
    errors = []
    ident = record['id']

    def problem(message):
        errors.append(f'{ident}: legal packaging: {message}')

    def read(path):
        try:
            value = json.loads(path.read_text())
            if not isinstance(value, dict):
                raise ValueError('expected object')
            return value
        except (OSError, ValueError) as exc:
            problem(f'invalid {path.relative_to(root)}: {exc}')
            return {}

    for name in REQUIRED_DOCUMENTS:
        path = root / name
        if path.is_symlink() or not path.is_file() or not path.stat().st_size:
            problem(f'missing, empty or linked {name}')
    scope_path = root / 'LICENSE-SCOPE.json'
    if not scope_path.is_file() or scope_path.is_symlink():
        return errors
    scope = read(scope_path)
    if scope.get('package') != ident or scope.get('version') != record['version']:
        problem('LICENSE-SCOPE.json identity/version differs from registry')
    registry_license = record.get('license', '').split(';', 1)[0].strip()
    if not registry_license:
        problem('registry lacks license declaration')
    for name in MANIFESTS:
        path = root / name
        if not path.is_file():
            continue  # Host/portable presence is checked by packages.py.
        if path.is_symlink():
            problem(f'linked manifest {name}')
            continue
        declared = read(path).get('license')
        if not declared or declared != registry_license:
            problem(f'{name} license differs from registry: {declared!r}')

    rows = scope.get('files')
    if not isinstance(rows, list) or not rows:
        problem('LICENSE-SCOPE.json lacks nonempty files inventory')
        return errors
    indexed = {}
    actual = {path.relative_to(root).as_posix(): path for path in package_files(root)}
    for row in rows:
        if not isinstance(row, dict):
            problem('invalid scope row')
            continue
        rel = row.get('path')
        if not isinstance(rel, str) or not rel or '\\' in rel or str(PurePosixPath(rel)) != rel or PurePosixPath(rel).is_absolute() or '..' in PurePosixPath(rel).parts:
            problem(f'unsafe scope path: {rel!r}')
            continue
        if rel in indexed:
            problem(f'duplicate scope path: {rel}')
        indexed[rel] = row
        if not row.get('category') or not row.get('license'):
            problem(f'missing category/license: {rel}')
        digest = row.get('sha256')
        if not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest):
            problem(f'invalid scope digest: {rel}')
        path = actual.get(rel)
        if path is None or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            problem(f'scoped file absent or linked: {rel}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            problem(f'stale scope digest: {rel}')
    # These three inventories cannot hash themselves or one another reliably.
    # No arbitrary directory/pattern exclusion may conceal operative content.
    exemptions = scope.get('inventory_excludes', [])
    if not isinstance(exemptions, list) or any(name not in INVENTORY_FILES for name in exemptions):
        problem('unsupported scope exclusions; only inventory metadata may be exempt')
    for rel in sorted(set(actual) - set(indexed) - INVENTORY_FILES):
        problem(f'file has no exact license scope: {rel}')
    return errors




def source_rights_release_errors(root: Path, record: dict) -> list[str]:
    """Enforce a recorded review hold, independently of valid license packaging.

    A resolution is valid only for its named exact bytes. This is a maintainer
    release-readiness control and adds no condition to any upstream license.
    """
    prefix = f"{record['id']}: source-rights release review: "
    licensing = record.get('licensing', {})
    if not isinstance(licensing, dict):
        return [prefix + 'invalid licensing record; expected object']
    review = licensing.get('releaseReview')
    if review is None:
        return []
    errors = []
    if not isinstance(review, dict):
        return [prefix + 'invalid review record']
    bindings = review.get('files')
    if not isinstance(bindings, dict) or not bindings:
        return [prefix + 'missing exact reviewed file bindings']
    for rel, expected in bindings.items():
        if not isinstance(rel, str) or not rel or '\\' in rel or PurePosixPath(rel).is_absolute() or str(PurePosixPath(rel)) != rel or '..' in PurePosixPath(rel).parts:
            errors.append(prefix + 'unsafe reviewed path')
            continue
        path = root / rel
        if not isinstance(expected, str) or not re.fullmatch('[0-9a-f]{64}', expected):
            errors.append(prefix + f'invalid reviewed hash: {rel}')
        elif path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
            errors.append(prefix + f'reviewed file absent or linked: {rel}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append(prefix + f'reviewed bytes changed; fresh source-rights review required: {rel}')
    status = review.get('status')
    if status == 'held':
        errors.append(prefix + 'held: ' + str(review.get('reason', review.get('issue', 'unresolved source rights'))))
    elif status == 'resolved':
        resolution = review.get('resolution')
        if not isinstance(resolution, dict) or any(not isinstance(resolution.get(key), str) or not resolution[key].strip() for key in ['reviewer', 'date', 'basis', 'evidence']):
            errors.append(prefix + 'resolution lacks reviewer, date, source basis or evidence')
    else:
        errors.append(prefix + 'unknown review status')
    return errors


def archive_legal_errors(source, expected_files: dict, ident: str, version: str) -> list[str]:
    """Check full verified plugin ZIP closure without extracting/running content.

    expected_files covers the complete source release, not one selected skill.
    No historical registry record is supplied, so manifests are compared only
    with each other. Registry consistency is enforced before source release.
    """
    errors = []
    for name in REQUIRED_DOCUMENTS:
        if name not in expected_files or not source.read(name).strip():
            errors.append(f'missing or empty {name}')
    if 'LICENSE-SCOPE.json' not in expected_files:
        return errors
    try:
        scope = json.loads(source.read('LICENSE-SCOPE.json'))
        if scope.get('package') != ident or scope.get('version') != version:
            errors.append('license scope identity/version mismatch')
        exemptions = scope.get('inventory_excludes', [])
        if not isinstance(exemptions, list) or any(name not in INVENTORY_FILES for name in exemptions):
            errors.append('unsupported license scope exclusions')
        rows = scope.get('files')
        if not isinstance(rows, list) or not rows:
            raise ValueError('expected nonempty files inventory')
        indexed = {}
        for row in rows:
            rel = row.get('path')
            if rel in indexed:
                errors.append(f'duplicate license scope path: {rel}')
            indexed[rel] = row
            if not row.get('category') or not row.get('license'):
                errors.append(f'missing license scope category/grant: {rel}')
            if rel not in expected_files or row.get('sha256') != expected_files[rel]:
                errors.append(f'license scope hash/closure mismatch: {rel}')
        for rel in sorted(set(expected_files) - set(indexed) - INVENTORY_FILES):
            errors.append(f'file has no license scope: {rel}')
    except (ValueError, AttributeError, TypeError) as exc:
        errors.append(f'invalid license scope: {exc}')
    declarations = []
    for name in MANIFESTS:
        if name not in expected_files:
            continue
        try:
            declared = json.loads(source.read(name)).get('license')
            if not isinstance(declared, str) or not declared.strip():
                errors.append(f'missing or invalid manifest license: {name}')
                continue
            declarations.append(declared)
        except (ValueError, AttributeError) as exc:
            errors.append(f'invalid manifest: {name}: {exc}')
    if not declarations or len(set(declarations)) != 1:
        errors.append('inconsistent or absent manifest license declarations')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--package', action='append', default=[])
    args = parser.parse_args()
    records = json.loads((args.root / 'catalog/packages.json').read_text())['packages']
    if args.package:
        unknown = set(args.package) - {row['id'] for row in records}
        if unknown:
            parser.error('unknown package: ' + ', '.join(sorted(unknown)))
        records = [row for row in records if row['id'] in args.package]
    errors = [error for row in records for error in legal_errors(args.root / 'plugins' / row['id'], row)]
    print(json.dumps({'packages': len(records), 'passed': not errors, 'errors': errors,
                      'scope': 'Packaging and metadata closure; not legal/provenance clearance.'}, indent=2))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
