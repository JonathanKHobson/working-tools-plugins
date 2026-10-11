"""Read and compare separately hosted historical downloads.

This inventory is deliberately outside the current plugin registry. A listed
download is evidence of an existing public artifact, never permission to copy
private source, create a tag, or promote it into the current storefront.
"""

from __future__ import annotations

import json
import hashlib
import io
import re
import stat
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen
from zipfile import BadZipFile, ZipFile

SCHEMA_VERSION = 'working-tools.external-products.v1'
_ID = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
_SHA = re.compile(r'[0-9a-f]{40}\Z')
_SHA256 = re.compile(r'[0-9a-f]{64}\Z')
_KINDS = {'plugin', 'desktop-extension', 'skill', 'source-archive', 'bundle', 'guide'}
_VERSIONS = {'semver', 'tag', 'revision', 'unversioned'}
_LIFECYCLES = {'active-guide-download', 'active-guide-page', 'frozen-legacy'}
_ROUTES = {'shareables-authoring', 'what-is-an-mcp-source', 'frozen-history'}


def _matches(pattern, value) -> bool:
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def _relative(path: str) -> bool:
    return (isinstance(path, str) and bool(path) and not path.startswith('/')
            and '\\' not in path and all(part not in {'', '.', '..'} for part in path.split('/')))


def _https(url: str) -> bool:
    parsed = urlparse(url) if isinstance(url, str) else None
    return bool(parsed and parsed.scheme == 'https' and parsed.hostname and not parsed.username
                and not parsed.password and not parsed.fragment)


