"""Offline coverage for the redesigned Site contract; never publishes a release."""
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
spec=importlib.util.spec_from_file_location('static_bridge',ROOT/'scripts/release_site_bridge.py')
bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)


class StaticSiteTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.workspace=Path(self.temp.name).resolve()
        self.site=self.workspace/'work/sites/working-tools';self.site.mkdir(parents=True)
        for path,text in {
            '.openai/hosting.json':json.dumps({'project_id':'site-current','static':{'directory':'dist'}}),
            'dist/index.html':'<main>Current Fresh Curiosity design</main>',
            'dist/assets/shell.css':'/* accepted header */',
            'dist/data/release-history.json':'{"products":[]}',
            'dist/data/plugin-releases.json':'{"packages":[]}',
            'dist/data/skill-downloads.json':'{"products":[]}',
            'dist/build-manifest.json':json.dumps({'site_origin':'https://example.test',
                'source_revisions':{'compass-suite':'c'*40}}),
        }.items():
            p=self.site/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
        self.git('init','-q');self.git('config','user.name','Fixture');self.git('config','user.email','fixture@example.test')
        self.git('add','.')
        self.projection=bridge.stamp_static_site(self.site)
        self.git('add','.');self.git('commit','-qm','Static fixture')
        self.head=self.git('rev-parse','HEAD').strip()

    def git(self,*args):
        return subprocess.check_output(['git',*args],cwd=self.site,text=True,stderr=subprocess.PIPE)

    def proof(self):
        return {'site_contract':bridge.STATIC_CONTRACT,'project_id':'site-current',
            'no_op':False,
            'source_commit':self.head,'maintained_source_commit':self.head,'remote_source_commit':self.head,
            'sites_version_source_commit':self.head,'version_id':'version-current','deployment_id':'deployment-current',
            'live_url':'https://example.test','static_projection':self.projection,
            'catalog_sha256':self.projection['catalog_sha256'],'skill_catalog_sha256':self.projection['skill_catalog_sha256'],
            'audience_before':'public','audience_after':'public','access_revision_before':2,'access_revision_after':2}

    def live_manifest(self,projection=None):
        return io.BytesIO(json.dumps({'release_projection':projection or self.projection}).encode())

    def test_stamp_preserves_historical_pin_and_all_ui_bytes(self):
        ui=(self.site/'dist/index.html').read_bytes();css=(self.site/'dist/assets/shell.css').read_bytes()
        stamped=bridge.stamp_static_site(self.site)
        self.assertEqual(stamped,self.projection)
        self.assertEqual(json.loads((self.site/'dist/build-manifest.json').read_text())['source_revisions'],{'compass-suite':'c'*40})
        self.assertEqual(ui,(self.site/'dist/index.html').read_bytes());self.assertEqual(css,(self.site/'dist/assets/shell.css').read_bytes())

    def test_newest_source_is_bound_without_legacy_remote_or_pin(self):
        with patch.object(bridge.urllib.request,'urlopen',return_value=self.live_manifest()) as read:
            self.assertTrue(bridge.site_source_matches(self.site,self.proof(),bridge.STATIC_CONTRACT))
        request=read.call_args.args[0]
        self.assertEqual(request.full_url,'https://example.test/build-manifest.json')
        self.assertEqual(request.get_header('User-agent'),'WorkingTools-ReleaseVerifier/1.0')

    def test_changed_committed_ui_and_stale_receipt_are_not_reused(self):
        proof=self.proof();(self.site/'dist/index.html').write_text('newer accepted UI')
        self.git('add','.');self.git('commit','-qm','New UI')
        with patch.object(bridge.urllib.request,'urlopen') as read:
            self.assertFalse(bridge.site_source_matches(self.site,proof,bridge.STATIC_CONTRACT))
            read.assert_not_called()

    def test_wrong_remote_native_source_identity_audience_and_asset_hash_rejected(self):
        cases=[('remote_source_commit','b'*40),('sites_version_source_commit','b'*40),
            ('project_id','old-site'),('audience_after','private'),('access_revision_after',3),
            ('catalog_sha256','f'*64),('skill_catalog_sha256','f'*64),('live_url','https://wrong.test')]
        for key,value in cases:
            with self.subTest(key=key),patch.object(bridge.urllib.request,'urlopen') as read:
                proof=self.proof();proof[key]=value
                self.assertFalse(bridge.site_source_matches(self.site,proof,bridge.STATIC_CONTRACT));read.assert_not_called()

    def test_wrong_live_payload_and_legacy_receipt_rejected(self):
        wrong={**self.projection,'payload_sha256':'f'*64}
        with patch.object(bridge.urllib.request,'urlopen',return_value=self.live_manifest(wrong)):
            self.assertFalse(bridge.site_source_matches(self.site,self.proof(),bridge.STATIC_CONTRACT))
        self.assertFalse(bridge.site_source_matches(self.site,{'maintained_source_commit':self.head},bridge.STATIC_CONTRACT))

    def test_dirty_site_does_not_reuse_proof(self):
        (self.site/'dist/assets/shell.css').write_text('unreviewed')
        with patch.object(bridge.urllib.request,'urlopen') as read:
            self.assertFalse(bridge.site_source_matches(self.site,self.proof(),bridge.STATIC_CONTRACT));read.assert_not_called()

    def test_unstaged_generated_path_and_symlink_are_rejected(self):
        new=self.site/'dist/new.html';new.write_text('new route')
        with self.assertRaisesRegex(ValueError,'unstaged'):bridge.stamp_static_site(self.site)
        new.unlink();new.symlink_to(self.site/'dist/index.html');self.git('add','dist/new.html')
        with self.assertRaisesRegex(ValueError,'Symlink'):bridge.stamp_static_site(self.site)

    def test_legacy_index_or_asset_regression_blocks_before_stamp(self):
        request={'site_contract':bridge.STATIC_CONTRACT,'site_source':str(self.site),
                 'site_guard':bridge.site_guard(self.site)}
        manifest=(self.site/'dist/build-manifest.json').read_bytes()
        for relative in ('dist/index.html','dist/assets/shell.css'):
            with self.subTest(relative=relative):
                path=self.site/relative;before=path.read_bytes();path.write_text('legacy rebuild output')
                with self.assertRaisesRegex(ValueError,'Protected Site file changed'):
                    bridge.stamp_static_site(self.site,request)
                self.assertEqual(manifest,(self.site/'dist/build-manifest.json').read_bytes())
                path.write_bytes(before)
        extra=self.site/'dist/assets/unreviewed.js';extra.write_text('new unowned asset');self.git('add','.')
        with self.assertRaisesRegex(ValueError,'outside the catalog'):
            bridge.stamp_static_site(self.site,request)

    def test_guide_body_can_update_but_header_cannot(self):
        page=self.site/'dist/tools/a/index.html';page.parent.mkdir(parents=True)
        page.write_text('<!-- fc-family:start -->accepted header<!-- fc-family:end -->'
                        '<!-- fc-icons:start -->accepted icons<!-- fc-icons:end --><main>old metadata</main>')
        self.git('add','.')
        request={'site_contract':bridge.STATIC_CONTRACT,'site_source':str(self.site),'site_guard':bridge.site_guard(self.site)}
        page.write_text(page.read_text().replace('old metadata','new metadata'))
        bridge.verify_site_guard(self.site,request)
        page.write_text(page.read_text().replace('accepted header','legacy header'))
        with self.assertRaisesRegex(ValueError,'header/icon changed'):bridge.stamp_static_site(self.site,request)

    def test_catalog_input_race_and_skill_readback(self):
        history=self.site/'dist/data/release-history.json';skills=self.site/'dist/data/skill-downloads.json'
        request={'catalog_file':str(history),'catalog_sha256':bridge.file_digest(history),
                 'skill_catalog_file':str(skills),'skill_catalog_sha256':bridge.file_digest(skills)}
        bridge.verify_request_inputs(request);skills.write_text('changed skill index')
        with self.assertRaisesRegex(ValueError,'skill_catalog_file'):bridge.verify_request_inputs(request)
        with patch.object(bridge.urllib.request,'urlopen',return_value=io.BytesIO(b'index')) as read:
            self.assertEqual(bridge.live_digest('https://example.test','skill-downloads.json'),bridge.hashlib.sha256(b'index').hexdigest())
        self.assertEqual(read.call_args.args[0].full_url,'https://example.test/data/skill-downloads.json')

    def test_context_and_prompt_select_current_pipeline(self):
        (self.workspace/'docs').mkdir();(self.workspace/'docs/project-map.md').write_text('current owner')
        (self.workspace/'tools').mkdir();(self.workspace/'tools/build_tool_introductions.py').write_text('# fixture')
        context=bridge.static_site_context({'site_workspace':str(self.workspace)},self.site)
        self.assertEqual(context['project_id'],'site-current')
        self.assertIn(str(self.workspace/'tools/build_tool_introductions.py'),context['guide_build'])
        prompt=bridge.static_site_prompt(Path('/request.json'))
        self.assertIn('Do not build from a legacy source repository',prompt)
        self.assertIn('skill_links_helper',prompt);self.assertIn('catalog_pending',prompt)
        self.assertIn('sites_version_source_commit',prompt)
        with self.assertRaisesRegex(ValueError,'does not own'):
            bridge.static_site_context({'site_workspace':str(self.workspace)},self.workspace/'legacy')

    def test_static_receipt_still_requires_native_verification_and_both_catalogs(self):
        (self.workspace/'docs').mkdir();(self.workspace/'docs/project-map.md').write_text('current owner')
        (self.workspace/'tools').mkdir();(self.workspace/'tools/build_tool_introductions.py').write_text('# fixture')
        publisher=self.workspace/'publisher';(publisher/'catalog').mkdir(parents=True)
        for name in ('release-history.json','skill-downloads.json'):
            (publisher/'catalog'/name).write_bytes((self.site/'dist/data'/name).read_bytes())
        receipt=self.workspace/'receipt.json';expected=self.workspace/'expected.json';expected.write_text('[]')
        proof={**self.proof(),'status':'deployed','published_set':[],'no_op':True};receipt.write_text(json.dumps(proof))
        config=self.workspace/'config.json';config.write_text(json.dumps({'site_source':str(self.site),
            'site_workspace':str(self.workspace),'site_contract':bridge.STATIC_CONTRACT,
            'site_receipt':str(receipt),'codex_command':'codex'}))
        indexed=self.git('ls-files','--cached','-z','--','.openai/hosting.json','dist')
        def git_output(argv,**kwargs):
            if argv[1]=='rev-parse':return self.head+'\n'
            if argv[1]=='status':return b''
            if argv[1]=='ls-files':return indexed
            raise AssertionError('Unexpected legacy Git operation: '+str(argv))
        def native(argv,**kwargs):
            self.assertEqual(argv[:2],['codex','exec']);self.assertEqual(kwargs['input'],bridge.static_site_prompt(publisher/'dist/release-manager/site-request.json'))
            self.assertEqual(argv[argv.index('-C')+1],str(self.site))
            receipt.write_text(json.dumps(proof));return type('Result',(),{'returncode':0})()
        def live(request,**kwargs):
            if request.full_url.endswith('/build-manifest.json'):return self.live_manifest()
            if request.full_url.endswith('/data/skill-downloads.json'):return io.BytesIO((publisher/'catalog/skill-downloads.json').read_bytes())
            if request.full_url.endswith('/data/release-history.json'):return io.BytesIO((publisher/'catalog/release-history.json').read_bytes())
            raise AssertionError(request.full_url)
        with (patch.object(bridge,'ROOT',publisher),patch.object(bridge,'verify_promotion'),
              patch.object(bridge.subprocess,'run',side_effect=native) as adapter,
              patch.object(bridge.subprocess,'check_output',side_effect=git_output),
              patch.object(bridge.urllib.request,'urlopen',side_effect=live),
              patch.dict(bridge.os.environ,{'WORKING_TOOLS_RELEASE_CONFIG':str(config),'WORKING_TOOLS_EXPECTED_RELEASES':str(expected)}),
              patch.object(sys,'argv',['release_site_bridge.py'])):
            bridge.main()
        adapter.assert_called_once()
        request=json.loads((publisher/'dist/release-manager/site-request.json').read_text())
        self.assertEqual(request['skill_catalog_sha256'],self.projection['skill_catalog_sha256'])
        self.assertIsNone(request['sources_dir'])
        self.assertEqual(request['static_context']['project_id'],'site-current')


if __name__=='__main__':unittest.main()
