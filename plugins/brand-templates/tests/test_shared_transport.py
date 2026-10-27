"""Observable parity, independent sessions, private bindings, and owned lifecycle."""
import os,sys,json,tempfile,time,signal,stat,unittest,importlib.util
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
from stdio_client import StdioClient
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runtime/brand-library'))
from stdio_proxy import backend_key,private_directory,connect
BASELINE=Path(os.environ.get('BRAND_BASELINE_ROOT', ROOT))
class SharedTransportTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='brd-test-',dir='/tmp');self.path=Path(self.tmp.name)
  self.sockets=self.path/'s';self.sockets.mkdir(mode=0o700)
  spec=importlib.util.spec_from_file_location('fixture',ROOT/'scripts/create_sample_collection.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
  self.fixture=f.build(self.path/'collection')
  self.env=dict(os.environ,BRAND_TEMPLATES_DATA_ROOT=str(self.fixture),BRAND_TEMPLATES_PYTHON=sys.executable,BRAND_BACKEND_SOCKET_DIR=str(self.sockets),BRAND_BACKEND_IDLE_SECONDS='0.3',PYTHONDONTWRITEBYTECODE='1')
  for k in ['BRAND_TEMPLATES_CATALOG','BRAND_TEMPLATES_SOURCE_MANIFEST']:self.env.pop(k,None)
  self.clients=[]
 def client(self,shared=True):
  root=ROOT if shared else BASELINE;env=dict(self.env)
  if not shared:env['BRAND_TEMPLATES_TRANSPORT']='direct'
  c=StdioClient([sys.executable,'-B',str(root/'scripts/brand_library_mcp.py')],env);self.clients.append(c);c.initialize();return c
 def receipts(self):return [json.loads(p.read_text()) for p in self.sockets.glob('*.pid')]
 def retire(self):
  end=time.monotonic()+6
  while self.receipts() and time.monotonic()<end:time.sleep(.05)
  self.assertEqual([],self.receipts(),'Owned backend must retire')
 def tearDown(self):
  for c in self.clients:c.close()
  self.retire();self.tmp.cleanup()
 def test_original_protocol_parity_all_tools_and_resource(self):
  a,b=self.client(False),self.client()
  for method,params in [('tools/list',None),('resources/list',None),('resources/templates/list',None),('tools/call',{'name':'search_brand_library','arguments':{'query':'fixture'}}),('tools/call',{'name':'browse_brand_library','arguments':{}}),('tools/call',{'name':'prepare_brand_handoff','arguments':{'brand_id':'fixture-neutral','brief':'test'}}),('tools/call',{'name':'prepare_brand_handoff','arguments':{'brand_id':'../secret'}})]:
   self.assertEqual(a.request(method,params)['result'],b.request(method,params)['result'],method)
  uri=a.request('resources/list')['result']['resources'][0]['uri']
  self.assertEqual(a.request('resources/read',{'uri':uri})['result'],b.request('resources/read',{'uri':uri})['result'])
 def test_concurrent_isolation_active_client_survives_idle_timeout(self):
  with ThreadPoolExecutor(max_workers=4) as pool:clients=list(pool.map(lambda _:self.client(),range(4)))
  self.assertEqual(1,len(self.receipts()))
  def query(pair):
   i,c=pair;return c.request('tools/call',{'name':'search_brand_library','arguments':{'query':'q'+str(i)}})['result']['structuredContent']['query']
  with ThreadPoolExecutor(max_workers=4) as pool:self.assertEqual(['q0','q1','q2','q3'],list(pool.map(query,enumerate(clients))))
  clients[0].close();self.clients.remove(clients[0]);time.sleep(.5)
  self.assertTrue(clients[1].request('tools/list')['result']['tools'])
  clients[1].process.stdin.write('{invalid}\n');clients[1].process.stdin.flush()
  self.assertTrue(clients[2].request('tools/list')['result']['tools'])
 def test_binding_security_and_fingerprint(self):
  self.client();receipt=self.receipts()[0];p=Path(receipt['socket']);self.assertEqual(0o600,stat.S_IMODE(p.stat().st_mode))
  with patch.dict(os.environ,self.env,clear=True):
   before=backend_key(sys.executable)
   with patch.dict(os.environ,{'BRAND_TEMPLATES_DATA_ROOT':str(self.path/'different')}):self.assertNotEqual(before,backend_key(sys.executable))
   with patch('stdio_proxy.peer_uid',return_value=os.getuid()+1):
    with self.assertRaises(PermissionError):connect(p)
   self.sockets.chmod(0o755)
   with self.assertRaises(ValueError):private_directory()
   self.sockets.chmod(0o700)
 def test_owned_client_crash_retires_backend_and_cold_restarts(self):
  c=self.client();old=self.receipts()[0]['pid'];c.process.kill();c.process.wait(timeout=5);c.close();self.clients.remove(c);self.retire()
  d=self.client();self.assertNotEqual(old,self.receipts()[0]['pid']);self.assertTrue(d.request('tools/list')['result']['tools'])
 def test_owned_backend_crash_fails_without_replay_new_session_recovers(self):
  a,b=self.client(),self.client();receipt=self.receipts()[0]
  # PID comes only from the backend this test started in its unique private socket directory.
  os.kill(receipt['pid'],signal.SIGKILL)
  self.assertNotEqual(0,a.process.wait(timeout=5));self.assertNotEqual(0,b.process.wait(timeout=5))
  c=self.client();self.assertNotEqual(receipt['pid'],self.receipts()[0]['pid']);self.assertTrue(c.request('tools/list')['result']['tools'])
if __name__=='__main__':unittest.main()
