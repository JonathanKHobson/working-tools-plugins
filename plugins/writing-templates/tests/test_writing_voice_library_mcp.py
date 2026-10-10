"""Behavior, integrity and MCP protocol checks for the installed synthetic library."""
import asyncio
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

PLUGIN = Path(__file__).resolve().parents[1]
RUNTIME = PLUGIN / 'runtime/writing-voice-library'
sys.path.insert(0, str(RUNTIME))
import catalog
import server
import feedback

class LibraryTests(unittest.TestCase):
    def test_validation_handoff_and_tamper_rejection(self):
        result = catalog.handoff('P28', 'Explain a bounded proposal.')
        self.assertEqual(result['validation']['profiles'], ['P28', 'V01'])
        self.assertIn('validation/profiles/P28.json', result['handoffText'])
        self.assertIn('automated QA was not run', result['instructions'])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'library'
            shutil.copytree(catalog.DATA_ROOT, root)
            (root / 'validation/validate.cjs').write_text('modified checker')
            with self.assertRaises(catalog.CatalogError):
                catalog.handoff('P28', data_root=root)

    def test_source_edition_handoff_and_tamper_rejection(self):
        result = catalog.handoff('V01', 'Request a bounded trial.')
        paths = {r['path'] for r in result['sourceReferences']}
        self.assertIn('source-edition/guides/V01.md', paths)
        self.assertIn('source-edition/excerpts/H01.md', paths)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'library'
            shutil.copytree(catalog.DATA_ROOT, root)
            path = root / 'source-edition/excerpts/H01.md'
            path.write_text('Invented source text')
            with self.assertRaises(catalog.CatalogError):
                catalog.handoff('V01', data_root=root)

    def test_catalog_and_portable_handoff(self):
        result = catalog.browse()
        original_ids = {f'V{i:02}' for i in range(1, 25)} | {f'P{i:02}' for i in range(25, 49)}
        self.assertTrue(original_ids.issubset({i['id'] for i in result['items']}))
        self.assertEqual(len(result['items']), json.loads((catalog.DATA_ROOT/'records/catalog.json').read_text())['record_count'])
        self.assertEqual({i['availability'] for i in result['items']}, {'ready'})
        self.assertTrue({'P26','P29','P32','P37'}.issubset({i['id'] for i in catalog.browse(type='voice_candidate')['items']}))
        handoff = catalog.handoff('P28', 'Explain a proposed decision.')
        self.assertEqual(handoff['route'], {'selected_resource_id':'P28','base_profile_id':'V01','module_ids':['P28']})
        self.assertEqual({r['id'] for r in handoff['resources']}, {'P28','V01'})
        self.assertIn('v2.0.0', handoff['handoffText'])
        for resource in handoff['resources']:
            self.assertFalse(Path(resource['guideRef']).is_absolute())
            self.assertNotIn('..', Path(resource['guideRef']).parts)
        self.assertEqual(Path(handoff['validation']['entrypoint']), catalog.DATA_ROOT/'validation/validate.py')
        self.assertEqual(Path(handoff['validation']['alternateEntrypoint']), catalog.DATA_ROOT/'validation/validate.cjs')
        self.assertEqual(handoff['state'],'prepared')
    def test_valid_modifiers_and_incompatible_routes(self):
        result = catalog.handoff('V12', 'Bounded brief', ['P27', 'P42'])
        self.assertEqual(result['route']['module_ids'], ['P27', 'P42'])
        for args in [('V12','',['P28']), ('V12','',['P29']), ('V01','',['P28','P28']), ('V01','','P28')]:
            with self.assertRaises(catalog.CatalogError):
                catalog.handoff(*args)
    def test_validation_errors(self):
        for bad in ['../../V01', '/tmp/a', 'V00', 'P99', None]:
            with self.assertRaises(catalog.CatalogError):
                catalog.handoff(bad)
        with self.assertRaises(catalog.CatalogError):
            catalog.handoff('V01', 'a'*10001)
        with self.assertRaises(catalog.CatalogError):
            catalog.browse(type='unknown')
    def test_path_containment_and_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'safe.txt').write_text('safe')
            (root/'link.txt').symlink_to(root/'safe.txt')
            (root/'linked').symlink_to(root, target_is_directory=True)
            for path in ('../safe.txt','/tmp/a','a/../safe.txt','link.txt','linked/safe.txt','safe.txt/child','./safe.txt','safe.txt\\other'):
                with self.assertRaises(catalog.CatalogError):
                    catalog.safe_read(root,path)
            self.assertEqual(catalog.safe_read(root,'safe.txt'),b'safe')
    def test_changed_samples_guides_and_catalog(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'library'
            shutil.copytree(catalog.DATA_ROOT,root)
            sample=root/'examples/V01/specimen.md'
            original=sample.read_bytes()
            sample.write_bytes(original+b'\nchanged')
            record=next(r for r in catalog.load_catalog(root) if r['id']=='V01')
            self.assertEqual(catalog.item_status(record,root)[0],'unavailable')
            with self.assertRaises(catalog.CatalogError):
                catalog.handoff('P28',data_root=root)
            sample.write_bytes(original)
            guide=root/record['guide_path']
            guide.write_text(guide.read_text()+'\nchanged')
            with self.assertRaises(catalog.CatalogError):
                catalog.handoff('V01',data_root=root)
            path=root/'records/catalog.json'
            path.write_text(path.read_text()+'\n')
            with self.assertRaises(catalog.CatalogError):
                catalog.browse(data_root=root)
    def test_html_and_actual_text(self):
        html=server.render_html()
        self.assertIn('LibraryBridge',html)
        self.assertIn('LibraryAdapter',html)
        self.assertNotIn('__LIBRARY_',html)
        self.assertNotIn('/Users/',html)
        data=server.ui_data()
        self.assertEqual(len(data['items']),len(catalog.load_catalog()))
        registered = {row['id']: row for row in catalog.load_catalog()}
        for item in data['items']:
            self.assertEqual(len(item['examples']),3)
            expected = {sample['brief_id'] for sample in registered[item['id']]['examples']}
            self.assertEqual({s['brief_id'] for s in item['examples']},expected)
            self.assertTrue(all('specimen:start' not in s['text'] and len(s['text'])>100 for s in item['examples']))
        escaped=server._json_for_script({'text':'</script><script>alert(1)</script>'})
        self.assertNotIn('</script>',escaped)

@unittest.skipUnless(importlib.util.find_spec('mcp'), 'Use the existing approved MCP Python binding for protocol checks')
class ProtocolTests(unittest.TestCase):
    def test_optional_feedback_binding_absence_keeps_browse_and_handoff(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(feedback.Path, 'home', return_value=Path(folder)):
                mcp = server.create_server()
            tools = asyncio.run(mcp.list_tools())
            self.assertEqual({tool.name for tool in tools},
                             {'search_writing_voice_library', 'browse_writing_voice_library', 'prepare_writing_voice_handoff'})
            result = asyncio.run(mcp.call_tool('browse_writing_voice_library', {'query': 'warm'}))
            self.assertFalse(result.isError)
            self.assertIn('V02', {item['id'] for item in result.structuredContent['items']})

    def test_stdio_protocol(self):
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        async def exercise():
            env={'PYTHONDONTWRITEBYTECODE':'1','WRITING_TEMPLATES_DATA_ROOT':str(catalog.DATA_ROOT)}
            if os.environ.get('WRITING_TEMPLATES_APPROVED_SOURCES'):
                env['WRITING_TEMPLATES_APPROVED_SOURCES']=os.environ['WRITING_TEMPLATES_APPROVED_SOURCES']
            params=StdioServerParameters(command=sys.executable,args=[str(RUNTIME/'server.py')],env=env)
            async with stdio_client(params) as (read,write):
                async with ClientSession(read,write) as session:
                    await session.initialize()
                    tools=(await session.list_tools()).tools
                    tool_by_name = {tool.name: tool for tool in tools}
                    self.assertEqual(set(tool_by_name), {'search_writing_voice_library', 'browse_writing_voice_library',
                        'prepare_writing_voice_handoff', 'record_library_search_miss',
                        'review_library_search_misses'})
                    for name in ('browse_writing_voice_library',):
                        tool = tool_by_name[name]
                        self.assertTrue(tool.annotations.readOnlyHint)
                        self.assertFalse(tool.annotations.destructiveHint)
                        self.assertEqual(tool.meta['ui']['resourceUri'], server.RESOURCE_URI)
                    self.assertFalse(tool_by_name['record_library_search_miss'].annotations.readOnlyHint)
                    self.assertFalse(tool_by_name['record_library_search_miss'].annotations.destructiveHint)
                    self.assertTrue(tool_by_name['review_library_search_misses'].annotations.readOnlyHint)
                    for name in ('search_writing_voice_library', 'prepare_writing_voice_handoff'):
                        self.assertFalse(tool_by_name[name].meta)
                    result = await session.call_tool('search_writing_voice_library', {'query':'warm'})
                    self.assertFalse(result.isError)
                    self.assertIn('V02', {i['id'] for i in result.structuredContent['items']})
                    resources=(await session.list_resources()).resources
                    self.assertEqual(resources[0].mimeType,server.RESOURCE_MIME)
                    resource=await session.read_resource(server.RESOURCE_URI)
                    self.assertIn('Writing Templates',resource.contents[0].text)
                    result=await session.call_tool('browse_writing_voice_library',{'query':'warm','type':'all'})
                    self.assertFalse(result.isError)
                    self.assertIn('V02',{i['id'] for i in result.structuredContent['items']})
                    result=await session.call_tool('prepare_writing_voice_handoff',{'profile_id':'P33','brief':'Explain a choice.'})
                    self.assertEqual(result.structuredContent['route']['base_profile_id'],'P29')
                    result=await session.call_tool('prepare_writing_voice_handoff',{'profile_id':'../../secrets'})
                    self.assertTrue(result.isError)
                    self.assertNotIn('/Users/',result.content[0].text)
        asyncio.run(exercise())

if __name__=='__main__':
    unittest.main()
