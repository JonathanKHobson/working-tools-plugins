"""Version and verify the optional, independently installable host hooks pack."""

from __future__ import annotations

import hashlib
import io
import json
import re
import stat
import subprocess
import tempfile
import zipfile
from pathlib import Path

from .catalog import SemVer
from .changes import propose_version
from .publisher import list_releases, publish, resolved_tag, run as publisher_run

REPOSITORY = 'JonathanKHobson/working-tools-plugins'
ID = 'codex-host-hooks'
PREFIX = 'integrations/codex-host-hooks/'
CATALOG = 'catalog/integrations.json'
TAG = re.compile(r'^codex-host-hooks/v(.+)$')
SHA = re.compile(r'^[0-9a-f]{64}$')


def _git(root, *args) -> bytes:
    return subprocess.check_output(['git', *args], cwd=root)


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _files(root: Path, commit: str) -> dict[str, str]:
    tree = _git(root, 'ls-tree', '-r', '-z', commit, PREFIX).split(b'\0')
    names = []
    for item in tree:
        if not item:
            continue
        metadata, raw_name = item.split(b'\t', 1)
        mode, kind, _oid = metadata.decode().split(' ', 2)
        name = raw_name.decode('utf-8')
        if mode not in {'100644', '100755'} or kind != 'blob':
            raise ValueError(f'{ID}: unsupported source entry {name}')
        if (not name.startswith(PREFIX) or any(part in {'.git', '.venv', '__pycache__', '.pytest_cache'}
                                                 for part in name.split('/'))
                or name.endswith(('.pyc', '.pyo', '.DS_Store'))):
            raise ValueError(f'{ID}: unreviewable source entry {name}')
        names.append(name)
    if not names:
        raise ValueError(f'{ID}: missing exact public source tree')
    return {name: _digest(_git(root, 'show', f'{commit}:{name}')) for name in sorted(names)}


def _load(root: Path) -> tuple[dict, dict]:
    document = json.loads((root / CATALOG).read_text(encoding='utf-8'))
    if document.get('schema_version') != 'working-tools.integrations.v1':
        raise ValueError('Invalid integration catalog schema')
    products = document.get('products')
    if not isinstance(products, list) or len(products) != 1 or products[0].get('id') != ID:
        raise ValueError('Integration catalog must contain the registered hooks pack')
    return document, products[0]


def _archive_matches(raw: bytes, version: str, files: dict[str, str]) -> bool:
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos]
            expected = {f'{ID}-{version}/{path[len(PREFIX):]}': digest for path, digest in files.items()}
            if len(names) != len(expected) or set(names) != set(expected):
                return False
            for info in infos:
                if (info.is_dir() or info.flag_bits & 1 or info.file_size > 16 * 1024 * 1024
                        or stat.S_IFMT(info.external_attr >> 16) not in (0, stat.S_IFREG)):
                    return False
                if len(info.filename.split('/')) < 2 or any(part in {'', '.', '..'} for part in info.filename.split('/')):
                    return False
                if _digest(archive.read(info)) != expected[info.filename]:
                    return False
            return True
    except (OSError, zipfile.BadZipFile, KeyError):
        return False