def validate_external_products(document: dict) -> list[str]:
    """Return named errors without opening links or reading private source."""
    errors = []
    if not isinstance(document, dict) or document.get('schema_version') != SCHEMA_VERSION:
        return ['schema_version must be working-tools.external-products.v1']
    sources, products = document.get('sources'), document.get('products')
    if not isinstance(sources, dict) or not isinstance(products, list):
        return ['sources object and products array are required']
    for key, source in sources.items():
        if not _matches(_ID, key) or not isinstance(source, dict):
            errors.append('invalid source identity')
            continue
        if not _https(source.get('repository')) or not source['repository'].startswith('https://github.com/'):
            errors.append(f'{key}: source repository must be a public GitHub HTTPS URL')
        if not _matches(_SHA, source.get('commit')):
            errors.append(f'{key}: exact source commit required')
    seen = set()
    for product in products:
        if not isinstance(product, dict):
            errors.append('malformed product')
            continue
        ident = product.get('id', '')
        if not _matches(_ID, ident) or ident in seen:
            errors.append('invalid or duplicate product ID')
            continue
        seen.add(ident)
        if product.get('kind') not in _KINDS or product.get('channel') != 'legacy':
            errors.append(f'{ident}: invalid kind or channel')
        disposition = product.get('disposition')
        if disposition not in {'download', 'page-only'}:
            errors.append(f'{ident}: invalid disposition')
        lifecycle = product.get('lifecycle')
        route = product.get('completion_route')
        if lifecycle not in _LIFECYCLES or route not in _ROUTES:
            errors.append(f'{ident}: explicit lifecycle and completion route required')
        elif (lifecycle == 'active-guide-download' and disposition != 'download'
              or lifecycle == 'active-guide-page' and disposition != 'page-only'
              or lifecycle == 'frozen-legacy' and route != 'frozen-history'
              or lifecycle != 'frozen-legacy' and route == 'frozen-history'
              or route == 'shareables-authoring' and (product.get('source') or {}).get('id') != 'shareables'
              or route == 'what-is-an-mcp-source' and (product.get('source') or {}).get('id') != 'what-is-an-mcp'):
            errors.append(f'{ident}: lifecycle, source and route disagree')
        version = product.get('version')
        if not isinstance(version, dict) or version.get('scheme') not in _VERSIONS:
            errors.append(f'{ident}: explicit version scheme required')
        elif version['scheme'] in {'unversioned', 'revision'}:
            if version.get('value') is not None:
                errors.append(f'{ident}: do not invent a version from a revision')
        elif not isinstance(version.get('value'), str) or not version['value']:
            errors.append(f'{ident}: named version missing')
        source = product.get('source', {})
        if not isinstance(source, dict) or source.get('id') not in sources:
            errors.append(f'{ident}: unknown source')
        elif source.get('commit') is not None and not _matches(_SHA, source['commit']):
            errors.append(f'{ident}: invalid product source commit')
        elif not isinstance(source.get('files'), list) or not source['files'] or any(not _relative(p) for p in source['files']):
            errors.append(f'{ident}: source files must be exact relative paths')
        elif len(source['files']) != len(set(source['files'])):
            errors.append(f'{ident}: duplicate source file')
        assets = product.get('assets')
        if not isinstance(assets, list) or (disposition == 'download' and not assets) or (disposition == 'page-only' and assets):
            errors.append(f'{ident}: asset/disposition mismatch')
            continue
        names = set()
        for asset in assets:
            if not isinstance(asset, dict) or not _relative(asset.get('name')) or '/' in asset['name']:
                errors.append(f'{ident}: invalid asset name')
                continue
            if asset['name'] in names:
                errors.append(f'{ident}: duplicate asset name')
            names.add(asset['name'])
            if not _https(asset.get('url')) or not isinstance(asset.get('role'), str) or not asset['role']:
                errors.append(f'{ident}: invalid asset URL or role')
            digest = asset.get('sha256')
            blob = asset.get('git_blob_sha1')
            if digest is not None and not _matches(_SHA256, digest):
                errors.append(f'{ident}: invalid SHA256')
            if blob is not None and not _matches(_SHA, blob):
                errors.append(f'{ident}: invalid Git blob SHA1')
            if digest is None and blob is None:
                errors.append(f'{ident}: asset has no immutable digest')
            if asset.get('verification') not in {'release-checksum', 'public-source-bytes', 'git-blob-only', 'public-download-bytes'}:
                errors.append(f'{ident}: invalid verification level')
            if asset.get('verification') == 'public-download-bytes' and (digest is None or not asset.get('verified_at')):
                errors.append(f'{ident}: public download requires SHA256 and verification time')
            if asset.get('fixed_url') is not None and not _https(asset['fixed_url']):
                errors.append(f'{ident}: invalid fixed source URL')
            if asset.get('original_url') is not None and not _https(asset['original_url']):
                errors.append(f'{ident}: invalid original Pages URL')
        members = product.get('members', [])
        if not isinstance(members, list) or not all(_matches(_ID, x) for x in members):
            errors.append(f'{ident}: malformed bundle members')
        history = product.get('historical_releases', [])
        latest_release = product.get('latest_release')
        if latest_release is not None and (
                not isinstance(latest_release, dict)
                or not isinstance(latest_release.get('tag'), str) or not latest_release['tag']
                or not _https(latest_release.get('release_url'))
                or not isinstance(latest_release.get('published_at'), str)
                or not _matches(_SHA256, latest_release.get('notes_sha256'))
                or any(not isinstance(latest_release.get(key), str) or not latest_release[key].strip()
                       for key in ('summary', 'why', 'compatibility', 'upgrade_guidance',
                                   'validation', 'release_notes'))):
            errors.append(f'{ident}: invalid latest release receipt')
        if not isinstance(history, list):
            errors.append(f'{ident}: historical_releases must be an array')
        else:
            tags = set()
            for release in history:
                if not isinstance(release, dict) or not isinstance(release.get('tag'), str) or not release['tag']:
                    errors.append(f'{ident}: malformed historical release')
                    continue
                if release['tag'] in tags:
                    errors.append(f'{ident}: duplicate historical tag')
                tags.add(release['tag'])
                if not _matches(_SHA, release.get('source_commit')):
                    errors.append(f'{ident}: historical release requires exact commit')
                if release.get('version_scheme') not in {'semver', 'tag'} or not release.get('version'):
                    errors.append(f'{ident}: historical release requires recorded version')
                if not isinstance(release.get('source_files'), list) or any(not _relative(p) for p in release['source_files']):
                    errors.append(f'{ident}: invalid historical source files')
                if not _https(release.get('release_url')) or not _matches(_SHA256, release.get('notes_sha256')):
                    errors.append(f'{ident}: missing release URL or notes hash')
                if release.get('release_notes') is not None and (
                        not isinstance(release['release_notes'], str)
                        or hashlib.sha256(release['release_notes'].encode()).hexdigest() != release.get('notes_sha256')):
                    errors.append(f'{ident}: historical release notes differ from digest')
                verification = release.get('verification')
                if not isinstance(verification, dict) or type(verification.get('download_verified')) is not bool or not verification.get('provenance'):
                    errors.append(f'{ident}: invalid historical verification')
                if not isinstance(release.get('assets'), list) or not release['assets']:
                    errors.append(f'{ident}: historical release lacks assets')
                    continue
                for old_asset in release['assets']:
                    if not _https(old_asset.get('url')) or not _matches(_SHA256, old_asset.get('sha256')):
                        errors.append(f'{ident}: historical asset lacks URL or SHA256')
                    if type(old_asset.get('size')) is not int or old_asset['size'] <= 0:
                        errors.append(f'{ident}: historical asset lacks positive size')
                    if old_asset.get('verification') not in {'github-asset-digest', 'public-download-bytes'}:
                        errors.append(f'{ident}: invalid historical asset verification')
                    if isinstance(verification, dict) and verification.get('download_verified') is True:
                        if old_asset.get('verification') != 'public-download-bytes' or not old_asset.get('verified_at'):
                            errors.append(f'{ident}: verified historical download lacks byte receipt')
    for product in products:
        if isinstance(product, dict):
            for member in product.get('members', []):
                if member not in seen:
                    errors.append(f"{product.get('id')}: missing bundle member {member}")
    return errors


