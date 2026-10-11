import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.release_manager import (SemVer, changed_products, evidence_notes,
                                     import_history, propose_version, select_current,
                                     validate_catalog, version_edits)


class ReleaseManagerTests(unittest.TestCase):
    def test_semver_precedence_build_and_backport(self):
        self.assertLess(SemVer('1.2.3-alpha.2'), SemVer('1.2.3-alpha.10'))
        self.assertLess(SemVer('1.2.3-alpha.10'), SemVer('1.2.3'))
        self.assertEqual(SemVer('1.2.3+build.4'), SemVer('1.2.3+build.5'))
        with self.assertRaises(ValueError):
            SemVer('1.2.3-01')
        product = {'releases': [self.release('x', '1.2.0'), self.release('x', '1.1.9')]}
        self.assertEqual(select_current(product)['version'], '1.2.0')
        product['releases'][0]['distribution_status'] = 'withdrawn'
        self.assertEqual(select_current(product)['version'], '1.1.9')

    @staticmethod
    def release(ident, version):
        return {'release_key': f'{ident}/v{version}', 'product_id': ident,
                'version': version, 'git_tag': f'{ident}/v{version}',
                'source_commit': 'a'*40, 'published_at': '2026-01-01T00:00:00Z',
                'release_url': 'https://example.test/release', 'channel': 'stable',
                'distribution_status': 'available', 'summary': 'Release',
                'notes': 'Changed files are listed.', 'notes_provenance': 'release-body',
                'assets': [{'role': 'installation', 'name': f'{ident}-{version}.zip',
                            'url': 'https://example.test/file', 'size': 1, 'sha256': 'a'*64}],
                'compatibility': 'See README.', 'upgrade_guidance': 'Review README.',
                'verification': {'archive_verified': True, 'layout_verified': True}}

    def test_catalog_rejects_stale_current_and_unverified_promotion(self):
        product = {'id': 'x', 'name': 'X', 'kind': 'plugin', 'repository': 'https://example.test',
                   'compatibility': 'See README.', 'upgrade_guidance': 'Review README.',
                   'current_release_key': 'x/v1.0.0', 'releases': [self.release('x', '1.0.0')]}
        catalog = {'schema_version': 'working-tools.releases.v1', 'products': [product]}
        self.assertEqual(validate_catalog(catalog), [])
        product['releases'][0]['verification']['layout_verified'] = False
        self.assertTrue(any('available record' in error for error in validate_catalog(catalog)))
        product['releases'][0]['distribution_status'] = 'unavailable'
        self.assertTrue(any('current_release_key' in error for error in validate_catalog(catalog)))

    def test_external_revision_is_preserved_but_never_current(self):
        external = {'id': 'legacy-skill', 'name': 'Legacy Skill', 'kind': 'external',
                    'channel': 'legacy', 'releases': [{'release_key': 'legacy:legacy-skill:a', 'version': None,
                    'version_scheme': 'revision', 'source_commit': 'a'*40,
                    'distribution_status': 'available',
                    'verification': {'download_verified': False, 'provenance': 'public-mirror'},
                    'assets': [{'name': 'legacy.skill', 'role': 'skill-file',
                                'url': 'https://example.test/legacy.skill', 'sha256': None}]}]}
        self.assertEqual(validate_catalog({'schema_version': 'working-tools.releases.v1', 'products': [external]}), [])
        self.assertIsNone(select_current(external))

    def test_malformed_catalog_reports_errors_without_crashing(self):
        malformed = {'schema_version': 'working-tools.releases.v1', 'products': [
            {'id': [], 'name': '', 'kind': 'plugin', 'repository': '',
             'compatibility': '', 'upgrade_guidance': '', 'current_release_key': None,
             'releases': [{'release_key': [], 'product_id': [], 'version': None,
                           'channel': [], 'distribution_status': [], 'assets': [
                               {'name': [], 'size': None, 'sha256': None}],
                           'verification': None}]}]}
        self.assertTrue(validate_catalog(malformed))

    def test_versions_and_factual_notes(self):
        changes = [{'status': 'modified', 'path': 'plugins/x/skills/a/SKILL.md'}]
        self.assertEqual(propose_version('1.2.3', changes), '1.2.4')
        self.assertEqual(propose_version('1.2.3', [{'status': 'added', 'path': 'plugins/x/skills/b/SKILL.md'}]), '1.3.0')
        self.assertEqual(propose_version('1.2.3', [{'status': 'removed', 'path': 'plugins/x/skills/b/SKILL.md'}]), '2.0.0')
        self.assertEqual(propose_version('1.2.3', changes, change_level='major'), '2.0.0')
        with self.assertRaises(ValueError):
            propose_version('1.2.3', changes, existing_versions=['1.2.4+older'])
        self.assertEqual(evidence_notes(changes), '- Updated `plugins/x/skills/a/SKILL.md`.')

    def test_version_edits_are_synchronized_and_read_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = ['catalog/packages.json', 'plugins/x/plugin.json',
                     'plugins/x/.codex-plugin/plugin.json', 'plugins/x/.claude-plugin/plugin.json']
            for path in paths:
                target = root/path; target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(json.dumps({'packages': [{'id': 'x', 'version': '1.0.0'}]}
                                             if path.startswith('catalog/') else {'name': 'x', 'version': '1.0.0'}))
            edits = version_edits(root, 'x', '1.0.1')
            self.assertEqual(set(edits), set(paths))
            self.assertTrue(all('1.0.1' in value for value in edits.values()))
            self.assertTrue(all('1.0.0' in (root/path).read_text() for path in paths))

    def test_product_diff_includes_instructions_and_explicit_shared_templates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.check_call(['git', 'init', '-q', directory])
            subprocess.check_call(['git', 'config', 'user.email', 'test@example.test'], cwd=root)
            subprocess.check_call(['git', 'config', 'user.name', 'Test'], cwd=root)
            paths = ['plugins/x/skills/a/SKILL.md', 'shared/card.md', 'site/index.html']
            for path in paths:
                target = root/path; target.parent.mkdir(parents=True, exist_ok=True); target.write_text('old')
            subprocess.check_call(['git', 'add', '.'], cwd=root)
            subprocess.check_call(['git', 'commit', '-qm', 'initial'], cwd=root)
            base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
            for path in paths:
                (root/path).write_text('new')
            subprocess.check_call(['git', 'add', '.'], cwd=root)
            subprocess.check_call(['git', 'commit', '-qm', 'change'], cwd=root)
            target = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
            result = changed_products(root, base, target, ['x', 'y'], shared_paths={'shared/card.md': ['y']})
            self.assertEqual([x['path'] for x in result['x']], ['plugins/x/skills/a/SKILL.md'])
            self.assertEqual([x['path'] for x in result['y']], ['shared/card.md'])
            self.assertNotIn('site/index.html', str(result))

    def test_history_pagination_error_does_not_return_partial_rows(self):
        calls = []
        def runner(args):
            calls.append(args[0])
            if args[0].endswith('page=1'):
                return json.dumps([{'tag_name': 'unrelated'}] * 100)
            raise RuntimeError('page 2 failed')
        with self.assertRaisesRegex(RuntimeError, 'page 2 failed'):
            import_history('owner', 'repo', repo_path=Path('.'), runner=runner)
        self.assertEqual(len(calls), 2)

    def test_exact_commit_archive_import(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.check_call(['git', 'init', '-q', directory])
            subprocess.check_call(['git', 'config', 'user.email', 'test@example.test'], cwd=root)
            subprocess.check_call(['git', 'config', 'user.name', 'Test'], cwd=root)
            files = {name: json.dumps({'name': 'x', 'version': '1.0.0'}).encode()
                     for name in ('plugin.json', '.codex-plugin/plugin.json', '.claude-plugin/plugin.json')}
            files['README.md'] = b'Instructions\n'
            for name, data in files.items():
                target = root/'plugins/x'/name; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(data)
            subprocess.check_call(['git', 'add', '.'], cwd=root)
            subprocess.check_call(['git', 'commit', '-qm', 'release'], cwd=root)
            commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
            with tempfile.TemporaryFile() as output:
                with zipfile.ZipFile(output, 'w') as archive:
                    for name, data in files.items():
                        archive.writestr(name, data)
                output.seek(0); data = output.read()
            asset = {'id': 1, 'name': 'x-1.0.0.zip', 'size': len(data),
                     'browser_download_url': 'https://example.test/x.zip',
                     'digest': 'sha256:' + hashlib.sha256(data).hexdigest()}
            release = {'id': 1, 'tag_name': 'x/v1.0.0', 'assets': [asset], 'html_url': 'https://example.test/release',
                       'name': 'Release', 'body': 'Changed instructions.', 'published_at': '2026-01-01T00:00:00Z'}
            def runner(args):
                if '/releases?' in args[0]: return json.dumps([release])
                if '/commits/' in args[0]: return json.dumps({'sha': commit})
                raise AssertionError(args)
            rows = import_history('owner', 'repo', repo_path=root, runner=runner, asset_fetcher=lambda _: data)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['distribution_status'], 'available')
            self.assertEqual(rows[0]['assets'][0]['sha256'], hashlib.sha256(data).hexdigest())
            reused = import_history('owner', 'repo', repo_path=root, runner=runner,
                                    asset_fetcher=lambda _: self.fail('verified asset should be reused'),
                                    previous_releases=rows)
            self.assertEqual(reused[0]['distribution_status'], 'available')
            asset['digest'] = 'sha256:' + '0'*64
            with self.assertRaisesRegex(ValueError, 'differs from GitHub digest'):
                import_history('owner', 'repo', repo_path=root, runner=runner,
                               asset_fetcher=lambda _: data, previous_releases=rows)


if __name__ == '__main__':
    unittest.main()
