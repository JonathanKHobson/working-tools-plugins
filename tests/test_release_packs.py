"""The independent hooks pack keeps its own release identity and recovery path."""

import json
import hashlib
import subprocess
import sys
import tempfile
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from release_manager import packs  # noqa: E402
from release_manager.catalog import validate_catalog  # noqa: E402

BASE = '27e1d491d44b134f30fe68cda55029c9f2fab9cb'


class HooksPackTest(unittest.TestCase):
    def test_published_baseline_archive_matches_tag_tree(self):
        files = packs._files(ROOT, BASE)
        self.assertEqual(len(files), 9)
        _, product = packs._load(ROOT)
        release = next(row for row in product['releases'] if row['version'] == '0.1.0')
        asset = next(row for row in release['assets'] if row['role'] == 'installation')
        request = urllib.request.Request(asset['url'], headers={
            'User-Agent': 'working-tools-release-validation/1.0'})
        with urllib.request.urlopen(request, timeout=30) as response:
            archive_bytes = response.read()
        self.assertEqual(len(archive_bytes), asset['size'])
        self.assertEqual(hashlib.sha256(archive_bytes).hexdigest(), asset['sha256'])
        self.assertTrue(packs._archive_matches(
            archive_bytes, '0.1.0', files))
        self.assertEqual(release['git_tag'], 'codex-host-hooks/v0.1.0')
        self.assertEqual(release['source_commit'], BASE)
        self.assertEqual(release['source_files'], files)

    def test_complete_history_projection_uses_tagged_archive_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = packs._build(ROOT, BASE, '0.1.0', Path(tmp))
            raw = {path.name: path.read_bytes() for path in paths}
            assets = [{'name': name, 'size': len(data),
                       'digest': 'sha256:' + hashlib.sha256(data).hexdigest(),
                       'browser_download_url': 'https://github.com/example/download/' + name}
                      for name, data in raw.items()]
            release = {'tag_name': 'codex-host-hooks/v0.1.0', 'assets': assets,
                       'published_at': '2026-10-11T00:00:00Z',
                       'html_url': 'https://github.com/example/releases/tag/codex-host-hooks/v0.1.0',
                       'name': 'Hooks 0.1.0', 'body': 'Reviewed hooks release.',
                       'draft': False, 'prerelease': False}
            products = packs.history_products(ROOT, releases=[release],
                                              asset_fetcher=lambda a: raw[a['name']],
                                              tag_resolver=lambda _tag: BASE)
            self.assertEqual(products[0]['kind'], 'integration')
            self.assertEqual(products[0]['current_release_key'], 'codex-host-hooks/v0.1.0')
            self.assertEqual(validate_catalog({'schema_version': 'working-tools.releases.v1',
                                               'products': products}), [])

    def test_noop_and_resume_one_unpushed_ledger_commit(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            source, remote = tmp / 'source', tmp / 'remote.git'
            subprocess.check_call(['git', 'clone', '--quiet', '--shared', str(ROOT), str(source)])
            subprocess.check_call(['git', 'checkout', '-qb', 'main', BASE], cwd=source)
            subprocess.check_call(['git', 'config', 'user.name', 'Fixture'], cwd=source)
            subprocess.check_call(['git', 'config', 'user.email', 'fixture@example.test'], cwd=source)
            subprocess.check_call(['git', 'init', '--bare', '--quiet', str(remote)])
            subprocess.check_call(['git', 'remote', 'set-url', 'origin', str(remote)], cwd=source)
            document, _ = packs._load(ROOT)
            product = document['products'][0]
            baseline = next(row for row in product['releases'] if row['version'] == '0.1.0')
            self.assertEqual(baseline['source_commit'], BASE)
            self.assertEqual(baseline['source_files'], packs._files(ROOT, BASE))
            product['version'] = baseline['version']
            product['source_commit'] = BASE
            product['source_files'] = baseline['source_files']
            product['compatibility'] = baseline['compatibility']
            product['upgrade_guidance'] = baseline['upgrade_guidance']
            product['releases'] = [baseline]
            document.pop('completion_receipt', None)
            (source / packs.CATALOG).write_text(json.dumps(document, indent=2) + '\n')
            subprocess.check_call(['git', 'add', packs.CATALOG], cwd=source)
            subprocess.check_call(['git', 'commit', '-qm', 'Seed integration catalog'], cwd=source)
            subprocess.check_call(['git', 'push', '-q', '-u', 'origin', 'main'], cwd=source)
            notes = source / 'catalog/integration-changes'
            self.assertEqual(packs.complete(source, notes), [])
            readme = source / packs.PREFIX / 'README.md'
            readme.write_text(readme.read_text().replace('codex-host-hooks-0.1.0.zip',
                                                         'codex-host-hooks-0.1.1.zip').replace(
                                                         'codex-host-hooks/v0.1.0', 'codex-host-hooks/v0.1.1'))
            subprocess.check_call(['git', 'add', str(readme.relative_to(source))], cwd=source)
            subprocess.check_call(['git', 'commit', '-qm', 'Revise hooks download instructions'], cwd=source)
            head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source).decode().strip()
            notes.mkdir()
            (notes / 'codex-host-hooks.json').write_text(json.dumps({
                'product_id': packs.ID, 'source_commit': head,
                'changed_files': [packs.PREFIX + 'README.md'], 'level': 'patch',
                'summary': 'Updated manual download directions',
                'why': 'Point the manual installer at the next reviewed archive',
                'notes': 'Updated the reviewed manual download directions.',
                'compatibility': 'Python 3.9+ on POSIX hosts; manual trust required.',
                'upgrade_guidance': 'Review the ZIP and merge the example hooks manually.',
                'validation': 'Fixture archive and source layout verified.',
                'source_review': 'The nine registered public files remain the exact scope.'}))
            published = {}
            def fake_publish(_repo, record, commit, paths, *, notes, title):
                release = {'html_url': 'https://github.com/example/releases/tag/' + record['git_tag'],
                           'published_at': '2026-10-11T00:00:00Z', 'body': notes,
                           'assets': [{'name': p.name, 'browser_download_url':
                                       'https://github.com/example/releases/download/' +
                                       record['git_tag'] + '/' + p.name} for p in paths]}
                published.setdefault(record['git_tag'], release)
                return published[record['git_tag']]
            original_git = packs._git
            pushes = []
            def fail_ledger_push(repo, *args):
                if args[:2] == ('push', 'origin'):
                    pushes.append(args)
                    if len(pushes) == 2:
                        raise subprocess.CalledProcessError(1, ['git', *args])
                return original_git(repo, *args)
            with patch.object(packs, 'publish', fake_publish), patch.object(packs, '_git', fail_ledger_push):
                with self.assertRaises(subprocess.CalledProcessError):
                    packs.complete(source, notes)
            self.assertEqual(len(published), 1)
            with patch.object(packs, 'publish', fake_publish):
                receipt = packs.complete(source, notes)
                self.assertEqual(len(receipt), 1)
                self.assertEqual(receipt[0]['version'], '0.1.1')
                self.assertEqual(packs.complete(source, notes), [])
            self.assertEqual(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source),
                             subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=source))
            # A crash after the ledger write but before its commit also resumes.
            readme.write_text(readme.read_text().replace('codex-host-hooks-0.1.1.zip',
                                                         'codex-host-hooks-0.1.2.zip').replace(
                                                         'codex-host-hooks/v0.1.1', 'codex-host-hooks/v0.1.2'))
            subprocess.check_call(['git', 'add', str(readme.relative_to(source))], cwd=source)
            subprocess.check_call(['git', 'commit', '-qm', 'Next download revision'], cwd=source)
            next_head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source).decode().strip()
            note = json.loads((notes / 'codex-host-hooks.json').read_text())
            note['source_commit'] = next_head
            (notes / 'codex-host-hooks.json').write_text(json.dumps(note))
            def fail_catalog_add(repo, *args):
                if args == ('add', '--', packs.CATALOG, 'catalog/integration-changes/codex-host-hooks.json'):
                    raise subprocess.CalledProcessError(1, ['git', *args])
                return original_git(repo, *args)
            with patch.object(packs, 'publish', fake_publish), patch.object(packs, '_git', fail_catalog_add):
                with self.assertRaises(subprocess.CalledProcessError):
                    packs.complete(source, notes)
            self.assertIn('0.1.2', (source / packs.CATALOG).read_text())
            with patch.object(packs, 'publish', fake_publish):
                recovered = packs.complete(source, notes)
            self.assertEqual(recovered[0]['version'], '0.1.2')
            self.assertEqual(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source),
                             subprocess.check_output(['git', 'rev-parse', 'origin/main'], cwd=source))


if __name__ == '__main__':
    unittest.main()
