#!/usr/bin/env python3
"""Verify portable source closure, pinned identities and safe public metadata."""
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runtime/video-style-library'))
import catalog
import server


def main():
    manifest = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
    assert manifest['name'] == ROOT.name
    assert len(list((ROOT / 'skills').glob('*/SKILL.md'))) == 1
    source = json.loads((ROOT / 'docs/source-provenance.json').read_text())
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    assert digest(ROOT / 'data/catalog.json') == source['catalog']['sha256']
    for name, sha in source['chooser']['sha256'].items():
        assert digest(ROOT / 'runtime/library-chooser' / name) == sha
    methods = json.loads((catalog.SOURCE / 'SOURCE-MANIFEST.json').read_text())
    assert methods['revision'] == source['methodRevision']
    for rel, sha in methods['sha256'].items():
        assert digest(catalog.SOURCE / rel) == sha, rel
    assert {i: catalog.source_hash(i) for i in catalog.STYLE_IDS} == source['methodSourceHashes']
    families = catalog.load_families()
    assert len(families) == 30 and sum(len(f['examples']) for f in families) == 38
    assert len(catalog.library_items()) == 37
    text = (ROOT / 'data/catalog.json').read_text()
    projection = json.loads(text)
    assert projection.get('projection', '').startswith('Factual identity')
    excluded = {'starterPrompt', 'styleRules', 'usageGuidance', 'productionMethod', 'typography', 'palette', 'producerEvidence'}
    assert all(not excluded.intersection(example) for family in projection['families'] for example in family['examples'])
    assert not any(p in text for p in ('/Users/', '/Volumes/', 'file:', 'api_key', '.config/', 'storyboards.sqlite3'))
    assert not list(ROOT.rglob('*.sqlite3'))
    assert not any(p.is_symlink() for p in ROOT.rglob('*'))
    for p in ROOT.rglob('*'):
        if p.is_file() and p.suffix in {'.md', '.json', '.py', '.js', '.html', '.css', '.txt'}:
            assert not re.search(r'/(?:Users|Volumes)/[A-Za-z0-9]', p.read_text()), f'Private host path: {p}'
    html = server.render_html()
    assert '__LIBRARY_' not in html
    assert '__STORYBOARD_' not in server.render_storyboard_html()
    for path in (ROOT / 'skills').rglob('*.md'):
        for match in re.finditer(r'\]\(([^)#]+)', path.read_text()):
            target = match.group(1)
            if '://' not in target:
                assert (path.parent / target).exists(), (path, target)
    print(json.dumps({'families': 30, 'examples': 38, 'methods': 7,
                      'methodSourceFilesVerified': len(methods['sha256']),
                      'chooserFilesVerified': len(source['chooser']['sha256']),
                      'discoveryHeads': 1, 'privateStatePackaged': False}))


if __name__ == '__main__':
    main()
