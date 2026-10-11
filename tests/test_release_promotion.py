import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
spec=importlib.util.spec_from_file_location('release_site_bridge',ROOT/'scripts/release_site_bridge.py')
bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)

class PromotionTests(unittest.TestCase):
    def test_public_readback_identifies_verifier_and_hashes_exact_bytes(self):
        import hashlib
        import io
        from unittest.mock import patch
        body = b'{"schema_version": 1, "products": []}\n'
        with patch.object(bridge.urllib.request, 'urlopen', return_value=io.BytesIO(body)) as read:
            self.assertEqual(bridge.live_digest('https://example.test/'), hashlib.sha256(body).hexdigest())
        request = read.call_args.args[0]
        self.assertEqual(request.full_url, 'https://example.test/data/release-history.json')
        self.assertEqual(request.get_header('User-agent'), 'WorkingTools-ReleaseVerifier/1.0')
        self.assertEqual(request.get_header('Accept'), 'application/json')
    def expected(self):return [{'product_id':'a','version':'1.2.0','sha256':'b'*64,'source_commit':'a'*40}]
    def release(self,version='1.2.0',**kw):return dict(tag_name='a/v'+version,draft=False,prerelease=False,assets=[dict(name='a-'+version+'.zip',state='uploaded',digest='sha256:'+'b'*64)],**kw)
    def test_current_and_backport(self):
        self.assertTrue(bridge.verify_promotion(self.expected(),[[self.release('1.1.5'),self.release()]],lambda _: 'a'*40))
    def test_newer_racing_release_blocks(self):
        with self.assertRaisesRegex(ValueError,'stale'):
            bridge.verify_promotion(self.expected(),[[self.release(),self.release('1.3.0')]],lambda _: 'a'*40)
    def test_changed_tag_blocks(self):
        with self.assertRaisesRegex(ValueError,'tag changed'):
            bridge.verify_promotion(self.expected(),[[self.release()]],lambda _: 'c'*40)
    def test_digest_mismatch_blocks(self):
        r=self.release();r['assets'][0]['digest']='sha256:'+'c'*64
        with self.assertRaisesRegex(ValueError,'stale'):
            bridge.verify_promotion(self.expected(),[[r]],lambda _: 'a'*40)
    def test_draft_prerelease_not_promoted(self):
        r=self.release('2.0.0');r['draft']=True
        p=self.release('2.0.0-beta.1');p['prerelease']=True
        self.assertTrue(bridge.verify_promotion(self.expected(),[[r,p,self.release()]],lambda _: 'a'*40))


