import json
from pathlib import Path
import sys,tempfile,unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import complete_update

class PromotionTests(unittest.TestCase):
    def test_only_verified_current_version_advances(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'catalog').mkdir();path=root/'catalog/packages.json'
            rows=[{'id':k,'version':'1.1.0','distribution':'prepared'} for k in ('ready','older','absent')]
            path.write_text(json.dumps({'packages':rows}))
            verified=[{'product_id':'ready','version':'1.1.0'},{'product_id':'older','version':'1.0.0'}]
            with patch.object(complete_update,'ROOT',root),patch.object(complete_update,'current_published_set',return_value=verified):
                self.assertTrue(complete_update.promote_verified_registry({}))
                self.assertEqual([r['distribution'] for r in json.loads(path.read_text())['packages']],['released','prepared','prepared'])
                before=path.read_bytes();self.assertFalse(complete_update.promote_verified_registry({}));self.assertEqual(before,path.read_bytes())

    def test_history_accepts_preserved_portable_metadata_layout(self):
        import zipfile
        from release_manager.history import _supported_layout
        with tempfile.TemporaryDirectory() as d:
            archive=Path(d)/'x.zip'
            files={p:json.dumps({'name':'x','version':'1.0.1'}) for p in ('plugin.portable.json','.codex-plugin/plugin.json','.claude-plugin/plugin.json')}
            files['README.md']='Installation guidance'
            with zipfile.ZipFile(archive,'w') as z:
                for name,data in files.items():z.writestr(name,data)
            self.assertTrue(_supported_layout(archive,files,'x','1.0.1'))
            self.assertFalse(_supported_layout(archive,files,'x','1.0.0'))
            del files['.codex-plugin/plugin.json']
            self.assertFalse(_supported_layout(archive,files,'x','1.0.1'))
