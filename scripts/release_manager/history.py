"""Import every GitHub release page and verify exact tagged package assets."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from urllib.parse import quote
import zipfile

from .inventory import expected_package_files


def _gh(args: list[str]) -> bytes:
    return subprocess.check_output(['gh', 'api', *args])


def _json(runner, endpoint: str):
    raw = runner([endpoint])
    return json.loads(raw.decode() if isinstance(raw, bytes) else raw)


def _asset_bytes(asset: dict, runner, owner: str, repository: str) -> bytes:
    return runner([f'repos/{owner}/{repository}/releases/assets/{asset["id"]}',
                   '-H', 'Accept: application/octet-stream'])


def _role(product_id: str, version: str, name: str) -> str:
    if name == f'{product_id}-{version}.zip':
        return 'installation'
    if name == f'{product_id}-{version}.files.json':
        return 'file-manifest'
    if name in {'SHA256SUMS', 'sha256sums.txt'} or name.endswith('.sha256'):
        return 'checksum'
    return 'companion'


def _remote_tree(owner, repository, commit, product_id, runner):
    response = _json(runner, f'repos/{owner}/{repository}/git/trees/{commit}?recursive=1')
    if response.get('truncated') is not False or not isinstance(response.get('tree'), list):
        raise ValueError(f'{commit}: incomplete GitHub tree response')
    prefix = f'plugins/{product_id}/'
    result = {}
    for row in response['tree']:
        path = row.get('path', '')
        if not path.startswith(prefix):
            continue
        if row.get('type') != 'blob' or row.get('mode') not in {'100644', '100755'}:
            raise ValueError(f'{commit}: unsupported package tree entry {path}')
        relative = path[len(prefix):]
        parts = relative.split('/')
        if (not relative or any(part in {'.git', '.venv', '__pycache__', '.pytest_cache'} for part in parts)
                or parts[-1] == '.DS_Store' or parts[-1].endswith(('.pyc', '.pyo'))):
            continue
        result[relative] = row['sha']
    if not result:
        raise ValueError(f'{commit}: no package files in remote tree')
    return result


def _manifest_from_remote_tree(archive, tree):
    """Prove ZIP member bytes equal each Git blob without fetching every blob."""
    from scripts.release_archive import MAX_FILE_UNCOMPRESSED_BYTES, MAX_TOTAL_UNCOMPRESSED_BYTES
    files = {}
    with zipfile.ZipFile(archive) as zf:
        infos = zf.infolist()
        if len(infos) != len(tree) or len(infos) > 100000:
            raise ValueError('archive file count differs from exact commit tree')
        if sum(info.file_size for info in infos) > MAX_TOTAL_UNCOMPRESSED_BYTES:
            raise ValueError('archive exceeds total uncompressed size limit')
        if {info.filename for info in infos} != set(tree):
            raise ValueError('archive file paths differ from exact commit tree')
        for info in infos:
            if info.file_size > MAX_FILE_UNCOMPRESSED_BYTES:
                raise ValueError(f'archive member too large: {info.filename}')
            data = zf.read(info)
            if len(data) != info.file_size:
                raise ValueError(f'archive member size mismatch: {info.filename}')
            oid = hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()
            if oid != tree[info.filename]:
                raise ValueError(f'archive member differs from exact commit: {info.filename}')
            files[info.filename] = hashlib.sha256(data).hexdigest()
    return files


def _supported_layout(archive, expected, product_id, version):
    root_manifest = 'plugin.json' if 'plugin.json' in expected else 'plugin.portable.json'
    required = (root_manifest, '.codex-plugin/plugin.json', '.claude-plugin/plugin.json', 'README.md')
    if not all(path in expected for path in required):
        return False
    try:
        with zipfile.ZipFile(archive) as zf:
            for path in required[:3]:
                manifest = json.loads(zf.read(path))
                if manifest.get('name') != product_id or manifest.get('version') != version:
                    return False
    except (ValueError, KeyError, zipfile.BadZipFile):
        return False
    return True


def _prior_asset(previous, asset):
    """Reuse verified bytes only when immutable GitHub metadata still agrees."""
    checks = previous.get('verification', {}) if previous else {}
    if checks.get('archive_verified') is not True or checks.get('layout_verified') is not True:
        return None
    digest = asset.get('digest')
    if not isinstance(digest, str) or not digest.startswith('sha256:'):
        return None
    matches = [old for old in previous.get('assets', [])
               if old.get('name') == asset.get('name')
               and old.get('url') == asset.get('browser_download_url')
               and old.get('size') == asset.get('size')
               and 'sha256:' + old.get('sha256', '') == digest]
    return matches[0] if len(matches) == 1 else None


def import_history(owner: str, repository: str, *, repo_path: Path,
                   runner=None, asset_fetcher=None, package_ids=None,
                   cache_dir: Path | None = None, previous_releases=()) -> list[dict]:
    """Return complete historical entries; any API/page failure raises.

    Download every new or changed asset to calculate actual bytes. A prior
    verified asset may be reused only when exact tag commit and GitHub digest,
    URL, size and name still match. Installation ZIP bytes are verified against
    the exact tag's source tree and existing archive checker. The caller should
    replace/merge a stored catalog only after this returns.
    """
    runner = runner or _gh
    if asset_fetcher is None:
        def asset_fetcher(asset):
            cache_key = f'{asset["id"]}-{hashlib.sha256(asset["name"].encode()).hexdigest()[:16]}.asset'
            cache_path = Path(cache_dir)/cache_key if cache_dir is not None else None
            expected = asset.get('digest', '').removeprefix('sha256:')
            if cache_path is not None and cache_path.is_file():
                cached = cache_path.read_bytes()
                if len(cached) == asset['size'] and (not expected or hashlib.sha256(cached).hexdigest() == expected):
                    return cached
            downloaded = _asset_bytes(asset, runner, owner, repository)
            if cache_path is not None:
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                cache_path.write_bytes(downloaded)
            return downloaded
    releases, page = [], 1
    while True:
        rows = _json(runner, f'repos/{owner}/{repository}/releases?per_page=100&page={page}')
        if not isinstance(rows, list):
            raise ValueError(f'GitHub releases page {page} was not an array')
        releases.extend(rows)
        if len(rows) < 100:
            break
        page += 1
        if page > 1000:
            raise ValueError('GitHub release pagination exceeded 1000 pages')
    if not releases:
        raise ValueError('GitHub returned no releases; refusing to replace catalog')
    release_ids=[row.get('id') for row in releases]
    if len(release_ids)!=len(set(release_ids)):
        raise ValueError('GitHub release pagination returned duplicate IDs; retry a stable snapshot')
    previous_by_key = {row['release_key']: row for row in previous_releases}
    results = []
    archive_module = __import__('scripts.release_archive', fromlist=['verify_archive'])
    for release in releases:
        tag = release['tag_name']
        if '/v' not in tag:
            continue
        product_id, version = tag.rsplit('/v', 1)
        if package_ids is not None and product_id not in package_ids:
            continue
        from .catalog import SemVer
        parsed = SemVer(version)
        # GitHub's commit endpoint dereferences both lightweight and annotated tags.
        commit_data = _json(runner, f'repos/{owner}/{repository}/commits/{quote(tag, safe="")}')
        commit = commit_data['sha']
        if not isinstance(commit,str) or len(commit) != 40 or any(char not in '0123456789abcdef' for char in commit):
            raise ValueError(f'{tag}: unresolved source commit')
        assets = []
        installation_bytes = None
        asset_unavailable = False
        previous = previous_by_key.get(tag)
        if previous and previous.get('source_commit') != commit:
            previous = None
        reused_installation = False
        for asset in release.get('assets', []):
            prior_asset = _prior_asset(previous, asset)
            if prior_asset is not None:
                data = None
                digest = prior_asset['sha256']
            else:
                try:
                    data = asset_fetcher(asset)
                except (OSError, RuntimeError, subprocess.CalledProcessError):
                    advertised = asset.get('digest', '')
                    if not advertised.startswith('sha256:') or len(advertised) != 71:
                        raise
                    digest = advertised.removeprefix('sha256:')
                    if any(c not in '0123456789abcdef' for c in digest):
                        raise ValueError(f'{tag}: malformed GitHub asset digest')
                    data = None
                    asset_unavailable = True
                else:
                    if not isinstance(data, bytes):
                        raise TypeError(f'{tag}: asset fetcher must return bytes')
                    if len(data) != asset['size']:
                        raise ValueError(f'{tag}: asset {asset["name"]} size differs from GitHub metadata')
                    digest = hashlib.sha256(data).hexdigest()
                    advertised = asset.get('digest', '')
                    if advertised and advertised != 'sha256:' + digest:
                        raise ValueError(f'{tag}: asset {asset["name"]} differs from GitHub digest')
            role = _role(product_id, version, asset['name'])
            assets.append({'role': role, 'name': asset['name'], 'url': asset['browser_download_url'],
                           'size': asset['size'], 'sha256': digest})
            if role == 'installation':
                installation_bytes = data
                reused_installation = prior_asset is not None
        archive_verified = False
        layout_verified = False
        verification_reason = ""
        if reused_installation:
            archive_verified = True
            layout_verified = True
        if installation_bytes is not None:
            with tempfile.TemporaryDirectory(prefix='working-tools-release-') as directory:
                archive = Path(directory)/f'{product_id}-{version}.zip'
                archive.write_bytes(installation_bytes)
                try:
                    expected = expected_package_files(repo_path, commit, product_id)
                except (subprocess.CalledProcessError, ValueError):
                    tree = _remote_tree(owner, repository, commit, product_id, runner)
                    expected = _manifest_from_remote_tree(archive, tree)
                result = archive_module.verify_archive(archive, expected, hashlib.sha256(installation_bytes).hexdigest())
                archive_verified = result['passed']
                if not archive_verified:verification_reason = '; '.join(result.get('errors', []))
                layout_verified = archive_verified and _supported_layout(archive, expected, product_id, version)
        channel = 'draft' if release.get('draft') else ('prerelease' if release.get('prerelease') or parsed.prerelease else 'stable')
        status = ('available' if not asset_unavailable and archive_verified and layout_verified
                  else 'draft' if channel == 'draft' else 'unavailable')
        results.append({
            'release_key': tag, 'product_id': product_id, 'version': version,
            'git_tag': tag, 'source_commit': commit, 'published_at': release.get('published_at') or release.get('created_at'),
            'release_url': release['html_url'], 'channel': channel,
            'distribution_status': status, 'summary': release.get('name') or tag,
            'notes': release.get('body') or 'No published notes recorded.',
            'notes_provenance': f'github-release:{release["id"]}', 'assets': assets,
            'compatibility': 'See package documentation at this tag.',
            'upgrade_guidance': 'Review the tagged package README before upgrading.',
            'verification': {'archive_verified': archive_verified, 'layout_verified': layout_verified,
                             **({'reason': verification_reason} if verification_reason else {})},
        })
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-path', type=Path, required=True)
    parser.add_argument('--owner', default='JonathanKHobson')
    parser.add_argument('--repository', default='working-tools-plugins')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--cache-dir', type=Path)
    parser.add_argument('--product-id', action='append')
    args = parser.parse_args(argv)
    ids = set(args.product_id) if args.product_id else None
    rows = import_history(args.owner, args.repository, repo_path=args.repo_path,
                          package_ids=ids, cache_dir=args.cache_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # A failed import never truncates a previous complete history file.
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=args.output.parent,
                                     prefix=args.output.name + '.', suffix='.tmp', delete=False) as stream:
        json.dump(rows, stream, indent=2, ensure_ascii=False)
        stream.write('\n')
        temporary = Path(stream.name)
    temporary.replace(args.output)
    print(json.dumps({'imported': len(rows), 'output': str(args.output)}))


if __name__ == '__main__':
    main()
