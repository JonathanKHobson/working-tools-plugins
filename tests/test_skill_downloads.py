import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from release_manager import skill_downloads as sd


def history(version='1.0.0', commit='a'*40):
    return {'products': [{'id': 'demo', 'kind': 'plugin', 'current_release_key': 'demo/v'+version,
        'releases': [{'release_key': 'demo/v'+version, 'version': version, 'source_commit': commit,
        'distribution_status': 'available', 'verification': {'archive_verified': True, 'layout_verified': True},
        'assets': [{'name': 'demo-'+version+'.zip', 'role': 'installation', 'size': 3,
                    'sha256': hashlib.sha256(b'zip').hexdigest()}]}]}]}

class DownloadTests(unittest.TestCase):
    def test_update_noop_and_new_version_preserve_original_releases(self):
        releases = {}
        builds = []
        def remote(tag):
            return releases.get(tag) if tag.startswith('skill-bundles') else {'assets': [{'name': 'demo-'+tag.split('/v')[1]+'.zip', 'url':'source'}]}
        def build(archive, expected, sha, ident, version, commit, out):
            builds.append(version)
            path = out / ('demo-one-'+version+'.zip');path.write_bytes(version.encode())
            return [{'id':'one', 'directory':'one', 'file':path.name, 'size':path.stat().st_size,
                     'sha256':sd.digest(path), 'original_entry':'skills/one/SKILL.md',
                     'source_commit':commit,'plugin_version':version}]
        def publish(repo, record, commit, paths, **kw):
            tag=record['tag'];prefix=f'https://github.com/{repo}/releases/download/{tag}/'
            release={'draft':False,'html_url':'https://github.com/'+repo+'/releases/tag/'+tag,
                     'assets':[{'name':p.name,'size':p.stat().st_size,'state':'uploaded',
                                'digest':'sha256:'+sd.digest(p),'browser_download_url':prefix+p.name} for p in paths]}
            releases[tag]=release
            return release
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'catalog').mkdir()
            with (patch.object(sd,'_release',side_effect=remote),
                  patch.object(sd,'resolved_tag',side_effect=lambda repo,tag:'b'*40 if '1.1.0' in tag else 'a'*40),
                  patch.object(sd,'run',return_value=b'zip'),
                  patch.object(sd,'expected_package_files',return_value={'skills/one/SKILL.md':'c'*64}),
                  patch('skill_bundles.build_skill_bundles',side_effect=build),
                  patch.object(sd,'publish',side_effect=publish) as published):
                first=sd.synchronize(root,history());before=(root/'catalog/skill-downloads.json').read_bytes()
                self.assertEqual(sd.synchronize(root,history()),first)
                self.assertEqual((root/'catalog/skill-downloads.json').read_bytes(),before)
                self.assertEqual(builds,['1.0.0']);self.assertEqual(published.call_count,1)
                second=sd.synchronize(root,history('1.1.0','b'*40))
                self.assertEqual(builds,['1.0.0','1.1.0']);self.assertEqual(len(releases),2)
                self.assertEqual(second['products'][0]['version'],'1.1.0')
                releases[second['products'][0]['tag']]['assets'][0]['digest']='sha256:'+'0'*64
                with self.assertRaisesRegex(ValueError,'identity changed'):
                    sd.synchronize(root,history('1.1.0','b'*40))
                self.assertEqual(published.call_count,2)

    def test_unverified_release_refused(self):
        broken=history();broken['products'][0]['releases'][0]['verification']['archive_verified']=False
        with self.assertRaisesRegex(ValueError,'Unverified'):
            sd.current_plugins(broken)

    def test_wrong_remote_asset_url_refused(self):
        row={'file':'x.zip','size':1,'sha256':'a'*64,'url':'https://expected/x.zip'}
        release={'assets':[{'name':'x.zip','state':'uploaded','size':1,'digest':'sha256:'+'a'*64,'browser_download_url':'https://wrong/x.zip'}]}
        with self.assertRaises(ValueError):sd._asset_proof(release,[row])

class TransactionTests(unittest.TestCase):
    def test_bundle_failure_prevents_catalog_commit_and_site_adapter(self):
        import complete_update
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'catalog').mkdir()
            (root/'catalog/release-history.json').write_text(json.dumps(history()))
            events=[]
            def command(*args, **kw):events.append(args)
            with (patch.object(complete_update,'ROOT',root),
                  patch.object(complete_update,'run',return_value=b''),
                  patch.object(complete_update,'command',side_effect=command),
                  patch.object(sd,'synchronize',side_effect=ValueError('bundle rejected')) as bundles,
                  patch.object(complete_update.subprocess,'run') as adapter):
                with self.assertRaisesRegex(ValueError,'bundle rejected'):
                    complete_update.sync_site({'site_adapter':['fake'],'site_receipt':str(root/'receipt.json')},{})
                bundles.assert_called_once_with(root,history())
                adapter.assert_not_called()
                self.assertEqual(len(events),1)
                self.assertIn('scripts/sync_release_catalog.py',events[0])

if __name__=='__main__':unittest.main()
