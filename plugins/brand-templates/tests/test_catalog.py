import hashlib,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runtime/brand-library'))
from catalog import catalog,search,handoff,select,validate
from server import render_html

class BrandTests(unittest.TestCase):
    def test_complete_preserved_edition(self):
        items=catalog();self.assertEqual(104,len([i for i in items if i['id']!='fresh-curiosity-a2']))
        self.assertEqual(json.loads((ROOT/'library/catalog.json').read_text())['total'],len(items))
        self.assertEqual(106,sum(len(i['sourceTemplateIds']) for i in items))
        for row in json.loads((ROOT/'provenance/source-files.json').read_text())['files']:
            p=ROOT/row['path'];self.assertTrue(p.is_file() and not p.is_symlink(),row['path'])
            self.assertEqual(row['sha256'],hashlib.sha256(p.read_bytes()).hexdigest(),row['path'])
    def test_search_handoff(self):
        item=catalog()[0];found=search(item['name']);self.assertIn(item['id'],[i['id'] for i in found['items']])
        data=handoff(item['id'],'A workshop poster')
        self.assertEqual(item['sourceHash'],data['sourceHash']);self.assertIn('A workshop poster',data['handoffText'])
        self.assertGreater(data['verifiedFiles'],20)
    def test_unknown_and_traversal(self):
        for value in ['../secret','missing-brand','/etc/passwd']:
            with self.assertRaises(ValueError):select(value)
    def test_missing_or_modified_source(self):
        item=catalog()[0]
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'library').mkdir();(root/'provenance').mkdir()
            (root/'library/catalog.json').write_text(json.dumps({'brands':[item]}))
            rel='templates/'+item['id']+'/DESIGN.md';p=root/rel;p.parent.mkdir(parents=True)
            expected=hashlib.sha256(b'expected').hexdigest()
            (root/'provenance/source-files.json').write_text(json.dumps({'files':[{'path':rel,'sha256':expected},{'path':'library/catalog.json','sha256':hashlib.sha256((root/'library/catalog.json').read_bytes()).hexdigest()}]}))
            with self.assertRaisesRegex(ValueError,'Missing'):validate(item['id'],root)
            p.write_text('changed')
            with self.assertRaisesRegex(ValueError,'differs'):validate(item['id'],root)
            p.write_text('expected');self.assertEqual(1,validate(item['id'],root)[2])
            (root/'library/catalog.json').write_text(json.dumps({'brands':[dict(item,name='Altered title')]}))
            with self.assertRaisesRegex(ValueError,'catalog differs'):validate(item['id'],root)
    def test_self_contained_ui(self):
        body=render_html();self.assertIn('Brand Templates',body);self.assertIn('data:image/webp;base64,',body)
        self.assertNotIn('__LIBRARY_',body)

if __name__=='__main__':unittest.main()