def load_external_products(path: str | Path) -> dict:
    document = json.loads(Path(path).read_text(encoding='utf-8'))
    errors = validate_external_products(document)
    if errors:
        raise ValueError('\n'.join(errors))
    return document


def changed_external_products(document: dict, checkouts: dict[str, str | Path], *, runner=None,
                              require_all: bool = True) -> dict[str, list[str]]:
    """Compare each pinned public source commit with its checkout HEAD.

    Only registered exact paths count. Missing checkouts are an error, not a
    reason to report all products as changed. The caller decides whether a
    change warrants review; this function never chooses or publishes a version.
    """
    errors = validate_external_products(document)
    if errors:
        raise ValueError('\n'.join(errors))
    needed = {p['source']['id'] for p in document['products']}
    for source_id in sorted(needed):
        if require_all and source_id not in checkouts:
            raise ValueError(f'missing checkout for {source_id}')
    result = {}
    for product in document['products']:
        source = product['source']
        source_id = source['id']
        if source_id not in checkouts:
            continue
        base = source.get('commit', document['sources'][source_id]['commit'])
        checkout = Path(checkouts[source_id])
        args = ['git', 'diff', '--name-only', '--no-renames', base, 'HEAD', '--', *source['files']]
        raw = runner(source_id, checkout, args) if runner else subprocess.check_output(args, cwd=checkout)
        changed = sorted(set((raw.decode() if isinstance(raw, bytes) else raw).splitlines()).intersection(source['files']))
        if changed:
            result[product['id']] = changed
    return result


