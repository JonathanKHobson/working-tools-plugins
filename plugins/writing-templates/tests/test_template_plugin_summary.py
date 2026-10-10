"""Keep the portable plugin's type summary tied to catalog records."""
import json
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_template_plugin import catalog_type_summary  # noqa: E402


class TemplatePluginSummaryTests(unittest.TestCase):
    def test_summary_tracks_new_modules_without_a_hand_edited_count(self):
        catalog = json.loads((ROOT / 'library/voice-library/records/catalog.json').read_text())
        records = catalog['records']
        counts = Counter(row['resource_type'] for row in records)
        current = catalog_type_summary(records)
        self.assertIn(f'{counts["module"]} modules', current)
        expanded = records + [{'resource_type': 'module'} for _ in range(4)]
        self.assertIn(f'{counts["module"] + 4} modules', catalog_type_summary(expanded))
        self.assertIn(f'{counts["voice_candidate"]} voice candidates', catalog_type_summary(expanded))


if __name__ == '__main__':
    unittest.main()
