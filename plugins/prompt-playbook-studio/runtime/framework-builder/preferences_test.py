"""Isolated storage tests; never touch the user's preference file."""

import json
import os
from pathlib import Path
import stat
import tempfile
import unittest

from preferences import load_preferences, save_preferences


class PreferencesTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'private' / 'preferences.json'

    def test_missing_file_returns_defaults_without_creating_file(self):
        self.assertEqual(load_preferences(_path=self.path), {
            'version': 1, 'lensId': '', 'instructions': '', 'keepOpen': False,
        })
        self.assertFalse(self.path.exists())

    def test_roundtrip_and_exact_stored_schema(self):
        saved = save_preferences('systems-integrator', 'Remember my audience.\nUse examples.', True,
                                 _path=self.path)
        self.assertEqual(load_preferences(_path=self.path), saved)
        self.assertEqual(json.loads(self.path.read_text(encoding='utf-8')), saved)
        self.assertEqual(set(saved), {'version', 'lensId', 'instructions', 'keepOpen'})

    def test_rejects_invalid_types_lens_and_length(self):
        invalid = [
            (None, '', False), ('other', '', False),
            ('', None, False), ('', 'x' * 8001, False),
            ('', '', 1), ('', '', 'true'),
        ]
        for lens_id, instructions, keep_open in invalid:
            with self.subTest(values=(lens_id, type(instructions), keep_open)):
                with self.assertRaisesRegex(ValueError, 'Invalid framework preferences'):
                    save_preferences(lens_id, instructions, keep_open, _path=self.path)
                self.assertFalse(self.path.exists())
        self.assertEqual(len(save_preferences('', 'x' * 8000, False, _path=self.path)['instructions']), 8000)

    def test_malformed_existing_file_is_reported_and_preserved(self):
        self.path.parent.mkdir()
        for raw in ('{oops', '{"version":1,"lensId":"","instructions":"","keepOpen":false,"draft":"secret"}',
                    '{"version":1,"lensId":"","instructions":"","keepOpen":0}'):
            with self.subTest(raw=raw):
                self.path.write_text(raw, encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'Invalid framework preferences'):
                    load_preferences(_path=self.path)
                with self.assertRaisesRegex(ValueError, 'Invalid framework preferences'):
                    save_preferences('', '', False, _path=self.path)
                self.assertEqual(self.path.read_text(encoding='utf-8'), raw)

    def test_atomic_replace_and_private_permissions(self):
        save_preferences('', 'first', False, _path=self.path)
        first_inode = self.path.stat().st_ino
        save_preferences('skeptical-verifier', 'second', True, _path=self.path)
        self.assertNotEqual(self.path.stat().st_ino, first_inode)
        self.assertEqual(stat.S_IMODE(self.path.stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(self.path.parent.stat().st_mode), 0o700)
        self.assertEqual(load_preferences(_path=self.path)['instructions'], 'second')
        self.assertEqual(sorted(os.listdir(self.path.parent)), ['preferences.json'])


if __name__ == '__main__':
    unittest.main()
