"""Project reviewed historical readings and local style specifications.

The source edition is separate from measured specimens and canonical routing.
It cannot upgrade validation claims or replace retained examples.
"""
import hashlib
import json
from pathlib import Path


def edition_root(library):
    return Path(library) / 'source-edition'


def load_edition(library):
    root = edition_root(library)
    path = root / 'edition.json'
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    if data['schema'] != 'wvl-source-edition/1':
        raise ValueError('Unknown source edition')
    for name, expected in data['files'].items():
        path = (root / name).resolve()
        if not path.is_relative_to(root.resolve()):
            raise ValueError('Source path escape')
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Stale source edition: ' + name)
    return data


def enrich_records(records, library, render, node, parser):
    edition = load_edition(library)
    if not edition:
        return
    root = edition_root(library)
    queue, targets = [], []
    def markdown(target, path):
        target['markdown'] = (root / path).read_text()
        queue.append(target['markdown'])
        targets.append(target)
    for rec in records:
        extra = edition['records'][rec['id']]
        rec['sourceEdition'] = edition['version']
        rec['humanReferences'] = extra['humanReferences']
        authority = dict(extra['styleAuthority'])
        markdown(authority, authority['path'])
        authority['formats'] = []
        for fmt in extra.get('formats', []):
            item = dict(fmt)
            markdown(item, item['path'])
            authority['formats'].append(item)
        rec['styleAuthority'] = authority
        for source in extra['samples']:
            item = dict(source)
            markdown(item, item['path'])
            item.update(id=rec['id'] + '/' + item['key'], briefId='HUMAN-READING',
                        kind='human', measurement=None)
            item['sourceMarkdown'] = item['markdown']
            item['sha256'] = hashlib.sha256(item['markdown'].encode()).hexdigest()
            rec['samples'].append(item)
        originals = [s for s in rec['samples'] if s.get('kind') != 'human']
        historical = [s for s in rec['samples'] if s.get('kind') == 'human']
        # Keep the familiar first sample, then make human readings one click away.
        rec['samples'] = originals[:1] + historical + originals[1:]
        for s in originals:
            if s['key'].startswith('historical-'):
                s['label'] = {'historical-full': 'Decision memo', 'historical-update': 'Schedule update',
                              'historical-invitation': 'Invitation', 'historical-transfer': 'New-topic example'}.get(s['key'], s['label'])
    for target, rendered in zip(targets, render(queue, node, parser)):
        target.update(rendered)


def bundle_references(record, files, library):
    """Return explicit loading instructions and add a closed reference tree."""
    if 'styleAuthority' not in record:
        return ''
    edition = load_edition(library)
    entry = edition['records'][record['id']]
    root = edition_root(library)
    paths = set(entry['bundleFiles'])
    # A module's base remains a dependency, including its written specification.
    base_id = record['route']['base_profile_id']
    paths.update(edition['records'][base_id]['bundleFiles'])
    for path in sorted(paths):
        files['references/source-edition/' + path] = (root / path).read_text()
    guide = entry['styleAuthority']['path']
    readings = entry['readingPath']
    return ('\n## Style specification and human readings\n\n'
            f'Read the [style specification](references/source-edition/{guide}) and '
            f'[selected historical readings](references/source-edition/{readings}) before drafting. '
            'Use the stated technique and its limits, not a source author’s identity or biography. '
            'Historical passages illustrate particular choices; they are not exact-output targets. '
            'Read a relevant retained library demonstration as well. Preserve quotations as quotations; '
            'do not carry source names, claims, dates, cultural attitudes or memorable wording into new prose. '
            'Follow the user’s actual facts, genre and audience. Apply an APA or MLA format reference only '
            'when that separate format is requested; never blend their citation conventions. '
            'Before returning the draft, check its movement against the specification and check all '
            'facts against the brief. Optional devices remain optional.\n')


def download_sample(sample):
    text = '## ' + sample['label'] + '\n\n' + sample['sourceMarkdown']
    if sample.get('kind') != 'human':
        return text
    source = sample['source']
    return (text + '\n\nSource: [' + source['title'] + '](' + source['url'] + '). '
            + source['author'] + '. ' + source['publicationDate'] + '.\n\n'
            + source.get('locator', '') + '\n\n' + source.get('relationship', '') + '\n\n'
            + source.get('credit', '') + '\n\n' + source.get('rights', '')
            + '. [Reuse terms](' + source.get('rightsUrl', source['url']) + ').\n')


def source_profile(value):
    """Download profiles retain source Markdown; rendered duplicates stay in the UI catalog."""
    if isinstance(value, dict):
        return {key: source_profile(item) for key, item in value.items()
                if key not in {'html', 'plainText', 'guideHtml', 'guidePlainText'}}
    if isinstance(value, list):
        return [source_profile(item) for item in value]
    return value
