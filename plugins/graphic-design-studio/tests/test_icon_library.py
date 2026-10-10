import importlib.util,json,unittest
from pathlib import Path
from unittest.mock import patch
from email.message import Message
P=Path(__file__).resolve().parents[1]/'scripts/icon_library.py'
spec=importlib.util.spec_from_file_location('icons',P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
SVG=b'<svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2"><path d="M3 10L12 2l9 8"/></g></svg>'
class IconTests(unittest.TestCase):
 def test_valid_geometry_and_hash_receipt(self):
  info={'prefix':'lucide','info':{'name':'Lucide','license':{'title':'ISC','url':'https://example.org/license'}}}
  with patch.object(m,'collection',return_value=info),patch.object(m,'fetch',return_value=(SVG,m.HOST+'/lucide/home.svg')):
   r=m.get('lucide:home');self.assertEqual(r['svg_sha256'],m.hashlib.sha256(r['svg'].encode()).hexdigest());self.assertIn('M3 10L12 2l9 8',r['svg'])
 def test_active_svg_elements_and_attributes_refused(self):
  for body in ['<script>alert(1)</script>','<image href="https://evil.test/x"/>','<foreignObject/>','<path d="M0 0" onload="x"/>','<path d="M0 0" fill="url(https://evil.test)"/>','<path style="fill:red"/>','<use href="#id"/>','<svg viewBox="0 0 1 1"/>']:
   with self.subTest(body=body),self.assertRaises(ValueError):m.passive_svg(('<svg xmlns="'+m.NS+'" viewBox="0 0 24 24">'+body+'</svg>').encode())
 def test_xml_namespaces_entities_and_limits_refused(self):
  for raw in [b'<!DOCTYPE svg [<!ENTITY x "xxx">]>'+SVG,b'<?xml-stylesheet href="https://evil.test"?>'+SVG,SVG.replace(b'<path ',b'<path xmlns="https://evil.test" '),SVG.replace(b'M3 10L12 2l9 8',b'M1e999 0'),b'x'*262145,SVG.replace(b'0 0 24 24',b'0 0 -1 24')]:
   with self.subTest(raw=raw[:40]),self.assertRaises(ValueError):m.passive_svg(raw)
 def test_ids_search_and_response_validation(self):
  for s in ['../../x:y','lucide:home?x=1','lucide:home:extra','lucide:%2e%2e','lucide:<svg>']:
   with self.assertRaises(ValueError):m.icon_id(s)
  with patch.object(m,'data',return_value=({'icons':['lucide:home','lucide:check'],'collections':{}},'url','hash')):
   self.assertEqual(m.search('home',limit=1)['icons'],['lucide:home'])
  for q,limit in [('https://private.test',1),('x',0),('x',51),('x',True)]:
   with self.assertRaises(ValueError):m.search(q,limit=limit)
  with patch.object(m,'data',return_value=({'icons':['../p:evil'],'collections':{}},'url','hash')),self.assertRaises(ValueError):m.search('home')
 def test_rights_missing_stops_before_svg_fetch(self):
  with patch.object(m,'collection',return_value={'info':{'license':{}}}),patch.object(m,'fetch') as f,self.assertRaises(ValueError):m.get('lucide:home')
  f.assert_not_called()
 def test_overall_deadline_interrupts_trickle_and_restores_handler(self):
  old=m.signal.getsignal(m.signal.SIGALRM)
  class Trickle:
   headers={}
   def read(self,n):m.time.sleep(0.1);return b'x'
  start=m.time.monotonic()
  with self.assertRaises(TimeoutError),m.request_deadline(0.01):m.read_response(Trickle(),10)
  self.assertLess(m.time.monotonic()-start,0.09)
  self.assertEqual(m.signal.getsignal(m.signal.SIGALRM),old)
  self.assertEqual(m.signal.getitimer(m.signal.ITIMER_REAL),(0.0,0.0))
 def test_no_redirect_and_unsupported_origin(self):
  with self.assertRaises(ValueError):m.NoRedirect().redirect_request(None,None,302,'',{},'https://evil.test')
  with self.assertRaises(ValueError):m.fetch('https://evil.test')
 def test_response_size_encoding_and_request_boundary(self):
  class Response:
   def __init__(self,body,encoding='identity'):
    self.body=body;self.headers=Message();self.headers['Content-Type']='image/svg+xml';self.headers['Content-Encoding']=encoding
   def read(self,n):b,self.body=self.body[:n],self.body[n:];return b
   def __enter__(self):return self
   def __exit__(self,*args):pass
   def geturl(self):return m.HOST+'/lucide/home.svg'
  with self.assertRaises(ValueError):m.read_response(Response(b'x'*12),10)
  with self.assertRaises(ValueError):m.read_response(Response(b'x','gzip'),10)
  class Opener:
   def open(self,req,timeout):
    self.req=req;self.timeout=timeout;return Response(SVG)
  op=Opener()
  with patch.object(m.urllib.request,'build_opener',return_value=op) as build:
   raw,url=m.fetch('/lucide/home.svg',svg=True);self.assertEqual(raw,SVG);self.assertEqual(op.req.get_method(),'GET');self.assertEqual(op.timeout,10);self.assertEqual(build.call_args.args[0].proxies,{})
if __name__=='__main__':unittest.main()
