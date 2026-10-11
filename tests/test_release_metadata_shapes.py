"""Metadata refresh preserves public schemas and hashes dependency outputs."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from release_manager import local_sync


class MetadataShapeTests(unittest.TestCase):
    def test_dict_manifest_preserves_scope_and_hashes_refreshed_dependencies(self):
        with tempfile.TemporaryDirectory() as directory:
            public=Path(directory)
            (public/'README.md').write_text('changed content\n')
            (public/'unreviewed.md').write_text('outside reviewed scope\n')
            provenance={'version':'old','files':[{'path':'README.md','output_sha256':'stale',
                'source_sha256':'historical-source'}]}
            license_scope={'version':'old','files':[{'path':'PROVENANCE.json','sha256':'stale',
                'license':'MIT'}]}
            manifest={'schema_version':1,'version':'old','inventory_excludes':['PUBLIC_FILE_MANIFEST.json'],
                'files':{'README.md':'stale','PROVENANCE.json':'stale','LICENSE-SCOPE.json':'stale',
                         'PUBLIC_FILE_MANIFEST.json':'excluded-self','unreviewed.md':'unchanged'}}
            for name,data in [('PROVENANCE.json',provenance),('LICENSE-SCOPE.json',license_scope),
                              ('PUBLIC_FILE_MANIFEST.json',manifest)]:
                local_sync.write(public/name,data)
            allowed={'README.md','PROVENANCE.json','LICENSE-SCOPE.json','PUBLIC_FILE_MANIFEST.json'}
            local_sync.refresh_metadata(public,allowed,'1.2.3')
            result=local_sync.read(public/'PUBLIC_FILE_MANIFEST.json')
            self.assertIsInstance(result['files'],dict)
            self.assertEqual(set(result['files']),set(manifest['files']))
            self.assertEqual(result['files']['PUBLIC_FILE_MANIFEST.json'],'excluded-self')
            self.assertEqual(result['files']['unreviewed.md'],'unchanged')
            for name in ('README.md','PROVENANCE.json','LICENSE-SCOPE.json'):
                self.assertEqual(result['files'][name],local_sync.digest((public/name).read_bytes()))
            provenance=local_sync.read(public/'PROVENANCE.json')
            self.assertEqual(provenance['files'][0]['source_sha256'],'historical-source')
            license_scope=local_sync.read(public/'LICENSE-SCOPE.json')
            self.assertEqual(license_scope['files'][0]['sha256'],local_sync.digest((public/'PROVENANCE.json').read_bytes()))
            self.assertEqual(license_scope['files'][0]['license'],'MIT')
            self.assertEqual(result['version'],'1.2.3')

    def test_list_manifest_retains_rows_bytes_and_historical_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            public=Path(directory);(public/'README.md').write_text('changed content\n')
            manifest={'version':'old','self_excluded':'PUBLIC_FILE_MANIFEST.json','files':[
                {'path':'README.md','sha256':'stale','bytes':0,'source_sha256':'historical'},
                {'path':'PUBLIC_FILE_MANIFEST.json','sha256':'excluded-self'}]}
            local_sync.write(public/'PUBLIC_FILE_MANIFEST.json',manifest)
            local_sync.refresh_metadata(public,{'README.md','PUBLIC_FILE_MANIFEST.json'},'1.2.3')
            result=local_sync.read(public/'PUBLIC_FILE_MANIFEST.json')
            self.assertIsInstance(result['files'],list)
            self.assertEqual(result['files'][0],{'path':'README.md',
                'sha256':local_sync.digest((public/'README.md').read_bytes()),
                'bytes':(public/'README.md').stat().st_size,'source_sha256':'historical'})
            self.assertEqual(result['files'][1],manifest['files'][1])

    def test_dict_manifest_real_dependency_cycle_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            public=Path(directory)
            local_sync.write(public/'PUBLIC_FILE_MANIFEST.json',{'files':{'PROVENANCE.json':'stale'}})
            local_sync.write(public/'PROVENANCE.json',{'files':[{'path':'PUBLIC_FILE_MANIFEST.json','sha256':'stale'}]})
            with self.assertRaisesRegex(ValueError,'Cyclic metadata hashes'):
                local_sync.refresh_metadata(public,{'PUBLIC_FILE_MANIFEST.json','PROVENANCE.json'},'1.2.3')


if __name__=='__main__':unittest.main()
