import importlib.util
from pathlib import Path
import sys
import unittest
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
