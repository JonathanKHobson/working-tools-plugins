"""Compare shipped product trees and propose conservative, evidence-based versions."""

from __future__ import annotations

import subprocess

from .catalog import SemVer


def _git(repo, args, runner=None):
    raw = runner(args) if runner else subprocess.check_output(['git', *args], cwd=repo)
    return raw.encode() if isinstance(raw, str) else raw


def changed_products(repo, base: str, target: str, product_ids,
                     *, shared_paths: dict[str, list[str]] | None = None, runner=None) -> dict[str, list[dict]]:
    """Return only changes to distributable product files.

    shared_paths explicitly assigns shared template paths/prefixes to products.
    Website, catalog, release bookkeeping and unrelated files are excluded.
    """
    ids = set(product_ids)
    shared_paths = shared_paths or {}
    for owners in shared_paths.values():
        if not set(owners) <= ids:
            raise ValueError('shared_paths references an unknown product')
    raw = _git(repo, ['diff', '--name-status', '-z', '--no-renames', base, target, '--'], runner)
    parts = raw.decode('utf-8').split('\0')
    changes = {ident: [] for ident in ids}
    for i in range(0, len(parts)-1, 2):
        status, path = parts[i], parts[i+1]
        if not path:
            continue
        owners = set()
        if path.startswith('plugins/'):
            sub = path.split('/', 2)
            if len(sub) == 3 and sub[1] in ids:
                owners.add(sub[1])
        for scope, assigned in shared_paths.items():
            if path == scope or path.startswith(scope.rstrip('/') + '/'):
                owners.update(assigned)
        if not owners:
            continue
        kind = {'A': 'added', 'D': 'removed', 'M': 'modified', 'T': 'modified'}.get(status[0], 'modified')
        for ident in owners:
            changes[ident].append({'status': kind, 'path': path})
    return {ident: sorted(rows, key=lambda row: row['path']) for ident, rows in sorted(changes.items()) if rows}


def propose_version(current: str, changes: list[dict], *, change_level: str | None = None,
                    existing_versions=()) -> str | None:
    """Return the next version or None for no shipped change.

    Explicit major/minor/patch classification is allowed. A removed skill
    invocation or required config file is conservatively major; adding a
    skill is minor; compatible corrections are patch. Review semantics of
    modified instructions/config separately and pass change_level if breaking.
    """
    if not changes:
        return None
    version = SemVer(current)
    if change_level is not None and change_level not in {'major', 'minor', 'patch'}:
        raise ValueError('change_level must be major, minor, or patch')
    removed_breaking = any(row['status'] == 'removed' and (
        row['path'].endswith('/SKILL.md') or row['path'].endswith('/mcp.json')
        or row['path'].endswith('/plugin.json')) for row in changes)
    added_skill = any(row['status'] == 'added' and row['path'].endswith('/SKILL.md') for row in changes)
    inferred = 'major' if removed_breaking else 'minor' if added_skill else 'patch'
    rank = {'patch': 0, 'minor': 1, 'major': 2}
    level = max((inferred, change_level or 'patch'), key=rank.get)
    if level == 'major':
        proposal = f'{version.major+1}.0.0'
    elif level == 'minor':
        proposal = f'{version.major}.{version.minor+1}.0'
    else:
        proposal = f'{version.major}.{version.minor}.{version.patch+1}'
    if any(SemVer(proposal) == SemVer(value) for value in existing_versions):
        raise ValueError(f'proposed version already exists: {proposal}')
    return proposal


def evidence_notes(changes: list[dict]) -> str:
    """Factual path-level draft notes; deliberately no runtime claims."""
    if not changes:
        return 'No distributable package file changes.'
    verbs = {'added': 'Added', 'removed': 'Removed', 'modified': 'Updated'}
    return '\n'.join(f'- {verbs[row["status"]]} `{row["path"]}`.' for row in changes)
