#!/usr/bin/env python3
"""Stage, verify and publish only a reviewed additive Fresh Curiosity release.

Every phase is explicit. Existing releases and unrelated catalog records are
preserved. This script never builds packages or deploys the Site.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

REPOSITORY = 'JonathanKHobson/shareables'
BRAND_ID = 'fresh-curiosity-a2'
WRITING_ID = 'P49'
BRAND_OWNER = Path(__file__).resolve().parents[1]

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def gh(*arguments):
    result = subprocess.run(['gh', *arguments], text=True, capture_output=True, check=True)
    return result.stdout

def manifest(args):
    record = read(args.stage / 'release-manifest.json')
    if record['repository'] != REPOSITORY or record['tag'] != args.tag:
        raise ValueError('Release identity differs from its reviewed stage')
    for row in record['files']:
        path = args.stage / row['name']
        if not path.is_file() or path.stat().st_size != row['bytes'] or digest(path) != row['sha256']:
            raise ValueError('Staged bytes changed: ' + row['name'])
    return record

def remote(tag):
    # Draft assets use an untagged transport URL until publication. The native
    # gh resolver finds the exact draft by tag even when REST by-tag is 404.
    view = json.loads(gh('release', 'view', tag, '--repo', REPOSITORY, '--json', 'tagName,isDraft,url,assets'))
    if view['tagName'] != tag:
        raise ValueError('Resolved release has an unexpected tag')
    return {'tag_name': view['tagName'], 'draft': view['isDraft'], 'html_url': view['url'], 'assets': [{'id': int(row['apiUrl'].rsplit('/', 1)[-1]), 'name': row['name'], 'size': row['size'], 'digest': row.get('digest'), 'browser_download_url': row['url']} for row in view['assets']]}

def verified_remote_assets(release, receipt):
    actual = {row['name']: row for row in release.get('assets', [])}
    if set(actual) != {row['name'] for row in receipt['files']}:
        raise ValueError('Remote asset set changed after verification')
    for row in receipt['files']:
        asset = actual[row['name']]
        if asset['id'] != row['assetId'] or asset['size'] != row['bytes'] or asset.get('digest') not in (None, 'sha256:' + row['sha256']):
            raise ValueError('Remote verified asset changed: ' + row['name'])

def stage(args):
    required = [args.writing_bundle, args.brand_bundle, args.brand_guide, args.writing_guide]
    if any(p is None for p in required):
        raise ValueError('Stage needs both final ZIPs and both final PDFs')
    args.stage.mkdir(parents=True, exist_ok=True)
    inputs = [(args.writing_bundle, 'writing-resource-p49.zip'), (args.brand_bundle, 'brand-kit-fresh-curiosity-a2.zip'), (args.brand_guide, 'brand-guide-fresh-curiosity-a2.pdf'), (args.writing_guide, 'Fresh-Curiosity-Writing-Guide.pdf')]
    rows = []
    for source, name in inputs:
        if source.is_symlink() or not source.is_file():
            raise ValueError('Final artifact must be a regular file: ' + str(source))
        destination = args.stage / name
        if source.resolve() != destination.resolve():
            shutil.copy2(source, destination)
        rows.append({'name': name, 'sha256': digest(destination), 'bytes': destination.stat().st_size})
    sums = args.stage / 'SHA256SUMS.txt'
    sums.write_text(''.join(row['sha256'] + '  ' + row['name'] + '\n' for row in rows))
    rows.append({'name': sums.name, 'sha256': digest(sums), 'bytes': sums.stat().st_size})
    notes = args.stage / 'release-notes.md'
    notes.write_text('Fresh Curiosity A2 brand and writing sources with two human-readable PDF guides. The complete brand kit includes both guides, brand and writing authorities, three skills, character and composition assets, bundled fonts and notices, public source boundaries and the attributed four-axis reading guides. P49 is an independent editorial writing candidate. Its three demonstrations are synthetic; descriptive text measurements and editorial settings remain distinct. Private personal samples are excluded. Existing library assets remain unchanged.\n')
    record = {'schemaVersion': 'fresh-curiosity-additive-release/1', 'repository': REPOSITORY, 'tag': args.tag, 'status': 'staged_not_uploaded', 'files': rows}
    write(args.stage / 'release-manifest.json', record)
    return record

def upload(args):
    record = manifest(args)
    check = subprocess.run(['gh', 'release', 'view', args.tag, '--repo', REPOSITORY, '--json', 'tagName'], text=True, capture_output=True)
    if check.returncode == 0:
        existing = remote(args.tag)
        if existing.get('draft') is not True:
            raise ValueError('Existing published release is preserved; choose a new versioned tag')
        expected = {row['name']: row for row in record['files']}
        for asset in existing.get('assets', []):
            row = expected.get(asset['name'])
            if not row or asset.get('size') != row['bytes'] or asset.get('digest') != 'sha256:' + row['sha256']:
                raise ValueError('Existing draft asset differs; no overwrite is permitted: ' + asset['name'])
        uploaded = {asset['name'] for asset in existing.get('assets', [])}
        paths = [str(args.stage / row['name']) for row in record['files'] if row['name'] not in uploaded]
        if paths:
            gh('release', 'upload', args.tag, *paths, '--repo', REPOSITORY)
    else:
        if '404' not in check.stderr and 'release not found' not in check.stderr.lower():
            raise ValueError('Release lookup failed without confirmed absence: ' + check.stderr.strip())
        gh('release', 'create', args.tag, *[str(args.stage / row['name']) for row in record['files']], '--repo', REPOSITORY, '--draft', '--title', 'Fresh Curiosity A2 brand and writing package', '--notes-file', str(args.stage / 'release-notes.md'))
    record['status'] = 'uploaded_as_draft_not_verified'
    write(args.stage / 'release-manifest.json', record)
    return record

def verify(args):
    record = manifest(args)
    release = remote(args.tag)
    actual = {row['name']: row for row in release.get('assets', [])}
    if set(actual) != {row['name'] for row in record['files']}:
        raise ValueError('Remote asset set differs from the exact five-file stage')
    results = []
    with tempfile.TemporaryDirectory(prefix='fresh-curiosity-release-verify-') as temporary:
        folder = Path(temporary)
        for row in record['files']:
            asset = actual[row['name']]
            if asset['size'] != row['bytes']:
                raise ValueError('Remote asset size differs: ' + row['name'])
            if asset.get('digest') not in (None, 'sha256:' + row['sha256']):
                raise ValueError('Remote GitHub digest differs: ' + row['name'])
            gh('release', 'download', args.tag, '--repo', REPOSITORY, '--pattern', row['name'], '--dir', str(folder))
            downloaded = folder / row['name']
            if downloaded.stat().st_size != row['bytes'] or digest(downloaded) != row['sha256']:
                raise ValueError('Downloaded remote bytes differ: ' + row['name'])
            results.append({**row, 'assetId': asset['id'], 'remoteUrl': asset['browser_download_url'], 'remoteDownloadedSha256': digest(downloaded), 'verified': True})
    receipt = {'schemaVersion': 'fresh-curiosity-additive-release-verification/1', 'repository': REPOSITORY, 'tag': args.tag, 'releaseUrl': release['html_url'], 'draft': release['draft'], 'verified': True, 'files': results, 'browserDownloadVerified': False}
    write(args.stage / 'remote-verification.json', receipt)
    record['status'] = 'draft_remote_bytes_verified' if release['draft'] else 'published_remote_bytes_verified'
    write(args.stage / 'release-manifest.json', record)
    return receipt

def publish(args):
    record = manifest(args)
    receipt = read(args.stage / 'remote-verification.json')
    if receipt.get('verified') is not True or receipt['tag'] != args.tag:
        raise ValueError('Exact remote byte verification is required before publishing')
    if {row['name']: row['sha256'] for row in receipt['files']} != {row['name']: row['sha256'] for row in record['files']}:
        raise ValueError('Remote verification no longer matches the stage')
    release = remote(args.tag)
    verified_remote_assets(release, receipt)
    if release['draft']:
        gh('release', 'edit', args.tag, '--repo', REPOSITORY, '--draft=false')
    release = remote(args.tag)
    if release['draft']:
        raise ValueError('GitHub release is still a draft')
    verified_remote_assets(release, receipt)
    receipt['draft'] = False
    receipt['releaseUrl'] = release['html_url']
    by_name = {row['name']: row for row in release['assets']}
    for row in receipt['files']:
        row['remoteUrl'] = by_name[row['name']]['browser_download_url']
    write(args.stage / 'remote-verification.json', receipt)
    record['status'] = 'published_remote_bytes_verified'
    write(args.stage / 'release-manifest.json', record)
    return {'releaseUrl': release['html_url'], 'published': True}

def apply(args):
    record = manifest(args)
    receipt = read(args.stage / 'remote-verification.json')
    release = remote(args.tag)
    if release['draft'] or receipt.get('verified') is not True or receipt['tag'] != args.tag:
        raise ValueError('Published, byte-verified release is required for URL projection')
    verified_remote_assets(release, receipt)
    expected = {row['name']: row for row in record['files']}
    prefix = f'https://github.com/{REPOSITORY}/releases/download/{args.tag}/'
    writing_catalog = args.writing_owner / 'library/voice-library/records/catalog.json'
    canonical_before = digest(writing_catalog)
    # The canonical writing record stays source-based. Shared UI generation is
    # owned elsewhere; this step changes only P49 transport metadata publicly.
    writing_public = args.site / 'writing-library/catalog.json'
    document = read(writing_public)
    old_rows = {row['id']: row for row in document['records'] if row['id'] != WRITING_ID}
    row = next(row for row in document['records'] if row['id'] == WRITING_ID)
    if digest(args.writing_bundle or args.stage / 'writing-resource-p49.zip') != expected['writing-resource-p49.zip']['sha256']:
        raise ValueError('Selected writing package differs from the verified release')
    row['downloads'].update(bundle=prefix + 'writing-resource-p49.zip', skill=prefix + 'writing-resource-p49.zip', bundleSha256=expected['writing-resource-p49.zip']['sha256'], bundleBytes=expected['writing-resource-p49.zip']['bytes'], pdf=prefix + 'Fresh-Curiosity-Writing-Guide.pdf', pdfSha256=expected['Fresh-Curiosity-Writing-Guide.pdf']['sha256'], pdfBytes=expected['Fresh-Curiosity-Writing-Guide.pdf']['bytes'])
    assert all(next(r for r in document['records'] if r['id'] == ident) == previous for ident, previous in old_rows.items())
    pending = [(writing_public, document), (args.site / 'writing-library/downloads/P49/profile.json', row)]
    from os import environ
    binding = Path.home() / '.config/studio-tools/design-library.json'
    config = read(binding) if binding.is_file() else {}
    collection = config.get('collections', {}).get('brand-templates', {})
    brand_catalog = Path(environ.get('BRAND_TEMPLATES_CATALOG') or collection.get('catalog') or BRAND_OWNER / 'library/catalog.json')
    for catalog_path in (brand_catalog, args.site / 'brand-library/catalog.json'):
        document = read(catalog_path)
        old_rows = {row['id']: row for row in document['brands'] if row['id'] != BRAND_ID}
        row = next(row for row in document['brands'] if row['id'] == BRAND_ID)
        if row['bundle']['sha256'] != expected['brand-kit-fresh-curiosity-a2.zip']['sha256']:
            raise ValueError('Brand catalog package differs from the verified release')
        row['bundle'].update(href=prefix + 'brand-kit-fresh-curiosity-a2.zip', sha256=expected['brand-kit-fresh-curiosity-a2.zip']['sha256'], bytes=expected['brand-kit-fresh-curiosity-a2.zip']['bytes'])
        row['guide']['pdf'] = prefix + 'brand-guide-fresh-curiosity-a2.pdf'
        assert all(next(r for r in document['brands'] if r['id'] == ident) == previous for ident, previous in old_rows.items())
        assert document['templateBindingCount'] == 106
        pending.append((catalog_path, document))
    for catalog_path, document in pending:
        write(catalog_path, document)
    provenance_path = Path(environ.get('BRAND_TEMPLATES_SOURCE_MANIFEST') or collection.get('source_manifest') or BRAND_OWNER / 'provenance/source-files.json')
    provenance = read(provenance_path)
    row = next(row for row in provenance['files'] if row['path'] == 'library/catalog.json')
    row['sha256'] = digest(brand_catalog)
    if 'bytes' in row:
        row['bytes'] = brand_catalog.stat().st_size
    write(provenance_path, provenance)
    return {'status': 'verified_urls_projected_locally_not_site_deployed', 'releaseUrl': release['html_url'], 'preservedWritingRecords': len(read(writing_public)['records']) - 1, 'preservedBrandRecords': len(old_rows), 'designBindings': 106, 'writingCanonicalCatalogUnchanged': canonical_before == digest(writing_catalog)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['stage', 'upload', 'verify', 'publish', 'apply'])
    parser.add_argument('--stage', type=Path, required=True)
    parser.add_argument('--tag', default='fresh-curiosity-a2-2026-10-09')
    parser.add_argument('--writing-bundle', type=Path)
    parser.add_argument('--brand-bundle', type=Path)
    parser.add_argument('--brand-guide', type=Path)
    parser.add_argument('--writing-guide', type=Path)
    parser.add_argument('--writing-owner', type=Path, default=Path.home() / 'plugins/writing-templates')
    parser.add_argument('--site', type=Path, help='Explicit existing Site output tree for the apply phase')
    args = parser.parse_args()
    if args.phase == 'apply' and args.site is None:
        parser.error('The apply phase requires an explicit --site output tree')
    if not args.tag.startswith('fresh-curiosity-a2-') or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-.' for c in args.tag):
        raise ValueError('Use a bounded versioned Fresh Curiosity tag')
    print(json.dumps(globals()[args.phase](args), ensure_ascii=False))

if __name__ == '__main__':
    main()
