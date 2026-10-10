import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('activity_search', ROOT / 'skills/lesson-experience-design/scripts/search_activities.py')
LIB = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LIB)


class ActivitySearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = LIB.load_library(LIB.DEFAULT_LIBRARY)

    def test_time_filter_fits_upper_bound(self):
        result = LIB.search(self.rows, 'retrieval', 20, 'solo')
        self.assertTrue(result)
        self.assertTrue(all(r['duration_minutes']['max'] <= 20 for r in result))
        self.assertEqual(LIB.search(self.rows, max_minutes=1), [])

    def test_query_and_id(self):
        self.assertTrue(LIB.search(self.rows, 'play evidence'))
        self.assertEqual(LIB.search(self.rows, activity_id='fof-card-0051')[0]['title'], 'SCAVENGER HUNT')
        self.assertEqual(LIB.search(self.rows, 'term-that-cannot-match'), [])

    def test_every_card_has_evidence_and_rights(self):
        self.assertEqual(len(self.rows), 31)
        for row in self.rows:
            self.assertIn('not learner-piloted', row['readiness'])
            self.assertTrue(row.get('origin_and_rights') or row.get('rights_handling'))
            self.assertEqual(len(row['source_sha256']), 64)

    def test_duplicate_and_malformed_fail(self):
        data = json.loads(LIB.DEFAULT_LIBRARY.read_text())
        bad_cases = []
        duplicate = copy.deepcopy(data)
        duplicate['activities'].append(duplicate['activities'][0])
        bad_cases.append(duplicate)
        malformed = copy.deepcopy(data)
        malformed['activities'][0]['duration_minutes']['max'] = -1
        bad_cases.append(malformed)
        for bad in bad_cases:
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'bad.json'
                path.write_text(json.dumps(bad))
                with self.assertRaises(ValueError):
                    LIB.load_library(path)


if __name__ == '__main__':
    unittest.main()
