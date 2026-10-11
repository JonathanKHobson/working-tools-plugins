"""Publication state, optimistic source checks and safe failure boundaries."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import complete_update
from release_manager import local_sync
import test_release_manager_integration as fixtures


class ToolingGuardTests(unittest.TestCase):
    def test_preparation_marks_prepared_and_preserves_concurrent_source_before_refresh(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);canonical=fixtures.CompletionContractTests().fixture(root)
            (canonical/'x/references/shared.md').write_text('planned change\n')
            original=local_sync.apply_content
            def concurrent(*args,**kwargs):
                original(*args,**kwargs)
                (canonical/'x/README.md').write_text('concurrent user edit\n')
            before=(root/'plugins/x/plugin.json').read_bytes()
            with patch.object(complete_update,'ROOT',root),patch.object(local_sync,'apply_content',side_effect=concurrent):
                with self.assertRaisesRegex(ValueError,'Canonical source changed'):
                    complete_update.prepare({'canonical_root':str(canonical)})
            self.assertEqual((canonical/'x/README.md').read_text(),'concurrent user edit\n')
            self.assertEqual((root/'plugins/x/plugin.json').read_bytes(),before)
            with patch.object(complete_update,'ROOT',root),patch.object(complete_update,'command'):
                complete_update.prepare({'canonical_root':str(canonical)})
            self.assertEqual(local_sync.read(root/'catalog/packages.json')['packages'][0]['distribution'],'prepared')

    def test_source_edit_during_metadata_refresh_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);canonical=fixtures.CompletionContractTests().fixture(root)
            original=local_sync.refresh_metadata
            def concurrent(*args,**kwargs):
                original(*args,**kwargs)
                (canonical/'x/README.md').write_text('new source edit\n')
            with patch.object(local_sync,'refresh_metadata',side_effect=concurrent):
                with self.assertRaisesRegex(ValueError,'Canonical source changed'):
                    local_sync.refresh_reviewed(root,canonical,'x','1.0.1','Specific notes')
            self.assertEqual((canonical/'x/README.md').read_text(),'new source edit\n')

    def test_push_rejects_wrong_branch_and_remote_divergence(self):
        with patch.object(complete_update,'run',return_value=b'feature\n'),patch.object(complete_update,'command') as command:
            with self.assertRaisesRegex(ValueError,'main branch'):complete_update.push_main()
            command.assert_not_called()
        error=subprocess.CalledProcessError(1,['git','merge-base'])
        with patch.object(complete_update,'run',side_effect=[b'main\n',error]),patch.object(complete_update,'command') as command:
            with self.assertRaisesRegex(ValueError,'contain current origin/main'):complete_update.push_main()
            self.assertEqual([call.args for call in command.call_args_list],[('git','fetch','origin','main')])
        with patch.object(complete_update,'run',side_effect=[b'main\n',b'']),patch.object(complete_update,'command') as command:
            complete_update.push_main()
            self.assertEqual([call.args for call in command.call_args_list],[('git','fetch','origin','main'),('git','push','origin','HEAD:main')])

    def test_staging_keeps_tracked_deletion_and_omits_absent_optional_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'new.json').write_text('{}')
            with patch.object(complete_update,'ROOT',root),patch.object(complete_update,'run',return_value=b'deleted.md\0'):
                self.assertEqual(complete_update.stageable_paths(['new.json','deleted.md','PROVENANCE.json']),['new.json','deleted.md'])

    def test_missing_site_receipt_fails_before_release_operation(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config=root/'config.json'
            local_sync.write(config,{'site_adapter':['fake']})
            with patch.object(complete_update,'ROOT',root),patch.object(complete_update,'prepare') as prepare,patch.object(sys,'argv',[
                    'complete_update.py','--config',str(config),'--publish']):
                with self.assertRaisesRegex(ValueError,'site_receipt'):complete_update.main()
            prepare.assert_not_called();self.assertFalse((root/'dist').exists())

    def test_missing_package_in_exact_build_has_explicit_error(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);fixtures.CompletionContractTests().fixture(root)
            folder=root/'catalog/releases/x';folder.mkdir(parents=True)
            local_sync.write(folder/'1.0.0.json',{'notes':'Actual package update'})
            with patch.object(complete_update,'ROOT',root),patch.object(complete_update,'run',return_value=b'a'*40),patch.object(complete_update,'exact_commit_build',return_value={'packages':[]}),patch.object(complete_update,'publish') as publish:
                with self.assertRaisesRegex(ValueError,'build lacks package: x'):
                    complete_update.publish_pending({}, {'changed':[{'id':'x','version':'1.0.0'}]})
            publish.assert_not_called()


if __name__=='__main__':unittest.main()