class SiteSourceTests(unittest.TestCase):
    source='a'*40
    other='b'*40

    def proof(self):
        return {'maintained_source_commit':self.source,'live_url':'https://example.test'}

    def git(self,head=None,remote=None,dirty=b''):
        head=head or self.source;remote=remote or self.source
        def output(args,**_kwargs):
            if args[1]=='rev-parse':return head+'\n'
            if args[1]=='ls-remote':return remote+'\trefs/heads/main\n'
            if args[1]=='status':return dirty
            raise AssertionError(args)
        return output

    def test_live_build_manifest_uses_verifier_identity_and_exact_revision(self):
        body=json.dumps({'source_revisions':{'compass-suite':self.source}}).encode()
        with patch.object(bridge.urllib.request,'urlopen',return_value=io.BytesIO(body)) as read:
            self.assertEqual(bridge.live_source_revision('https://example.test/'),self.source)
        request=read.call_args.args[0]
        self.assertEqual(request.full_url,'https://example.test/build-manifest.json')
        self.assertEqual(request.get_header('User-agent'),'WorkingTools-ReleaseVerifier/1.0')
        self.assertEqual(request.get_header('Accept'),'application/json')
        with patch.object(bridge.urllib.request,'urlopen',return_value=io.BytesIO(b'{"source_revisions":{}}')):
            with self.assertRaisesRegex(ValueError,'exact compass-suite'):
                bridge.live_source_revision('https://example.test')

    def test_current_clean_checkout_remote_and_live_build_match(self):
        with (patch.object(bridge.subprocess,'check_output',side_effect=self.git()),
              patch.object(bridge,'live_source_revision',return_value=self.source)):
            self.assertTrue(bridge.site_source_matches(Path('/site'),self.proof()))

    def test_stale_ui_checkout_and_remote_ahead_do_not_reuse(self):
        for state in ({'head':self.other,'remote':self.other},
                      {'head':self.source,'remote':self.other},
                      {'dirty':b' M data/release-history.json'}):
            with self.subTest(state=state):
                with (patch.object(bridge.subprocess,'check_output',side_effect=self.git(**state)),
                      patch.object(bridge,'live_source_revision') as live):
                    self.assertFalse(bridge.site_source_matches(Path('/site'),self.proof()))
                    live.assert_not_called()

    def test_live_wrong_source_does_not_reuse(self):
        with (patch.object(bridge.subprocess,'check_output',side_effect=self.git()),
              patch.object(bridge,'live_source_revision',return_value=self.other)):
            self.assertFalse(bridge.site_source_matches(Path('/site'),self.proof()))

    def test_post_cli_rejects_stale_live_source_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'catalog').mkdir();(root/'dist/release-manager').mkdir(parents=True)
            history=root/'catalog/release-history.json';history.write_text('{"products":[]}')
            expected=root/'expected.json';expected.write_text('[]')
            receipt=root/'receipt.json'
            config=root/'config.json';config.write_text(json.dumps({
                'site_source':str(root/'site'),'site_receipt':str(receipt),'codex_command':'codex'}))
            digest=bridge.hashlib.sha256(history.read_bytes()).hexdigest()
            def cli(*_args,**_kwargs):
                receipt.write_text(json.dumps({'status':'deployed','deployment_id':'dep-1',
                    'catalog_sha256':digest,'published_set':[],
                    'maintained_source_commit':self.source,'live_url':'https://example.test'}))
                return type('Result',(),{'returncode':0})()
            with (patch.object(bridge,'ROOT',root),
                  patch.object(bridge,'verify_promotion'),
                  patch.object(bridge.subprocess,'run',side_effect=cli),
                  patch.object(bridge.subprocess,'check_output',side_effect=self.git()),
                  patch.object(bridge,'live_digest',return_value=digest),
                  patch.object(bridge,'live_source_revision',return_value=self.other),
                  patch.dict(bridge.os.environ,{'WORKING_TOOLS_RELEASE_CONFIG':str(config),
                                               'WORKING_TOOLS_EXPECTED_RELEASES':str(expected)}),
                  patch.object(sys,'argv',['release_site_bridge.py'])):
                with self.assertRaisesRegex(SystemExit,'Live Site build'):
                    bridge.main()

    def test_same_catalog_with_newer_ui_source_runs_deployment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'catalog').mkdir();(root/'dist/release-manager').mkdir(parents=True)
            history=root/'catalog/release-history.json';history.write_text('{"products":[]}')
            expected=root/'expected.json';expected.write_text('[]')
            receipt=root/'receipt.json'
            config=root/'config.json';config.write_text(json.dumps({
                'site_source':str(root/'site'),'site_receipt':str(receipt),'codex_command':'codex'}))
            digest=bridge.hashlib.sha256(history.read_bytes()).hexdigest()
            prior={'status':'deployed','deployment_id':'old','catalog_sha256':digest,
                   'published_set':[],'maintained_source_commit':self.source,
                   'live_url':'https://example.test'}
            receipt.write_text(json.dumps(prior))
            def cli(*_args,**_kwargs):
                receipt.write_text(json.dumps({**prior,'deployment_id':'new',
                    'maintained_source_commit':self.other}))
                return type('Result',(),{'returncode':0})()
            with (patch.object(bridge,'ROOT',root),
                  patch.object(bridge,'verify_promotion'),
                  patch.object(bridge.subprocess,'run',side_effect=cli) as adapter,
                  patch.object(bridge.subprocess,'check_output',side_effect=self.git(
                      head=self.other,remote=self.other)),
                  patch.object(bridge,'live_digest',return_value=digest),
                  patch.object(bridge,'live_source_revision',return_value=self.other),
                  patch.dict(bridge.os.environ,{'WORKING_TOOLS_RELEASE_CONFIG':str(config),
                                               'WORKING_TOOLS_EXPECTED_RELEASES':str(expected)}),
                  patch.object(sys,'argv',['release_site_bridge.py'])):
                bridge.main()
            adapter.assert_called_once()
            self.assertEqual(json.loads(receipt.read_text())['deployment_id'],'new')
if __name__=='__main__':unittest.main()

class ReviewedPathTests(unittest.TestCase):
    def test_symlink_ancestor_rejected(self):
        import tempfile
        from release_manager.local_sync import safe_file
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'target').mkdir();(root/'link').symlink_to(root/'target',target_is_directory=True)
            with self.assertRaisesRegex(ValueError,'Symlink'):
                safe_file(root,'link/SKILL.md')
    def test_traversal_rejected(self):
        from release_manager.local_sync import safe_file
        with self.assertRaisesRegex(ValueError,'Unsafe'):
            safe_file(ROOT,'../private.txt')
