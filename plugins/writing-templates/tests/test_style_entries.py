"""Keep all generated style entrypoints traceable to current source guides."""
import re
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_style_entries import entries  # noqa: E402


class StyleEntryTests(unittest.TestCase):
    def test_all_entries_match_sources_and_links_resolve(self):
        library = ROOT / 'library/voice-library'
        generated = dict(entries(library))
        catalog = json.loads((library / 'records/catalog.json').read_text())
        self.assertEqual(len(generated), catalog['record_count'])
        self.assertEqual(set(generated), {p.parent.name for p in (library / 'styles').glob('*/STYLE.md')})
        for ident, expected in generated.items():
            path = library / 'styles' / ident / 'STYLE.md'
            self.assertEqual(path.read_text(), expected, ident)
            for link in re.findall(r'\]\(([^\n)]+)\)', expected):
                if ':' not in link:
                    self.assertTrue((path.parent / link.split('#')[0]).resolve().is_file(), (ident, link))

    def test_conditional_skills_link_their_style_entry(self):
        for path in (ROOT / 'templates').glob('*/SKILL.md'):
            ident = path.parent.name
            if ident == 'create-writing-voice':
                continue
            link = f'../../library/voice-library/styles/{ident}/STYLE.md'
            self.assertIn(f']({link})', path.read_text())
            self.assertTrue((path.parent / link).resolve().is_file())


if __name__ == '__main__':
    unittest.main()
