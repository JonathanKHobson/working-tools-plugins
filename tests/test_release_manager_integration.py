"""Contract checks around publishing and local completion entry points."""

import hashlib
import fcntl
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from scripts.release_manager import publisher, local_sync
import complete_update


class PublisherContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.package = Path(self.temp.name)/'x-1.0.0.zip'
        self.package.write_bytes(b'archive bytes')
        self.commit = 'a'*40
        self.tag = 'x/v1.0.0'
        self.record = {'id': 'x', 'version': '1.0.0', 'git_tag': self.tag}
        self.asset = {'name': self.package.name, 'size': self.package.stat().st_size,
                      'state': 'uploaded', 'url': 'https://example.test/asset',
                      'digest': 'sha256:' + hashlib.sha256(self.package.read_bytes()).hexdigest()}

    def test_matching_draft_resumes_without_replacing_existing_asset(self):
        draft = {'id': 7, 'tag_name': self.tag, 'target_commitish': self.commit,
                 'draft': True, 'assets': [self.asset]}
        published = {**draft, 'draft': False}
        with (patch.object(publisher, 'list_releases', return_value=[[draft]]),
              patch.object(publisher, 'api', side_effect=[draft, published]) as api,
              patch.object(publisher, 'resolved_tag', return_value=self.commit),
              patch.object(publisher, 'run', return_value=self.package.read_bytes()) as run):
            result = publisher.publish('owner/repo', self.record, self.commit,
                                       [self.package], notes='Reviewed file changes.')
        self.assertFalse(result['draft'])
        self.assertEqual(api.call_count, 2)
        self.assertTrue(run.called)
        self.assertTrue(all(call.args[:2] == ('gh', 'api') for call in run.call_args_list))

    def test_published_tag_collision_rejected_before_assets(self):
        published = {'id': 7, 'tag_name': self.tag, 'draft': False, 'assets': [self.asset]}
        with (patch.object(publisher, 'list_releases', return_value=[[published]]),
              patch.object(publisher, 'resolved_tag', return_value='b'*40)):
            with self.assertRaisesRegex(ValueError, 'Published tag collision'):
                publisher.publish('owner/repo', self.record, self.commit,
                                  [self.package], notes='Reviewed file changes.')

    def test_asset_digest_collision_rejected(self):
        wrong = {**self.asset, 'digest': 'sha256:' + 'f'*64, 'url': 'https://example.test/asset'}
        published = {'id': 7, 'tag_name': self.tag, 'draft': False, 'assets': [wrong]}
        with (patch.object(publisher, 'list_releases', return_value=[[published]]),
              patch.object(publisher, 'resolved_tag', return_value=self.commit),
              patch.object(publisher, 'run', return_value=b'wrong bytes')):
            with self.assertRaisesRegex(ValueError, 'Immutable asset collision'):
                publisher.publish('owner/repo', self.record, self.commit,
                                  [self.package], notes='Reviewed file changes.')

    def test_exact_commit_build_refuses_abbreviated_revision(self):
        with patch.object(publisher, 'run', return_value=self.commit.encode()):
            with self.assertRaisesRegex(ValueError, 'full exact commit'):
                publisher.exact_commit_build(Path(self.temp.name), 'aaaaaaa', Path(self.temp.name)/'out')


