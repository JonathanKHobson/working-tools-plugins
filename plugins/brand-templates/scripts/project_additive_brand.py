#!/usr/bin/env python3
"""Append one complete authored kit without rebuilding established collections.

Registers source hashes and copies only selected preview/guide/bundle files to
an existing local public projection. No upload, installation or deployment.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile

OWNER = Path(__file__).resolve().parents[1]
IDENT = 'fresh-curiosity-a2'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def append(rows, row):
    matched = [i for i, old in enumerate(rows) if old['id'] == row['id']]
    if len(matched) > 1:
        raise ValueError('Duplicate existing brand')
    if matched:
        rows[matched[0]] = row
    else:
        rows.append(row)

def copy_file(source, target):
    if not source.is_file() or source.is_symlink():
        raise ValueError('Source must be a real regular file: ' + str(source))
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True, help='Canonical package root with brand/, assets/, skills/')
    ap.add_argument('--output', type=Path, required=True, help='Existing public brand-library directory')
    ap.add_argument('--guide', type=Path, required=True, help='Reviewed brand guide PDF')
    ap.add_argument('--preview', type=Path, action='append', required=True, help='Reviewed WebP preview; first becomes gallery cover')
    ap.add_argument('--reference', type=Path, action='append', default=[], help='Explicit public reference asset; private evidence is never scanned')
    ap.add_argument('--public-file', action='append', default=[], help='Explicit additional package-relative public file, such as qa/color-pairings.json')
    ap.add_argument('--axes', type=Path, help='Final P49 portable axis directory from the Writing Library owner')
    ap.add_argument('--evidence', type=Path, required=True)
    ap.add_argument('--download-base', help='Verified versioned HTTPS GitHub release download directory')
    a = ap.parse_args()
    source = a.source.resolve()
    row = read(source / 'brand/brand.json')
    if row['id'] != IDENT or row.get('sourceTemplateIds') != []:
        raise ValueError('Only independent Fresh Curiosity A2 without design bindings is admitted')
    catalog_path = OWNER / 'library/catalog.json'
    original = read(catalog_path)
    public = read(a.output / 'catalog.json')
    preserve = {r['id']: r for r in original['brands'] if r['id'] != IDENT}
    preserve_public = {r['id']: r for r in public['brands'] if r['id'] != IDENT}
    prior_files = {str(p.relative_to(a.output)): sha(p) for p in a.output.rglob('*') if p.is_file() and p.suffix in ('.zip', '.pdf') and IDENT not in p.name}
    kit = OWNER / 'templates' / IDENT
    kit.mkdir(parents=True, exist_ok=True)
    for path in (source / 'brand').rglob('*'):
        if path.is_file():
            copy_file(path, kit / 'brand' / path.relative_to(source / 'brand'))
    for path in (source / 'assets').rglob('*'):
        if path.is_file():
            copy_file(path, kit / 'assets' / path.relative_to(source / 'assets'))
    for name in ('README.md', 'MASTER.md', 'ABOUT.md'):
        path = source / name
        if path.is_file():
            copy_file(path, kit / name)
    writing = source / 'writing'
    if writing.is_dir():
        for path in writing.rglob('*'):
            if path.is_file() and path.suffix in ('.md', '.json'):
                copy_file(path, kit / 'writing' / path.relative_to(writing))
    if a.axes:
        expected_axes = {'README.md', 'voice.md', 'tone.md', 'style.md', 'format.md', 'profile.json'}
        if not expected_axes.issubset({p.name for p in a.axes.iterdir() if p.is_file()}):
            raise ValueError('Final P49 axis closure requires README, four guides and profile.json')
        def axis_paths(value):
            if isinstance(value, dict):
                return {k: axis_paths(v) for k, v in value.items()}
            if isinstance(value, list):
                return [axis_paths(v) for v in value]
            if isinstance(value, str) and value.startswith('source-edition/companions/P49/'):
                return 'writing/' + value.removeprefix('source-edition/companions/P49/')
            return value
        for name in sorted(expected_axes):
            path = a.axes / name
            target = kit / 'writing/axes' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if name.endswith('.json'):
                write(target, axis_paths(read(path)))
            else:
                target.write_text(path.read_text().replace('../../../source-edition/companions/P49/', '../'))
        (kit / 'writing/axes/SOURCE.md').write_text('# Portable axis projection\n\nThese six files project the final P49 axis edition maintained by Writing Templates. Markdown evidence links resolve against this kit\'s public writing authority; JSON source paths use `writing/` relative to the kit root. The upstream four-axis attribution, commit and CC BY 4.0 notice remain in README.md and profile.json. Levels are editorial prominence, not measured personal traits.\n')
    for path in (source / 'skills').rglob('*'):
        if path.is_file():
            copy_file(path, kit / 'skills' / path.relative_to(source / 'skills'))
    for relative in a.public_file:
        path = (source / relative).resolve()
        if not path.is_relative_to(source):
            raise ValueError('Public file must remain inside its source package')
        copy_file(path, kit / relative)
    for path in a.reference:
        if re.search('private|personal-sample|corpus', str(path), re.I):
            raise ValueError('Private evidence cannot enter the kit')
        rel = path.resolve().relative_to(source) if path.resolve().is_relative_to(source) else Path('references') / path.name
        copy_file(path, kit / rel)
        if path.name == 'GENERATION.md':
            destination = kit / rel
            destination.write_text(re.sub(r'/(?:Users|Volumes)/[^\s`<>]+', '[local provenance path omitted]', destination.read_text()))
    for path in (source / 'guides').glob('*.pdf'):
        copy_file(path, kit / 'guides' / path.name)
    guide_relative = 'guides/' + a.guide.name
    copy_file(a.guide, kit / guide_relative)
    legacy_duplicate = kit / 'guide.pdf'
    if legacy_duplicate.is_file():
        registered = next((r for r in read(OWNER / 'provenance/source-files.json')['files'] if r['path'] == f'templates/{IDENT}/guide.pdf'), None)
        if not registered or sha(legacy_duplicate) != registered['sha256']:
            raise ValueError('Legacy duplicate differs from the registered generated copy; preserve and review it')
        legacy_duplicate.unlink()
    (kit / 'SKILL.md').write_text('---\nname: fresh-curiosity-a2-brand\ndescription: "Apply the complete Fresh Curiosity A2 brand identity, public authority, assets and writing guidance."\n---\n\n# Fresh Curiosity A2\n\nRead the [brand skill](skills/fresh-curiosity-brand/SKILL.md) and [complete design authority](brand/DESIGN.md), then use the linked assets and format rules. The [human guide](' + guide_relative + ') accompanies the complete source package. Selection does not install or publish.\n')
    (kit / 'DESIGN.md').write_text('# Fresh Curiosity A2 design authority\n\nThe [complete maintained authority](brand/DESIGN.md) defines this identity. Read its rules and linked public source records before applying the brand.\n')
    (kit / 'STYLE.md').write_text('# Fresh Curiosity writing authority\n\nRead the [complete writing authority](writing/AUTHORITY.md) and [selected writing guide](writing/STYLE.md). P49 is an independent editorial candidate. Synthetic examples and private personal evidence are different states; only public authored guidance is included.\n')
    for path in kit.rglob('*.json'):
        if re.search(r'/(?:Users|Volumes)/|file://', path.read_text()):
            raise ValueError('Public kit JSON contains a private host path: ' + path.name)
    for path in kit.rglob('*.md'):
        text = path.read_text()
        if re.search(r'/(?:Users|Volumes)/|file://', text):
            raise ValueError('Public kit contains a private host path: ' + path.name)
        for target in re.findall(r'\]\(([^)]+)\)', text):
            rel = target.strip('<>').split('#')[0]
            if not rel or ':' in rel:
                continue
            resolved = (path.parent / rel).resolve()
            if not resolved.is_relative_to(kit.resolve()) or not resolved.exists():
                raise ValueError('Unclosed kit link: ' + str(path.relative_to(kit)) + ' -> ' + target)
    row['sourceHash'] = sha(kit / 'brand/DESIGN.md')
    row['sourceTemplateNames'] = {}
    row['templateVariations'] = []
    previews = []
    for index, path in enumerate(a.preview):
        if path.suffix.lower() != '.webp':
            raise ValueError('MCP cover expects actual WebP previews')
        rel = f'media/{IDENT}-{index + 1}.webp'
        copy_file(path, OWNER / 'library' / rel)
        copy_file(path, a.output / rel)
        previews.append({'src': rel, 'label': ['Complete brand guide', 'Visual reference', 'Additional example'][min(index, 2)]})
    row['previews'] = previews
    row['guide'] = {'pdf': f'guides/{IDENT}.pdf', 'preview': previews[0]['src'], 'markdown': f'guides/{IDENT}.md'}
    row['localFiles'] = {'guide': guide_relative, 'skill': 'SKILL.md', 'design': 'DESIGN.md', 'guideSource': 'brand/DESIGN.md'}
    row['bundle'] = {'href': f'bundles/brand-kit-{IDENT}.zip', 'filename': 'Fresh Curiosity A2 brand kit.zip'}
    # Transport hashes stay in the catalog, avoiding a self-referential archive.
    internal = dict(row)
    internal['bundle'] = {'filename': row['bundle']['filename'], 'status': 'portable_kit_source'}
    write(kit / 'brand.json', internal)
    write(kit / 'brand/brand.json', internal)
    archive = a.output / 'bundles' / f'brand-kit-{IDENT}.zip'
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(kit.rglob('*')):
            if path.is_file():
                info = zipfile.ZipInfo('fresh-curiosity-a2/' + path.relative_to(kit).as_posix(), date_time=(2026, 10, 9, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                z.writestr(info, path.read_bytes())
    row['bundle'].update(sha256=sha(archive), bytes=archive.stat().st_size)
    pdf = a.output / row['guide']['pdf']
    copy_file(a.guide, pdf)
    guide_markdown = (kit / 'brand/DESIGN.md').read_text()
    guide_markdown = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: m[0] if m[2].startswith(('http:', 'https:', '#')) else f'{m[1]} (`{m[2]}` in the brand kit)', guide_markdown)
    md = a.output / row['guide']['markdown']
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(guide_markdown)
    if a.download_base:
        if not a.download_base.startswith('https://github.com/JonathanKHobson/shareables/releases/download/'):
            raise ValueError('Unexpected release location')
        row['bundle']['href'] = a.download_base.rstrip('/') + '/' + archive.name
        row['guide']['pdf'] = a.download_base.rstrip('/') + '/brand-guide-' + IDENT + '.pdf'
    append(original['brands'], row)
    original['total'] = len(original['brands'])
    original['templateBindingCount'] = sum(len(r['sourceTemplateIds']) for r in original['brands'])
    write(catalog_path, original)
    append(public['brands'], row)
    public['total'] = len(public['brands'])
    public['templateBindingCount'] = sum(len(r['sourceTemplateIds']) for r in public['brands'])
    write(a.output / 'catalog.json', public)
    provenance_path = OWNER / 'provenance/source-files.json'
    provenance = read(provenance_path)
    prefix = f'templates/{IDENT}/'
    provenance['files'] = [r for r in provenance['files'] if not r['path'].startswith(prefix) and r['path'] != 'library/catalog.json' and not r['path'].startswith(f'library/media/{IDENT}-')]
    for path in [catalog_path, *[p for p in kit.rglob('*') if p.is_file()], *[OWNER / 'library' / p['src'] for p in previews]]:
        provenance['files'].append({'path': str(path.relative_to(OWNER)), 'sha256': sha(path), 'bytes': path.stat().st_size})
    provenance['files'].sort(key=lambda r: r['path'])
    write(provenance_path, provenance)
    for key, old in preserve.items():
        assert next(r for r in read(catalog_path)['brands'] if r['id'] == key) == old
    for key, old in preserve_public.items():
        assert next(r for r in read(a.output / 'catalog.json')['brands'] if r['id'] == key) == old
    for rel, expected in prior_files.items():
        assert sha(a.output / rel) == expected
    assert original['templateBindingCount'] == 106
    write(a.evidence, {'status': 'registered_and_projected_locally_not_installed_not_published', 'brandId': IDENT, 'canonicalCount': original['total'], 'publicCount': public['total'], 'templateBindings': original['templateBindingCount'], 'preservedCanonicalRecords': len(preserve), 'preservedPublicRecords': len(preserve_public), 'preservedDownloadFiles': len(prior_files), 'bundleSha256': row['bundle']['sha256'], 'bundleBytes': row['bundle']['bytes'], 'privateCorpusIncluded': False})
    print(json.dumps({'id': IDENT, 'brands': original['total'], 'templateBindings': 106, 'bundleSha256': row['bundle']['sha256']}))

if __name__ == '__main__':
    main()