def _build(root: Path, commit: str, version: str, output: Path) -> list[Path]:
    files = _files(root, commit)
    archive = output / f'{ID}-{version}.zip'
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in files:
            info = zipfile.ZipInfo(f'{ID}-{version}/{path[len(PREFIX):]}', (2026, 10, 11, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, _git(root, 'show', f'{commit}:{path}'), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    if not _archive_matches(archive.read_bytes(), version, files):
        raise ValueError('Built hooks archive differs from exact committed source')
    manifest = output / 'source-release-manifest.json'
    manifest.write_text(json.dumps({'release': f'{ID}/v{version}', 'source_commit': commit,
                                    'archive': archive.name, 'sha256': _digest(archive.read_bytes()),
                                    'files': [{'path': path[len(PREFIX):], 'sha256': digest,
                                               'bytes': len(_git(root, 'show', f'{commit}:{path}'))}
                                              for path, digest in files.items()]},
                                   indent=2) + '\n', encoding='utf-8')
    checksums = output / 'SHA256SUMS.txt'
    checksums.write_text(f'{_digest(archive.read_bytes())}  {archive.name}\n'
                         f'{_digest(manifest.read_bytes())}  {manifest.name}\n', encoding='utf-8')
    return [archive, checksums, manifest]


def _asset_rows(release: dict, paths: list[Path]) -> list[dict]:
    by_name = {a['name']: a for a in release['assets']}
    roles = {'SHA256SUMS.txt': 'checksum', 'source-release-manifest.json': 'file-manifest'}
    if set(by_name) != {p.name for p in paths}:
        raise ValueError('Integration release asset inventory differs from intended set')
    return [{'name': p.name, 'role': roles.get(p.name, 'installation'),
             'url': by_name[p.name]['browser_download_url'], 'size': p.stat().st_size,
             'sha256': _digest(p.read_bytes())} for p in paths]


def _verify_companions(raw: dict[str, bytes], version: str, commit: str,
                       files: dict[str, str]) -> None:
    archive_name = f'{ID}-{version}.zip'
    manifest = json.loads(raw['source-release-manifest.json'])
    archive_hash = _digest(raw[archive_name])
    if (manifest.get('release') != f'{ID}/v{version}' or manifest.get('source_commit') != commit
            or manifest.get('archive') != archive_name or manifest.get('sha256') != archive_hash):
        raise ValueError('Hooks release manifest identity differs from exact source')
    entries = manifest.get('files')
    if not isinstance(entries, list) or {PREFIX + x.get('path', ''): x.get('sha256') for x in entries} != files:
        raise ValueError('Hooks release manifest file inventory differs from tag tree')
    expected = f'{archive_hash}  {archive_name}\n{_digest(raw["source-release-manifest.json"])}  source-release-manifest.json\n'
    if raw['SHA256SUMS.txt'] != expected.encode():
        raise ValueError('Hooks checksum file differs from downloaded release bytes')


def _flatten_releases() -> list[dict]:
    return [row for page in list_releases(REPOSITORY) for row in page]


def _publication(entry: dict) -> dict:
    archive = next(asset for asset in entry['assets'] if asset['role'] == 'installation')
    return {'id': ID, 'version': entry['version'], 'source_commit': entry['source_commit'],
            'release_url': entry['release_url'], 'sha256': archive['sha256']}


def _note_relative(root: Path, notes_dir: Path) -> str:
    expected = root / 'catalog/integration-changes'
    if notes_dir.resolve() != expected.resolve():
        raise ValueError('Hooks release notes must live in catalog/integration-changes')
    return f'catalog/integration-changes/{ID}.json'


def _resume_ledger(root: Path, document: dict, product: dict) -> list[dict]:
    """Finish only an interrupted, already published catalog receipt."""
    catalog_status = _git(root, 'status', '--porcelain', '--', CATALOG).decode().strip()
    pending = document.get('completion_receipt')
    if not isinstance(pending, dict):
        if catalog_status:
            raise ValueError('Integration catalog changed without a completion receipt')
        return []
    entry = next((row for row in product['releases'] if row['version'] == pending.get('version')),
                 None)
    if (not entry or pending.get('product_id') != ID
            or pending.get('source_commit') != entry['source_commit']
            or product['source_commit'] != entry['source_commit']):
        raise ValueError('Integration completion receipt disagrees with release ledger')
    if catalog_status:
        staged = _git(root, 'diff', '--cached', '--name-only').decode().splitlines()
        note_relative = f'catalog/integration-changes/{ID}.json'
        if any(path not in {CATALOG, note_relative} for path in staged):
            raise ValueError('Unrelated staged changes prevent scoped integration ledger recovery')
        head = _git(root, 'rev-parse', 'HEAD').decode().strip()
        if head != entry['source_commit']:
            raise ValueError('Dirty integration ledger is not based on its release source commit')
        with tempfile.TemporaryDirectory(prefix='hooks-recovery-') as tmp:
            paths = _build(root, head, entry['version'], Path(tmp))
            release = publish(REPOSITORY, {'id': ID, 'version': entry['version'],
                                           'git_tag': entry['git_tag']},
                              head, paths, notes=entry['notes'], title=f'Optional Codex host hooks {entry["version"]}')
            if release.get('body') != entry['notes']:
                raise ValueError('Recovered hooks release notes differ from ledger')
        _git(root, 'add', '--', CATALOG, note_relative)
        subprocess.check_call(['git', 'commit', '--only', '-m', f'Record {ID} {entry["version"]}',
                               '--', CATALOG, note_relative], cwd=root)
    # A completed ledger commit may still be local after its push failed.
    head = _git(root, 'rev-parse', 'HEAD').decode().strip()
    subject = _git(root, 'log', '-1', '--format=%s').decode().strip()
    if subject != f'Record {ID} {entry["version"]}':
        return []
    _git(root, 'fetch', 'origin', 'main')
    remote = _git(root, 'rev-parse', 'origin/main').decode().strip()
    if remote == head:
        return []
    allowed = {CATALOG, f'catalog/integration-changes/{ID}.json'}
    pending_paths = set(_git(root, 'diff', '--name-only', remote, head).decode().splitlines())
    if (_git(root, 'rev-list', '--count', f'{remote}..{head}').decode().strip() != '1'
            or pending_paths != allowed):
        raise ValueError('Pending integration ledger push includes unrelated changes')
    subprocess.check_call(['git', 'merge-base', '--is-ancestor', remote, head], cwd=root)
    _git(root, 'push', 'origin', f'{head}:refs/heads/main')
    return [_publication(entry)]


def complete(root: Path, notes_dir: Path) -> list[dict]:
    """Complete a committed hooks source change; unchanged baseline returns [].

    A failed publish leaves the old ledger in place. Re-running against the
    same source commit resumes an existing draft or verifies published bytes.
    """
    root, notes_dir = Path(root), Path(notes_dir)
    note_relative = _note_relative(root, notes_dir)
    document, product = _load(root)
    baseline = product['source_commit']
    head = _git(root, 'rev-parse', 'HEAD').decode().strip()
    subprocess.check_call(['git', 'merge-base', '--is-ancestor', baseline, head], cwd=root)
    if _git(root, 'status', '--porcelain', '--', PREFIX).strip():
        raise ValueError('Hooks source must be committed before completion')
    current = _files(root, head)
    changes = []
    for path in sorted(set(current) | set(product['source_files'])):
        old, new = product['source_files'].get(path), current.get(path)
        if old != new:
            changes.append({'path': path, 'status': 'added' if old is None else 'removed' if new is None else 'modified'})
    if not changes:
        return _resume_ledger(root, document, product)
    if _git(root, 'status', '--porcelain', '--', CATALOG).strip():
        raise ValueError('Integration catalog has unrelated local changes; reconcile it first')
    note_path = root / note_relative
    if not note_path.is_file():
        raise ValueError('Specific authored hooks release note missing')
    note = json.loads(note_path.read_text(encoding='utf-8'))
    required = ('summary', 'why', 'notes', 'compatibility', 'upgrade_guidance', 'validation', 'source_review')
    if (note.get('product_id') != ID or note.get('source_commit') != head
            or note.get('changed_files') != [row['path'] for row in changes]
            or any(not isinstance(note.get(k), str) or not note[k].strip() for k in required)):
        raise ValueError('Hooks note must match exact source commit and sorted changed files')
    if (set(current) != set(product['source_files']) and note.get('approved_source_files') != sorted(current)):
        raise ValueError('Added or removed hooks file requires an exact approved file inventory')
    version = propose_version(product['version'], changes, change_level=note.get('level'),
                              existing_versions=[row['version'] for row in product['releases']])
    SemVer(version)
    readme = _git(root, 'show', f'{head}:{PREFIX}README.md').decode()
    if f'codex-host-hooks/v{version}' not in readme or f'codex-host-hooks-{version}.zip' not in readme:
        raise ValueError('Committed README download instructions must name the proposed exact version')
    with tempfile.TemporaryDirectory(prefix='hooks-release-') as tmp:
        paths = _build(root, head, version, Path(tmp))
        _git(root, 'fetch', 'origin', 'main')
        remote = _git(root, 'rev-parse', 'origin/main').decode().strip()
        subprocess.check_call(['git', 'merge-base', '--is-ancestor', remote, head], cwd=root)
        unpublished_paths = _git(root, 'diff', '--name-only', remote, head).decode().splitlines()
        if not unpublished_paths or any(not path.startswith(PREFIX) for path in unpublished_paths):
            raise ValueError('Unpushed source commits include paths outside the reviewed hooks pack')
        _git(root, 'push', 'origin', f'{head}:refs/heads/main')
        tag = f'{ID}/v{version}'
        release = publish(REPOSITORY, {'id': ID, 'version': version, 'git_tag': tag},
                          head, paths, notes=note['notes'], title=f'Optional Codex host hooks {version}')
        if release.get('body') != note['notes']:
            raise ValueError('Published hooks notes differ from authored note')
        entry = {'version': version, 'git_tag': tag, 'source_commit': head,
                 'published_at': release['published_at'], 'release_url': release['html_url'],
                 'summary': note['summary'], 'notes': note['notes'], 'notes_provenance': 'specific authored release note',
                 'why': note['why'],
                 'compatibility': note['compatibility'], 'upgrade_guidance': note['upgrade_guidance'],
                 'validation': note['validation'], 'source_review': note['source_review'],
                 'source_files': current, 'assets': _asset_rows(release, paths)}
        product['version'], product['source_commit'], product['source_files'] = version, head, current
        product['compatibility'], product['upgrade_guidance'] = note['compatibility'], note['upgrade_guidance']
        product['releases'].append(entry)
        document['completion_receipt'] = {'product_id': ID, 'version': version,
                                          'source_commit': head}
        catalog_path = root / CATALOG
        catalog_path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        _git(root, 'add', '--', CATALOG, note_relative)
        subprocess.check_call(['git', 'commit', '--only', '-m', f'Record {ID} {version}',
                               '--', CATALOG, note_relative], cwd=root)
        ledger_commit = _git(root, 'rev-parse', 'HEAD').decode().strip()
        _git(root, 'push', 'origin', f'{ledger_commit}:refs/heads/main')
        return [_publication(entry)]


def history_products(root: Path, *, releases=None, asset_fetcher=None, tag_resolver=None) -> list[dict]:
    """Import every matching GitHub release and prove its ZIP equals the tag tree."""
    root = Path(root)
    _, product = _load(root)
    release_rows = releases if releases is not None else _flatten_releases()
    matching = [row for row in release_rows if TAG.fullmatch(row.get('tag_name', ''))]
    if not matching:
        raise ValueError('GitHub returned no hooks pack releases')
    known = {row['git_tag']: row for row in product['releases']}
    records = []
    for row in matching:
        tag = row['tag_name']
        version = TAG.fullmatch(tag).group(1)
        SemVer(version)
        commit = tag_resolver(tag) if tag_resolver else resolved_tag(REPOSITORY, tag)
        if not re.fullmatch(r'[0-9a-f]{40}', commit):
            raise ValueError(f'{tag}: unresolved exact tag commit')
        files = _files(root, commit)
        if tag in known and (known[tag]['source_commit'] != commit or known[tag]['source_files'] != files):
            raise ValueError(f'{tag}: immutable source differs from integration ledger')
        assets = row.get('assets', [])
        expected_names = {f'{ID}-{version}.zip', 'SHA256SUMS.txt', 'source-release-manifest.json'}
        if {asset.get('name') for asset in assets} != expected_names:
            raise ValueError(f'{tag}: incomplete integration asset set')
        verified, raw_assets = [], {}
        for asset in assets:
            raw = asset_fetcher(asset) if asset_fetcher else publisher_run(
                'gh', 'api', '-H', 'Accept: application/octet-stream', asset['url'])
            digest = _digest(raw)
            if (len(raw) != asset['size'] or asset.get('digest') != 'sha256:' + digest):
                raise ValueError(f'{tag}: asset bytes differ from GitHub digest')
            if asset['name'].endswith('.zip') and not _archive_matches(raw, version, files):
                raise ValueError(f'{tag}: installation archive differs from exact tagged source')
            raw_assets[asset['name']] = raw
            verified.append({'name': asset['name'],
                             'role': 'installation' if asset['name'].endswith('.zip') else
                                     'checksum' if asset['name'] == 'SHA256SUMS.txt' else 'file-manifest',
                             'url': asset['browser_download_url'], 'size': asset['size'], 'sha256': digest})
        _verify_companions(raw_assets, version, commit, files)
        prior = known.get(tag, {})
        record = {'release_key': tag, 'product_id': ID, 'version': version, 'git_tag': tag,
                  'source_commit': commit, 'published_at': row.get('published_at') or row.get('created_at'),
                  'release_url': row['html_url'], 'channel': 'draft' if row.get('draft') else
                  'prerelease' if row.get('prerelease') or SemVer(version).prerelease else 'stable',
                  'distribution_status': 'draft' if row.get('draft') else 'available',
                  'summary': prior.get('summary') or row.get('name') or f'{ID} {version}',
                  'notes': row.get('body') or prior.get('notes') or 'Published integration release.',
                  'notes_provenance': prior.get('notes_provenance') or 'GitHub release body',
                  'compatibility': prior.get('compatibility') or product['compatibility'],
                  'upgrade_guidance': prior.get('upgrade_guidance') or product['upgrade_guidance'],
                  'assets': verified,
                  'verification': {'archive_verified': True, 'layout_verified': True}}
        records.append(record)
    eligible = [r for r in records if r['channel'] == 'stable' and r['distribution_status'] == 'available']
    current = max(eligible, key=lambda r: SemVer(r['version'])) if eligible else None
    return [{'id': ID, 'name': product['name'], 'kind': 'integration',
             'repository': product['repository'], 'compatibility': product['compatibility'],
             'upgrade_guidance': product['upgrade_guidance'],
             'current_release_key': current['release_key'] if current else None,
             'releases': sorted(records, key=lambda r: SemVer(r['version']), reverse=True)}]
