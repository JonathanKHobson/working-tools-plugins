"""Portable runtime boundaries; no network or browser needed."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('api_anything', ROOT / 'scripts/api_anything.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

class RuntimeTests(unittest.TestCase):
    def test_pinned_source_is_complete(self):
        self.assertEqual(len(a.verify_source()['files']), 169)

    def test_missing_setup_does_not_run_or_fetch(self):
        with tempfile.TemporaryDirectory() as d, patch.object(a.subprocess, 'run') as run:
            with self.assertRaisesRegex(ValueError, 'setup'):
                a.verify_runtime(Path(d))
            run.assert_not_called()

    def test_tampered_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root/'x').write_text('changed')
            with self.assertRaisesRegex(ValueError, 'integrity'):
                a.verify_files(root, {'x':'0'*64})

    def test_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'x').symlink_to('/etc/hosts')
            with self.assertRaisesRegex(ValueError, 'symlink'):
                a.verify_files(root, {'x':'0'*64})

    def test_unsafe_manifest_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(ValueError, 'path'):
                a.verify_files(Path(d), {'../x':'0'*64})

    def test_private_state_cannot_be_packaged(self):
        with self.assertRaisesRegex(ValueError, 'outside'):
            a.state_path(ROOT/'sessions', Path('/tmp/runtime-test'))
        with self.assertRaisesRegex(ValueError, 'outside'):
            a.state_path(Path('/tmp/runtime-test/state'), Path('/tmp/runtime-test'))

    def test_setup_refuses_nonempty_directory(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'keep').write_text('user data')
            with patch.object(a.subprocess,'run') as run:
                with self.assertRaisesRegex(ValueError,'empty'):
                    a.setup(root)
                run.assert_not_called()
            self.assertEqual((root/'keep').read_text(),'user data')

    def test_missing_direct_dependency_is_not_ready(self):
        with tempfile.TemporaryDirectory() as d:
            runtime=Path(d)
            (runtime/'package.json').write_text(json.dumps({'dependencies':{'zod':'*'}}))
            with patch.object(a.subprocess, 'run') as run:
                with self.assertRaisesRegex(ValueError, 'dependencies'):
                    a.check_startup(runtime)
                run.assert_not_called()

    def test_broken_cli_startup_is_not_ready(self):
        import subprocess
        with tempfile.TemporaryDirectory() as d:
            runtime=Path(d)
            (runtime/'package.json').write_text(json.dumps({'dependencies':{}}))
            with patch.object(a.shutil,'which',return_value='/node'), patch.object(
                a.subprocess,'run',side_effect=[subprocess.CompletedProcess([],0,'v22.20.0'),
                                              subprocess.CompletedProcess([],1,'','Cannot find package')]):
                with self.assertRaisesRegex(ValueError, 'startup'):
                    a.check_startup(runtime)

    def test_node_version_requirement(self):
        for version in ['v22.12.9','v20.20.0','nonsense']:
            self.assertFalse(a.supported_node(version))
        for version in ['v22.13.0','v22.20.0','v24.1.0']:
            self.assertTrue(a.supported_node(version))

if __name__ == '__main__':
    unittest.main()
