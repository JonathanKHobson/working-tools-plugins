"""Offline queue checks, including unchanged evidence and explicit release boundaries."""
import contextlib
import io
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import complete_update
from release_manager import pending,local_sync
import test_release_manager_integration as fixtures_module


class PendingTests(unittest.TestCase):
    def fixture(self,root,names=('x',)):
        self.fixtures=fixtures_module.CompletionContractTests()
        canonical=self.fixtures.fixture(root,names)
        return {'canonical_root':str(canonical),'site_adapter':['fake-adapter'],
                'site_receipt':str(root/'site-receipt.json')},canonical

    def test_default_command_is_local_only_and_keeps_source_notes_versions_and_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config,canonical=self.fixture(root)
            (canonical/'x/README.md').write_text('private current source bytes\n')
            (root/'catalog/changes/x.json').unlink()
            config_file=root/'config.json';local_sync.write(config_file,config)
            receipt=root/'dist/release-manager/receipt.json';receipt.parent.mkdir(parents=True)
            receipt.write_text('{"status":"catalog_pending","private_recovery":"retained"}')
            kept={p:p.read_bytes() for p in root.rglob('*') if p.is_file() and p!=config_file}
            with (patch.object(complete_update,'ROOT',root),
                  patch.object(complete_update,'command',side_effect=AssertionError('no build or publish')),
                  patch.object(complete_update,'prepare',side_effect=AssertionError('no prepare')),
                  patch.object(complete_update,'sync_site',side_effect=AssertionError('no deployment')),
                  patch.object(pending.subprocess,'check_output',side_effect=AssertionError('no git needed')),
                  patch.object(sys,'argv',['complete_update.py','--config',str(config_file),'--json']),
                  contextlib.redirect_stdout(io.StringIO()) as output):
                complete_update.main()
            journal=json.loads(output.getvalue())
            self.assertEqual(journal['entries'][0]['state'],'pending-review')
            self.assertFalse(journal['entries'][0]['notes_ready'])
            recovery=next(b for b in journal['boundaries'] if b['kind']=='publication-recovery')
            self.assertEqual(recovery['state'],'incomplete')
            self.assertEqual(recovery['receipt_status'],'catalog_pending')
            self.assertEqual(journal['entries'][0]['recorded_version'],'1.0.0')
            self.assertNotIn('private current source bytes',output.getvalue())
            for path,original in kept.items():self.assertEqual(path.read_bytes(),original)
            mode=stat.S_IMODE((root/'dist/release-manager/pending.json').stat().st_mode)
            self.assertEqual(mode,0o600)

    def test_status_refresh_is_stable_and_first_seen_survives_further_work(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config,canonical=self.fixture(root)
            (canonical/'x/README.md').write_text('First correction.\n')
            first=pending.refresh(root,config)
            path=root/'dist/release-manager/pending.json';original=path.read_bytes()
            second=pending.refresh(root,config)
            self.assertEqual(first,second);self.assertEqual(path.read_bytes(),original)
            (canonical/'x/README.md').write_text('Next correction.\n')
            third=pending.refresh(root,config)
            self.assertEqual(first['entries'][0]['first_seen'],third['entries'][0]['first_seen'])
            self.assertNotEqual(first['fingerprint'],third['fingerprint'])
            config_file=root/'config.json';local_sync.write(config_file,config)
            with patch.object(complete_update,'ROOT',root),patch.object(sys,'argv',[
                    'complete_update.py','--config',str(config_file),'--status']),contextlib.redirect_stdout(io.StringIO()) as output:
                complete_update.main()
            self.assertIn('Local pending queue: 1 product(s)',output.getvalue())

    def test_scoped_refresh_preserves_other_pending_products_exactly(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config,canonical=self.fixture(root,('x','y'))
            for ident in ('x','y'):(canonical/ident/'README.md').write_text('Pending '+ident+'\n')
            first=pending.refresh(root,config)
            other=next(e for e in first['entries'] if e['id']=='y')
            (canonical/'x/README.md').write_text('original readme\n')
            second=pending.refresh(root,config,['x'])
            self.assertEqual(second['entries'],[other])
            self.assertEqual(second['boundaries'],first['boundaries'])

    def test_reviewed_added_file_and_unreviewed_file_are_observed_without_import(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config,canonical=self.fixture(root)
            rel=self.fixtures.add_reviewed_support(root,canonical)
            unknown=canonical/'x/references/unreviewed.md';unknown.write_text('Secret contents.\n')
            journal=pending.refresh(root,config,['x'])
            entry=journal['entries'][0]
            self.assertEqual(entry['reviewed_additions'],[rel])
            self.assertEqual(entry['changes'][0]['source'],'reviewed-addition')
            self.assertIn('canonical: unreviewed path references/unreviewed.md',entry['review_signals'])
            self.assertFalse((root/'plugins/x/references/unreviewed.md').exists())
            self.assertTrue((root/'catalog/changes/x.json').exists())
            self.assertNotIn('Secret contents',json.dumps(journal))

    def test_reviewed_public_projections_do_not_requeue_completed_release_but_public_drift_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config,canonical=self.fixture(root)
            document=local_sync.read(root/'catalog/source-inventory.json');row=document['packages'][0]
            row['canonical_files']={p:h for p,h in row['files'].items() if p!='plugin.json'}
            (canonical/'x/plugin.json').unlink()
            row['public_projection_overrides']=['PROVENANCE.json']
            (canonical/'x/PROVENANCE.json').write_text('{"private":"canonical audit"}')
            local_sync.write(root/'catalog/source-inventory.json',document)
            self.assertIsNone(pending.plugin_observation(root,config,row,'1.0.0'))
            (root/'plugins/x/plugin.json').write_text('{"version":"unreviewed"}')
            observed=pending.plugin_observation(root,config,row,'1.0.0')
            self.assertEqual([r['path'] for r in observed['changes']],['plugin.json'])

    def test_divergent_changes_are_pending_conflicts_not_queue_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config,canonical=self.fixture(root)
            (canonical/'x/README.md').write_text('canonical change\n')
            (root/'plugins/x/README.md').write_text('public change\n')
            entry=pending.refresh(root,config)['entries'][0]
            self.assertEqual(entry['state'],'pending-review')
            self.assertIn('divergent',entry['conflicts'][0])
            self.assertNotEqual(entry['changes'][0]['canonical_sha256'],entry['changes'][0]['public_sha256'])

    def test_corrupt_journal_fails_without_destruction(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config,canonical=self.fixture(root)
            path=root/'dist/release-manager/pending.json';path.parent.mkdir(parents=True)
            path.write_bytes(b'{broken previous journal')
            with self.assertRaisesRegex(ValueError,'corrupt'):pending.refresh(root,config)
            self.assertEqual(path.read_bytes(),b'{broken previous journal')

    def test_full_queue_includes_integration_external_and_site_local_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config,canonical=self.fixture(root)
            integration=root/'integrations/hooks';integration.mkdir(parents=True)
            (integration/'method.py').write_text('changed\n')
            local_sync.write(root/'catalog/integrations.json',{'products':[{'id':'hooks','version':'0.1.0',
                'source_root':'integrations/hooks','source_files':{'integrations/hooks/method.py':'a'*64}}]})
            checkout=root/'guide';checkout.mkdir()
            subprocess.check_call(['git','init','-q'],cwd=checkout)
            (checkout/'guide.md').write_text('prior guide\n')
            subprocess.check_call(['git','add','guide.md'],cwd=checkout)
            subprocess.check_call(['git','-c','user.name=Fixture','-c','user.email=fixture@example.test',
                'commit','-qm','Fixture baseline'],cwd=checkout)
            base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=checkout).decode().strip()
            (checkout/'guide.md').write_text('new guide\n')
            config.update({'external_checkouts':{'guide':str(checkout)},'site_source':str(checkout)})
            local_sync.write(root/'catalog/external-products.json',{'sources':{'guide':{'commit':base}},
                'products':[{'id':'guide','lifecycle':'active-guide-page','version':{'value':None},
                    'source':{'id':'guide','files':['guide.md']}}]})
            journal=pending.refresh(root,config)
            self.assertEqual({e['kind'] for e in journal['entries']},{'integration','external','site'})
            self.assertEqual({b['state'] for b in journal['boundaries'] if b['kind']!='publication-recovery'},{'pending'})
            self.assertIn('committed unpublished changes not checked',pending.summary(journal))

    def test_shared_input_queues_each_reviewed_destination_without_copying(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config,canonical=self.fixture(root,('x','y'))
            source=root/'shared/method.md';source.parent.mkdir();source.write_text('Updated shared method.\n')
            config['shared_shipped_paths']={'shared/method.md':[
                'plugins/x/references/shared.md','plugins/y/references/shared.md']}
            journal=pending.refresh(root,config)
            self.assertEqual({entry['id'] for entry in journal['entries']},{'x','y'})
            for entry in journal['entries']:
                self.assertEqual(entry['changes'][0]['source'],'shared')
                self.assertEqual(entry['changes'][0]['shared_sha256'],local_sync.digest(source.read_bytes()))
                self.assertEqual((root/'plugins'/entry['id']/'references/shared.md').read_text(),'original instruction\n')
                self.assertEqual((canonical/entry['id']/'references/shared.md').read_text(),'original instruction\n')

    def test_committed_site_changes_compare_saved_deployment_baseline_without_network(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config,canonical=self.fixture(root)
            site=root/'site';site.mkdir()
            subprocess.check_call(['git','init','-q'],cwd=site)
            (site/'logo.svg').write_text('prior logo\n')
            subprocess.check_call(['git','add','logo.svg'],cwd=site)
            commit=['git','-c','user.name=Fixture','-c','user.email=fixture@example.test','commit','-qm']
            subprocess.check_call(commit+['Deployment baseline'],cwd=site)
            base=subprocess.check_output(['git','rev-parse','HEAD'],cwd=site).decode().strip()
            (site/'logo.svg').write_text('committed new logo\n')
            subprocess.check_call(['git','add','logo.svg'],cwd=site)
            subprocess.check_call(commit+['Unpublished local logo'],cwd=site)
            proof=root/'site-receipt.json';local_sync.write(proof,{'maintained_source_commit':base})
            config.update({'site_source':str(site),'site_receipt':str(proof)})
            actual=subprocess.check_output
            with patch.object(pending.subprocess,'check_output',wraps=actual) as git:
                journal=pending.refresh(root,config)
            self.assertEqual(journal['entries'][0]['changes'][0]['path'],'logo.svg')
            self.assertEqual(journal['boundaries'][0]['deployment_baseline'],base)
            for call in git.call_args_list:self.assertEqual(call.kwargs['env']['GIT_NO_LAZY_FETCH'],'1')
            proof.write_text('unreadable receipt')
            journal=pending.refresh(root,config)
            self.assertEqual(journal['boundaries'][0]['state'],'unknown-deployment-baseline')

    def test_failed_publish_preserves_queue_and_recovery_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config,canonical=self.fixture(root)
            (canonical/'x/README.md').write_text('Pending correction.\n')
            pending.refresh(root,config)
            path=root/'dist/release-manager/pending.json';original=path.read_bytes()
            receipt=root/'dist/release-manager/receipt.json'
            local_sync.write(receipt,{'status':'preparing','changed':[],'published':[]})
            original_receipt=receipt.read_bytes()
            config_file=root/'config.json';local_sync.write(config_file,config)
            with patch.object(complete_update,'ROOT',root),patch.object(complete_update,'external_plan',side_effect=ValueError('publisher unavailable')),patch.object(sys,'argv',[
                    'complete_update.py','--config',str(config_file),'--publish']):
                with self.assertRaisesRegex(ValueError,'publisher unavailable'):complete_update.main()
            self.assertEqual(path.read_bytes(),original)
            self.assertEqual(receipt.read_bytes(),original_receipt)

    def test_successful_publication_reconciles_queue_only_after_completed_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);config,canonical=self.fixture(root)
            (canonical/'x/README.md').write_text('Pending correction.\n')
            pending.refresh(root,config,['x'])
            path=root/'dist/release-manager/pending.json';original=path.read_bytes()
            (canonical/'x/README.md').write_text('original readme\n')
            config_file=root/'config.json';local_sync.write(config_file,config)
            def complete_site(_,receipt):
                self.assertEqual(path.read_bytes(),original)
                receipt['status']='complete'
            with (patch.object(complete_update,'ROOT',root),
                  patch.object(complete_update,'pending_entries',return_value=[]),
                  patch.object(complete_update,'unfinished_committed_entries',return_value=[]),
                  patch.object(complete_update,'prepare',return_value=[]),
                  patch.object(complete_update,'sync_site',side_effect=complete_site),
                  patch.object(complete_update,'command',side_effect=AssertionError('no source work')),
                  patch.object(sys,'argv',['complete_update.py','--config',str(config_file),'--publish','--package','x']),
                  contextlib.redirect_stdout(io.StringIO())):
                complete_update.main()
            self.assertEqual(pending.read_previous(path)['entries'],[])
            self.assertEqual(local_sync.read(root/'dist/release-manager/receipt.json')['status'],'complete')

    def test_operation_flags_are_mutually_exclusive(self):
        for flags in (['--status','--publish'],['--publish','--prepare-only'],['--reconcile-only']):
            with self.subTest(flags=flags),patch.object(sys,'argv',['complete_update.py',*flags]),contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):complete_update.main()
