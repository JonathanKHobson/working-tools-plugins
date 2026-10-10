"""Relocated complete-runtime protocol and integrity tests with external synthetic data."""
import asyncio, importlib.util, json, os
from pathlib import Path
import shutil, sys, tempfile, unittest
ROOT=Path(__file__).resolve().parents[1]
class PublicRuntimeTests(unittest.TestCase):
 def test_relocated_stdio_routes_closure_resource_and_feedback(self):
  from mcp import ClientSession,StdioServerParameters
  from mcp.client.stdio import stdio_client
  with tempfile.TemporaryDirectory() as tmp:
   work=Path(tmp);pkg=work/'relocated plugin';shutil.copytree(ROOT,pkg,ignore=shutil.ignore_patterns('__pycache__'))
   spec=importlib.util.spec_from_file_location('fixture',pkg/'scripts/create_sample_collection.py');fixture=importlib.util.module_from_spec(spec);spec.loader.exec_module(fixture);data=fixture.build(work/'external collection')
   home=work/'empty home';home.mkdir();env=dict(os.environ,HOME=str(home),WRITING_TEMPLATES_PYTHON=sys.executable,WRITING_TEMPLATES_DATA_ROOT=str(data),PYTHONDONTWRITEBYTECODE='1');env.pop('WRITING_LIBRARY_FEEDBACK_DB',None)
   env.pop('WRITING_TEMPLATES_APPROVED_SOURCES',None) # This fixture owns its own integrity pins.
   bootstrap=os.environ.get('WRITING_TEMPLATES_BOOTSTRAP_PYTHON',sys.executable)
   async def run():
    params=StdioServerParameters(command=bootstrap,args=[str(pkg/'scripts/writing_voice_library_mcp.py')],env=env)
    async with stdio_client(params) as (r,w):
     async with ClientSession(r,w) as s:
      await s.initialize();tools={t.name:t for t in (await s.list_tools()).tools}
      self.assertEqual(set(tools),{'search_writing_voice_library','browse_writing_voice_library','prepare_writing_voice_handoff'})
      self.assertFalse(tools['search_writing_voice_library'].meta);self.assertTrue(tools['browse_writing_voice_library'].meta)
      for method in ('search_writing_voice_library','browse_writing_voice_library'):
       reply=await s.call_tool(method,{'query':'synthetic'});self.assertFalse(reply.isError);self.assertEqual(4,len(reply.structuredContent['items']))
      reply=await s.call_tool('prepare_writing_voice_handoff',{'profile_id':'P28','brief':'Only fictional test desk facts.'})
      self.assertFalse(reply.isError);payload=reply.structuredContent
      self.assertEqual(payload['route'],{'selected_resource_id':'P28','base_profile_id':'V01','module_ids':['P28']})
      self.assertEqual(2,len(payload['sourceReferences']));self.assertEqual(12,len(payload['fourAxes']['references']));self.assertEqual(['P28','V01'],payload['validation']['profiles'])
      self.assertTrue(Path(payload['validation']['entrypoint']).is_relative_to(data))
      for args in ({'profile_id':'../V01'},{'profile_id':'V01','modifier_ids':['P29']}):
       self.assertTrue((await s.call_tool('prepare_writing_voice_handoff',args)).isError)
      resources=(await s.list_resources()).resources;self.assertEqual(1,len(resources));body=(await s.read_resource(resources[0].uri)).contents[0].text
      self.assertIn('synthetic fixture',body);self.assertNotIn('__LIBRARY_',body)
      source=data/'guides/V01.md';original=source.read_bytes();source.write_bytes(original+b'\nchanged')
      self.assertTrue((await s.call_tool('prepare_writing_voice_handoff',{'profile_id':'P28'})).isError);source.write_bytes(original)
      source=data/'validation/validate.cjs';original=source.read_bytes();source.write_bytes(original+b'\nchanged')
      self.assertTrue((await s.call_tool('prepare_writing_voice_handoff',{'profile_id':'P28'})).isError);source.write_bytes(original)
    env['WRITING_LIBRARY_FEEDBACK_DB']=str(work/'private feedback.sqlite')
    async with stdio_client(StdioServerParameters(command=bootstrap,args=[str(pkg/'scripts/writing_voice_library_mcp.py')],env=env)) as (r,w):
     async with ClientSession(r,w) as s:
      await s.initialize();self.assertEqual(5,len((await s.list_tools()).tools))
      result=await s.call_tool('review_library_search_misses',{});self.assertFalse(result.isError);self.assertEqual('not_created',json.loads(result.content[0].text)['store_state'])
      self.assertFalse((work/'private feedback.sqlite').exists())
      payload={'task_key':'6dc638c8-5390-4bde-b0dd-4412c45aa738','need_key':'synthetic-check','route':'synthetic fixture','intent':'Verify explicit feedback only','search_terms':'empty synthetic match','evidence':'Synthetic test observed no matching fixture records','result_count':0}
      logged=await s.call_tool('record_library_search_miss',payload);self.assertTrue(json.loads(logged.content[0].text)['logged']);self.assertTrue((work/'private feedback.sqlite').exists())
      logged=await s.call_tool('record_library_search_miss',payload);self.assertTrue(json.loads(logged.content[0].text)['deduplicated'])
      result=await s.call_tool('review_library_search_misses',{});self.assertEqual(1,len(json.loads(result.content[0].text)['records']))
   asyncio.run(run())
 def test_fixture_refuses_nonempty_and_package_paths(self):
  spec=importlib.util.spec_from_file_location('fixture_test',ROOT/'scripts/create_sample_collection.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
  with tempfile.TemporaryDirectory() as d:
   Path(d,'existing').write_text('preserve')
   with self.assertRaises(ValueError):f.build(Path(d))
  with self.assertRaises(ValueError):f.build(ROOT/'data')
if __name__=='__main__':unittest.main()
