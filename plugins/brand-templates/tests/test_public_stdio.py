"""All admitted original kits plus relocated external-fixture protocol checks."""
import asyncio,hashlib,importlib.util,json,os
from pathlib import Path
import shutil,sys,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
class PublicRuntimeTests(unittest.TestCase):
 def test_all104_original_kits_and_asset_hashes(self):
  sys.path.insert(0,str(ROOT/'runtime/brand-library'))
  from catalog import catalog,validate
  items=catalog();self.assertEqual(104,len(items));self.assertNotIn('fresh-curiosity-a2',{i['id'] for i in items})
  for item in items:
   selected,closure,count=validate(item['id']);self.assertGreater(count,20);self.assertEqual(item['id'],selected['id']);self.assertEqual(64,len(closure))
  for row in json.loads((ROOT/'provenance/source-files.json').read_text())['files']:
   self.assertEqual(row['sha256'],hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest(),row['path'])
 def test_relocated_launcher_original_and_external_collection(self):
  from mcp import ClientSession,StdioServerParameters
  from mcp.client.stdio import stdio_client
  with tempfile.TemporaryDirectory() as tmp:
   work=Path(tmp);pkg=work/'relocated plugin';shutil.copytree(ROOT,pkg,ignore=shutil.ignore_patterns('__pycache__'))
   home=work/'empty home';home.mkdir();env=dict(os.environ,HOME=str(home),BRAND_TEMPLATES_PYTHON=sys.executable,PYTHONDONTWRITEBYTECODE='1');env.pop('BRAND_TEMPLATES_DATA_ROOT',None)
   bootstrap=os.environ.get('BRAND_TEMPLATES_BOOTSTRAP_PYTHON',sys.executable)
   async def run():
    async with stdio_client(StdioServerParameters(command=bootstrap,args=[str(pkg/'scripts/brand_library_mcp.py')],env=env)) as (r,w):
     async with ClientSession(r,w) as s:
      await s.initialize();tools={t.name:t for t in (await s.list_tools()).tools};self.assertEqual(set(tools),{'search_brand_library','browse_brand_library','prepare_brand_handoff'})
      self.assertFalse(tools['search_brand_library'].meta);self.assertTrue(tools['browse_brand_library'].meta)
      for method in ('search_brand_library','browse_brand_library'):
       result=await s.call_tool(method,{});self.assertFalse(result.isError);self.assertEqual(104,result.structuredContent['total'])
      items=json.loads((pkg/'library/catalog.json').read_text())['brands']
      for item in items:
       result=await s.call_tool('prepare_brand_handoff',{'brand_id':item['id'],'brief':'Fictional source-preserving adaptation.'});self.assertFalse(result.isError);self.assertEqual(item['sourceHash'],result.structuredContent['sourceHash'])
      resources=(await s.list_resources()).resources;self.assertEqual(1,len(resources));body=(await s.read_resource(resources[0].uri)).contents[0].text;self.assertIn('data:image/webp;base64,',body);self.assertNotIn('__LIBRARY_',body)
      self.assertTrue((await s.call_tool('prepare_brand_handoff',{'brand_id':'../secret'})).isError)
    spec=importlib.util.spec_from_file_location('fixture',pkg/'scripts/create_sample_collection.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f);data=f.build(work/'external collection');env['BRAND_TEMPLATES_DATA_ROOT']=str(data)
    async with stdio_client(StdioServerParameters(command=bootstrap,args=[str(pkg/'scripts/brand_library_mcp.py')],env=env)) as (r,w):
     async with ClientSession(r,w) as s:
      await s.initialize();result=await s.call_tool('prepare_brand_handoff',{'brand_id':'fixture-neutral'});self.assertFalse(result.isError);self.assertEqual(2,result.structuredContent['verifiedFiles'])
      source=data/'templates/fixture-neutral/DESIGN.md';original=source.read_bytes();source.write_bytes(original+b'\nchanged');self.assertTrue((await s.call_tool('prepare_brand_handoff',{'brand_id':'fixture-neutral'})).isError);source.write_bytes(original)
   asyncio.run(run())
if __name__=='__main__':unittest.main()
