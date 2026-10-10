"""Synthetic coverage tests; no private source or inventory regeneration."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1]/'scripts/source_inventory.py'
spec = importlib.util.spec_from_file_location('source_inventory', MODULE)
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'public'
        self.canonical = Path(self.temp.name)/'canonical'
        self.package = self.root/'plugins/fixture'
        self.catalog = [{'id': 'fixture', 'version': '1.0.0'}]
        source = {
            'plugin.json': json.dumps({'name': 'fixture', 'version': '1.0.0'}).encode(),
            'skills/demo/SKILL.md': b'# Complete demo\n',
            'libraries/deep/skills/second/SKILL.md': b'# Nested skill\n',
            'references/full-method.md': b'The full supported procedure.\n',
        }
        for path, raw in source.items():
            self.write(self.package/path, raw)
            self.write(self.canonical/'fixture'/path, raw)
        hashes = {path: digest(raw) for path, raw in source.items()}
        components = [{'id': 'fixture:'+path, 'kind': 'skill-head', 'path': path}
                      for path in source if path.endswith('SKILL.md')]
        extra = b'Unredistributed synthetic collection\n'
        self.write(self.canonical/'fixture/held/profiles.json', extra)
        self.entry = {'id': 'fixture', 'version': '1.0.0',
                      'canonical_source': {'id': 'fixture', 'revision': {
                          'kind': inventory.REVISION_KIND, 'sha256': inventory.tree_digest(hashes)}},
                      'files': hashes, 'components': components,
                      'excluded_source': {'files': 1, 'tree_sha256': inventory.tree_digest({'held/profiles.json': digest(extra)}),
                                          'dispositions': [{'scope': 'held', 'disposition': 'private',
                                                            'reason': 'Synthetic ungranted source',
                                                            'capability_effect': 'Requires an authorized external collection'}]}}
        self.baseline_entry = {'id': 'reviewed-fixture', 'canonical_owner': 'fixture', 'disposition': 'included',
                               'capability_effect': 'Complete fixture method',
                               'expected_components': [c['id'] for c in components], 'evidence': ['Synthetic reviewed source receipt']}
        self.snapshot = {'schema_version': 1, 'packages': [self.entry]}
        self.baseline = {'schema_version': 1, 'entries': [self.baseline_entry]}
        self.save()

    def write(self, path, raw):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)

    def save(self):
        for name, document in [('source-inventory.json', self.snapshot), ('coverage-baseline.json', self.baseline), ('packages.json', {'packages': self.catalog})]:
            self.write(self.root/'catalog'/name, (json.dumps(document)+'\n').encode())

    def check(self, canonical=False):
        self.save()
        return inventory.validate_inventory(self.root, self.catalog, self.canonical if canonical else None)

    def assertError(self, fragment, *, canonical=False):
        errors = self.check(canonical)
        self.assertTrue(any(fragment in error for error in errors), errors)
        return errors

    def test_reviewed_public_and_live_canonical_modes_pass(self):
        self.assertEqual(self.check(), [])
        self.assertEqual(self.check(canonical=True), [])

    def test_digest_record_format_is_locked(self):
        expected = hashlib.sha256(('a'*64+'  a.txt\n'+'b'*64+'  z.txt\n').encode()).hexdigest()
        self.assertEqual(inventory.tree_digest({'z.txt': 'b'*64, 'a.txt': 'a'*64}), expected)
        self.assertEqual(inventory.tree_digest({}), digest(b''))

    def test_removed_skill_and_support_are_named(self):
        for path in ['skills/demo/SKILL.md', 'references/full-method.md']:
            with self.subTest(path=path):
                (self.package/path).unlink()
                self.assertError('missing file '+path)
                self.write(self.package/path, b'restored')

    def test_unexpected_public_file_is_named(self):
        self.write(self.package/'new-unreviewed.md', b'new')
        self.assertError('unexpected file new-unreviewed.md')

    def test_changed_public_hash_is_named(self):
        self.write(self.package/'references/full-method.md', b'changed')
        self.assertError('changed file references/full-method.md')

    def test_wrong_inventory_version_and_manifest_version(self):
        self.entry['version'] = '2.0.0'
        self.assertError('wrong version')
        self.entry['version'] = '1.0.0'
        self.write(self.package/'plugin.json', b'{"version":"9.0.0"}')
        self.assertError('wrong version in plugin.json')

    def test_stale_source_revision_is_rejected(self):
        self.entry['canonical_source']['revision']['sha256'] = '0'*64
        self.assertError('source revision digest differs')

    def test_registry_and_inventory_removal_cannot_erase_baseline(self):
        self.catalog.clear()
        self.snapshot['packages'].clear()
        shutil.rmtree(self.package)
        self.assertError('included owner missing from source inventory: fixture')

    def test_inventory_owner_must_be_in_included_baseline(self):
        self.baseline['entries'].clear()
        self.assertError('inventory owner absent from included baseline')

    def test_missing_extra_and_duplicate_package_ids(self):
        self.snapshot['packages'].clear()
        self.assertError('missing package ID fixture')
        self.snapshot['packages'] = [self.entry, copy.deepcopy(self.entry)]
        self.assertError('duplicate ID fixture')
        self.snapshot['packages'] = [self.entry]
        self.catalog.append(copy.deepcopy(self.catalog[0]))
        self.assertError('catalog: duplicate ID fixture')
        self.catalog = []
        self.assertError('unexpected package ID fixture')

    def test_unregistered_physical_package_is_detected(self):
        (self.root/'plugins/orphan').mkdir()
        self.assertError('unexpected package ID orphan')

    def test_canonical_included_hash_and_missing_file(self):
        path = self.canonical/'fixture/references/full-method.md'
        path.write_text('changed')
        self.assertError('canonical fixture: changed file references/full-method.md', canonical=True)
        path.unlink()
        self.assertError('canonical fixture: missing file references/full-method.md', canonical=True)

    def test_canonical_extra_add_remove_and_change_are_not_rebaselined(self):
        path = self.canonical/'fixture/held/profiles.json'
        original = path.read_bytes()
        changes = [('changed', lambda: path.write_text('changed')), ('removed', path.unlink),
                   ('added', lambda: self.write(path.parent/'another-private-name.json', b'new'))]
        for state, change in changes:
            with self.subTest(state=state):
                path.write_bytes(original)
                additional = path.parent/'another-private-name.json'
                additional.unlink(missing_ok=True)
                change()
                errors = self.assertError('unreviewed excluded source additions/removals/changes', canonical=True)
                self.assertFalse(any('another-private-name' in error or str(self.canonical) in error for error in errors))
                self.assertTrue(any('reviewed scopes: held' in error for error in errors))

    def test_public_mode_does_not_claim_live_source_verification(self):
        shutil.rmtree(self.canonical)
        self.assertEqual(self.check(), [])
        result = subprocess.run([sys.executable, str(MODULE), '--root', str(self.root)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('live canonical source not checked', json.loads(result.stdout)['verification'])

    def test_live_namespace_requires_baseline_owner_for_all_manifest_forms(self):
        for manifest in ('plugin.json', '.codex-plugin/plugin.json', '.claude-plugin/plugin.json'):
            with self.subTest(manifest=manifest):
                source = self.canonical/'unreviewed-owner'
                self.write(source/manifest, b'{}')
                self.assertError('package ID without baseline owner: unreviewed-owner', canonical=True)
                shutil.rmtree(source)

    def test_nonincluded_canonical_owner_is_valid_namespace_coverage(self):
        source = self.canonical/'held-owner'
        self.write(source/'.claude-plugin/plugin.json', b'{}')
        self.baseline['entries'].append({'id': 'held-owner', 'canonical_owner': 'held-owner', 'disposition': 'private',
                                        'capability_effect': 'Private source excluded from the public edition',
                                        'expected_components': [], 'evidence': ['Synthetic private source receipt']})
        self.assertEqual(self.check(canonical=True), [])

    def test_namespace_ignores_nonpackage_folders_and_public_mode(self):
        self.write(self.canonical/'ordinary-notes/README.md', b'Nonpackage material')
        self.assertEqual(self.check(canonical=True), [])
        self.write(self.canonical/'unreviewed-owner/plugin.json', b'{}')
        self.assertEqual(self.check(), [])

    def test_excluded_scope_must_match_even_when_count_and_hash_match(self):
        self.entry['excluded_source']['dispositions'][0]['scope'] = 'unrelated'
        errors = self.assertError('unreviewed excluded source scope', canonical=True)
        self.assertFalse(any('held/profiles.json' in error or str(self.canonical) in error for error in errors))
        self.assertFalse(any('additions/removals/changes' in error for error in errors))

    def test_excluded_scope_matches_exact_path_and_directory_prefix(self):
        row = self.entry['excluded_source']['dispositions'][0]
        for scope in ('held/profiles.json', 'held', 'held/'):
            with self.subTest(scope=scope):
                row['scope'] = scope
                self.assertEqual(self.check(canonical=True), [])
        row['scope'] = 'hel'
        self.assertError('unreviewed excluded source scope', canonical=True)

    def test_scope_matching_is_component_bounded(self):
        row = self.entry['excluded_source']['dispositions'][0]
        row['scope'] = 'held/profile'
        self.assertError('unreviewed excluded source scope', canonical=True)

    def test_every_baseline_row_requires_evidence(self):
        self.baseline_entry['evidence'] = []
        self.assertError('evidence must be a nonempty list')
        self.baseline_entry['evidence'] = ['Synthetic reviewed source receipt']
        self.baseline['entries'].append({'id': 'blocked-owner', 'canonical_owner': 'blocked-owner',
                                        'disposition': 'blocked', 'capability_effect': 'Unresolved external requirement',
                                        'expected_components': [], 'evidence': []})
        self.assertError('coverage-baseline blocked-owner: evidence must be a nonempty list')

    def test_exclusions_need_reason_and_capability_effect(self):
        for field in ('reason', 'capability_effect'):
            row = self.entry['excluded_source']['dispositions'][0]
            value = row.pop(field)
            self.assertError('requires '+field)
            row[field] = value
        self.entry['excluded_source']['dispositions'] = []
        self.assertError('require explicit dispositions')

    def test_baseline_nonincluded_dispositions_remain_explicit(self):
        for disposition in ('external', 'private', 'retired', 'blocked'):
            row = {'id': 'held-'+disposition, 'canonical_owner': 'outside-owner', 'disposition': disposition,
                   'expected_components': [], 'evidence': ['Synthetic hold receipt']}
            self.baseline['entries'].append(row)
            self.assertError('nonincluded disposition requires capability_effect')
            row['capability_effect'] = 'Explicitly unavailable; source/runtime permission still required'
            self.assertEqual(self.check(), [])
        self.baseline['entries'].append(copy.deepcopy(self.baseline_entry))
        self.assertError('coverage-baseline: duplicate ID reviewed-fixture')

    def test_malformed_paths_and_digests(self):
        for path in ('../escape', '/absolute', 'a\\b', 'a//b', './a', 'a/../b', 'a\x00b', 'a\nb', 'a\u0085b', 'a\u202eb', 'C:/host'):
            with self.subTest(path=repr(path)):
                self.entry['files'][path] = 'a'*64
                self.assertError('malformed relative file path')
                del self.entry['files'][path]
        self.entry['files']['references/full-method.md'] = 'INVALID'
        self.assertError('invalid sha256 for references/full-method.md')

    def test_nested_skill_requires_named_component(self):
        self.entry['components'].pop()
        self.assertError('SKILL.md lacks named component: libraries/deep/skills/second/SKILL.md')
        self.assertError('expected component missing')

    def test_component_ids_paths_and_kinds_are_checked(self):
        self.entry['components'].append(copy.deepcopy(self.entry['components'][0]))
        self.assertError('duplicate component ID')
        self.entry['components'].pop()
        component = self.entry['components'][0]
        component['kind'] = ''
        self.assertError('component kind must be nonempty')
        component['kind'] = 'skill-head'
        component['path'] = 'missing.md'
        self.assertError('component path not included: missing.md')
        component['id'] = 'other:skills/demo/SKILL.md'
        self.assertError('component ID must use a safe owner-prefixed path')

    def test_component_ids_are_globally_unique(self):
        second = copy.deepcopy(self.entry)
        second['id'] = 'second'
        second['canonical_source']['id'] = 'second'
        self.snapshot['packages'].append(second)
        self.catalog.append({'id': 'second', 'version': '1.0.0'})
        shutil.copytree(self.package, self.root/'plugins/second')
        self.assertError('duplicate component ID fixture:skills/demo/SKILL.md')

    def test_generated_files_match_packages_exclusions(self):
        for rel in ('.git/metadata', '.venv/site.py', '__pycache__/x', '.pytest_cache/state', '.DS_Store', 'x.pyc', 'x.pyo'):
            self.write(self.package/rel, b'generated')
            self.write(self.canonical/'fixture'/rel, b'generated')
        self.assertEqual(self.check(canonical=True), [])

    def test_symlinks_are_rejected_even_inside_excluded_trees(self):
        target = self.package/'references/full-method.md'
        link = self.package/'.venv/linked'
        link.parent.mkdir()
        link.symlink_to(target)
        self.assertError('symlink is not distributable')
        link.unlink()
        (self.canonical/'fixture/held-link').symlink_to(target)
        self.assertError('unsafe or unreadable source tree', canonical=True)

    def test_selected_canonical_owner_directory_alias_passes(self):
        maintained = Path(self.temp.name)/'maintained-source'
        (self.canonical/'fixture').rename(maintained)
        (self.canonical/'fixture').symlink_to(maintained, target_is_directory=True)
        self.assertEqual(self.check(canonical=True), [])
        (maintained/'held/linked').symlink_to(maintained/'references/full-method.md')
        self.assertError('unsafe or unreadable source tree', canonical=True)

    def test_broken_canonical_owner_alias_fails_without_private_target(self):
        shutil.rmtree(self.canonical/'fixture')
        target = Path(self.temp.name)/'private-missing-owner'
        (self.canonical/'fixture').symlink_to(target, target_is_directory=True)
        errors = self.assertError('missing or broken canonical owner directory', canonical=True)
        self.assertFalse(any(str(target) in error for error in errors))

    def test_public_owner_directory_alias_remains_rejected(self):
        maintained = Path(self.temp.name)/'public-maintained-source'
        self.package.rename(maintained)
        self.package.symlink_to(maintained, target_is_directory=True)
        self.assertError('symlink package ID fixture')
        self.assertError('symlink package root')

    def declare_alias(self, relative='runtime/private-runtime', target='../../private-owned-runtime'):
        alias = self.canonical/'fixture'/relative
        alias.parent.mkdir(parents=True, exist_ok=True)
        alias.symlink_to(target, target_is_directory=True)
        self.entry['excluded_source']['aliases'] = [{
            'path': relative, 'target_sha256': digest(target.encode('utf-8')),
            'disposition': 'external', 'reason': 'Recipient-owned runtime reference',
            'capability_effect': 'Runtime requires an authorized local collection',
        }]
        return alias

    def test_declared_excluded_alias_skips_destination_and_regular_count(self):
        target = Path(self.temp.name)/'private-owned-runtime'
        self.write(target/'private-sentinel.txt', b'Must not be scanned')
        self.declare_alias(target=str(target))
        self.assertEqual(self.check(canonical=True), [])
        # Its declared target text can be locked without requiring availability.
        shutil.rmtree(target)
        self.assertEqual(self.check(canonical=True), [])

    def test_declared_excluded_alias_target_drift_is_private(self):
        alias = self.declare_alias()
        alias.unlink()
        target = '../../changed-private-target'
        alias.symlink_to(target, target_is_directory=True)
        errors = self.assertError('excluded alias target hash changed', canonical=True)
        self.assertFalse(any(target in error or str(self.canonical) in error for error in errors))

    def test_declared_excluded_alias_cannot_hide_included_file(self):
        shutil.rmtree(self.canonical/'fixture/skills')
        self.declare_alias(relative='skills')
        self.assertError('excluded alias overlaps an included file', canonical=True)
        self.entry['excluded_source']['aliases'][0]['path'] = 'skills/demo/SKILL.md'
        self.assertError('excluded alias overlaps an included file', canonical=True)

    def test_declared_excluded_alias_missing_is_rejected(self):
        alias = self.declare_alias()
        alias.unlink()
        self.assertError('missing or unsafe excluded alias', canonical=True)

    def test_declared_alias_cannot_authorize_public_link(self):
        self.declare_alias()
        link = self.package/'runtime/private-runtime'
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to('../../private-owned-runtime', target_is_directory=True)
        self.assertError('symlink is not distributable')

    def test_excluded_alias_schema_and_explanation_are_required(self):
        self.declare_alias()
        row = self.entry['excluded_source']['aliases'][0]
        for field, value in [('path', '../private'), ('target_sha256', 'bad'),
                             ('disposition', 'included'), ('disposition', {}),
                             ('reason', ''), ('capability_effect', '')]:
            with self.subTest(field=field, value=value):
                old = row[field]
                row[field] = value
                self.assertTrue(self.check())
                row[field] = old
        self.entry['excluded_source']['aliases'] = None
        self.assertError('aliases must be a list')

    def test_json_duplicate_paths_are_rejected(self):
        self.save()
        path = self.root/'catalog/source-inventory.json'
        path.write_text('{"schema_version":1,"packages":[],"packages":[]}')
        errors = inventory.validate_inventory(self.root, self.catalog)
        self.assertTrue(any('missing or invalid JSON' in error for error in errors))

    def test_invalid_shapes_do_not_crash(self):
        for field, value in [('files', []), ('components', None), ('canonical_source', None), ('excluded_source', None)]:
            previous = self.entry[field]
            self.entry[field] = value
            self.assertTrue(self.check())
            self.entry[field] = previous
        self.entry['excluded_source']['files'] = True
        self.assertError('nonnegative integer')
        self.entry['excluded_source']['dispositions'][0]['disposition'] = []
        self.assertError('invalid disposition')

    def test_blocked_capability_is_explicit_in_cli_summary(self):
        self.baseline['entries'].append({'id': 'unresolved-route', 'canonical_owner': 'outside-owner',
                                        'disposition': 'blocked', 'capability_effect': 'Still unavailable pending rights review',
                                        'expected_components': [], 'evidence': ['Synthetic unresolved receipt']})
        self.save()
        result = subprocess.run([sys.executable, str(MODULE), '--root', str(self.root)], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0)
        summary = json.loads(result.stdout)
        self.assertEqual(summary['coverage_dispositions']['blocked'], 1)
        self.assertIn('remain unresolved', summary['coverage_note'])

    def test_cli_fails_and_never_rewrites_inventory(self):
        self.save()
        before = (self.root/'catalog/source-inventory.json').read_bytes()
        self.write(self.package/'new.md', b'unreviewed')
        result = subprocess.run([sys.executable, str(MODULE), '--root', str(self.root)], text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)['status'], 'failed')
        self.assertEqual(before, (self.root/'catalog/source-inventory.json').read_bytes())


if __name__ == '__main__':
    unittest.main()
