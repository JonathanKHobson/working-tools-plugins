"""Project the reviewed measurement contract into native and portable skill QA."""
import hashlib
import json
import re
import statistics
from pathlib import Path

SCHEMA = 'wvl-qa-profile/1'


def serialize(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n'


def profile(row, library):
    library = Path(library)
    catalog = json.loads((library / 'records/catalog.json').read_text())
    records = {r['id']: r for r in catalog['records']}
    corpus = json.loads((library / 'evaluation/metrics-corpus-v1.json').read_text())
    samples = {s['sample_id']: s for s in corpus['samples']}
    selected = []
    for example in row['examples']:
        raw = (library / example['path']).read_bytes()
        sample = samples[example['id']]
        if hashlib.sha256(raw).hexdigest() != example['sha256'] or sample['text_sha256'] != example['sha256']:
            raise ValueError('Stale QA measurement: ' + example['id'])
        selected.append(sample)
    observed = []
    for feature in selected[0]['features']:
        fid = feature['feature_id']
        values = [f['raw_value'] for s in selected for f in s['features']
                  if f['feature_id'] == fid and f['raw_value'] is not None]
        observed.append({'featureId': fid, 'unit': feature['unit'], 'n': len(values),
                         'min': min(values) if values else None,
                         'median': statistics.median(values) if values else None,
                         'max': max(values) if values else None})
    checks = []
    guide_ids = list(dict.fromkeys([row['route']['base_profile_id'], row['id']] + row['route']['module_ids']))
    for ident in guide_ids:
        text = (library / 'source-edition/guides' / (ident + '.md')).read_text()
        for heading in ('Working rules', 'Avoid'):
            match = re.search(r'^## ' + re.escape(heading) + r'\n(.*?)(?=^## |\Z)', text, re.M | re.S)
            if not match:
                raise ValueError('Missing required QA rule section: ' + ident + ' ' + heading)
            for index, label in enumerate(re.findall(r'^- (.+)$', match[1], re.M), 1):
                checks.append({'id': ident + ('-require-' if heading == 'Working rules' else '-avoid-') + str(index),
                               'label': label, 'source': 'source-edition/guides/' + ident + '.md'})
    checks.extend([
        {'id': 'facts', 'label': 'Preserve every supplied fact, exact quotation, uncertainty, authorization and applicable constraint.', 'source': 'brief supplied by user'},
        {'id': 'mechanism', 'label': 'Check the complete selected/base guides: movement, task fit, optional devices and expressly permitted exceptions.', 'source': records[row['id']]['guide_path']},
        {'id': 'format', 'label': 'Check the separately requested format, if any. APA and MLA are distinct; do not combine their requirements.', 'source': 'selected format guide, if applicable'},
    ])
    observed_note = ('Three retained suitable fictional specimens. No historical reading enters these measurements. '
                     'Sparse features have fewer observations.' if row['id'] in {'P50', 'P51', 'P52', 'P53'} else
                     'Three retained task specimens, including a serious-incident override. No historical reading enters these measurements. Sparse features have fewer observations.')
    return {'schema': SCHEMA, 'resourceId': row['id'], 'name': row['name'], 'route': row['route'],
            'extractorVersion': 'wvl-metrics/1.0.0', 'hardConstraints': [],
            'toneTargets': row['communication_targets'],
            'incidentOverride': {k: v for k, v in row['incident_override'].items() if isinstance(v, list)},
            'observedFeatures': observed, 'manualChecks': checks,
            'observedBasis': {'status': 'descriptive_only_not_acceptance_limits',
                              'sampleIds': [s['sample_id'] for s in selected],
                              'sourceHashes': {s['sample_id']: s['text_sha256'] for s in selected},
                              'note': observed_note}}


def portable_files(row, library):
    library = Path(library)
    validation = library / 'validation'
    files = {'references/qa-profile.json': serialize(profile(row, library)),
             'references/validation.md': (validation / 'WORKFLOW.md').read_text(),
             'references/editorial-companion.md': (validation / 'editorial-companion.md').read_text()}
    for name in ('validate.cjs', 'validate.py'):
        files['scripts/' + name] = (validation / name).read_text()
    for path in (library / 'metrics').glob('*.cjs'):
        files['scripts/metrics/' + path.name] = path.read_text()
    files['references/measurement-method.md'] = (library / 'metrics/README.md').read_text()
    for path in (validation / 'vendor/marked').rglob('*'):
        if path.is_file():
            files['scripts/vendor/marked/' + path.relative_to(validation / 'vendor/marked').as_posix()] = path.read_text()
    return files


PORTABLE_INSTRUCTIONS = '''
## Humanizer Light

After drafting, apply the [compact editorial pass](references/editorial-companion.md). Check stock framing, unsupported claims and empty repetition while preserving the selected template's deliberate mechanics, punctuation and author voice. This pass is part of the template workflow.

## Draft validation

After drafting and after each revision, follow [the QA workflow](references/validation.md). Run `python3 scripts/validate.py --input draft.md` from this skill folder (or `node scripts/validate.cjs --input draft.md`). The included [QA profile](references/qa-profile.json) selects this template. Python is an optional launcher; the original measurement engine requires Node 20 or newer. The pinned Markdown parser is included; no network or package install is needed.

Use the report to fix explicit constraint violations, review diagnostic deviations and check the guide rules and tone rubric. Re-run on the final text. Never widen a constraint to pass a draft, rewrite an attributed quotation, or trade meaning for a statistic. If execution is unavailable, perform the editorial review and say automated QA was not run. A successful script exit is not proof of full style conformity.
'''


if __name__ == '__main__':
    library = Path(__file__).resolve().parents[1] / 'library/voice-library'
    records = json.loads((library / 'records/catalog.json').read_text())['records']
    destination = library / 'validation/profiles'
    destination.mkdir(parents=True, exist_ok=True)
    for row in records:
        (destination / (row['id'] + '.json')).write_text(serialize(profile(row, library)))
    runtime = [p for p in (library / 'metrics').glob('*.cjs')]
    runtime += [library / ('validation/' + name) for name in ('validate.py', 'validate.cjs')]
    runtime += [p for p in (library / 'validation/vendor').rglob('*') if p.is_file()]
    files = runtime + [library / 'validation/WORKFLOW.md', library / 'validation/editorial-companion.md'] + list(destination.glob('*.json'))
    manifest = {'schema': 'wvl-qa-manifest/1',
                'runtimeFiles': sorted(str(p.relative_to(library)) for p in runtime),
                'files': {str(p.relative_to(library)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    (library / 'validation/manifest.json').write_text(serialize(manifest))
    print('Generated ' + str(len(records)) + ' QA profiles from reviewed sources.')
