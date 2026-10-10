import asyncio
import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from store import ExplorerStore,ExplorerError,compute,default_view,validate_dataset
from server import create_server,render_html

COLUMNS=[{'key':'group','label':'Group','type':'category'},{'key':'value','label':'Value','type':'number','unit':'ms'},{'key':'note','label':'Note','type':'text'}]
ROWS=[{'id':rid,'values':{'group':g,'value':v,'note':n}} for rid,g,v,n in [('r1','North',10,'a'),('r2',None,None,'missing'),('r3','',50,'empty'),('r4','North',0,'zero'),('r5','Missing',None,'literal')]]

def sample(): return validate_dataset('Fixture','source-v1',True,COLUMNS,ROWS)
class StoreTests(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory();self.store=ExplorerStore(self.tmp.name);self.created=self.store.create('Fixture','source-v1',True,COLUMNS,ROWS);self.did=self.created['dataset_id']
    def tearDown(self):self.tmp.cleanup()
    def test_missing_zero_and_empty(self):
        data=sample();view=default_view(data);a=compute(data,view)
        self.assertEqual((a['row_count'],a['known_count'],a['missing_count'],a['min'],a['max'],a['mean']),(5,3,2,0,50,20))
        view['category_column']='group';view['category_value']=None
        self.assertEqual(compute(data,view)['row_count'],1)
        view['category_value']='Missing';self.assertEqual(compute(data,view)['row_count'],1)
        view['category_value']='';self.assertEqual(compute(data,view)['row_count'],1)
        view['category_column']=None;view['category_value']=None
        view['numeric_filter']={'column':'value','min':0,'max':0,'include_missing':False}
        self.assertEqual(compute(data,view)['selected_visible_ids'],[])
        self.assertEqual(compute(data,view)['row_count'],1)
        view['numeric_filter']['include_missing']=True
        self.assertEqual((compute(data,view)['row_count'],compute(data,view)['known_count']),(3,1))
        view['numeric_filter']['min']=100
        view['numeric_filter']['max']=200
        self.assertEqual((compute(data,view)['row_count'],compute(data,view)['mean']),(2,None))
    def test_conflict_retry_and_immutable(self):
        view=default_view(sample());view['selected_ids']=['r1'];one=self.store.save(self.did,1,'operation-1',view)
        self.assertEqual(one['revision'],2)
        self.assertEqual(self.store.save(self.did,1,'operation-1',view),one)
        other=default_view(sample())
        with self.assertRaises(ExplorerError) as err:self.store.save(self.did,1,'operation-1',other)
        self.assertEqual(err.exception.code,'operation_reused')
        with self.assertRaises(ExplorerError) as err:self.store.save(self.did,1,'operation-2',other)
        self.assertEqual(err.exception.code,'conflict');self.assertEqual(err.exception.current['revision'],2)
        self.assertEqual(self.store.read(self.did,True)['rows'],ROWS)
        self.assertNotIn('rows',self.store.read(self.did))
        self.assertEqual(self.store.db.stat().st_mode & 0o777,0o600)
    def test_private_path(self):
        with tempfile.TemporaryDirectory() as base:
            public=Path(base)/'public';public.mkdir(mode=0o755)
            with self.assertRaises(ExplorerError):ExplorerStore(public)
            link=Path(base)/'link';link.symlink_to(self.tmp.name, target_is_directory=True)
            with self.assertRaises(ExplorerError):ExplorerStore(link)
    def test_validation_bounds(self):
        with self.assertRaises(ExplorerError):validate_dataset('x','r',False,COLUMNS,[{'id':'x','values':{'group':'a','value':True,'note':''}}])
        with self.assertRaises(ExplorerError):validate_dataset('x','r',False,[{'key':'id','label':'ID','type':'number'}],[])
        with self.assertRaises(ExplorerError):validate_dataset('x','r',False,COLUMNS,ROWS*101)
        view=default_view(sample());view['selected_ids']=[{}]
        with self.assertRaises(ExplorerError):compute(sample(),view)
        view=default_view(sample());view['numeric_filter']={'column':'value','min':float('nan'),'max':None,'include_missing':False}
        with self.assertRaises(ExplorerError):compute(sample(),view)
    def test_sort_and_parity(self):
        data=sample();views=[]
        for direction in ('asc','desc'):
            for column in ('id','group','value'):
                view=default_view(data);view['sort']={'column':column,'direction':direction};view['selected_ids']=['r1','r2'];views.append(view)
        view=default_view(data);view['numeric_filter']={'column':'value','min':0,'max':40,'include_missing':True};views.append(view)
        view=default_view(data);view['category_column']='group';view['category_value']=None;views.append(view)
        payload={'data':data,'views':views}
        js="import {compute} from './web/compute.js';let input='';for await(const c of process.stdin)input+=c;const p=JSON.parse(input);console.log(JSON.stringify(p.views.map(v=>compute(p.data,v).aggregate)))"
        proc=subprocess.run(['node','--input-type=module','-e',js],input=json.dumps(payload),text=True,capture_output=True,cwd=ROOT,check=True)
        actual=json.loads(proc.stdout)
        for view,got in zip(views,actual):
            expected=compute(data,view)
            self.assertEqual(got,expected)
    def test_empty_and_extreme(self):
        data=validate_dataset('Extreme','rev',False,[{'key':'value','label':'Value','type':'number'}],[{'id':'a','values':{'value':1e308}},{'id':'b','values':{'value':-1e308}}])
        self.assertTrue(math.isfinite(compute(data,default_view(data))['mean']))
        js="import {compute} from './web/compute.js';let input='';for await(const c of process.stdin)input+=c;const d=JSON.parse(input);console.log(JSON.stringify(compute(d,d.view).aggregate))"
        proc=subprocess.run(['node','--input-type=module','-e',js],input=json.dumps({**data,'view':default_view(data)}),text=True,capture_output=True,cwd=ROOT,check=True)
        self.assertEqual(json.loads(proc.stdout),compute(data,default_view(data)))
        empty=validate_dataset('Empty','rev',False,[{'key':'value','label':'Value','type':'number'}],[])
        self.assertEqual(compute(empty,default_view(empty))['mean'],None)
class ProtocolTests(unittest.TestCase):
    def test_tools_and_resource(self):
        with tempfile.TemporaryDirectory() as tmp:
            server=create_server(tmp)
            async def check():
                created=await server.call_tool('data_create_dataset',{'title':'Fixture','source_revision':'r1','synthetic':True,'columns':COLUMNS,'rows':ROWS})
                self.assertFalse(created.isError);did=created.structuredContent['dataset_id']
                read=await server.call_tool('data_read_view',{'dataset_id':did});self.assertNotIn('rows',read.structuredContent)
                opened=await server.call_tool('data_open_explorer',{'dataset_id':did});self.assertEqual(len(opened.structuredContent['rows']),5)
                view=opened.structuredContent['view'];view['measure']='value'
                save=await server.call_tool('data_save_view',{'dataset_id':did,'expected_revision':1,'operation_id':'test-op-1','view':view})
                self.assertFalse(save.isError);self.assertEqual(save.structuredContent['revision'],2)
                again=await server.call_tool('data_save_view',{'dataset_id':did,'expected_revision':1,'operation_id':'test-op-1','view':view})
                self.assertEqual(again.structuredContent['revision'],2)
                bad=await server.call_tool('data_save_view',{'dataset_id':did,'expected_revision':1,'operation_id':'test-op-2','view':view})
                self.assertTrue(bad.isError);self.assertEqual(bad.structuredContent['error']['code'],'conflict')
            asyncio.run(check())
        html=render_html();self.assertLess(len(html.encode()),1_000_000);self.assertIn('Data Explorer',html)
if __name__=='__main__':unittest.main()