class LocalSyncContractTests(unittest.TestCase):
    def test_divergent_public_and_canonical_edits_are_conflicts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)/'public'; canonical = Path(directory)/'canonical'
            local = canonical/'x'/'README.md'; public = root/'plugins'/'x'/'README.md'
            for target, value in ((local, b'canonical edit'), (public, b'public edit')):
                target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(value)
            inventory = root/'catalog'/'source-inventory.json'
            inventory.parent.mkdir(parents=True, exist_ok=True)
            inventory.write_text(json.dumps({'packages': [{'id': 'x',
                'canonical_source': {'id': 'x'},
                'files': {'README.md': hashlib.sha256(b'baseline').hexdigest()}}]}))
            changes, conflicts = local_sync.plan(root, canonical)
            self.assertFalse(changes)
            self.assertEqual(len(conflicts), 1)
            self.assertIn('divergent', conflicts[0])

    def test_product_root_link_requires_exact_reviewed_target_and_blocks_nested_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)/'public'; canonical = Path(directory)/'canonical'
            physical = Path(directory)/'physical'/'x'
            physical.mkdir(parents=True); canonical.mkdir()
            (canonical/'x').symlink_to(physical, target_is_directory=True)
            (physical/'README.md').write_bytes(b'baseline')
            public = root/'plugins/x/README.md'
            public.parent.mkdir(parents=True); public.write_bytes(b'baseline')
            inventory = root/'catalog/source-inventory.json'
            inventory.parent.mkdir(parents=True)
            inventory.write_text(json.dumps({'packages': [{'id': 'x',
                'canonical_source': {'id': 'x'},
                'files': {'README.md': hashlib.sha256(b'baseline').hexdigest()}}]}))
            with self.assertRaisesRegex(ValueError, 'Unapproved canonical product root symlink'):
                local_sync.plan(root, canonical)
            other = Path(directory)/'other'; other.mkdir()
            with self.assertRaisesRegex(ValueError, 'target differs'):
                local_sync.plan(root, canonical, {'x': str(other.resolve())})
            self.assertEqual(local_sync.plan(root, canonical, {'x': str(physical.resolve())}), ({}, []))
            (physical/'README.md').unlink()
            (physical/'README.md').symlink_to(public)
            changes, conflicts = local_sync.plan(root, canonical, {'x': str(physical.resolve())})
            self.assertFalse(changes)
            self.assertIn('unsafe source path', conflicts[0])


