#!/usr/bin/env python3
"""Generate short, source-traceable STYLE.md entrypoints for registered resources.

The source-edition guides remain the editable style specifications. These
entries are navigation views, regenerated from those guides and the catalog.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / 'library/voice-library'


def section(markdown, heading, next_level=2):
    hashes = '#' * next_level
    pattern = rf'(?ms)^{hashes} {re.escape(heading)}\n\n(.*?)(?=^{hashes} |\Z)'
    match = re.search(pattern, markdown)
    if not match:
        raise ValueError(f'Missing source guide section: {heading}')
    return match.group(1).strip()


def example(markdown):
    match = re.search(r'(?ms)^### Follows the mechanism\n\n(.*?)(?=^### Near miss)', markdown)
    if not match:
        raise ValueError('Missing worked contrast')
    return match.group(1).strip()


def detail(markdown, alternatives):
    for heading in alternatives:
        try:
            return section(markdown, heading, 3)
        except ValueError:
            pass
    raise ValueError('Missing style detail: ' + ', '.join(alternatives))


def style_entry(row, base, selected_guide, base_guide):
    """Use links relative to library/voice-library/styles/<ID>/STYLE.md."""
    ident = row['id']
    selected_sha = hashlib.sha256(selected_guide.encode()).hexdigest()
    base_sha = hashlib.sha256(base_guide.encode()).hexdigest()
    movement = section(selected_guide, 'Core movement')
    rules = section(selected_guide, 'Working rules')
    reader = detail(selected_guide, ('Reader and use', 'Audience, fit and unsuitable uses'))
    expression = detail(selected_guide, ('Language and feeling', 'Sentence and paragraph devices'))
    # These sections are authored as three inspectable rules; fail if the
    # source shape changes so a generated card never silently loses content.
    rule_lines = [line for line in rules.splitlines() if line.startswith('- ')]
    if len(rule_lines) != 3:
        raise ValueError(f'{ident}: expected three source working rules')
    demonstrated = example(selected_guide)
    base_line = (f'- [Base profile {base["id"]} guide](../../source-edition/guides/{base["id"]}.md) '
                 f'(`sha256:{base_sha}`)\n') if base['id'] != ident else ''
    return (f'# {ident} · {row["name"]} · STYLE.md\n\n'
            'Generated navigation view of the Writing Library specification. '
            'The linked complete guide defines this resource; this file does not '
            'add an independent rule, personal identity or universal writing standard.\n\n'
            f'**Use:** {row["description"]}\n\n'
            f'**Route:** selected {ident}; base {base["id"]}; modules '
            f'{", ".join(row["route"]["module_ids"]) or "none"}.\n\n'
            f'## Movement\n\n{movement}\n\n'
            f'## Reader and expression\n\n**Fit.** {reader}\n\n'
            f'**Voice and mechanics.** {expression}\n\n'
            '## Working rules from the complete guide\n\n'
            + '\n\n'.join(rule_lines) + '\n\n'
            f'## Synthetic example\n\n{demonstrated}\n\n'
            'This is a constructed teaching example. Use its movement, not its '
            'names, facts, wording or implied authorization. The complete guide '
            'also shows a near miss and explains the difference.\n\n'
            '## Read before drafting\n\n'
            f'- [Selected complete style guide](../../source-edition/guides/{ident}.md) '
            f'(`sha256:{selected_sha}`)\n'
            + base_line
            + '- [Four-axis editorial reference](axes/README.md) '
            '(read after the complete selected/base and routed module guides, before drafting)\n'
            + f'- [Selected historical reading notes](../../source-edition/readings/{ident}.md)\n'
            f'- [Selected synthetic examples](../../examples/{ident}/specimen.md)\n'
            f'- [Selected QA profile](../../validation/profiles/{ident}.json)\n\n'
            '## Boundaries and unknowns\n\n'
            f'{row["truth_boundary"]}\n\n'
            'The selected and base guides govern task fit, required and optional '
            'moves, exceptions, and conformance. The user brief governs facts, '
            'format and authorization. Historical readings illustrate techniques; '
            'they are not exact output targets. Separation remains uncalibrated; '
            'repeatability and reader preference have not been established. '
            'Automated QA cannot certify meaning or factual fidelity.\n')


def entries(library=LIBRARY):
    catalog = json.loads((library / 'records/catalog.json').read_text())
    rows = catalog['records']
    by_id = {row['id']: row for row in rows}
    if len(rows) != catalog['record_count'] or len(by_id) != len(rows):
        raise ValueError('Catalog count must match its unique registered resources')
    for row in rows:
        base = by_id[row['route']['base_profile_id']]
        selected_guide = (library / 'source-edition/guides' / (row['id'] + '.md')).read_text()
        base_guide = (library / 'source-edition/guides' / (base['id'] + '.md')).read_text()
        yield row['id'], style_entry(row, base, selected_guide, base_guide)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Fail if generated entries are stale')
    args = parser.parse_args()
    stale = []
    for ident, content in entries():
        path = LIBRARY / 'styles' / ident / 'STYLE.md'
        if args.check:
            if not path.exists() or path.read_text() != content:
                stale.append(ident)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    if stale:
        raise SystemExit('Stale STYLE.md entries: ' + ', '.join(stale))
    count = json.loads((LIBRARY / 'records/catalog.json').read_text())['record_count']
    print(f'{count} STYLE.md entries verified' if args.check else f'{count} STYLE.md entries generated')


if __name__ == '__main__':
    main()
