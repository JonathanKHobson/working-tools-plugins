"""Fixture checks for the offline plugin change journal."""
from __future__ import annotations

import fcntl
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/plugin_change_record.py'
spec = importlib.util.spec_from_file_location('plugin_change_record', SCRIPT)
recorder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(recorder)


class RecorderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'plugins'
        self.root.mkdir()
        self.state = self.base / 'state'
        self.config = {'canonical_root': str(self.root), 'state_dir': str(self.state)}
        self.alpha = self.product('alpha')
        (self.alpha / 'scripts').mkdir()
        (self.alpha / 'scripts/run.py').write_text('one')

    def product(self, ident):
        path = self.root / ident
        (path / '.codex-plugin').mkdir(parents=True)
        (path / '.codex-plugin/plugin.json').write_text('{}')
        return path

    def journal(self):
        return json.loads((self.state / 'journal.json').read_text())

    def test_baseline_and_edit_add_delete_revert(self):
        first = recorder.record(self.config)
        self.assertEqual((first['status'], first['changed'], first['revision']), ('recorded', 0, 0))
        self.assertEqual(self.journal()['events'], [])
        source = self.alpha / 'scripts/run.py'
        source.write_text('two')
        self.assertEqual(recorder.record(self.config, 'test')['changed'], 1)
        event = self.journal()['events'][-1]
        self.assertEqual(event['origin'], 'test')
        self.assertEqual(event['changes'][0]['operation'], 'edited')
        self.assertEqual(event['changes'][0]['path'], 'scripts/run.py')
        source.write_text('one')
        self.assertEqual(recorder.record(self.config)['changed'], 1)
        extra = self.alpha / 'references/guide.md'
        extra.parent.mkdir()
        extra.write_text('guide')
        self.assertEqual(self.journal()['revision'], 2)
        self.assertEqual(recorder.record(self.config)['changed'], 1)
        self.assertEqual(self.journal()['events'][-1]['changes'][0]['operation'], 'added')
        extra.unlink()
        self.assertEqual(recorder.record(self.config)['changed'], 1)
        self.assertEqual(self.journal()['events'][-1]['changes'][0]['operation'], 'deleted')

    def test_noop_bytes_and_exclusions(self):
        recorder.record(self.config)
        before = self.journal()
        source = self.alpha / 'scripts/run.py'
        os.utime(source, None)
        (self.alpha / '.DS_Store').write_text('x')
        (self.alpha / 'scripts/temp.pyc').write_text('x')
        (self.alpha / 'node_modules').mkdir()
        (self.alpha / 'node_modules/fake.js').write_text('x')
        result = recorder.record(self.config)
        self.assertEqual((result['status'], result['changed']), ('unchanged', 0))
        after = self.journal()
        self.assertEqual((after['revision'], after['events'], after['observed_at']),
                         (before['revision'], before['events'], before['observed_at']))
        self.assertEqual(after['products']['alpha']['files']['scripts/run.py']['sha256'],
                         before['products']['alpha']['files']['scripts/run.py']['sha256'])

    def test_new_removed_product_and_unavailable_mount(self):
        recorder.record(self.config)
        beta = self.product('beta')
        self.assertEqual(recorder.record(self.config)['changed'], 1)
        self.assertEqual(self.journal()['events'][-1]['changes'][0]['plugin'], 'beta')
        # A missing override is unavailable, never interpreted as deletion.
        missing = self.base / 'unmounted/beta'
        self.config['canonical_sources'] = {'beta': str(missing)}
        prior = self.journal()
        result = recorder.record(self.config)
        self.assertIn('beta', result['unavailable'])
        self.assertEqual(self.journal(), prior)
        self.config.pop('canonical_sources')
        for child in (beta / '.codex-plugin').iterdir():
            child.unlink()
        (beta / '.codex-plugin').rmdir()
        beta.rmdir()
        result = recorder.record(self.config)
        self.assertGreater(result['changed'], 0)
        self.assertNotIn('beta', self.journal()['products'])
        self.root.rename(self.base / 'detached')
        prior = self.journal()
        self.assertEqual(recorder.record(self.config)['status'], 'unavailable')
        self.assertEqual(self.journal(), prior)

    def test_manifest_removal_keeps_known_product_and_actual_files(self):
        recorder.record(self.config)
        (self.alpha / '.codex-plugin/plugin.json').unlink()
        result = recorder.record(self.config)
        self.assertEqual(result['changed'], 1)
        self.assertIn('alpha', self.journal()['products'])
        self.assertIn('scripts/run.py', self.journal()['products']['alpha']['files'])
        self.assertEqual(self.journal()['events'][-1]['changes'][0]['path'],
                         '.codex-plugin/plugin.json')

    def test_nested_symlink_records_target_without_traversal(self):
        outside = self.base / 'secret.txt'
        outside.write_text('sensitive')
        (self.alpha / 'references').mkdir()
        (self.alpha / 'references/link').symlink_to(outside)
        recorder.record(self.config)
        entry = self.journal()['products']['alpha']['files']['references/link']
        self.assertEqual(entry['kind'], 'symlink')
        self.assertEqual(entry['target'], str(outside))
        self.assertNotIn('sensitive', json.dumps(self.journal()))

    def test_corrupt_state_fails_closed_and_quiet_cli(self):
        recorder.record(self.config)
        path = self.state / 'journal.json'
        path.write_bytes(b'{broken')
        with self.assertRaisesRegex(ValueError, 'corrupt'):
            recorder.record(self.config)
        self.assertEqual(path.read_bytes(), b'{broken')
        config_path = self.base / 'config.json'
        config_path.write_text(json.dumps(self.config))
        result = subprocess.run([sys.executable, str(SCRIPT), '--config', str(config_path), '--quiet'],
                                capture_output=True, timeout=3)
        self.assertEqual((result.returncode, result.stdout, result.stderr), (0, b'', b''))
        self.assertEqual(path.read_bytes(), b'{broken')
        self.assertIn('corrupt', (self.state / 'errors.log').read_text())

    def test_malformed_event_history_fails_closed(self):
        recorder.record(self.config)
        path = self.state / 'journal.json'
        journal = self.journal()
        journal['events'] = [{'id': 'x', 'at': 'now', 'origin': 'test', 'changes': [42]}]
        journal['pending_refresh_ids'] = [7]
        path.write_text(json.dumps(journal))
        before = path.read_bytes()
        with self.assertRaisesRegex(ValueError, 'corrupt'):
            recorder.record(self.config)
        self.assertEqual(path.read_bytes(), before)
        journal['pending_refresh_ids'] = []
        path.write_text(json.dumps(journal))
        with self.assertRaisesRegex(ValueError, 'corrupt'):
            recorder.record(self.config)

    def test_concurrent_lock_is_bounded(self):
        self.state.mkdir()
        with (self.state / 'journal.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = recorder.record(self.config)
        self.assertEqual(result['status'], 'busy')
        self.assertFalse((self.state / 'journal.json').exists())

    def test_pending_refresh_retries_after_release_lock(self):
        public = self.base / 'public'
        package = public / 'scripts/release_manager'
        package.mkdir(parents=True)
        (package / '__init__.py').write_text('')
        (package / 'pending.py').write_text(
            'import json\nfrom pathlib import Path\n'
            'def refresh(root, config, product_ids=None):\n'
            '    (Path(root)/"refreshed.json").write_text(json.dumps(product_ids))\n')
        (public / 'catalog').mkdir()
        (public / 'catalog/packages.json').write_text(json.dumps({'packages': [{'id': 'alpha'}]}))
        release_config = self.base / 'release.json'
        release_config.write_text(json.dumps({'public_source': str(public)}))
        self.config['release_config'] = str(release_config)
        lock_path = public / 'dist/release-manager/completion.lock'
        lock_path.parent.mkdir(parents=True)
        with lock_path.open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = recorder.record(self.config)
            self.assertEqual(result['queue_error'], 'release completion busy')
            self.assertEqual(self.journal()['pending_refresh_ids'], ['alpha'])
        result = recorder.record(self.config)
        self.assertIsNone(result['queue_error'])
        self.assertEqual(json.loads((public / 'refreshed.json').read_text()), ['alpha'])
        self.assertEqual(self.journal()['pending_refresh_ids'], [])


if __name__ == '__main__':
    unittest.main()
