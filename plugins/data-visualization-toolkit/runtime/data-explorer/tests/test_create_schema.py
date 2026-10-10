"""Native callers receive the exact column/row shape; data values stay unchanged."""
import asyncio,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from server import create_server
from mcp.server.fastmcp.exceptions import ToolError

class DatasetSchemaTests(unittest.TestCase):
    def test_schema_discloses_required_nested_fields_and_types(self):
        async def check():
            with tempfile.TemporaryDirectory() as directory:
                server=create_server(directory);tools=await server.list_tools();tool=next(t for t in tools if t.name=='data_create_dataset');schema=tool.inputSchema
                columns=schema['properties']['columns'];rows=schema['properties']['rows']
                column=schema['$defs'][columns['items']['$ref'].split('/')[-1]];row=schema['$defs'][rows['items']['$ref'].split('/')[-1]]
                self.assertEqual(set(column['required']),{'key','label','type'});self.assertNotIn('name',column['properties']);self.assertFalse(column['additionalProperties'])
                self.assertEqual(set(column['properties']['type']['enum']),{'number','category','text'});self.assertIn('unit',column['properties'])
                self.assertEqual(set(row['required']),{'id','values'});self.assertFalse(row['additionalProperties']);self.assertEqual(row['properties']['values']['type'],'object');self.assertEqual(set(row['properties']['values']['additionalProperties']['type']),{'string','number','null'})
                self.assertEqual((columns['minItems'],columns['maxItems'],rows['maxItems']),(1,12,500));self.assertTrue({'columns','rows'}<=set(schema['required']))
        asyncio.run(check())
    def test_wrong_native_name_rejected_valid_zero_missing_and_empty_preserved(self):
        async def check():
            with tempfile.TemporaryDirectory() as directory:
                server=create_server(directory);sample=json.loads((ROOT.parents[1]/'examples/sample-dataset.json').read_text());wrong=json.loads(json.dumps(sample));wrong['columns'][0]['name']=wrong['columns'][0].pop('label')
                with self.assertRaises(ToolError) as failure:await server.call_tool('data_create_dataset',wrong)
                self.assertIn('label',str(failure.exception));self.assertIn('name',str(failure.exception))
                valid=await server.call_tool('data_create_dataset',sample);self.assertFalse(valid.isError);aggregate=valid.structuredContent['aggregate'];self.assertEqual((aggregate['row_count'],aggregate['known_count'],aggregate['missing_count'],aggregate['mean']),(4,3,1,20))
                opened=await server.call_tool('data_open_explorer',{'dataset_id':valid.structuredContent['dataset_id']});self.assertEqual(opened.structuredContent['rows'],sample['rows']);self.assertEqual(opened.structuredContent['columns'][1]['unit'],'minutes')
                empty={**sample,'rows':[]};created=await server.call_tool('data_create_dataset',empty);self.assertFalse(created.isError);self.assertEqual(created.structuredContent['aggregate']['row_count'],0);self.assertIsNone(created.structuredContent['aggregate']['mean'])
                bad=json.loads(json.dumps(sample));bad['rows'][0]['values']['duration']=True;rejected=await server.call_tool('data_create_dataset',bad);self.assertTrue(rejected.isError);self.assertEqual(rejected.structuredContent['error']['code'],'invalid_input')
        asyncio.run(check())
if __name__=='__main__':unittest.main()
