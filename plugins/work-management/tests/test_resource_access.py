"""Offline lookup and recipe admission boundaries."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import resource_access as access


class ResourceAccessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.recipes = self.root / 'recipes'
        self.recipes.mkdir()
        self.directory = self.root / 'directory.json'
        self.items = [dict(id='sample', name='Sample Gallery', url='https://example.org/',
                           category='web-inspiration', owner_plugins=['ux-design-toolkit'],
                           identity_status='verified', access_route='browser',
                           purpose='Interface references',
                           api_anything={'status': 'tested', 'site': 'sample', 'operations': ['search']})]
        self.directory.write_text(json.dumps({'schema_version': 1, 'resources': self.items}))
        self.p1 = patch.object(access, 'DIRECTORY', self.directory)
        self.p2 = patch.object(access, 'RECIPES', self.recipes)
        self.p1.start(); self.p2.start()
        self.addCleanup(self.p1.stop); self.addCleanup(self.p2.stop)
        self.spec = dict(name='sample', baseUrl='https://example.org', operations=[
            {'name': 'search', 'readOnly': True, 'request': {'method': 'GET', 'url': 'https://example.org/search'}}])
        self._write_recipe()

    def _write_recipe(self):
        files = {'sample.json': json.dumps(self.spec).encode(), 'sample.md': b'# Sample recipe\n'}
        for name, data in files.items():
            (self.recipes / name).write_bytes(data)
        (self.recipes / 'manifest.json').write_text(json.dumps({'files': {
            name: hashlib.sha256(data).hexdigest() for name, data in files.items()}}))

    def test_lookup_and_schema(self):
        items = access.resources()
        self.assertEqual([x['id'] for x in access.list_resources(items, owner='ux-design-toolkit')], ['sample'])
        self.assertEqual(access.list_resources(items, category='icons'), [])
        self.assertEqual([x['id'] for x in access.search(items, 'sample interface')], ['sample'])
        self.assertEqual(access.show(items, 'sample')['url'], 'https://example.org/')
        self.directory.write_text(json.dumps({'schema_version': 2, 'resources': self.items}))
        with self.assertRaisesRegex(ValueError, 'schema'):
            access.resources()

    def test_install_and_idempotence(self):
        state = self.root / 'private-state'
        result = access.install_api('sample', state, self.items)
        self.assertEqual(result['status'], 'installed')
        self.assertEqual((state/'sites/sample.json').read_bytes(), (self.recipes/'sample.json').read_bytes())
        self.assertEqual(access.install_api('sample', state, self.items)['status'], 'already-installed')

    def test_missing_and_tampered_recipe_refused(self):
        (self.recipes/'sample.md').unlink()
        with self.assertRaisesRegex(ValueError, 'unavailable'):
            access.install_api('sample', self.root/'state', self.items)
        self.assertFalse((self.root/'state').exists())
        self._write_recipe()
        (self.recipes/'sample.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            access.install_api('sample', self.root/'state', self.items)
        self.assertFalse((self.root/'state').exists())

    def test_traversal_and_symlink_refused(self):
        with self.assertRaisesRegex(ValueError, 'site ID'):
            access.install_api('../sample', self.root/'state', self.items)
        state_link = self.root/'linked-state'
        state_link.symlink_to(self.root/'actual', target_is_directory=True)
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            access.install_api('sample', state_link, self.items)
        (self.recipes/'sample.md').unlink()
        (self.recipes/'sample.md').symlink_to(self.recipes/'sample.json')
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            access.install_api('sample', self.root/'state', self.items)

    def test_write_operation_and_existing_difference_refused(self):
        self.spec['operations'][0]['request']['method'] = 'POST'
        self._write_recipe()
        with self.assertRaisesRegex(ValueError, 'read-only GET'):
            access.install_api('sample', self.root/'state', self.items)
        self.assertFalse((self.root/'state').exists())
        self.spec['operations'][0]['request']['method'] = 'GET'
        self._write_recipe()
        sites = self.root/'state/sites'
        sites.mkdir(parents=True)
        (sites/'sample.md').write_text('private edits')
        with self.assertRaisesRegex(ValueError, 'differs'):
            access.install_api('sample', self.root/'state', self.items)
        self.assertFalse((sites/'sample.json').exists())
        self.assertEqual((sites/'sample.md').read_text(), 'private edits')

    def test_publish_failure_rolls_back_both_files(self):
        real_link = access.os.link
        calls = 0

        def fail_second(source, destination):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError('simulated second-file failure')
            return real_link(source, destination)

        with patch.object(access.os, 'link', side_effect=fail_second):
            with self.assertRaisesRegex(OSError, 'second-file failure'):
                access.install_api('sample', self.root/'state', self.items)
        self.assertEqual(list((self.root/'state/sites').iterdir()), [])

    def test_plugin_state_refused(self):
        with self.assertRaisesRegex(ValueError, 'outside the plugin'):
            access.install_api('sample', access.ROOT/'private-state', self.items)
        disguised = access.ROOT.parent/'unrelated'/'..'/access.ROOT.name/'private-state'
        with self.assertRaisesRegex(ValueError, 'outside the plugin'):
            access.install_api('sample', disguised, self.items)
        self.assertFalse((access.ROOT/'private-state').exists())


if __name__ == '__main__':
    unittest.main()