def plan_active_external_updates(document: dict, checkouts: dict[str, str | Path],
                                 notes_dir: str | Path, *, runner=None) -> dict:
    """Validate a completed guide change before its owning publisher runs.

    This is a handoff gate, not a GitHub/Sites publisher or a version allocator.
    A durable, product-specific note must match the exact public source commit
    and changed registered paths. The caller publishes through the owning guide
    workflow, verifies live bytes, then advances this ledger's pinned commit.
    """
    changes = changed_external_products(document, checkouts, runner=runner, require_all=False)
    products = {p['id']: p for p in document['products']}
    result = {'ready': [], 'needs_notes': [], 'frozen_differences': []}
    for ident, paths in sorted(changes.items()):
        product = products[ident]
        if product['lifecycle'] == 'frozen-legacy':
            result['frozen_differences'].append({'product_id': ident, 'changed_files': paths})
            continue
        source_id = product['source']['id']
        checkout = Path(checkouts[source_id])
        command = ['git', 'rev-parse', 'HEAD']
        raw = runner(source_id, checkout, command) if runner else subprocess.check_output(command, cwd=checkout)
        head = (raw.decode() if isinstance(raw, bytes) else raw).strip()
        if not _matches(_SHA, head):
            raise ValueError(f'{ident}: exact source HEAD could not be resolved')
        command = ['git', 'status', '--porcelain', '--', *product['source']['files']]
        raw = runner(source_id, checkout, command) if runner else subprocess.check_output(command, cwd=checkout)
        if (raw.decode() if isinstance(raw, bytes) else raw).strip():
            raise ValueError(f'{ident}: registered source files are not committed')
        note_path = Path(notes_dir) / f'{ident}.json'
        if not note_path.is_file():
            result['needs_notes'].append({'product_id': ident, 'source_commit': head,
                                          'changed_files': paths, 'note': note_path.name})
            continue
        note = json.loads(note_path.read_text(encoding='utf-8'))
        required = ('summary', 'why', 'compatibility', 'upgrade_guidance', 'validation',
                    'release_notes', 'authoring_provenance')
        if (not isinstance(note, dict) or note.get('product_id') != ident
                or note.get('source_commit') != head or note.get('changed_files') != paths
                or any(not isinstance(note.get(key), str) or not note[key].strip() for key in required)):
            raise ValueError(f'{ident}: authored note must identify the product, exact commit and files, '
                             'with specific rationale, compatibility, validation, provenance and release notes')
        result['ready'].append({
            'product_id': ident, 'lifecycle': product['lifecycle'],
            'completion_route': product['completion_route'],
            'source_repository': document['sources'][source_id]['repository'],
            'base_commit': product['source'].get('commit', document['sources'][source_id]['commit']),
            'source_commit': head, 'changed_files': paths, 'note': note_path.name,
            'disposition': product['disposition'],
        })
    return result


def _git_bytes(checkout: Path, commit: str, path: str) -> bytes:
    return subprocess.check_output(['git', 'show', f'{commit}:{path}'], cwd=checkout)


def _check_install_archive(name: str, data: bytes) -> None:
    if not name.endswith(('.zip', '.skill')):
        return
    try:
        with ZipFile(io.BytesIO(data)) as archive:
            names = archive.namelist()
            if not names or len(names) != len(set(names)):
                raise ValueError(f'{name}: archive empty or contains duplicate paths')
            usable = 0
            for item in archive.infolist():
                path = item.filename
                parts = path.rstrip('/').split('/')
                if (not path or path.startswith('/') or '\\' in path or
                        any(part in {'', '.', '..'} for part in parts) or
                        stat.S_IFMT(item.external_attr >> 16) == stat.S_IFLNK):
                    raise ValueError(f'{name}: unsafe archive member')
                if not item.is_dir():
                    usable += 1
                    archive.read(item)
            if not usable:
                raise ValueError(f'{name}: no installable files')
    except BadZipFile as exc:
        raise ValueError(f'{name}: invalid installation archive') from exc


def _release_assets(release: dict, paths: list[Path], verified_at: str) -> list[dict]:
    by_name = {asset['name']: asset for asset in release['assets']}
    return [{'name': path.name, 'url': by_name[path.name]['browser_download_url'],
             'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'size': path.stat().st_size,
             'verification': 'public-download-bytes', 'verified_at': verified_at}
            for path in paths]