class CompletionContractTests(unittest.TestCase):
    def fixture(self, root, names=('x',)):
        canonical = root/'canonical'
        rows = []
        packages = []
        for ident in names:
            public = root/'plugins'/ident
            private = canonical/ident
            payload = {
                'references/shared.md': b'original instruction\n',
                'README.md': b'original readme\n',
                'CHANGELOG.md': b'# Changelog\n',
                'PROVENANCE.json': b'{"version":"1.0.0","files":[]}',
                'plugin.json': b'{"version":"1.0.0"}',
                '.codex-plugin/plugin.json': b'{"version":"1.0.0"}',
                '.claude-plugin/plugin.json': b'{"version":"1.0.0"}',
            }
            for rel, content in payload.items():
                for base in (public, private):
                    target = base/rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(content)
            files = {rel: hashlib.sha256(content).hexdigest() for rel, content in payload.items()}
            rows.append({'id': ident, 'version': '1.0.0',
                'canonical_source': {'id': ident, 'revision': {'sha256': '0'*64}},
                'files': files})
            packages.append({'id': ident, 'version': '1.0.0', 'distribution': 'released'})
            notes = root/'catalog/changes'/(ident+'.json')
            notes.parent.mkdir(parents=True, exist_ok=True)
            notes.write_text(json.dumps({'level': 'patch', 'summary': 'Correct an instruction.',
                'why': 'The reviewed instruction was inaccurate.',
                'compatibility': 'No invocation changes.',
                'upgrade_guidance': 'Replace the prior package.',
                'validation': 'Compared the reviewed instruction text.',
                'notes': 'The shared reference now has the corrected sentence.'}))
        (root/'catalog/source-inventory.json').write_text(json.dumps({'packages': rows}))
        (root/'catalog/packages.json').write_text(json.dumps({'packages': packages}))
        return canonical

    def test_committed_public_instruction_is_detected_by_actual_prepare(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical = self.fixture(root)
            (root/'plugins/x/README.md').write_text('corrected readme\n')
            with (patch.object(complete_update, 'ROOT', root),
                  patch.object(complete_update, 'command')):
                entries = complete_update.prepare({'canonical_root': str(canonical)})
            self.assertEqual(entries[0]['version'], '1.0.1')
            self.assertEqual(entries[0]['changed_files'], ['README.md'])
            self.assertEqual((canonical/'x/README.md').read_text(), 'corrected readme\n')
            self.assertFalse((root/'catalog/changes/x.json').exists())
            with (patch.object(complete_update, 'ROOT', root),
                  patch.object(complete_update, 'command')):
                self.assertEqual(complete_update.prepare({'canonical_root': str(canonical)}), [])

    def test_refresh_retains_existing_exact_version_heading_bytes(self):
        headings = (
            b'# Changelog\n\n## 0.3.0\n\nAuthored notes.\n',
            '# Changelog\r\n\r\n## 0.3.0 · 2026-10-11\r\n\r\nAuthored notes.\r\n'.encode(),
        )
        for original in headings:
            with self.subTest(original=original), tempfile.TemporaryDirectory() as directory:
                root = Path(directory); canonical = self.fixture(root)
                public_changelog = root/'plugins/x/CHANGELOG.md'
                public_changelog.write_bytes(original)
                local_sync.refresh_reviewed(root, canonical, 'x', '0.3.0', 'Generated notes')
                self.assertEqual(public_changelog.read_bytes(), original)
                self.assertEqual((canonical/'x/CHANGELOG.md').read_bytes(), original)

    def test_refresh_inserts_missing_version_despite_prefix_collision(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); canonical = self.fixture(root)
            changelog = root/'plugins/x/CHANGELOG.md'
            changelog.write_text('# Changelog\n\n## 0.3.00 · 2026-10-11\n\nPrior entry.\n')
            local_sync.refresh_reviewed(root, canonical, 'x', '0.3.0', 'New reviewed notes')
            content = changelog.read_text()
            self.assertIn('## 0.3.0\n\nNew reviewed notes', content)
            self.assertIn('## 0.3.00 · 2026-10-11\n\nPrior entry.', content)
            self.assertEqual(content.count('## 0.3.0\n'), 1)

    def test_shared_source_change_releases_every_reviewed_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical = self.fixture(root, ('x', 'y'))
            source = root/'shared/template.md'
            source.parent.mkdir()
            source.write_text('corrected shared instruction\n')
            config = {'canonical_root': str(canonical),
                'shared_shipped_paths': {'shared/template.md': [
                    'plugins/x/references/shared.md', 'plugins/y/references/shared.md']}}
            with (patch.object(complete_update, 'ROOT', root),
                  patch.object(complete_update, 'command')):
                entries = complete_update.prepare(config)
            self.assertEqual({row['id'] for row in entries}, {'x', 'y'})
            self.assertTrue(all(row['version'] == '1.0.1' for row in entries))
            self.assertTrue(all(row['shared_sources'] == ['shared/template.md'] for row in entries))
            for ident in ('x', 'y'):
                self.assertEqual((root/'plugins'/ident/'references/shared.md').read_bytes(), source.read_bytes())
                self.assertEqual((canonical/ident/'references/shared.md').read_bytes(), source.read_bytes())
            self.assertIn('shared/template.md', complete_update.scoped_paths(entries))

    def test_prepare_accepts_only_pinned_product_root_link_for_shared_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            canonical = self.fixture(root)
            physical = root/'physical/x'
            physical.parent.mkdir()
            (canonical/'x').rename(physical)
            (canonical/'x').symlink_to(physical, target_is_directory=True)
            source = root/'shared/template.md'
            source.parent.mkdir(); source.write_text('corrected shared instruction\n')
            config = {'canonical_root': str(canonical), 'canonical_sources': {'x': str(physical.resolve())},
                'shared_shipped_paths': {'shared/template.md': ['plugins/x/references/shared.md']}}
            with (patch.object(complete_update, 'ROOT', root),
                  patch.object(complete_update, 'command')):
                entries = complete_update.prepare(config)
            self.assertEqual(entries[0]['changed_files'], ['references/shared.md'])
            self.assertEqual((physical/'references/shared.md').read_bytes(), source.read_bytes())
            self.assertEqual((root/'plugins/x/references/shared.md').read_bytes(), source.read_bytes())

    def test_scoped_paths_exclude_unrelated_infrastructure(self):
        paths = complete_update.scoped_paths([{'id': 'x', 'version': '1.0.1',
            'changed_files': ['skills/a/SKILL.md']}])
        self.assertIn('plugins/x/skills/a/SKILL.md', paths)
        self.assertIn('catalog/releases/x/1.0.1.json', paths)
        self.assertNotIn('scripts/complete_update.py', paths)
        self.assertNotIn('catalog/external-products.json', paths)
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            complete_update.scoped_paths([{'id': 'x', 'version': '1.0.1',
                'changed_files': ['../private.txt']}])

    def test_scoped_commit_stages_only_reviewed_paths(self):
        entry = {'id': 'x', 'version': '1.0.1', 'changed_files': ['README.md']}
        outputs = [b'', b'catalog/releases/x/1.0.1.json\0', b'a'*40]
        with (patch.object(complete_update, 'run', side_effect=outputs),
              patch.object(complete_update, 'command') as command):
            self.assertEqual(complete_update.commit_prepared([entry]), 'a'*40)
        added = command.call_args_list[0].args
        self.assertEqual(added[:4], ('git', 'add', '-A', '--'))
        self.assertIn('plugins/x/README.md', added)
        self.assertNotIn('scripts/complete_update.py', added)
        self.assertEqual(command.call_args_list[1].args[:3], ('git', 'commit', '-m'))

    def test_current_set_requires_every_plugin_and_exact_install_asset(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = root/'catalog/packages.json'; registry.parent.mkdir(parents=True)
            registry.write_text(json.dumps({'packages': [{'id': 'x'}]}))
            release = {'release_key': 'x/v1.0.0', 'version': '1.0.0',
                       'source_commit': 'a'*40, 'assets': [{'role': 'installation', 'sha256': 'b'*64}]}
            catalog = {'products': [{'id': 'x', 'kind': 'plugin',
                                     'current_release_key': 'x/v1.0.0', 'releases': [release]}]}
            with patch.object(complete_update, 'ROOT', root):
                self.assertEqual(complete_update.current_published_set(catalog),
                    [{'release_key': 'x/v1.0.0', 'product_id': 'x', 'version': '1.0.0',
                      'source_commit': 'a'*40, 'sha256': 'b'*64}])
                (root/'catalog/integrations.json').write_text(json.dumps({'products': [{'id': 'pack'}]}))
                with self.assertRaisesRegex(ValueError, 'missing=.*pack'):
                    complete_update.current_published_set(catalog)
                catalog['products'].append({'id': 'pack', 'kind': 'integration',
                    'current_release_key': 'pack/v0.1.0', 'releases': [{
                        'release_key': 'pack/v0.1.0', 'version': '0.1.0',
                        'source_commit': 'c'*40, 'assets': [
                            {'role': 'installation', 'sha256': 'd'*64}]}]})
                self.assertEqual(len(complete_update.current_published_set(catalog)), 2)
                catalog['products'][0]['current_release_key'] = None
                with self.assertRaisesRegex(ValueError, 'No verified current'):
                    complete_update.current_published_set(catalog)

    def test_reconcile_reuses_pending_receipt_without_prepare_or_version_bump(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = root/'dist/release-manager'; state.mkdir(parents=True)
            prior = {'status': 'catalog_pending', 'changed': [{'id': 'x', 'version': '1.0.1',
                     'changed_files': ['README.md']}], 'published': [{'id': 'x', 'version': '1.0.1'}],
                     'source_commit': 'a'*40}
            (state/'receipt.json').write_text(json.dumps(prior))
            config = root/'config.json'; config.write_text('{}')
            with (patch.object(complete_update, 'ROOT', root),
                  patch.object(complete_update, 'pending_entries', return_value=[]),
                  patch.object(complete_update, 'external_plan', return_value=({'ready': []}, {})),
                  patch.object(complete_update, 'prepare') as prepare,
                  patch.object(complete_update, 'command') as command,
                  patch.object(complete_update, 'publish_pending', return_value=prior['published']) as publish,
                  patch.object(complete_update, 'sync_site') as sync,
                  patch.object(sys, 'argv', ['complete_update.py', '--config', str(config), '--reconcile-only'])):
                complete_update.main()
            prepare.assert_not_called()
            publish.assert_not_called()
            sync.assert_called_once()
            self.assertEqual(json.loads((state/'receipt.json').read_text())['changed'], prior['changed'])
            command.assert_not_called()

    def test_completed_receipt_checks_new_source_without_republishing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = root/'dist/release-manager'; state.mkdir(parents=True)
            prior = {'status': 'complete', 'changed': [{'id': 'x', 'version': '1.0.1',
                'changed_files': ['README.md']}], 'published': [{'id': 'x', 'version': '1.0.1'}]}
            (state/'receipt.json').write_text(json.dumps(prior))
            config = root/'config.json'; config.write_text('{}')
            with (patch.object(complete_update, 'ROOT', root),
                  patch.object(complete_update, 'pending_entries', return_value=[]),
                  patch.object(complete_update, 'external_plan', return_value=({'ready': []}, {})),
                  patch.object(complete_update, 'unfinished_committed_entries', return_value=[]),
                  patch.object(complete_update, 'prepare', return_value=[]) as prepare,
                  patch.object(complete_update, 'publish_pending') as publish,
                  patch.object(complete_update, 'sync_site') as sync,
                  patch.object(complete_update, 'command') as command,
                  patch.object(sys, 'argv', ['complete_update.py', '--config', str(config)])):
                complete_update.main()
            prepare.assert_called_once()
            sync.assert_called_once()
            publish.assert_not_called()
            command.assert_not_called()

    def test_reconcile_only_after_completion_skips_package_detection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = root/'dist/release-manager'; state.mkdir(parents=True)
            (state/'receipt.json').write_text(json.dumps({'status': 'complete',
                'changed': [], 'published': []}))
            config = root/'config.json'; config.write_text('{}')
            with (patch.object(complete_update, 'ROOT', root),
                  patch.object(complete_update, 'pending_entries', return_value=[]),
                  patch.object(complete_update, 'external_plan', return_value=({'ready': []}, {})),
                  patch.object(complete_update, 'unfinished_committed_entries', return_value=[]),
                  patch.object(complete_update, 'prepare') as prepare,
                  patch.object(complete_update, 'publish_pending') as publish,
                  patch.object(complete_update, 'sync_site') as sync,
                  patch.object(complete_update, 'command') as command,
                  patch.object(sys, 'argv', ['complete_update.py', '--config', str(config), '--reconcile-only'])):
                complete_update.main()
            prepare.assert_not_called()
            publish.assert_not_called()
            command.assert_not_called()
            sync.assert_called_once()

    def test_reconcile_only_resumes_verified_external_ledger_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = root/'dist/release-manager'; state.mkdir(parents=True)
            (state/'receipt.json').write_text(json.dumps({'status': 'external_publishing',
                'changed': [], 'published': [], 'external_pending_ledger': True,
                'external_in_progress': {'product_id': 'guide', 'source_commit': 'b'*40}}))
            config = root/'config.json'; config.write_text('{}')
            def committed(receipt):
                receipt['external_pending_ledger'] = False
                receipt['external_in_progress'] = None
                receipt['status'] = 'catalog_pending'
            with (patch.object(complete_update, 'ROOT', root),
                  patch.object(complete_update, 'commit_external_ledger', side_effect=committed) as commit,
                  patch.object(complete_update, 'external_plan') as plan,
                  patch.object(complete_update, 'pending_entries', return_value=[]),
                  patch.object(complete_update, 'unfinished_committed_entries', return_value=[]),
                  patch.object(complete_update, 'prepare') as prepare,
                  patch.object(complete_update, 'publish_pending') as publish,
                  patch.object(complete_update, 'sync_site') as sync,
                  patch.object(sys, 'argv', ['complete_update.py', '--config', str(config), '--reconcile-only'])):
                complete_update.main()
            commit.assert_called_once()
            plan.assert_not_called()
            prepare.assert_not_called()
            publish.assert_not_called()
            sync.assert_called_once()

    def test_missing_receipt_recovers_only_current_unpublished_record(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            records = [{'id': 'x', 'version': '1.0.1'}, {'id': 'y', 'version': '2.0.0'}]
            target = root/'catalog/packages.json'; target.parent.mkdir(parents=True)
            target.write_text(json.dumps({'packages': records}))
            for row in records:
                record = root/'catalog/releases'/row['id']/(row['version']+'.json')
                record.parent.mkdir(parents=True)
                record.write_text(json.dumps({'product_id': row['id'], 'version': row['version'],
                    'git_tag': row['id']+'/v'+row['version'], 'changed_files': ['README.md']}))
            pages = [[{'tag_name': 'x/v1.0.0', 'draft': False},
                      {'tag_name': 'y/v2.0.0', 'draft': False}]]
            with (patch.object(complete_update, 'ROOT', root),
                  patch.object(complete_update, 'run', return_value=b'a'*40),
                  patch.object(complete_update, 'list_releases', return_value=pages)):
                pending = complete_update.unfinished_committed_entries()
            self.assertEqual(pending, [{'id': 'x', 'version': '1.0.1',
                'changed_files': ['README.md'], 'shared_sources': []}])

    def test_external_completion_records_verified_guide_before_site(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            current = {'commit': 'a'*40}
            def ledger(_):
                return {'products': [{'id': 'guide', 'source': {'id': 'shareables',
                    'commit': current['commit']}, 'disposition': 'download'}]}
            calls = []
            def command(*args, **kwargs):
                calls.append(args)
                if 'scripts/complete_external_update.py' in args:
                    current['commit'] = 'b'*40
            receipt = {'status': 'complete', 'changed': [], 'published': []}
            plan = {'ready': [{'product_id': 'guide', 'source_commit': 'b'*40}]}
            with (patch.object(complete_update, 'ROOT', root),
                  patch('release_manager.legacy.load_external_products', side_effect=ledger),
                  patch.object(complete_update, 'command', side_effect=command),
                  patch.object(complete_update, 'run', side_effect=[
                      b'', b'catalog/external-products.json\0'])):
                complete_update.publish_external({'external_checkouts': {'shareables': '/reviewed'}},
                    receipt, plan, {'shareables': '/reviewed'})
            self.assertEqual(current['commit'], 'b'*40)
            self.assertEqual(receipt['status'], 'catalog_pending')
            self.assertFalse(receipt['external_pending_ledger'])
            self.assertEqual(receipt['external_published'][0]['source_commit'], 'b'*40)
            self.assertTrue(any(call[:3] == ('git', 'push', 'origin') for call in calls))
            self.assertEqual(sum('scripts/complete_external_update.py' in call for call in calls), 1)

    def test_integration_completion_noop_and_retry_receipt_are_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger = root/'catalog/integrations.json'; ledger.parent.mkdir(parents=True)
            ledger.write_text('{"products":[]}')
            receipt = {'status': 'complete', 'changed': [], 'published': []}
            published = {'id': 'pack', 'version': '0.1.0', 'source_commit': 'a'*40,
                         'release_url': 'https://example.test/release', 'sha256': 'b'*64}
            module = types.ModuleType('release_manager.packs')
            module.complete = lambda root, notes: []
            with (patch.object(complete_update, 'ROOT', root),
                  patch.dict(sys.modules, {'release_manager.packs': module})):
                complete_update.publish_integrations(receipt)
                self.assertEqual(receipt['status'], 'complete')
                self.assertFalse(receipt['integration_in_progress'])
                module.complete = lambda root, notes: [published]
                complete_update.publish_integrations(receipt)
                complete_update.publish_integrations(receipt)
            self.assertEqual(receipt['status'], 'catalog_pending')
            self.assertEqual(receipt['integrations_published'], [published])

    def test_second_completion_cannot_take_publication_lock(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            state = root/'dist/release-manager'; state.mkdir(parents=True)
            config = root/'config.json'; config.write_text('{}')
            with (state/'completion.lock').open('w') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                with (patch.object(complete_update, 'ROOT', root),
                      patch.object(sys, 'argv', ['complete_update.py', '--config', str(config)])):
                    with self.assertRaisesRegex(SystemExit, 'Another completion run'):
                        complete_update.main()

    def test_no_shipped_change_completes_without_push(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root/'config.json'; config.write_text('{}')
            with (patch.object(complete_update, 'ROOT', root),
                  patch.object(complete_update, 'pending_entries', return_value=[]),
                  patch.object(complete_update, 'external_plan', return_value=({'ready': []}, {})),
                  patch.object(complete_update, 'unfinished_committed_entries', return_value=[]),
                  patch.object(complete_update, 'prepare', return_value=[]),
                  patch.object(complete_update, 'command') as command,
                  patch.object(complete_update, 'sync_site') as sync,
                  patch.object(sys, 'argv', ['complete_update.py', '--config', str(config)])):
                complete_update.main()
            command.assert_not_called()
            sync.assert_called_once()
            self.assertEqual(json.loads((root/'dist/release-manager/receipt.json').read_text())['status'], 'catalog_pending')

    def test_site_receipt_must_match_full_expected_set(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog_path = root/'catalog/release-history.json'; catalog_path.parent.mkdir(parents=True)
            (root/'catalog/packages.json').write_text(json.dumps({'packages': [{'id': 'x'}]}))
            catalog_path.write_text(json.dumps({'products': [{'id': 'x', 'kind': 'plugin',
                'current_release_key': 'x/v1.0.0', 'releases': [{'release_key': 'x/v1.0.0',
                'version': '1.0.0', 'source_commit': 'a'*40,
                'assets': [{'role': 'installation', 'sha256': 'b'*64}]}]}]}))
            proof_path = root/'proof.json'
            proof_path.write_text(json.dumps({'status': 'deployed', 'deployment_id': 'dep-1',
                'source_commit': 'c'*40, 'maintained_source_commit': 'c'*40,
                'live_url': 'https://example.test', 'version_id': 'v-1', 'published_set': []}))
            config = {'site_adapter': ['fake-adapter'], 'site_receipt': str(proof_path),
                      '_config_path': str(root/'config.json')}
            receipt = {'status': 'releases_published', 'changed': [], 'published': []}
            with (patch.object(complete_update, 'ROOT', root),
                  patch.object(complete_update, 'command'),
                  patch.object(complete_update, 'run', return_value=b''),
                  patch.object(complete_update.subprocess, 'run') as adapter):
                with self.assertRaisesRegex(ValueError, 'full current release set'):
                    complete_update.sync_site(config, receipt)
            self.assertEqual(adapter.call_args.kwargs['env']['WORKING_TOOLS_RELEASE_CONFIG'], config['_config_path'])
            self.assertEqual(receipt['status'], 'catalog_pending')
            self.assertEqual(len(receipt['expected_published_set']), 1)

    def test_site_projection_refuses_uncommitted_external_ledger(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with (patch.object(complete_update, 'ROOT', root),
                  patch.object(complete_update, 'run', return_value=b' M catalog/external-products.json'),
                  patch.object(complete_update, 'command') as command):
                with self.assertRaisesRegex(ValueError, 'ledger must be committed'):
                    complete_update.sync_site({'site_adapter': ['fake-adapter']},
                        {'status': 'catalog_pending', 'changed': [], 'published': []})
            command.assert_not_called()

    def test_site_projection_refuses_uncommitted_integration_ledger(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger = root/'catalog/integrations.json'; ledger.parent.mkdir()
            ledger.write_text('{"products":[]}')
            with (patch.object(complete_update, 'ROOT', root),
                  patch.object(complete_update, 'run', side_effect=[
                      b'', b' M catalog/integrations.json']),
                  patch.object(complete_update, 'command') as command):
                with self.assertRaisesRegex(ValueError, 'Integration release ledger must be committed'):
                    complete_update.sync_site({'site_adapter': ['fake-adapter']},
                        {'status': 'catalog_pending', 'changed': [], 'published': []})
            command.assert_not_called()


if __name__ == '__main__':
    unittest.main()
