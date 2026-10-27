"""Filesystem-only sync checks; no model or hook delivery is run."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ENGINE = Path(__file__).parents[1] / 'scripts' / 'sync_antigravity.py'


class SyncFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state = self.root / 'state'
        self.state.mkdir()
        self.global_skills = self.root / 'skills'
        self.global_skills.mkdir()
        self.native = self.root / 'native'
        self.native.mkdir()
        self.source = self.root / 'source'
        (self.source / 'skills' / 'one').mkdir(parents=True)
        (self.source / 'skills' / 'one' / 'SKILL.md').write_text('---\nname: one\n---\nFirst\n')
        self.inventory = self.root / 'inventory.json'
        self.inventory.write_text(json.dumps({'installed': [self.package('alpha')]}))
        self.fake_agy = self.root / 'agy'
        self.fake_agy.write_text(
            '#!' + sys.executable + '\n'
            'import os,sys,shutil\nfrom pathlib import Path\n'
            'a=sys.argv[1:]\n'
            'native=Path(os.environ["FAKE_NATIVE"])\n'
            'if a[:2]==["plugin","validate"]: sys.exit(0)\n'
            'if a[:2]==["plugin","install"]:\n'
            ' p=Path(a[2]); dst=native/p.name\n'
            ' if dst.exists(): shutil.rmtree(dst)\n'
            ' shutil.copytree(p,dst)\n'
            ' if os.environ.get("FAIL_INSTALL")==p.name: sys.exit(7)\n'
            ' sys.exit(0)\n'
            'if a[:2]==["plugin","uninstall"]:\n'
            ' dst=native/a[2]\n'
            ' if dst.exists(): shutil.rmtree(dst)\n'
            ' sys.exit(0)\n'
            'sys.exit(3)\n')
        self.fake_agy.chmod(0o755)
        self.config = self.root / 'config.json'
        self.config.write_text(json.dumps({
            'state_dir': str(self.state), 'global_skills_dir': str(self.global_skills),
            'native_plugins_dir': str(self.native), 'agy': str(self.fake_agy),
            'default_inventory': str(self.inventory), 'hook_guard_paths': {},
            'command_timeout_seconds': 2, 'require_external_volume': False,
        }))

    def package(self, name):
        source = self.root / f'source-{name}' if name != 'alpha' else self.source
        if name != 'alpha':
            (source / 'skills' / 'two').mkdir(parents=True, exist_ok=True)
            (source / 'skills' / 'two' / 'SKILL.md').write_text('---\nname: two\n---\nSecond\n')
        return {'name': name, 'version': '1.0.0', 'marketplaceName': 'personal',
                'source': {'path': str(source)}}

    def run_sync(self, mode, env=None):
        run_env = {**os.environ, 'FAKE_NATIVE': str(self.native), **(env or {})}
        return subprocess.run([sys.executable, '-B', str(ENGINE), '--config',
                               str(self.config), mode], capture_output=True,
                              text=True, env=run_env)

    def test_noop_and_source_change(self):
        first = self.run_sync('--apply')
        self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
        state = self.state / 'sync-state.json'
        before = state.stat().st_mtime_ns
        second = self.run_sync('--apply')
        self.assertEqual(second.returncode, 0, second.stdout)
        self.assertEqual(json.loads(second.stdout)['actions'], [])
        self.assertEqual(state.stat().st_mtime_ns, before)
        (self.source / 'skills' / 'one' / 'SKILL.md').write_text('---\nname: one\n---\nChanged\n')
        checked = self.run_sync('--check')
        self.assertEqual(checked.returncode, 0, checked.stdout)
        self.assertIn('source-content alpha--one', json.loads(checked.stdout)['actions'][0])
        self.assertEqual(self.run_sync('--apply').returncode, 0)

    def test_extra_file_conflict(self):
        self.assertEqual(self.run_sync('--apply').returncode, 0)
        extra = self.state / 'adapters' / 'alpha' / 'unexpected.txt'
        extra.write_text('keep me')
        checked = self.run_sync('--check')
        self.assertEqual(checked.returncode, 1)
        self.assertTrue(any('Extra adapter package entry' in x
                            for x in json.loads(checked.stdout)['conflicts']))
        self.assertEqual(self.run_sync('--apply').returncode, 2)
        self.assertEqual(extra.read_text(), 'keep me')
        extra.unlink()
        native_extra = self.native / 'alpha' / 'unexpected.txt'
        native_extra.write_text('keep me too')
        checked = self.run_sync('--check')
        self.assertEqual(checked.returncode, 1)
        self.assertTrue(any('Extra native package entry' in x
                            for x in json.loads(checked.stdout)['conflicts']))
        self.assertEqual(native_extra.read_text(), 'keep me too')

    def test_missing_state_mount_stops_before_change(self):
        self.assertEqual(self.run_sync('--apply').returncode, 0)
        link = self.global_skills / 'alpha--one'
        target = os.readlink(link)
        config = json.loads(self.config.read_text())
        config['state_dir'] = str(self.root / 'missing-mount')
        self.config.write_text(json.dumps(config))
        self.assertEqual(self.run_sync('--apply').returncode, 2)
        self.assertEqual(os.readlink(link), target)

    def test_source_mount_loss_stops_before_change(self):
        self.assertEqual(self.run_sync('--apply').returncode, 0)
        link = self.global_skills / 'alpha--one'
        target = os.readlink(link)
        (self.source / 'skills' / 'one' / 'SKILL.md').unlink()
        (self.source / 'skills' / 'one').rmdir()
        (self.source / 'skills').rmdir()
        self.source.rmdir()
        stopped = self.run_sync('--apply')
        self.assertEqual(stopped.returncode, 2)
        self.assertIn('Missing canonical source', stopped.stderr)
        self.assertEqual(os.readlink(link), target)

    def test_partial_native_failure_rolls_back(self):
        self.assertEqual(self.run_sync('--apply').returncode, 0)
        baseline = (self.state / 'sync-state.json').read_bytes()
        self.inventory.write_text(json.dumps({'installed': [self.package('alpha'),
                                                             self.package('beta')]}))
        failed = self.run_sync('--apply', {'FAIL_INSTALL': 'beta'})
        self.assertEqual(failed.returncode, 2, failed.stdout + failed.stderr)
        result = json.loads(failed.stdout)
        self.assertTrue(result['rollback']['verified'], result)
        self.assertEqual((self.state / 'sync-state.json').read_bytes(), baseline)
        self.assertFalse((self.native / 'beta').exists())
        self.assertFalse((self.global_skills / 'beta--two').exists())
        self.assertTrue((self.native / 'alpha').exists())


if __name__ == '__main__':
    unittest.main()
