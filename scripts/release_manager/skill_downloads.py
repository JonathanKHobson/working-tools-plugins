"""Generate Site-only skill downloads as part of the existing release transaction.

Companion releases preserve old plugin assets. No canonical sources, versions,
installed skills, hooks or private bindings are written by this module.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote

from .inventory import expected_package_files
from .publisher import api, publish, resolved_tag, run

REPOSITORY = 'JonathanKHobson/working-tools-plugins'
SCHEMA = 'working-tools.skill-downloads.v1'
FORMAT = 1


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def current_plugins(history):
    result = []
    for product in history['products']:
        if product.get('kind') != 'plugin':
            continue
        matches = [r for r in product['releases'] if r['release_key'] == product.get('current_release_key')]
        if len(matches) != 1:
            raise ValueError('Missing unique current plugin release: ' + product['id'])
        release = matches[0]
        if (release.get('distribution_status') != 'available'
                or not release.get('verification', {}).get('archive_verified')
                or not release.get('verification', {}).get('layout_verified')):
            raise ValueError('Unverified plugin release: ' + product['id'])
        assets = [a for a in release['assets'] if a['role'] == 'installation']
        if len(assets) != 1:
            raise ValueError('Expected one verified plugin archive')
        result.append((product['id'], release, assets[0]))
    return sorted(result, key=lambda row: row[0])


def _release(tag):
    try:
        return api(REPOSITORY, 'releases/tags/' + quote(tag, safe=''))
    except subprocess.CalledProcessError as exc:
        if b'404' in (exc.stderr or b''):
            return None
        raise


def _asset_proof(release, entries):
    """Re-use immutable downloaded-byte receipts only with matching remote digests."""
    actual = {a['name']: a for a in release['assets']}
    if len(actual) != len(release['assets']) or set(actual) != {a['file'] for a in entries}:
        raise ValueError('Skill release asset inventory changed')
    for row in entries:
        asset = actual[row['file']]
        if (asset.get('state') != 'uploaded' or asset['size'] != row['size']
                or asset.get('digest') != 'sha256:' + row['sha256']
                or asset['browser_download_url'] != row['url']):
            raise ValueError('Skill release asset identity changed: ' + row['file'])


def validate_index(index):
    if index.get('schema_version') != SCHEMA or index.get('format_version') != FORMAT:
        raise ValueError('Unsupported skill download index')
    seen = set()
    for product in index['products']:
        ident = product['id']
        if ident in seen or not re.fullmatch(r'[a-z0-9][a-z0-9-]*', ident):
            raise ValueError('Duplicate or unsafe skill product')
        seen.add(ident)
        if not re.fullmatch('[0-9a-f]{40}', product['source_commit']):
            raise ValueError('Invalid skill source revision')
        skills = product['skills']
        if not skills or len({s['id'] for s in skills}) != len(skills):
            raise ValueError('Missing or duplicate skill identity')
        for row in [*skills, product['manifest'], product['checksums']]:
            if (not re.fullmatch('[0-9a-f]{64}', row['sha256']) or row['size'] < 1
                    or Path(row['file']).name != row['file']
                    or row['url'] != f'https://github.com/{REPOSITORY}/releases/download/{product["tag"]}/{row["file"]}'):
                raise ValueError('Unsafe skill download asset metadata')
    return index


def synchronize(root, history, output=None):
    """Backfill or refresh current plugins; unchanged verified products do no build/upload.

    Called on every normal publish/reconcile before the Site catalog is promoted.
    Failure retains verified checkpoints and resumable GitHub drafts; the Site is not promoted.
    """
    from skill_bundles import build_skill_bundles
    root = Path(root)
    index_path = root / 'catalog/skill-downloads.json'
    previous = validate_index(json.loads(index_path.read_text())) if index_path.is_file() else {'products': []}
    old = {p['id']: p for p in previous['products']}
    output = Path(output or root / 'dist/skill-downloads')
    products = []
    for ident, source, archive in current_plugins(history):
        version, commit = source['version'], source['source_commit']
        tag = f'skill-bundles-v{FORMAT}/{ident}/v{version}'
        existing = _release(tag)
        prior = old.get(ident)
        if prior and prior['tag'] == tag:
            if prior['source_commit'] != commit or prior['plugin_sha256'] != archive['sha256']:
                raise ValueError('Immutable plugin source changed: ' + ident)
            if existing and not existing['draft']:
                if resolved_tag(REPOSITORY, tag) != commit:
                    raise ValueError('Skill companion tag changed: ' + ident)
                _asset_proof(existing, [*prior['skills'], prior['manifest'], prior['checksums']])
                products.append(prior)
                continue
        if resolved_tag(REPOSITORY, source['release_key']) != commit:
            raise ValueError('Parent plugin tag changed: ' + ident)
        folder = output / ident / version
        folder.mkdir(parents=True, exist_ok=True)
        plugin_zip = folder / archive['name']
        if not plugin_zip.is_file() or digest(plugin_zip) != archive['sha256']:
            original = _release(source['release_key'])
            found = [a for a in original['assets'] if a['name'] == archive['name']]
            if len(found) != 1:
                raise ValueError('Missing original plugin download')
            raw = run('gh', 'api', '-H', 'Accept: application/octet-stream', found[0]['url'])
            if len(raw) != archive['size'] or hashlib.sha256(raw).hexdigest() != archive['sha256']:
                raise ValueError('Downloaded plugin differs from verified release')
            plugin_zip.write_bytes(raw)
        expected = expected_package_files(root, commit, ident)
        skills = build_skill_bundles(plugin_zip, expected, archive['sha256'], ident, version, commit, folder)
        prefix = f'https://github.com/{REPOSITORY}/releases/download/{tag}/'
        skills = [{**row, 'url': prefix + row['file']} for row in skills]
        manifest = folder / 'skill-bundles.json'
        manifest.write_text(json.dumps({'schema_version': SCHEMA, 'format_version': FORMAT,
            'id': ident, 'version': version, 'source_commit': commit,
            'plugin_sha256': archive['sha256'], 'skills': skills}, indent=2) + '\n')
        paths = [folder / row['file'] for row in skills] + [manifest]
        checksums = folder / 'skill-bundles.sha256'
        checksums.write_text(''.join(f'{digest(p)}  {p.name}\n' for p in paths))
        paths.append(checksums)
        published = publish(REPOSITORY, {'id': ident, 'version': version, 'tag': tag}, commit, paths,
            title=f'{ident} {version}: individual skill downloads',
            notes=f'Automatically generated skill downloads from {source["release_key"]} at {commit}. '
                  'Includes original supporting files and notices. These Site downloads do not register '
                  'plugin hooks, tools, accounts or MCP services. See each bundle README for setup. '
                  'The original plugin release is unchanged.')
        def asset_row(path):
            return {'file': path.name, 'size': path.stat().st_size, 'sha256': digest(path), 'url': prefix + path.name}
        product = {'id': ident, 'version': version, 'source_commit': commit,
            'plugin_sha256': archive['sha256'], 'tag': tag, 'release_url': published['html_url'],
            'skills': skills, 'manifest': asset_row(manifest), 'checksums': asset_row(checksums)}
        _asset_proof(published, [*skills, product['manifest'], product['checksums']])
        products.append(product)
        # Atomic checkpoints preserve successfully verified products on interruption.
        checkpoint = {'schema_version': SCHEMA, 'format_version': FORMAT,
                      'products': sorted([*products, *[p for p in previous['products']
                          if p['id'] not in {x['id'] for x in products}]], key=lambda p: p['id'])}
        validate_index(checkpoint)
        temp = index_path.with_suffix('.json.tmp')
        temp.write_text(json.dumps(checkpoint, indent=2) + '\n'); temp.replace(index_path)
    result = validate_index({'schema_version': SCHEMA, 'format_version': FORMAT, 'products': products})
    temp = index_path.with_suffix('.json.tmp')
    temp.write_text(json.dumps(result, indent=2) + '\n'); temp.replace(index_path)
    return result
