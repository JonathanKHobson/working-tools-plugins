#!/usr/bin/env python3
"""Register one reviewed writing candidate and append its public projection.

Existing records and published bundles remain byte-identical. This operation
does not install a plugin, upload assets or publish the Site.
"""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

from build_style_entries import style_entry
from build_voice_public import render, body, FEATURES, TYPE_LABELS, zip_bytes, clean
from voice_validation_package import profile, portable_files, PORTABLE_INSTRUCTIONS
from build_axis_references import write_references, augment_archive, load_profiles, render_files, profile_data
from build_voice_covers import outlined, wrap, art, rect, DESIGNS

OWNER = Path(__file__).resolve().parents[1]
LIB = OWNER / 'library/voice-library'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def read_json(path):
    return json.loads(Path(path).read_text())

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def append_record(rows, row, key='id'):
    matches = [i for i, old in enumerate(rows) if old[key] == row[key]]
    if len(matches) > 1:
        raise ValueError('Duplicate existing resource')
    if matches:
        rows[matches[0]] = row
    else:
        rows.append(row)


def admit_structure_expansion(packet: Path, public: Path, evidence: Path) -> None:
    """Admit the four reviewed structure modules through the existing additive owner.

    This branch is intentionally bounded to P50-P53. The P49 path below remains
    unchanged, and previously projected records and archives are checked after
    admission. Upload, installation and publication are separate operations.
    """
    ids = ('P50', 'P51', 'P52', 'P53')
    packet = packet.resolve()
    public = public.resolve()
    before_catalog = read_json(LIB / 'records/catalog.json')
    before_public = read_json(public / 'catalog.json')
    before_rows = {r['id']: r for r in before_catalog['records']}
    before_public_rows = {r['id']: r for r in before_public['records']}
    if any(ident in before_rows or ident in before_public_rows for ident in ids):
        raise ValueError('Structure expansion already admitted; review current sources before rerunning')
    if set(before_rows) != set(before_public_rows) or len(before_rows) != 49:
        raise ValueError('Expected the verified 49-resource canonical/public baseline')
    old_archives = {str(p.relative_to(public)): sha(p.read_bytes())
                    for p in (public / 'downloads').rglob('*.zip')}
    briefs = read_json(packet / 'briefs.json')
    by_brief = {b['id']: b for b in briefs['briefs']}
    if len(by_brief) != len(briefs['briefs']) or briefs.get('status') != 'fictional_exercises_only':
        raise ValueError('Expected distinct synthetic source briefs')
    staged = {}
    for ident in ids:
        source = packet / ident
        row = read_json(source / 'record.json')
        guide = (source / 'guide.md').read_text()
        readings = (source / 'readings.md').read_text()
        if row['id'] != ident or row['resource_type'] != 'module' or row['privacy_scope'] != 'generic_synthetic':
            raise ValueError(f'{ident}: unexpected resource type or scope')
        route = row['route']
        if route != {'base_profile_id': {'P50': 'V01', 'P51': 'V11', 'P52': 'V09', 'P53': 'V10'}[ident],
                     'selected_resource_id': ident, 'module_ids': [ident]}:
            raise ValueError(f'{ident}: route differs from reviewed base')
        if len(row['examples']) != 3 or not all(h in guide for h in ('## Working rules', '## Avoid', '### Follows the mechanism', '### Near miss')):
            raise ValueError(f'{ident}: incomplete selected authority')
        if re.search(r'\b(?:staged|unregistered|Proposed module guide)\b|/(?:Users|Volumes)/|file://', guide, re.I):
            raise ValueError(f'{ident}: authoring status or private path in authority')
        if not all('creativecommons.org/licenses/by/4.0/' in text or 'CC BY 4.0' in text for text in (guide, readings)):
            raise ValueError(f'{ident}: missing source-license attribution')
        for ex in row['examples']:
            name = Path(ex['path']).name
            raw = (source / 'examples' / name).read_bytes()
            content = raw.decode('utf-8')
            if sha(raw) != ex['sha256'] or ex['brief_id'] not in by_brief or ex['id'] not in by_brief[ex['brief_id']]['used_by']:
                raise ValueError(f'{ident}: example identity or brief mismatch')
            if content.count('<!-- specimen:start -->') != 1 or content.count('<!-- specimen:end -->') != 1:
                raise ValueError(f'{ident}: specimen markers are incomplete')
            if 'authorship: AI-authored synthetic by Codex' not in content:
                raise ValueError(f'{ident}: sample provenance is missing')
        if row['quote'] not in (source / 'examples/specimen.md').read_text():
            raise ValueError(f'{ident}: cover quote is not an exact specimen span')
        staged[ident] = (row, guide, readings)

    # Canonical authority, examples and their exact fictional briefs.
    (LIB / 'records/structure-briefs.json').write_text(json.dumps(briefs, ensure_ascii=False, indent=2) + '\n')
    edition = read_json(LIB / 'source-edition/edition.json')
    for ident, (row, guide, readings) in staged.items():
        (LIB / 'modules' / f'{ident}.md').write_text(guide)
        (LIB / 'source-edition/guides' / f'{ident}.md').write_text(guide)
        (LIB / 'source-edition/readings' / f'{ident}.md').write_text(readings)
        scoped = {'schema': briefs['schema'], 'status': briefs['status'],
                  'authorship': briefs['authorship'],
                  'briefs': [by_brief[ex['brief_id']] for ex in row['examples']]}
        companion = LIB / 'source-edition/companions' / ident / 'briefs.json'
        write_json(companion, scoped)
        for ex in row['examples']:
            name = Path(ex['path']).name
            target = LIB / ex['path']
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((packet / ident / 'examples' / name).read_bytes())
        before_catalog['records'].append(row)
        rels = [f'guides/{ident}.md', f'readings/{ident}.md', f'companions/{ident}/briefs.json']
        edition['records'][ident] = {
            'styleAuthority': {'title': row['name'] + ' · Complete writing guide',
                               'owner': 'Writing Library', 'path': rels[0],
                               'sources': row['authority_sources']},
            'humanReferences': [], 'samples': [], 'readingPath': rels[1],
            'bundleFiles': rels, 'formats': []}
        for rel in rels:
            edition['files'][rel] = sha((LIB / 'source-edition' / rel).read_bytes())
    before_catalog['record_count'] = len(before_catalog['records'])
    write_json(LIB / 'records/catalog.json', before_catalog)
    write_json(LIB / 'source-edition/edition.json', edition)

    # Measure the actual retained text. No new design target ranges are inferred.
    node = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
    parser = LIB / 'validation/vendor/marked/lib/marked.esm.js'
    env = dict(os.environ, VOICE_LAB_MARKED=str(parser))
    js = "const fs=require('node:fs');const {measure}=require(process.argv[1]);(async()=>{const paths=JSON.parse(fs.readFileSync(0,'utf8'));const rows=[];for(const p of paths){rows.push(await measure(fs.readFileSync(p,'utf8')))}process.stdout.write(JSON.stringify(rows))})().catch(e=>{process.stderr.write(e.message);process.exitCode=1})"
    paths = [str(LIB / ex['path']) for row, _, _ in staged.values() for ex in row['examples']]
    measured = json.loads(subprocess.run([str(node), '-e', js, str(LIB / 'metrics/measure.cjs')],
                                         input=json.dumps(paths), text=True, capture_output=True,
                                         check=True, env=env).stdout)
    corpus = read_json(LIB / 'evaluation/metrics-corpus-v1.json')
    acceptance = read_json(LIB / 'evaluation/content-acceptance.json')
    measurements = {}
    cursor = 0
    for ident, (row, _, _) in staged.items():
        measurements[ident] = []
        for ex in row['examples']:
            result = measured[cursor]
            cursor += 1
            result.update(sample_id=ex['id'], path=ex['path'])
            if result['text_sha256'] != ex['sha256']:
                raise ValueError(f'{ident}: measured text differs from retained bytes')
            corpus['samples'].append(result)
            acceptance['current_files'][ex['path']] = ex['sha256']
            measurements[ident].append(result)
    write_json(LIB / 'evaluation/metrics-corpus-v1.json', corpus)
    write_json(LIB / 'evaluation/content-acceptance.json', acceptance)
    manifest = read_json(LIB / 'validation/manifest.json')
    for ident, (row, _, _) in staged.items():
        target = LIB / 'validation/profiles' / f'{ident}.json'
        write_json(target, profile(row, LIB))
        manifest['files'][f'validation/profiles/{ident}.json'] = sha(target.read_bytes())
    write_json(LIB / 'validation/manifest.json', manifest)

    axes_path = LIB / 'axes/four-axes.json'
    axes = read_json(axes_path)
    new_terms = read_json(packet / 'axis-terms.json')
    if set(new_terms) & set(axes['terms']):
        raise ValueError('Structure axis term already exists')
    axes['terms'].update(new_terms)
    axes['profiles'].extend(read_json(packet / ident / 'axes-profile.json') for ident in ids)
    write_json(axes_path, axes)
    by_id = {r['id']: r for r in before_catalog['records']}
    for ident, (row, guide, _) in staged.items():
        base = by_id[row['route']['base_profile_id']]
        base_guide = (LIB / 'source-edition/guides' / f'{base["id"]}.md').read_text()
        style = style_entry(row, base, guide, base_guide)
        target = LIB / 'styles' / ident / 'STYLE.md'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(style)
    write_references(LIB)
    pins_path = OWNER / 'runtime/writing-voice-library/approved-sources.json'
    pins = read_json(pins_path)
    for ident, (row, _, _) in staged.items():
        for rel in (row['guide_path'], *[ex['path'] for ex in row['examples']],
                    f'source-edition/guides/{ident}.md', f'source-edition/readings/{ident}.md',
                    f'source-edition/companions/{ident}/briefs.json',
                    f'styles/{ident}/STYLE.md', f'validation/profiles/{ident}.json'):
            pins['files'][rel] = sha((LIB / rel).read_bytes())
    pins['files']['records/structure-briefs.json'] = sha((LIB / 'records/structure-briefs.json').read_bytes())
    pins.update(catalogSha256=sha((LIB / 'records/catalog.json').read_bytes()),
                sourceEditionSha256=sha((LIB / 'source-edition/edition.json').read_bytes()),
                validationManifestSha256=sha((LIB / 'validation/manifest.json').read_bytes()))
    write_json(pins_path, pins)

    # Append only the four selected public entries and local download sources.
    rendered = render([staged[ident][1] for ident in ids] +
                      [body((LIB / ex['path']).read_text()) for ident in ids for ex in staged[ident][0]['examples']],
                      node, parser)
    rendered_guides = dict(zip(ids, rendered[:4]))
    rendered_samples = iter(rendered[4:])
    doc, axis_profiles = load_profiles(LIB)
    from build_voice_covers import font as cover_font
    cover_specs = {
        'P50': ('book', '#dce8ef', '#243b55', '#7296b3', 'P33', 'criterion comparison'),
        'P51': ('warm', '#efe7fc', '#392c68', '#9b78c5', 'V11', 'question path'),
        'P52': ('clean', '#e3f3ef', '#1f4f47', '#7ebaa8', 'V09', 'progressive depth'),
        'P53': ('mono', '#dfe9e4', '#1c3733', '#6a9a83', 'V10', 'decision record'),
    }
    cover_data = read_json(public / 'data/cover-designs.json')
    for ident, (row, guide, _) in staged.items():
        key, bg, fg, accent, motif, layout = cover_specs[ident]
        quote = ('Markdown files in Git as the documentation source of truth.'
                 if ident == 'P53' else row['quote'].replace('**', ''))
        lines = wrap(quote, key, 70, 700)
        defs = {}
        lettering = outlined(lines, key, 70, 98, 124, 82,
                             '#f3f8f5' if ident == 'P53' else fg, defs)
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="900" height="650" viewBox="0 0 900 650" role="img" aria-labelledby="title desc">'
               f'<title id="title">{row["name"]} · {quote}</title><desc id="desc">AI-authored synthetic editorial cover demonstration.</desc>'
               '<defs>' + ''.join(defs.values()) + '</defs>' + rect(0, 0, 900, 650, bg)
               + art(motif, bg, fg, accent) + lettering + '</svg>')
        preview_rel = f'previews/{ident}.svg'
        for target in (public / preview_rel, OWNER / 'runtime/writing-voice-library/ui' / preview_rel):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(svg)
        cover_data['records'].append({'id': ident, 'name': row['name'], 'preview': preview_rel,
            'width': 900, 'height': 650, 'aspectRatio': '18/13',
            'palette': {'background': bg, 'ink': fg, 'accent': accent,
                        **({'panelInk': '#f3f8f5'} if ident == 'P53' else {})},
            'font': {'family': cover_font(key)[0]['name'].getDebugName(1),
                     'rendering': 'outlined glyph shapes; no external font dependency', 'quoteSourcePixels': 70},
            'layout': layout, 'visualIntent': f'{layout} visually supports the selected structure.',
            'coverQuote': {'text': quote, 'authorship': 'AI-authored original synthetic editorial cover demonstration',
                           'status': 'new_cover_example_not_measured_not_reviewed_as_source_corpus',
                           'sourceSampleId': row['examples'][0]['id'], 'sourceBriefId': row['examples'][0]['brief_id'],
                           'inheritedMeasuredValues': False},
            'quoteLines': lines, 'quoteBaselineBottom': 124 + (len(lines)-1)*82,
            'controlSafeRegion': {'x': 540, 'y': 520, 'width': 360, 'height': 130},
            'sha256': sha(svg.encode())})
        samples = []
        for ex, measurement in zip(row['examples'], measurements[ident]):
            markdown = body((LIB / ex['path']).read_text())
            html_data = next(rendered_samples)
            features = [{'id': f['feature_id'], 'label': FEATURES[i]['label'],
                         'value': f['raw_value'], 'unit': f['unit'], 'status': f['status'],
                         'reason': f['reason']} for i, f in enumerate(measurement['features'])]
            samples.append({'id': ex['id'], 'key': ex['id'].split('/')[1], 'briefId': ex['brief_id'],
                            'label': row['example_labels'][len(samples)], 'markdown': markdown,
                            'sourceMarkdown': (LIB / ex['path']).read_text(), 'sha256': ex['sha256'],
                            'kind': 'synthetic', 'attribution': 'AI-authored demonstration · Fictional scenario',
                            **html_data,
                            'measurement': {'features': features, 'counts': measurement['counts'],
                                            'eligible': measurement['full_fingerprint_eligible'],
                                            'extractorVersion': measurement['extractor_version'],
                                            'textSha256': measurement['text_sha256'], 'separation': 'uncalibrated'}})
        rec = {'id': ident, 'name': row['name'], 'version': row['version'],
               'type': row['resource_type'], 'typeLabel': TYPE_LABELS[row['resource_type']],
               'description': row['description'], 'mechanism': row['mechanism'],
               'rhythm': row['rhythm'], 'tags': row['tags'], 'route': row['route'],
               'skillName': row['skill_name'], 'truthBoundary': row['truth_boundary'],
               'neighborDifference': row['neighbor_difference'], 'neighbors': row['nearest_neighbors'],
               'separation': row['separation'], 'repeatability': row['repeatability'],
               'evidenceStatus': 'reviewed_synthetic_examples_not_reader_validated',
               'independenceStatus': row['independence_status'], 'guideMarkdown': guide,
               'guideHtml': rendered_guides[ident]['html'], 'samples': samples,
               'targets': row['communication_targets'],
               'observations': {'status': 'not_estimated', 'ratings': [],
                                'note': 'No empirical reader outcome or personal voice measurement is asserted.'},
               'sources': row['authority_sources'], 'researchLimits': row['research']['limits'],
               'sourceEdition': edition['version'], 'humanReferences': [],
               'styleAuthority': {'title': row['name'] + ' · Complete writing guide',
                                  'owner': 'Writing Library', 'sources': row['authority_sources'],
                                  'html': rendered_guides[ident]['html'], 'formats': []},
               'quote': {'text': row['quote'], 'sampleId': samples[0]['id'],
                         'briefId': samples[0]['briefId'],
                         'attribution': 'AI-authored synthetic demonstration · Fictional scenario',
                         'sourceExact': True, 'sourceSha256': samples[0]['sha256']},
               'downloads': {'bundle': f'downloads/{ident}/bundle.zip',
                             'skill': f'downloads/{ident}/bundle.zip',
                             'raw': f'downloads/{ident}/raw.json',
                             'markdown': f'downloads/{ident}/examples.md',
                             'profile': f'downloads/{ident}/profile.json', 'preview': preview_rel}}
        base_id = row['route']['base_profile_id']
        base_guide = (LIB / 'source-edition/guides' / f'{base_id}.md').read_text()
        base_guide = re.sub(r'\[([^\]]+)\]\(\.\./readings/[^)]+\)',
                            r'\1 (historical reading in the source library)', base_guide)
        style = (LIB / 'styles' / ident / 'STYLE.md').read_text()
        style = style.replace(f'../../source-edition/guides/{ident}.md', 'references/guide.md')
        style = style.replace(f'../../source-edition/guides/{base_id}.md', 'references/base-guide.md')
        style = style.replace(f'../../source-edition/readings/{ident}.md', 'references/readings.md')
        style = style.replace(f'../../examples/{ident}/specimen.md', 'examples/specimen.md')
        style = style.replace(f'../../validation/profiles/{ident}.json', 'references/qa-profile.json')
        portable = {'STYLE.md': style, 'references/guide.md': guide,
                    'references/base-guide.md': base_guide,
                    'references/readings.md': (LIB / 'source-edition/readings' / f'{ident}.md').read_text(),
                    'references/briefs.json': (LIB / 'source-edition/companions' / ident / 'briefs.json').read_text()}
        for ex in row['examples']:
            portable['examples/' + Path(ex['path']).name] = (LIB / ex['path']).read_text()
        portable.update(portable_files(row, LIB))
        skill = (f'---\nname: writing-resource-{ident.lower()}\n'
                 f'description: "Apply {row["name"]} using its selected and base guides, exact fictional briefs and fact boundaries."\n---\n\n'
                 f'# {row["name"]}\n\nRead [STYLE.md](STYLE.md), the [complete selected guide](references/guide.md), '
                 f'[base guide](references/base-guide.md), [source notes](references/readings.md) and '
                 f'[fictional example briefs](references/briefs.json). Route to {base_id} + {ident}. '
                 'Use the current user brief as the fact boundary. The included examples are AI-authored fictional demonstrations; '
                 'their descriptive measurements do not establish reader benefit, human authorship or repeatability.\n'
                 + PORTABLE_INSTRUCTIONS)
        portable['SKILL.md'] = skill
        portable['agent-manifest.json'] = json.dumps({'schema': 'wvl-portable-agent/1',
            'resourceId': ident, 'baseProfileId': base_id, 'moduleIds': [ident],
            'entrypoint': 'SKILL.md', 'styleEntrypoint': 'STYLE.md',
            'privacyScope': 'generic_synthetic', 'sourceVersion': row['version'],
            'status': 'editorial_module_uncalibrated', 'generatedProjection': True})
        portable['README.md'] = ('# Portable Writing Library structure\n\n'
            'Read SKILL.md and both complete guides. All example briefs are fictional; source and license notes are in references/readings.md. '
            'The bundle can be read offline. Node 20+ is needed only for optional text measurements.\n')
        import posixpath
        for name, value in portable.items():
            if not name.endswith('.md'):
                continue
            for target in re.findall(r'\]\(([^)]+)\)', value):
                relative = target.strip('<>').split('#')[0]
                if relative and ':' not in relative and not relative.startswith('axes/') and posixpath.normpath(posixpath.join(posixpath.dirname(name), relative)) not in portable:
                    raise ValueError(f'{ident}: unclosed portable link {name} -> {target}')
        archive = zip_bytes({f'writing-resource-{ident.lower()}/' + name: value for name, value in portable.items()})
        archive = augment_archive(archive, doc, axis_profiles[ident], LIB)
        dest = public / 'downloads' / ident
        dest.mkdir(parents=True, exist_ok=True)
        (dest / 'bundle.zip').write_bytes(archive)
        (dest / 'SKILL.md').write_text(skill)
        (dest / 'examples.md').write_text('\n\n---\n\n'.join(s['sourceMarkdown'] for s in samples))
        write_json(dest / 'profile.json', clean(rec))
        write_json(dest / 'raw.json', {'schema': 'wvl-public-raw/1', 'resourceId': ident,
            'status': 'synthetic_examples_only_raw_descriptive_features_not_quality',
            'samples': measurements[ident]})
        rec['downloads']['bundleSha256'] = sha(archive)
        rec['downloads']['bundleBytes'] = len(archive)
        before_public['records'].append(rec)
        native = OWNER / 'templates' / ident
        native.mkdir(parents=True, exist_ok=True)
        (native / 'SKILL.md').write_text(skill.replace('(STYLE.md)',
            f'(../../library/voice-library/styles/{ident}/STYLE.md)').replace(
            '(references/guide.md)', f'(../../library/voice-library/source-edition/guides/{ident}.md)').replace(
            '(references/base-guide.md)', f'(../../library/voice-library/source-edition/guides/{base_id}.md)').replace(
            '(references/readings.md)', f'(../../library/voice-library/source-edition/readings/{ident}.md)').replace(
            '(references/briefs.json)', f'(../../library/voice-library/source-edition/companions/{ident}/briefs.json)').split('## Humanizer Light')[0])
    write_json(public / 'data/cover-designs.json', cover_data)
    public_axes = read_json(public / 'data/four-axes.json')
    public_axes['terms'].update(new_terms)
    public_axes['profiles'].extend(axis_profiles[ident] for ident in ids)
    write_json(public / 'data/four-axes.json', public_axes)
    for brief in briefs['briefs']:
        if brief['id'] not in {b['id'] for b in before_public['briefs']}:
            before_public['briefs'].append({'id': brief['id'], 'markdown':
                '**Fictional exercise.** ' + brief['task'] + '\n\nFacts:\n' +
                '\n'.join('- ' + fact for fact in brief['facts']) + '\n\nUnknowns:\n' +
                '\n'.join('- ' + item for item in brief['unknowns'])})
    counts = before_public['counts']
    counts['resources'] = len(before_public['records'])
    counts['profileSkills'] = sum(r['type'] in ('legacy_profile', 'voice_candidate') for r in before_public['records'])
    counts['modules'] = sum(r['type'] == 'module' for r in before_public['records'])
    counts['aliases'] = sum(r['type'] == 'alias' for r in before_public['records'])
    counts['merges'] = sum(r['type'] == 'merge' for r in before_public['records'])
    counts['commonSamples'] = sum(s['briefId'] in ('E-B01', 'E-B02', 'E-B03')
                                   for r in before_public['records'] for s in r['samples'])
    counts['samples'] = sum(len(r['samples']) for r in before_public['records'])
    write_json(public / 'catalog.json', before_public)
    llms = public / 'llms.txt'
    llms.write_text(llms.read_text() + '\n## Four selectable writing structures\n\n'
        'P50 Comparison–Contrast, P51 Socratic Inquiry, P52 Layered Disclosure and P53 Architecture Decision Record '
        'are source-attributed modules with twelve labeled fictional AI-authored demonstrations. '
        'Use their selected/base guides and exact briefs; the examples do not validate reader outcomes.\n')
    for ident, old in before_rows.items():
        assert next(r for r in read_json(LIB / 'records/catalog.json')['records'] if r['id'] == ident) == old
    for ident, old in before_public_rows.items():
        assert next(r for r in read_json(public / 'catalog.json')['records'] if r['id'] == ident) == old
    for name, old_hash in old_archives.items():
        assert sha((public / name).read_bytes()) == old_hash
    write_json(evidence, {'status': 'registered_and_projected_locally_not_installed_not_uploaded_not_published',
        'ids': list(ids), 'canonicalCount': 53, 'publicCount': 53,
        'preservedCanonicalRecords': len(before_rows), 'preservedPublicRecords': len(before_public_rows),
        'preservedZipFiles': len(old_archives),
        'sourceCatalogSha256': pins['catalogSha256'],
        'bundleSha256': {ident: sha((public / 'downloads' / ident / 'bundle.zip').read_bytes()) for ident in ids},
        'measurementBasis': 'twelve_actual_synthetic_examples_only', 'privateCorpusIncluded': False})
    print(json.dumps({'ids': ids, 'records': 53, 'evidence': str(evidence)}))

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, help='Reviewed P49 writing folder: record.json, STYLE.md, readings.md, examples/*.md')
    ap.add_argument('--canonical-p49', action='store_true', help='Reproject the maintained public P49 companions, without importing a personal authoring package')
    ap.add_argument('--structure-expansion', type=Path, help='Reviewed P50-P53 packet with exact fictional briefs')
    ap.add_argument('--output', type=Path, required=True, help='Existing public writing-library directory')
    ap.add_argument('--evidence', type=Path, required=True)
    ap.add_argument('--download-base', help='Previously verified HTTPS release download directory')
    ap.add_argument('--cover', type=Path, help='Reviewed public PNG used as the new template cover')
    ap.add_argument('--guide', type=Path, help='Reviewed human writing guide PDF')
    ap.add_argument('--preserve-shared-metadata', action='store_true', help='Reproject only the selected record and files; leave shared schema/discovery files to their owner')
    a = ap.parse_args()
    if a.structure_expansion:
        if a.source or a.canonical_p49 or a.cover or a.guide or a.download_base:
            ap.error('--structure-expansion cannot be combined with P49 source or P49 assets')
        admit_structure_expansion(a.structure_expansion, a.output, a.evidence)
        return
    if a.canonical_p49 and a.source:
        ap.error('--canonical-p49 and --source are mutually exclusive')
    if not a.source and not a.canonical_p49:
        ap.error('--source is required for the existing P49 admission')
    source = LIB / 'source-edition/companions/P49' if a.canonical_p49 else a.source.resolve()
    row = (next(r for r in read_json(LIB / 'records/catalog.json')['records'] if r['id'] == 'P49')
           if a.canonical_p49 else read_json(source / 'record.json'))
    ident = row['id']
    if ident != 'P49' or row['resource_type'] != 'voice_candidate':
        raise ValueError('This reviewed additive admission is restricted to P49')
    if row['route'] != {'base_profile_id': ident, 'selected_resource_id': ident, 'module_ids': []}:
        raise ValueError('New candidate must retain its own independent base')
    if row.get('privacy_scope') != 'generic_synthetic':
        raise ValueError('Only public synthetic examples can be admitted')
    for target in row['communication_targets']:
        target.setdefault('task', 'ordinary suitable use; serious incidents use the documented override')
        target.setdefault('kind', 'editorial_target')
        target.setdefault('rubric', 'communication-rubric/1.0.0')
    if any(k not in ('humor', 'enthusiasm', 'persuasive_intent', 'reason') for k in row['incident_override']):
        row['authored_incident_override'] = row['incident_override']
        row['incident_override'] = {'humor': [1, 1], 'enthusiasm': [1, 2], 'persuasive_intent': [1, 1], 'reason': 'The complete authority removes playful performance and promotional pressure during incidents; known state, limits and action govern.'}
    guide = (source / 'STYLE.md').read_text()
    authority_path = source / 'AUTHORITY.md'
    if authority_path.exists():
        guide = guide.replace('(AUTHORITY.md)', '(#complete-authority)')
        guide += '\n\n## Complete authority\n\n' + authority_path.read_text()
    readings = (source / 'readings.md').read_text()
    companions = {str(p.relative_to(source)): p.read_text() for p in source.rglob('*') if p.is_file() and p.suffix in ('.md', '.json') and p.name != 'record.json'}
    character_path = source.parent / 'brand/CHARACTERS.md'
    if not a.canonical_p49 and character_path.is_file():
        character_text = character_path.read_text()
        character_text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', lambda m: m[0] if m[2].startswith(('https:', 'http:', '#')) else f'{m[1]} ({m[2]} in the matching Fresh Curiosity A2 brand kit)', character_text)
        companions['brand/CHARACTERS.md'] = character_text
        companions = {name: text.replace('(../brand/CHARACTERS.md)', '(brand/CHARACTERS.md)') for name, text in companions.items()}
    def mark_brand_dependencies(text):
        def replace(match):
            label, target = match.groups()
            if target.startswith(('../brand/', '../assets/', '../references/', '../guides/', '../qa/', '../scripts/')):
                return f'{label} ({target} in the matching Fresh Curiosity A2 brand kit)'
            return match[0]
        return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace, text)
    guide = mark_brand_dependencies(guide.replace('(../brand/CHARACTERS.md)', '(brand/CHARACTERS.md)'))
    companions = {name: mark_brand_dependencies(text) for name, text in companions.items()}
    def relink(text, prefix):
        def replace(match):
            label, target = match.groups()
            path, _, anchor = target.partition('#')
            if path in companions:
                return f'[{label}]({prefix}{path}' + (('#' + anchor) if anchor else '') + ')'
            return match[0]
        return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace, text)
    source_guide = relink(guide, f'../companions/{ident}/')
    for text in [guide, readings]:
        if re.search(r'/(?:Users|Volumes)/|file://', text):
            raise ValueError('Public authority contains a private host path')
    before_catalog = read_json(LIB / 'records/catalog.json')
    before_public = read_json(a.output / 'catalog.json')
    prior_row = next((r for r in before_catalog['records'] if r['id'] == ident), {})
    row = {**prior_row, **row}
    prior_public = next((r for r in before_public['records'] if r['id'] == ident), {})
    preserved = {r['id']: r for r in before_catalog['records'] if r['id'] != ident}
    preserved_public = {r['id']: r for r in before_public['records'] if r['id'] != ident}
    bundle_before = {str(p.relative_to(a.output)): sha(p.read_bytes()) for p in (a.output / 'downloads').rglob('*.zip') if ident not in p.parts}
    row['guide_path'] = f'modules/{ident}.md'
    row['examples'] = []
    for key, brief in [('specimen', 'E-B01'), ('transfer-a', 'E-B02'), ('transfer-b', 'E-B03')]:
        raw = (source / 'examples' / (key + '.md')).read_bytes()
        text = raw.decode('utf8')
        brief_match = re.search(r'^brief_id:\s*(\S+)', text, re.M)
        if brief_match:
            brief = brief_match[1]
        if '<!-- specimen:start -->' not in text or '<!-- specimen:end -->' not in text:
            raise ValueError('Examples require specimen markers')
        if re.search(r'/(?:Users|Volumes)/|file://', text):
            raise ValueError('Synthetic example contains a host path')
        destination = LIB / 'examples' / ident / (key + '.md')
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
        row['examples'].append({'id': ident + '/' + key, 'brief_id': brief, 'path': str(destination.relative_to(LIB)), 'sha256': sha(raw)})
    (LIB / row['guide_path']).write_text(relink(guide, f'../source-edition/companions/{ident}/'))
    (LIB / 'source-edition/guides' / (ident + '.md')).write_text(source_guide)
    (LIB / 'source-edition/readings' / (ident + '.md')).write_text(relink(readings, f'../companions/{ident}/'))
    for name, text in companions.items():
        companion_path = LIB / 'source-edition/companions' / ident / name
        companion_path.parent.mkdir(parents=True, exist_ok=True)
        companion_path.write_text(text)
    append_record(before_catalog['records'], row)
    before_catalog['record_count'] = len(before_catalog['records'])
    write_json(LIB / 'records/catalog.json', before_catalog)
    edition = read_json(LIB / 'source-edition/edition.json')
    refs = row.get('authority_sources', [])
    edition['records'][ident] = {'styleAuthority': {'title': row['name'] + ' · Complete writing guide', 'owner': 'Writing Library', 'path': f'guides/{ident}.md', 'sources': refs}, 'humanReferences': [], 'samples': [], 'readingPath': f'readings/{ident}.md', 'bundleFiles': [f'guides/{ident}.md', f'readings/{ident}.md'] + [f'companions/{ident}/{name}' for name in companions], 'formats': []}
    for rel in edition['records'][ident]['bundleFiles']:
        edition['files'][rel] = sha((LIB / 'source-edition' / rel).read_bytes())
    write_json(LIB / 'source-edition/edition.json', edition)
    node = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'
    parser = LIB / 'validation/vendor/marked/lib/marked.esm.js'
    env = dict(os.environ, VOICE_LAB_MARKED=str(parser))
    js = "const fs=require('node:fs');const {measure}=require(process.argv[1]);(async()=>{const paths=JSON.parse(fs.readFileSync(0,'utf8'));const rows=[];for(const p of paths){rows.push(await measure(fs.readFileSync(p,'utf8')))}process.stdout.write(JSON.stringify(rows))})().catch(e=>{process.stderr.write(e.message);process.exitCode=1})"
    measured = json.loads(subprocess.run([str(node), '-e', js, str(LIB / 'metrics/measure.cjs')], input=json.dumps([str(LIB / ex['path']) for ex in row['examples']]), text=True, capture_output=True, check=True, env=env).stdout)
    corpus = read_json(LIB / 'evaluation/metrics-corpus-v1.json')
    for ex, measurement in zip(row['examples'], measured):
        measurement.update(sample_id=ex['id'], path=ex['path'])
        if measurement['text_sha256'] != ex['sha256']:
            raise ValueError('Extractor identity differs from source bytes')
        append_record(corpus['samples'], measurement, 'sample_id')
    write_json(LIB / 'evaluation/metrics-corpus-v1.json', corpus)
    acceptance = read_json(LIB / 'evaluation/content-acceptance.json')
    acceptance['current_files'].update({ex['path']: ex['sha256'] for ex in row['examples']})
    write_json(LIB / 'evaluation/content-acceptance.json', acceptance)
    qa = profile(row, LIB)
    write_json(LIB / 'validation/profiles' / (ident + '.json'), qa)
    manifest = read_json(LIB / 'validation/manifest.json')
    manifest['files'][f'validation/profiles/{ident}.json'] = sha((LIB / 'validation/profiles' / (ident + '.json')).read_bytes())
    write_json(LIB / 'validation/manifest.json', manifest)
    style = style_entry(row, row, source_guide, source_guide)
    style_path = LIB / 'styles' / ident / 'STYLE.md'
    style_path.parent.mkdir(parents=True, exist_ok=True)
    style_path.write_text(style)
    # Refresh only this selected reference set; all other resources are owned
    # by their existing projections and must remain byte-identical.
    axes_doc, axis_profiles = load_profiles(LIB)
    for name, content in render_files(axes_doc, axis_profiles[ident]).items():
        target = LIB / 'styles' / ident / 'axes' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    pin_path = OWNER / 'runtime/writing-voice-library/approved-sources.json'
    pins = read_json(pin_path)
    selected_paths = [row['guide_path'], *[ex['path'] for ex in row['examples']],
                      f'source-edition/guides/{ident}.md', f'source-edition/readings/{ident}.md',
                      f'styles/{ident}/STYLE.md', f'validation/profiles/{ident}.json',
                      f'axes/{ident}-authoring.json']
    selected_paths += [f'source-edition/companions/{ident}/{name}' for name in companions]
    selected_paths += [f'styles/{ident}/axes/{name}' for name in render_files(axes_doc, axis_profiles[ident])]
    for rel in selected_paths:
        pins['files'][rel] = sha((LIB / rel).read_bytes())
    pins.update(catalogSha256=sha((LIB / 'records/catalog.json').read_bytes()), sourceEditionSha256=sha((LIB / 'source-edition/edition.json').read_bytes()), validationManifestSha256=sha((LIB / 'validation/manifest.json').read_bytes()), axesSha256=sha((LIB / 'axes/four-axes.json').read_bytes()))
    write_json(pin_path, pins)
    samples = []
    texts = [guide] + [body((LIB / ex['path']).read_text()) for ex in row['examples']]
    rendered = render(texts, node, parser)
    labels = row.get('example_labels', ['Synthetic feature explanation', 'Synthetic workshop invitation', 'Synthetic serious incident'])
    for ex, m, h, label in zip(row['examples'], measured, rendered[1:], labels):
        features = [{'id': f['feature_id'], 'label': FEATURES[i]['label'], 'value': f['raw_value'], 'unit': f['unit'], 'status': f['status'], 'reason': f['reason']} for i, f in enumerate(m['features'])]
        samples.append({'id': ex['id'], 'key': ex['id'].split('/')[1], 'briefId': ex['brief_id'], 'label': label, 'markdown': body((LIB / ex['path']).read_text()), 'sourceMarkdown': (LIB / ex['path']).read_text(), 'sha256': ex['sha256'], 'kind': 'synthetic', **h, 'measurement': {'features': features, 'counts': m['counts'], 'eligible': m['full_fingerprint_eligible'], 'extractorVersion': m['extractor_version'], 'textSha256': m['text_sha256'], 'separation': 'uncalibrated'}})
    quote = row['quote']
    if quote not in samples[0]['markdown']:
        raise ValueError('Quote must be an exact span from synthetic specimen')
    if a.cover:
        if a.cover.suffix.lower() != '.png':
            raise ValueError('Cover source must be actual PNG')
        cover = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="900" height="540" viewBox="0 0 900 540"><image width="900" height="540" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/png;base64,' + base64.b64encode(a.cover.read_bytes()).decode() + '"/></svg>'
    elif a.canonical_p49:
        cover = (a.output / 'previews/P49.svg').read_text()
    else:
        import html
        cover = '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="540" viewBox="0 0 900 540"><rect width="900" height="540" fill="#FFF7F0"/><text x="60" y="110" font-family="Georgia,serif" font-size="42" fill="#30293D">Fresh Curiosity</text><text x="60" y="160" font-family="sans-serif" font-size="20" fill="#30293D">P49 · Independent writing candidate</text><text x="60" y="260" font-family="Georgia,serif" font-size="24" fill="#30293D">' + html.escape(quote[:75]) + '</text><text x="60" y="480" font-family="sans-serif" font-size="16" fill="#30293D">Synthetic demonstration · descriptive measurements only</text></svg>'
    preview = a.output / 'previews/P49.svg'
    preview.parent.mkdir(parents=True, exist_ok=True)
    preview.write_text(cover)
    native_cover = OWNER / 'runtime/writing-voice-library/ui/previews/P49.svg'
    native_cover.parent.mkdir(parents=True, exist_ok=True)
    native_cover.write_text(cover)
    rec = {'id': ident, 'name': row['name'], 'version': row['version'], 'type': row['resource_type'], 'typeLabel': TYPE_LABELS[row['resource_type']], 'description': row['description'], 'mechanism': row['mechanism'], 'rhythm': row['rhythm'], 'tags': row['tags'], 'route': row['route'], 'skillName': row['skill_name'], 'truthBoundary': row['truth_boundary'], 'neighborDifference': row['neighbor_difference'], 'neighbors': row['nearest_neighbors'], 'separation': row['separation'], 'repeatability': row['repeatability'], 'evidenceStatus': row['evidence_status'], 'independenceStatus': row['independence_status'], 'guideMarkdown': guide, 'guideHtml': rendered[0]['html'], 'samples': samples, 'targets': row['communication_targets'], 'observations': {'status': 'not_estimated', 'ratings': [], 'note': 'No empirical human voice measurement or audience rating is asserted.'}, 'sources': refs, 'researchLimits': row['research']['limits'], 'sourceEdition': edition['version'], 'humanReferences': [], 'styleAuthority': {'title': row['name'] + ' · Complete writing guide', 'owner': 'Writing Library', 'sources': refs, 'html': rendered[0]['html'], 'formats': []}, 'quote': {'text': quote, 'sampleId': samples[0]['id'], 'briefId': samples[0]['briefId'], 'attribution': 'Original fictional demonstration · AI-authored synthetic sample', 'sourceExact': True, 'sourceSha256': samples[0]['sha256']}, 'downloads': {'bundle': f'downloads/{ident}/bundle.zip', 'skill': f'downloads/{ident}/bundle.zip', 'raw': f'downloads/{ident}/raw.json', 'markdown': f'downloads/{ident}/examples.md', 'profile': f'downloads/{ident}/profile.json', 'preview': f'previews/{ident}.svg'}}
    files = {'references/guide.md': relink(guide, 'source-companions/'), 'references/readings.md': relink(readings, 'source-companions/'), 'STYLE.md': style.replace('../../source-edition/guides/P49.md', 'references/guide.md').replace('../../source-edition/readings/P49.md', 'references/readings.md').replace('../../examples/P49/specimen.md', 'examples/specimen.md').replace('../../validation/profiles/P49.json', 'references/qa-profile.json')}
    files.update({'references/source-companions/' + name: text for name, text in companions.items()})
    axes = LIB / 'styles' / ident / 'axes'
    if not axes.is_dir():
        axes = LIB / 'axes'
    if axes.is_dir():
        for path in axes.rglob('*'):
            if path.is_file() and path.suffix in ('.md', '.json'):
                text = path.read_text().replace('../../../source-edition/companions/P49/', '../references/source-companions/').replace('source-edition/companions/P49/', 'references/source-companions/')
                files['axes/' + str(path.relative_to(axes))] = text
    for ex in row['examples']:
        files['examples/' + Path(ex['path']).name] = (LIB / ex['path']).read_text()
    files.update(portable_files(row, LIB))
    skill = f'---\nname: writing-resource-p49\ndescription: "Apply {row["name"]} using the complete authority guide, synthetic examples and explicit fact boundaries."\n---\n\n# {row["name"]}\n\nRead [STYLE.md](STYLE.md), the [complete guide](references/guide.md) and [source boundaries](references/readings.md). This independent editorial candidate routes to P49, without modules. Use the actual user brief, preserve facts and uncertainty, and never import fictional example content. Examples are synthetic. Descriptive fingerprints measure those examples only; they do not validate personal voice, preference, originality or repeatability.\n' + PORTABLE_INSTRUCTIONS
    files['SKILL.md'] = skill
    if a.canonical_p49 and 'briefs.json' in companions:
        skill = skill.replace('Examples are synthetic.',
            'Examples are synthetic. When reviewing these teaching fixtures, read their '
            '[exact fictional briefs](references/source-companions/briefs.json). '
            'These facts never replace the actual artifact brief.')
        files['SKILL.md'] = skill
    files['agent-manifest.json'] = json.dumps({'schema': 'wvl-portable-agent/1', 'resourceId': ident, 'baseProfileId': ident, 'moduleIds': [], 'entrypoint': 'SKILL.md', 'styleEntrypoint': 'STYLE.md', 'privacyScope': 'generic_synthetic', 'sourceVersion': row['version'], 'status': 'editorial_candidate_uncalibrated', 'generatedProjection': True})
    files['README.md'] = '# Portable writing template\n\nRead SKILL.md and the complete guide. The bundle requires no network to read. Node 20+ is required for optional offline text measurements. Installation is separate. No private personal corpus is included.\n'
    import posixpath
    for name, value in files.items():
        if not name.endswith('.md'):
            continue
        for target in re.findall(r'\]\(([^)]+)\)', value):
            relative = target.strip('<>').split('#')[0]
            if relative and ':' not in relative and posixpath.normpath(posixpath.join(posixpath.dirname(name), relative)) not in files:
                raise ValueError('Unclosed portable writing link: ' + name + ' -> ' + target)
    archive = zip_bytes({'writing-resource-p49/' + name: value for name, value in files.items()})
    dest = a.output / 'downloads' / ident
    dest.mkdir(parents=True, exist_ok=True)
    (dest / 'bundle.zip').write_bytes(archive)
    (dest / 'SKILL.md').write_text(skill)
    (dest / 'examples.md').write_text('\n\n---\n\n'.join(s['sourceMarkdown'] for s in samples))
    write_json(dest / 'raw.json', {'schema': 'wvl-public-raw/1', 'resourceId': ident, 'status': 'synthetic_examples_only_raw_descriptive_features_not_quality', 'samples': measured})
    if a.guide:
        shutil.copy2(a.guide, dest / 'guide.pdf')
        rec['downloads']['pdf'] = f'downloads/{ident}/guide.pdf'
        rec['downloads']['pdfSha256'] = sha(a.guide.read_bytes())
        rec['downloads']['pdfBytes'] = a.guide.stat().st_size
    if a.download_base:
        if not a.download_base.startswith('https://github.com/JonathanKHobson/shareables/releases/download/'):
            raise ValueError('Unexpected release base')
        rec['downloads']['bundle'] = rec['downloads']['skill'] = a.download_base.rstrip('/') + '/writing-resource-p49.zip'
        if a.guide:
            rec['downloads']['pdf'] = a.download_base.rstrip('/') + '/Fresh-Curiosity-Writing-Guide.pdf'
    rec['downloads']['bundleSha256'] = sha(archive)
    rec['downloads']['bundleBytes'] = len(archive)
    # Preserve explicitly managed additions from the shared axis/projection
    # owner while replacing the selected source authority and measurements.
    rec = {**prior_public, **rec}
    if a.canonical_p49 and not a.download_base:
        for key in ('bundle', 'skill'):
            if key in prior_public.get('downloads', {}):
                rec['downloads'][key] = prior_public['downloads'][key]
    rec['quote']['briefId'] = samples[0]['briefId']
    if 'axes' in rec:
        rec['axes'] = profile_data(axes_doc, axis_profiles[ident])
    if not a.guide:
        for key in ('pdf', 'pdfSha256', 'pdfBytes'):
            if key in prior_public.get('downloads', {}):
                rec['downloads'][key] = prior_public['downloads'][key]
    append_record(before_public['records'], rec)
    if a.canonical_p49 and 'briefs.json' in companions:
        briefs = json.loads(companions['briefs.json'])
        if briefs.get('status') != 'fictional_exercises_only':
            raise ValueError('P49 briefs must remain explicitly fictional')
        expected_briefs = {ex['brief_id'] for ex in row['examples']}
        if {brief['id'] for brief in briefs['briefs']} != expected_briefs:
            raise ValueError('P49 brief fixtures do not match the retained samples')
        for brief in briefs['briefs']:
            append_record(before_public['briefs'], {'id': brief['id'], 'markdown':
                '**Fictional exercise.** ' + brief['task'] + '\n\nFacts:\n' +
                '\n'.join('- ' + fact for fact in brief['facts']) + '\n\nUnknowns:\n' +
                '\n'.join('- ' + item for item in brief['unknowns'])})
    public_axes_path = a.output / 'data/four-axes.json'
    if public_axes_path.is_file():
        public_axes = read_json(public_axes_path)
        append_record(public_axes['profiles'], axis_profiles[ident])
        write_json(public_axes_path, public_axes)
    write_json(dest / 'profile.json', clean(rec))
    before_public['counts']['resources'] = len(before_public['records'])
    before_public['counts']['profileSkills'] = sum(r['type'] in ('legacy_profile', 'voice_candidate') for r in before_public['records'])
    before_public['counts']['commonSamples'] = sum(sum(s['briefId'] in ('E-B01', 'E-B02', 'E-B03') for s in r['samples']) for r in before_public['records'])
    before_public['counts']['samples'] = sum(len(r['samples']) for r in before_public['records'])
    write_json(a.output / 'catalog.json', before_public)
    if not a.preserve_shared_metadata:
        schema_path = a.output / 'agents/catalog.schema.json'
        schema = read_json(schema_path)
        schema['properties']['records'].pop('maxItems', None)
        write_json(schema_path, schema)
        llms = a.output / 'llms.txt'
        text = llms.read_text()
        if 'P49 Fresh Curiosity' not in text:
            text += '\n## Added own-brand writing template\n\nP49 Fresh Curiosity is an independent editorial candidate with three labeled synthetic examples, a complete public authority guide and separate intended tone versus measured text features. Private personal evidence is excluded. Use its exact current bundle URL in catalog.json.\n'
            llms.write_text(text)
    for key, old in preserved.items():
        assert next(r for r in read_json(LIB / 'records/catalog.json')['records'] if r['id'] == key) == old
    for key, old in preserved_public.items():
        assert next(r for r in read_json(a.output / 'catalog.json')['records'] if r['id'] == key) == old
    for name, expected in bundle_before.items():
        assert sha((a.output / name).read_bytes()) == expected
    native = OWNER / 'templates' / ident
    native.mkdir(parents=True, exist_ok=True)
    (native / 'SKILL.md').write_text(skill.replace('(STYLE.md)', '(../../library/voice-library/styles/P49/STYLE.md)').replace('(references/guide.md)', '(../../library/voice-library/source-edition/guides/P49.md)').replace('(references/readings.md)', '(../../library/voice-library/source-edition/readings/P49.md)').replace('(references/source-companions/briefs.json)', '(../../library/voice-library/source-edition/companions/P49/briefs.json)').split('## Humanizer Light')[0])
    write_json(a.evidence, {'status': 'registered_and_projected_locally_not_installed_not_published', 'id': ident, 'canonicalCount': len(before_catalog['records']), 'publicCount': len(before_public['records']), 'preservedCanonicalRecords': len(preserved), 'preservedPublicRecords': len(preserved_public), 'preservedZipFiles': len(bundle_before), 'sourceCatalogSha256': pins['catalogSha256'], 'bundleSha256': sha(archive), 'measurementBasis': 'three_actual_synthetic_examples_only', 'privateCorpusIncluded': False})
    print(json.dumps({'id': ident, 'records': len(before_catalog['records']), 'bundleSha256': sha(archive), 'evidence': str(a.evidence)}))

if __name__ == '__main__':
    main()
