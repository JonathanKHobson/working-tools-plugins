"""Legal packaging regressions; no test asserts legal clearance."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('license_checks', Path(__file__).resolve().parents[1] / 'scripts/license_checks.py')
legal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legal)


class LegalPackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.record = {'id':'sample','version':'1.0.0','license':'MIT'}
        for name in ['LICENSE','LICENSING.md','THIRD_PARTY_NOTICES.md','skills/demo/SKILL.md']:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Synthetic fixture.\n')
        self.write('plugin.json', {'license':'MIT'})
        self.refresh()

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))

    def refresh(self):
        self.write('LICENSE-SCOPE.json', {'package':'sample','version':'1.0.0','files':[
            {'path':path.relative_to(self.root).as_posix(),'category':'fixture','license':'MIT',
             'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
            for path in legal.package_files(self.root) if path.name != 'LICENSE-SCOPE.json'
        ]})

    def errors(self):
        return legal.legal_errors(self.root, self.record)

    def test_exact_scope_and_consistent_manifest_pass(self):
        self.assertEqual(self.errors(), [])

    def test_new_or_changed_file_blocks_release(self):
        (self.root / 'new.py').write_text('print(1)\n')
        self.assertTrue(any('no exact license scope: new.py' in e for e in self.errors()))
        (self.root / 'LICENSE').write_text('Changed grant\n')
        self.assertTrue(any('stale scope digest: LICENSE' in e for e in self.errors()))

    def test_manifest_license_mismatch_and_missing_document_block(self):
        self.write('plugin.json', {'license':'Apache-2.0'})
        (self.root / 'LICENSING.md').unlink()
        errors = self.errors()
        self.assertTrue(any('license differs from registry' in e for e in errors))
        self.assertTrue(any('missing, empty or linked LICENSING.md' in e for e in errors))

    def test_duplicate_path_and_wide_exclusion_do_not_hide_content(self):
        scope = json.loads((self.root / 'LICENSE-SCOPE.json').read_text())
        scope['files'].append(scope['files'][0])
        scope['inventory_excludes'] = ['skills/']
        self.write('LICENSE-SCOPE.json', scope)
        errors = self.errors()
        self.assertTrue(any('duplicate scope path' in e for e in errors))
        self.assertTrue(any('unsupported scope exclusions' in e for e in errors))

    def review_record(self, status='held'):
        record = dict(self.record)
        record['licensing'] = {'releaseReview': {
            'status': status, 'issue': 'synthetic-rights-question',
            'reason': 'Synthetic source permission unresolved.',
            'files': {'LICENSE': hashlib.sha256((self.root / 'LICENSE').read_bytes()).hexdigest()},
            'resolution': {'reviewer':'Fixture reviewer','date':'2026-10-24',
                           'basis':'Supplied synthetic source grant checked.',
                           'evidence':'Synthetic fixture, no external rights claim.'}
        }}
        return record

    def test_malformed_licensing_metadata_returns_actionable_error(self):
        for value in ('held', [], None, 3):
            with self.subTest(value=value):
                record = dict(self.record, licensing=value)
                self.assertEqual(legal.source_rights_release_errors(self.root, record),
                                 ['sample: source-rights release review: invalid licensing record; expected object'])

    def test_unresolved_rights_hold_blocks_even_when_packaging_passes(self):
        self.assertEqual(self.errors(), [])
        errors = legal.source_rights_release_errors(self.root, self.review_record())
        self.assertTrue(any('held:' in error for error in errors))

    def test_resolved_review_accepts_only_exact_reviewed_bytes(self):
        record = self.review_record('resolved')
        self.assertEqual(legal.source_rights_release_errors(self.root, record), [])
        (self.root / 'LICENSE').write_text('Changed source bytes\n')
        self.assertTrue(any('fresh source-rights review required' in error
                            for error in legal.source_rights_release_errors(self.root, record)))

    def test_resolution_cannot_clear_without_evidence_or_bindings(self):
        record = self.review_record('resolved')
        record['licensing']['releaseReview']['resolution'] = None
        self.assertTrue(any('resolution lacks' in error
                            for error in legal.source_rights_release_errors(self.root, record)))
        record['licensing']['releaseReview']['files'] = {}
        self.assertTrue(any('missing exact reviewed file bindings' in error
                            for error in legal.source_rights_release_errors(self.root, record)))

    def test_link_and_escaping_scope_are_rejected(self):
        (self.root / 'linked').symlink_to('/etc/hosts')
        self.refresh()
        self.assertTrue(any('absent or linked: linked' in e for e in self.errors()))
        scope = json.loads((self.root / 'LICENSE-SCOPE.json').read_text())
        scope['files'][0]['path'] = '../outside'
        self.write('LICENSE-SCOPE.json', scope)
        self.assertTrue(any('unsafe scope path' in e for e in self.errors()))


if __name__ == '__main__':
    unittest.main()