def complete_active_external_update(document: dict, product_id: str, checkout: str | Path,
                                    notes_dir: str | Path, *, branch: str = 'main',
                                    publish=None, fetch_bytes=None, git=None, sleep=None) -> dict:
    """Publish one reviewed guide revision and return its updated ledger.

    The source checkout is the owning public repo. Shareables also requires the
    note's private authoring provenance. The caller persists the returned
    ledger only after exact Pages byte verification succeeds. Existing public
    links remain on Pages; immutable release URLs enter the ledger.
    """
    from .publisher import publish as default_publish

    errors = validate_external_products(document)
    if errors:
        raise ValueError('\n'.join(errors))
    product = next((p for p in document['products'] if p['id'] == product_id), None)
    if product is None or product['lifecycle'] not in {'active-guide-download', 'active-guide-page'}:
        raise ValueError('Only registered active guide products may complete')
    source_id = product['source']['id']
    source = document['sources'][source_id]
    checkout = Path(checkout)
    def run(*args):
        return git(*args, cwd=checkout) if git else subprocess.check_output(args, cwd=checkout)
    origin = run('git', 'remote', 'get-url', 'origin').decode().strip()
    repo = source['repository'].removeprefix('https://github.com/').removesuffix('.git')
    if origin.removesuffix('.git') not in {source['repository'].removesuffix('.git'), f'git@github.com:{repo}'}:
        raise ValueError(f'{product_id}: checkout origin differs from registered public repository')
    base = product['source'].get('commit', source['commit'])
    head = run('git', 'rev-parse', 'HEAD').decode().strip()
    if not _matches(_SHA, head) or head == base:
        raise ValueError(f'{product_id}: no new exact source commit')
    files = product['source']['files']
    changed = sorted(set(run('git', 'diff', '--name-only', '--no-renames', base, head,
                             '--', *files).decode().splitlines()).intersection(files))
    if not changed:
        raise ValueError(f'{product_id}: no registered distribution file changed')
    if run('git', 'status', '--porcelain', '--', *files).strip():
        raise ValueError(f'{product_id}: registered source files are not committed')
    note_path = Path(notes_dir) / f'{product_id}.json'
    if not note_path.is_file():
        raise ValueError(f'{product_id}: durable authored note missing')
    note = json.loads(note_path.read_text(encoding='utf-8'))
    required = ('summary', 'why', 'compatibility', 'upgrade_guidance', 'validation',
                'release_notes', 'authoring_provenance')
    if (not isinstance(note, dict) or note.get('product_id') != product_id
            or note.get('source_commit') != head or note.get('changed_files') != changed
            or any(not isinstance(note.get(key), str) or not note[key].strip() for key in required)):
        raise ValueError(f'{product_id}: authored note does not match exact revision and change')
    if not branch or '/' in branch or not re.fullmatch(r'[A-Za-z0-9._-]+', branch):
        raise ValueError('Explicit simple source branch required')
    run('git', 'fetch', 'origin', branch)
    remote = run('git', 'rev-parse', f'origin/{branch}').decode().strip()
    run('git', 'merge-base', '--is-ancestor', remote, head)
    now = datetime.now(timezone.utc).isoformat()
    publisher = publish or default_publish
    downloader = fetch_bytes or (lambda url: urlopen(url, timeout=30).read())
    pause = sleep or time.sleep
    old_tag = f'guide-{product_id}-rev-{base[:12]}'
    new_tag = f'guide-{product_id}-rev-{head[:12]}'
    with tempfile.TemporaryDirectory(prefix='external-guide-release-') as tmp:
        old_dir, new_dir = Path(tmp) / 'old', Path(tmp) / 'new'
        old_dir.mkdir(); new_dir.mkdir()
        old_paths, new_paths = [], []
        for path in files:
            old_path, new_path = old_dir / Path(path).name, new_dir / Path(path).name
            old_path.write_bytes(_git_bytes(checkout, base, path))
            new_path.write_bytes(_git_bytes(checkout, head, path))
            _check_install_archive(old_path.name, old_path.read_bytes())
            _check_install_archive(new_path.name, new_path.read_bytes())
            old_paths.append(old_path); new_paths.append(new_path)
        if product['disposition'] == 'download':
            old_by_name = {a['name']: a for a in product['assets']}
            if set(old_by_name) != {p.name for p in old_paths}:
                raise ValueError(f'{product_id}: registered asset/source inventory mismatch')
            for old_path in old_paths:
                if hashlib.sha256(old_path.read_bytes()).hexdigest() != old_by_name[old_path.name]['sha256']:
                    raise ValueError(f'{product_id}: prior source does not match verified public baseline')
            old_notes = ('Preserved verified public guide download before revision. '
                         f'Source commit: {base}. Original page: {product["page_url"]}.')
            old_release = publisher(repo, {'id': product_id, 'version': base, 'git_tag': old_tag},
                                    base, old_paths, notes=old_notes, title=f'{product["name"]} source {base[:12]}')
            previous_notes_hash = (product.get('latest_release') or {}).get('notes_sha256')
            actual_old_notes = old_release.get('body')
            if previous_notes_hash:
                if not isinstance(actual_old_notes, str) or hashlib.sha256(actual_old_notes.encode()).hexdigest() != previous_notes_hash:
                    raise ValueError(f'{product_id}: prior release notes differ from ledger')
            elif actual_old_notes is not None and actual_old_notes != old_notes:
                raise ValueError(f'{product_id}: baseline archive notes collision')
        else:
            old_release = None
        # A fast-forward push updates the existing Pages source without changing paths.
        run('git', 'push', 'origin', f'{head}:refs/heads/{branch}')
        if product['disposition'] == 'download':
            new_release = publisher(repo, {'id': product_id, 'version': head, 'git_tag': new_tag},
                                    head, new_paths, notes=note['release_notes'],
                                    title=f'{product["name"]} source {head[:12]}')
            if new_release.get('body') != note['release_notes']:
                raise ValueError(f'{product_id}: published release notes differ from authored note')
        else:
            new_release = None
        # Pages deployment may lag the source push. A digest match, not an HTTP
        # success alone, closes the public link check.
        asset_by_name = {asset['name']: asset for asset in product['assets']}
        targets = ([(asset_by_name[path.name].get('original_url', asset_by_name[path.name]['url']), path)
                    for path in new_paths]
                   if product['disposition'] == 'download' else [(product['page_url'], new_paths[0])])
        for url, new_path in targets:
            expected = hashlib.sha256(new_path.read_bytes()).hexdigest()
            for attempt in range(6):
                try:
                    if hashlib.sha256(downloader(url + f'?revision={head}')).hexdigest() == expected:
                        break
                except OSError:
                    pass
                if attempt == 5:
                    raise ValueError(f'{product_id}: Pages download did not match committed release bytes')
                pause(5)
        updated = json.loads(json.dumps(document))
        target = next(p for p in updated['products'] if p['id'] == product_id)
        target['source']['commit'] = head
        if product['disposition'] == 'download':
            old_assets = _release_assets(old_release, old_paths, now)
            target.setdefault('historical_releases', []).insert(0, {
                'tag': old_tag, 'version_scheme': 'tag', 'version': old_tag,
                'source_commit': base, 'source_files': files,
                'release_url': old_release['html_url'], 'published_at': old_release['published_at'],
                'notes_sha256': previous_notes_hash or hashlib.sha256(old_notes.encode()).hexdigest(),
                'notes_provenance': ('previous authored release note' if previous_notes_hash
                                     else 'verified prior public snapshot'),
                'release_notes': actual_old_notes if previous_notes_hash else old_notes,
                'summary': (product.get('latest_release') or {}).get('summary', 'Preserved public guide snapshot'),
                'why': (product.get('latest_release') or {}).get('why', 'Keep the earlier installed bytes available'),
                'compatibility': (product.get('latest_release') or {}).get('compatibility', 'Historical snapshot'),
                'upgrade_guidance': (product.get('latest_release') or {}).get('upgrade_guidance', 'Use the newest guide revision for updates'),
                'verification': {'download_verified': True, 'provenance': 'exact release download bytes'},
                'assets': old_assets,
            })
            target['assets'] = [
                {**asset_by_name[new['name']], **new,
                 'original_url': asset_by_name[new['name']].get('original_url', asset_by_name[new['name']]['url'])}
                for new in _release_assets(new_release, new_paths, now)
            ]
            for asset in target['assets']:asset.pop('fixed_url', None)
            target['version'] = {'scheme': 'tag', 'value': new_tag}
            target['latest_release'] = {'tag': new_tag, 'release_url': new_release['html_url'],
                                        'published_at': new_release['published_at'],
                                        'notes_sha256': hashlib.sha256(note['release_notes'].encode()).hexdigest(),
                                        **{key: note[key] for key in required if key!='authoring_provenance'}}
        errors = validate_external_products(updated)
        if errors:
            raise ValueError('\n'.join(errors))
        return updated


