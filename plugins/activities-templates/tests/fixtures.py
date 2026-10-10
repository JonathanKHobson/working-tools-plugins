"""Authored synthetic source notes; no private Atlas content."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'runtime/studio_library'))
from catalog import DOMAINS, build_index


def make_fixture(directory):
    directory = Path(directory)
    vault = directory / 'synthetic-vault'
    vault.mkdir(parents=True, exist_ok=True)
    entries = vault / '01 Patterns/Entries'
    entries.mkdir(parents=True, exist_ok=True)
    for domain, config in DOMAINS.items():
        rule = config.get('collections', {}).get('patterns', {})
        metadata = {'title': 'Fixture ' + domain, 'slug': 'fixture-' + domain,
                    'status': 'reviewed', 'categories': rule.get('categories', [])[:1],
                    'browse_group': next(iter(rule.get('groups', [])), ''),
                    'objective': 'Synthetic method for runtime verification only.'}
        body = '# Synthetic source\n\nThis authored example has no field validation.\n\n## Steps\n1. Inspect the example.\n2. Explain its limits.\n'
        (entries / (domain + '.md')).write_text('---\n' + json.dumps(metadata) + '\n---\n' + body, encoding='utf-8')
    cards = vault / '03 Collections/File-O-Fun/Cards'
    cards.mkdir(parents=True, exist_ok=True)
    for i in range(1, 5):
        metadata = {'title': f'Synthetic Group Practice {i}', 'slug': f'synthetic-group-practice-{i}',
                    'status': 'reviewed', 'browse_group': 'Design And Facilitation',
                    'players_min': 2, 'players_max': 8, 'timebox': '10-15 minutes',
                    'delivery_mode': 'online', 'objective': 'Test chooser presentation with authored examples.'}
        (cards / f'practice-{i}.md').write_text('---\n' + json.dumps(metadata) + '\n---\n# Example activity\n\n## Steps\n1. State a small goal.\n2. Compare two options.\n3. Record the next step.\n\n## Review\nSynthetic fixture only.\n', encoding='utf-8')
    db = directory / 'synthetic-catalog.sqlite'
    build_index(vault, db)
    return vault, db
