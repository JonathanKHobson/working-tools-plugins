"""A later invalid product must not mutate an earlier valid release candidate."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import complete_update
from release_manager import local_sync
import test_release_manager_integration as integration_fixtures


class PreparePreflightTests(unittest.TestCase):
    def test_later_missing_reviewed_changelog_preserves_entire_batch(self):
        for present in (False,True):
            with self.subTest(unreviewed_file_present=present),tempfile.TemporaryDirectory() as directory:
                root=Path(directory);canonical=integration_fixtures.CompletionContractTests().fixture(root,('x','y'))
                for ident in ('x','y'):(canonical/ident/'README.md').write_text('Changed '+ident+'\n')
                inventory=local_sync.read(root/'catalog/source-inventory.json')
                del inventory['packages'][1]['files']['CHANGELOG.md']
                local_sync.write(root/'catalog/source-inventory.json',inventory)
                if not present:
                    for base in (root/'plugins/y',canonical/'y'):(base/'CHANGELOG.md').unlink()
                before={p:p.read_bytes() for p in root.rglob('*') if p.is_file()}
                with patch.object(complete_update,'ROOT',root),patch.object(complete_update,'command') as command:
                    with self.assertRaisesRegex(ValueError,'y: CHANGELOG.md must be admitted'):
                        complete_update.prepare({'canonical_root':str(canonical)})
                command.assert_not_called()
                self.assertEqual({p:p.read_bytes() for p in root.rglob('*') if p.is_file()},before)

    def test_later_missing_semantic_note_preserves_entire_batch(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);canonical=integration_fixtures.CompletionContractTests().fixture(root,('x','y'))
            for ident in ('x','y'):(canonical/ident/'README.md').write_text('Changed '+ident+'\n')
            (root/'catalog/changes/y.json').unlink()
            before={p:p.read_bytes() for p in root.rglob('*') if p.is_file()}
            with patch.object(complete_update,'ROOT',root),patch.object(complete_update,'command') as command:
                with self.assertRaisesRegex(ValueError,'y: authoring agent must supply'):
                    complete_update.prepare({'canonical_root':str(canonical)})
            command.assert_not_called()
            self.assertEqual({p:p.read_bytes() for p in root.rglob('*') if p.is_file()},before)


if __name__=='__main__':unittest.main()