def external_release_records(document: dict) -> list[dict]:
    """Project historical downloads into a unified history view.

    `current` is deliberately false for every record. Revision-only guides
    retain null `version`; their exact source commit is the stable identifier.
    """
    errors = validate_external_products(document)
    if errors:
        raise ValueError('\n'.join(errors))
    records = []
    for product in document['products']:
        source = document['sources'][product['source']['id']]
        product_commit = product['source'].get('commit', source['commit'])
        verified = bool(product['assets']) and all(
            asset.get('verification') == 'public-download-bytes' and asset.get('sha256')
            and asset.get('verified_at') for asset in product['assets'])
        latest = {
            'release_key': f"legacy:{product['id']}:{product_commit}",
            'version': product['version']['value'],
            'version_scheme': product['version']['scheme'],
            'source_commit': product_commit,
            'source_repository': source['repository'],
            'source_files': product['source']['files'],
            'distribution_status': 'available' if product['disposition'] == 'download' else 'page-only',
            'verification': {
                'download_verified': bool(verified),
                'provenance': source['role'] + ('; public download SHA256 matched' if verified
                                              else '; live download bytes not fully checked'),
            },
            'assets': [{**a,'url':a.get('fixed_url',a['url'])} for a in product['assets']],
            'bundle_members': product.get('members', []),
            'gaps': product.get('gaps', []),
            'page_url': product.get('page_url'),
        }
        if product.get('latest_release'):
            latest.update({'git_tag': product['latest_release']['tag'],
                           'release_url': product['latest_release']['release_url'],
                           'published_at': product['latest_release']['published_at'],
                           'notes_sha256': product['latest_release']['notes_sha256'],
                           'notes_provenance': 'specific authored guide release note',
                           **{key: product['latest_release'][key] for key in
                              ('summary', 'why', 'compatibility', 'upgrade_guidance',
                               'validation', 'release_notes')}})
        history = []
        for old in product.get('historical_releases', []):
            history.append({
                'release_key': f"legacy:{product['id']}:{old['tag']}",
                'version': old['version'], 'version_scheme': old['version_scheme'],
                'git_tag': old['tag'], 'source_commit': old['source_commit'],
                'source_repository': source['repository'], 'source_files': old['source_files'],
                'published_at': old['published_at'], 'release_url': old['release_url'],
                'notes_sha256': old['notes_sha256'], 'notes_provenance': old['notes_provenance'],
                'release_notes': old.get('release_notes'), 'summary': old.get('summary'),
                'why': old.get('why'), 'compatibility': old.get('compatibility'),
                'upgrade_guidance': old.get('upgrade_guidance'),
                'distribution_status': 'available', 'verification': old['verification'],
                'assets': old['assets'], 'bundle_members': product.get('members', []),
                'gaps': product.get('gaps', []), 'page_url': product.get('page_url'),
            })
        records.append({
            'id': product['id'], 'name': product['name'], 'kind': 'external',
            'product_kind': product['kind'], 'channel': 'legacy',
            'lifecycle': product['lifecycle'], 'completion_route': product['completion_route'],
            'current_release_key': None, 'repository': source['repository'],
            'releases': [latest, *history],
        })
    return records
