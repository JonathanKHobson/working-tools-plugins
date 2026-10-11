"""Historical downloads stay visible without becoming current plugins."""

import copy
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from release_manager.catalog import select_current, validate_catalog  # noqa: E402
from release_manager.legacy import (  # noqa: E402
    changed_external_products, external_release_records,
    load_external_products, validate_external_products, plan_active_external_updates,
    complete_active_external_update, _check_install_archive,
)


class ExternalProductsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = load_external_products(ROOT / 'catalog/external-products.json')

    def test_inventory_and_history_are_complete_and_separate(self):
        products = self.document['products']
        self.assertEqual(len(products), 26)
        self.assertEqual(sum(p['disposition'] == 'download' for p in products), 25)
        self.assertEqual(sum(len(p['assets']) for p in products), 37)
        historical = [release for p in products for release in p.get('historical_releases', [])]
        self.assertEqual(len(historical), 31)
        self.assertEqual(sum(len(release['assets']) for release in historical), 50)
        self.assertTrue(all(release['verification']['download_verified'] for release in historical))
        self.assertEqual(validate_external_products(self.document), [])
        history = {'schema_version': 'working-tools.releases.v1',
                   'products': external_release_records(self.document)}
        self.assertEqual(validate_catalog(history), [])
        self.assertTrue(all(select_current(p) is None for p in history['products']))
        self.assertTrue(all(p['channel'] == 'legacy' for p in products))
        self.assertEqual(sum(len(p['releases']) for p in history['products']), 57)

    def test_skill_formats_share_one_product_and_bundle_members_are_named(self):
        by_id = {p['id']: p for p in self.document['products']}
        self.assertEqual(len(by_id['safe-install-review']['assets']), 2)
        self.assertEqual(len(by_id['critical-compass-skill']['assets']), 2)
        self.assertEqual(len(by_id['humanizer-legacy-skill']['assets']), 2)
        self.assertEqual(len(by_id['job-application-skills-bundle']['members']), 4)
        self.assertEqual(by_id['understanding-ai-2026']['disposition'], 'page-only')
        self.assertEqual(by_id['understanding-ai-2026']['assets'], [])
        self.assertEqual(by_id['writing-enhancement-codex-collection']['members'], [])
        self.assertTrue(by_id['writing-enhancement-codex-collection']['gaps'])

    def test_source_change_detection_only_marks_registered_product_file(self):
        checkouts = {key: Path('/synthetic') for key in self.document['sources']}

        def runner(source_id, _checkout, args):
            self.assertEqual(args[:4], ['git', 'diff', '--name-only', '--no-renames'])
            return ('downloads/resume-crafter.skill\nREADME.md\n' if source_id == 'job-application-compass'
                    else 'index.html\n')

        result = changed_external_products(self.document, checkouts, runner=runner)
        self.assertEqual(result, {'job-application-resume-crafter': ['downloads/resume-crafter.skill']})

    def test_rejects_private_paths_and_unverified_digest_claim(self):
        bad = copy.deepcopy(self.document)
        bad['products'][0]['source']['files'] = ['/Users/example/private.txt']
        bad['products'][0]['assets'][0]['sha256'] = None
        self.assertTrue(any('source files' in e for e in validate_external_products(bad)))
        self.assertTrue(any('no immutable digest' in e for e in validate_external_products(bad)))

    def test_requires_all_source_checkouts(self):
        with self.assertRaisesRegex(ValueError, 'missing checkout'):
            changed_external_products(self.document, {}, runner=lambda *_: '')

    def test_install_archive_rejects_traversal_and_invalid_bytes(self):
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w') as z:
            z.writestr('../escaped.txt', 'bad')
        with self.assertRaisesRegex(ValueError, 'unsafe archive member'):
            _check_install_archive('guide.zip', data.getvalue())
        with self.assertRaisesRegex(ValueError, 'invalid installation archive'):
            _check_install_archive('guide.skill', b'not an archive')

    def test_lifecycle_gate_keeps_frozen_differences_out_of_release_plan(self):
        checkouts = {key: Path('/synthetic') for key in self.document['sources']}
        def runner(source_id, _checkout, args):
            if args[:2] == ['git', 'diff'] and source_id == 'job-application-compass':
                return 'downloads/resume-crafter.skill\n'
            return ''
        plan = plan_active_external_updates(self.document, checkouts, Path('/missing'), runner=runner)
        self.assertEqual(plan['ready'], [])
        self.assertEqual(plan['needs_notes'], [])
        self.assertEqual(plan['frozen_differences'][0]['product_id'], 'job-application-resume-crafter')

    def test_active_guide_completion_preserves_prior_bytes_and_only_advances_one_product(self):
        def archive(payload):
            data = io.BytesIO()
            with zipfile.ZipFile(data, 'w') as z:
                z.writestr('safe-install-review/SKILL.md', payload)
            return data.getvalue()
        old_bytes, new_bytes, next_bytes = archive('old'), archive('new'), archive('next')
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            remote, checkout = root / 'remote.git', root / 'source'
            subprocess.check_call(['git', 'init', '--bare', '--quiet', str(remote)])
            subprocess.check_call(['git', 'init', '--quiet', '-b', 'main', str(checkout)])
            subprocess.check_call(['git', 'config', 'user.name', 'Fixture'], cwd=checkout)
            subprocess.check_call(['git', 'config', 'user.email', 'fixture@example.test'], cwd=checkout)
            subprocess.check_call(['git', 'remote', 'add', 'origin', str(remote)], cwd=checkout)
            files = ['downloads/safe-install-review.skill', 'downloads/safe-install-review.zip']
            for path in files:
                target = checkout / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(old_bytes)
            subprocess.check_call(['git', 'add', '.'], cwd=checkout)
            subprocess.check_call(['git', 'commit', '-qm', 'Baseline'], cwd=checkout)
            base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=checkout).decode().strip()
            subprocess.check_call(['git', 'push', '-q', '-u', 'origin', 'main'], cwd=checkout)
            for path in files:
                (checkout / path).write_bytes(new_bytes)
            subprocess.check_call(['git', 'add', '.'], cwd=checkout)
            subprocess.check_call(['git', 'commit', '-qm', 'Update skill'], cwd=checkout)
            head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=checkout).decode().strip()
            document = copy.deepcopy(self.document)
            document['sources']['what-is-an-mcp']['commit'] = base
            product = next(p for p in document['products'] if p['id'] == 'safe-install-review')
            for asset in product['assets']:
                asset['sha256'] = hashlib.sha256(old_bytes).hexdigest()
            product['assets'].reverse()  # Asset order must not bind a file to another URL.
            notes = root / 'notes'; notes.mkdir()
            note = {'product_id': product['id'], 'source_commit': head, 'changed_files': files,
                    'summary': 'Updated review', 'why': 'Corrects the check',
                    'compatibility': 'Same installation contract', 'upgrade_guidance': 'Replace prior skill',
                    'validation': 'Fixture checks',
                    'release_notes': 'Review updated for the tested installer.',
                    'authoring_provenance': 'Reviewed owning guide source'}
            (notes / 'safe-install-review.json').write_text(json.dumps(note))
            published = []
            releases = {}
            def fake_publish(repo, record, commit, paths, *, notes, title):
                self.assertEqual(repo, 'JonathanKHobson/what-is-an-mcp')
                published.append((commit, [p.read_bytes() for p in paths]))
                if record['git_tag'] in releases:
                    return releases[record['git_tag']]
                release = {'html_url': 'https://github.com/example/releases/tag/' + record['git_tag'],
                        'published_at': '2026-10-11T00:00:00Z',
                        'body': notes,
                        'assets': [{'name': p.name, 'browser_download_url':
                                    'https://github.com/example/releases/download/' + record['git_tag'] + '/' + p.name}
                                   for p in paths]}
                releases[record['git_tag']] = release
                return release
            def fake_git(*args, cwd):
                if args == ('git', 'remote', 'get-url', 'origin'):
                    return b'https://github.com/JonathanKHobson/what-is-an-mcp.git\n'
                return subprocess.check_output(args, cwd=cwd)
            with self.assertRaisesRegex(ValueError, 'Pages download did not match'):
                complete_active_external_update(
                    document, 'safe-install-review', checkout, notes,
                    publish=fake_publish, fetch_bytes=lambda _url: b'wrong', git=fake_git,
                    sleep=lambda _seconds: None)
            self.assertEqual(len(releases), 2)
            updated = complete_active_external_update(
                document, 'safe-install-review', checkout, notes,
                publish=fake_publish,
                fetch_bytes=lambda url: new_bytes if 'jonathankhobson.github.io' in url else b'wrong URL',
                git=fake_git)
            item = next(p for p in updated['products'] if p['id'] == 'safe-install-review')
            sibling = next(p for p in updated['products'] if p['id'] == 'grounded-legal-research')
            self.assertEqual(item['source']['commit'], head)
            self.assertNotIn('commit', sibling['source'])
            self.assertEqual([commit for commit, _ in published], [base, head, base, head])
            self.assertEqual(published[0][1], [old_bytes] * 2)
            self.assertEqual(published[1][1], [new_bytes] * 2)
            self.assertEqual(len(item['historical_releases']), 1)
            self.assertTrue(all('/releases/download/' in a['url'] for a in item['assets']))
            self.assertTrue(all('jonathankhobson.github.io' in a['original_url'] for a in item['assets']))
            self.assertEqual(item['version']['value'], item['latest_release']['tag'])
            projected = next(p for p in external_release_records(updated) if p['id'] == 'safe-install-review')
            self.assertEqual(projected['releases'][0].get('release_notes'), note['release_notes'])
            self.assertEqual(validate_external_products(updated), [])
            for path in files:
                (checkout / path).write_bytes(next_bytes)
            subprocess.check_call(['git', 'add', '.'], cwd=checkout)
            subprocess.check_call(['git', 'commit', '-qm', 'Next skill update'], cwd=checkout)
            next_head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=checkout).decode().strip()
            next_note = {**note, 'source_commit': next_head, 'release_notes': 'Second tested update.'}
            (notes / 'safe-install-review.json').write_text(json.dumps(next_note))
            twice = complete_active_external_update(
                updated, 'safe-install-review', checkout, notes,
                publish=fake_publish,
                fetch_bytes=lambda url: next_bytes if 'jonathankhobson.github.io' in url else b'wrong URL',
                git=fake_git)
            twice_item = next(p for p in twice['products'] if p['id'] == 'safe-install-review')
            self.assertEqual(twice_item['source']['commit'], next_head)
            self.assertEqual(len(twice_item['historical_releases']), 2)
            self.assertEqual(len({r['tag'] for r in twice_item['historical_releases']}), 2)
            self.assertEqual(twice_item['historical_releases'][0]['release_notes'], note['release_notes'])
            with self.assertRaisesRegex(ValueError, 'no new exact source commit'):
                complete_active_external_update(twice, 'safe-install-review', checkout, notes,
                                                publish=fake_publish, git=fake_git)
            self.assertEqual(validate_external_products(twice), [])


if __name__ == '__main__':
    unittest.main()
