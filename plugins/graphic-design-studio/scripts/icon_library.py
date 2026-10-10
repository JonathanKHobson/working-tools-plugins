#!/usr/bin/env python3
"""Explicit public Iconify lookup. JSON stdout only; no local reads/writes or MCP.

Independent local implementation informed by Better Icons' search/get workflow.
Only HTTPS GET to api.iconify.design; never follows redirects or loads SVG links.
"""
from __future__ import annotations
import argparse,hashlib,json,math,re,sys,time,signal
from contextlib import contextmanager
from datetime import datetime,timezone
import urllib.request,urllib.parse
import xml.etree.ElementTree as ET

HOST='https://api.iconify.design'
NS='http://www.w3.org/2000/svg'
TOKEN=re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
NUM=r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'
ELEMENTS={'svg','g','path','circle','ellipse','rect','line','polyline','polygon'}
NUMERIC={'x','y','x1','x2','y1','y2','cx','cy','r','rx','ry','stroke-width','stroke-miterlimit','opacity','fill-opacity','stroke-opacity','stroke-dashoffset','pathLength'}
ENUMS={'fill-rule':{'nonzero','evenodd'},'clip-rule':{'nonzero','evenodd'},'stroke-linecap':{'butt','round','square'},'stroke-linejoin':{'miter','round','bevel'},'vector-effect':{'non-scaling-stroke'}}
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,headers,newurl):raise ValueError('API redirects refused')

def token(value):
 if not isinstance(value,str) or len(value)>100 or not TOKEN.fullmatch(value):raise ValueError('Invalid collection/icon name')
 return value

def icon_id(value):
 if not isinstance(value,str) or value.count(':')!=1:raise ValueError('Use collection:icon-name')
 return tuple(token(x) for x in value.split(':'))

def read_response(response,limit):
 if response.headers.get('Content-Encoding','identity').lower() not in {'','identity'}:raise ValueError('Encoded response refused')
 length=response.headers.get('Content-Length')
 if length and (not length.isdigit() or int(length)>limit):raise ValueError('Response size cap')
 end=time.monotonic()+20;chunks=[];total=0
 while True:
  chunk=response.read(min(16384,limit-total+1))
  if time.monotonic()>end:raise ValueError('Response duration cap')
  if not chunk:break
  total+=len(chunk)
  if total>limit:raise ValueError('Response size cap')
  chunks.append(chunk)
 return b''.join(chunks)

@contextmanager
def request_deadline(seconds=20):
 # This command-line helper runs on the main thread of a POSIX host. A socket
 # inactivity timeout alone cannot stop slow-trickle headers or blocking reads.
 if not hasattr(signal,'setitimer'):raise ValueError('Bounded requests require a POSIX CLI host')
 old_handler=signal.getsignal(signal.SIGALRM);start=time.monotonic()
 def expired(signum,frame):raise TimeoutError('Overall API request deadline exceeded')
 signal.signal(signal.SIGALRM,expired)
 old_timer=signal.setitimer(signal.ITIMER_REAL,seconds)
 try:yield
 finally:
  signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,old_handler)
  delay,interval=old_timer
  if delay>0:signal.setitimer(signal.ITIMER_REAL,max(0.000001,delay-(time.monotonic()-start)),interval)

def fetch(path,params=None,svg=False):
 # No caller-controlled origin, credentials, proxy configuration or redirects.
 if not (path in {'/search','/collection','/collections'} or re.fullmatch(r'/[a-z0-9-]+/[a-z0-9-]+\.svg',path)):raise ValueError('Unsupported API path')
 url=HOST+path+('?' + urllib.parse.urlencode(params) if params else '')
 request=urllib.request.Request(url,headers={'User-Agent':'KyleStudio-IconLibrary/1.0','Accept':'image/svg+xml' if svg else 'application/json','Accept-Encoding':'identity'},method='GET')
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect())
 with request_deadline():
  with opener.open(request,timeout=10) as response:
   if response.geturl()!=url:raise ValueError('Unexpected response URL')
   mime=response.headers.get_content_type()
   if mime!=('image/svg+xml' if svg else 'application/json'):raise ValueError('Unexpected content type')
   raw=read_response(response,262144 if svg else 1048576)
 return raw,url

def data(path,params=None):
 raw,url=fetch(path,params);value=json.loads(raw.decode('utf-8'))
 if not isinstance(value,dict):raise ValueError('Expected API object')
 return value,url,hashlib.sha256(raw).hexdigest()

def public_text(value,limit=500):
 if not isinstance(value,str) or len(value)>limit or any(ord(c)<32 for c in value):raise ValueError('Malformed metadata')
 return value

def metadata(info):
 if not isinstance(info,dict):raise ValueError('Collection metadata unavailable')
 result={'name':public_text(info.get('name',''))}
 for key,fields in [('author',('name','url')),('license',('title','spdx','url'))]:
  entry=info.get(key,{})
  if not isinstance(entry,dict):raise ValueError('Malformed collection metadata')
  result[key]={k:public_text(entry[k],1000) for k in fields if k in entry}
 return result

def collection(prefix):
 token(prefix);j,url,digest=data('/collection',{'prefix':prefix,'info':'true'})
 if j.get('prefix')!=prefix:raise ValueError('Collection mismatch')
 return {'prefix':prefix,'info':metadata(j.get('info')),'source_url':url,'response_sha256':digest}

def numbers(value):
 parts=re.findall(NUM,value)
 if not parts or any(not math.isfinite(float(x)) or abs(float(x))>100000 for x in parts):raise ValueError('Unbounded SVG geometry')

def passive_svg(raw):
 if len(raw)>262144:raise ValueError('SVG size cap')
 text=raw.decode('utf-8')
 if re.search(r'<!|<\?',text):raise ValueError('SVG declarations, comments, entities and processing instructions refused')
 root=ET.fromstring(text)
 if root.tag!='{'+NS+'}svg' or 'viewBox' not in root.attrib:raise ValueError('Expected namespaced SVG with viewBox')
 count=0
 def walk(node,depth):
  nonlocal count
  count+=1
  if count>512 or depth>16:raise ValueError('SVG structure cap')
  if not isinstance(node.tag,str) or not node.tag.startswith('{'+NS+'}'):raise ValueError('Foreign SVG namespace')
  tag=node.tag.split('}',1)[1]
  if tag not in ELEMENTS or (tag=='svg' and depth!=0):raise ValueError('Unsupported SVG element')
  if (node.text or '').strip() or (node.tail or '').strip():raise ValueError('SVG text content refused')
  if len(node.attrib)>32:raise ValueError('SVG attribute cap')
  for key,value in node.attrib.items():
   if len(value)>16000:raise ValueError('SVG attribute size cap')
   if key in {'fill','stroke','color'}:
    if not (value in {'none','currentColor','transparent','black','white'} or re.fullmatch(r'#[0-9a-fA-F]{3}(?:[0-9a-fA-F]{3})?(?:[0-9a-fA-F]{2})?',value)):raise ValueError('Unsupported SVG paint')
   elif key in NUMERIC:
    if not re.fullmatch(NUM,value):raise ValueError('Non-numeric SVG value')
    numbers(value)
   elif key in {'width','height'}:
    if not re.fullmatch(NUM+r'(?:em|px)?',value):raise ValueError('Unsupported SVG dimension')
    numbers(value)
   elif key=='viewBox':
    values=re.split(r'[\s,]+',value.strip())
    if len(values)!=4 or any(not re.fullmatch(NUM,v) for v in values) or float(values[2])<=0 or float(values[3])<=0:raise ValueError('Invalid viewBox')
    numbers(value)
   elif key in {'d','points','stroke-dasharray'}:
    pattern=r'[MmZzLlHhVvCcSsQqTtAaEe0-9+.,\s-]+' if key=='d' else r'[Ee0-9+.,\s-]+'
    if not re.fullmatch(pattern,value):raise ValueError('Unsupported geometry syntax')
    if re.search(r'\d',value):numbers(value)
   elif key=='transform':
    rest=re.sub(r'(?:matrix|translate|scale|rotate|skewX|skewY)\([Ee0-9+.,\s-]+\)','',value)
    if rest.strip():raise ValueError('Unsupported transform')
    numbers(value)
   elif key in ENUMS:
    if value not in ENUMS[key]:raise ValueError('Unsupported SVG enum')
   else:raise ValueError('Unsupported SVG attribute: '+key)
  for child in node:walk(child,depth+1)
 walk(root,0);ET.register_namespace('',NS)
 return ET.tostring(root,encoding='unicode',short_empty_elements=True)

def search(query,prefix=None,limit=12):
 if not isinstance(query,str) or not 1<=len(query.strip())<=80 or not re.fullmatch(r'[A-Za-z0-9 ,\'-]+',query):raise ValueError('Use a short generic public icon concept')
 if not isinstance(limit,int) or isinstance(limit,bool) or not 1<=limit<=50:raise ValueError('Limit must be 1..50')
 params={'query':query.strip(),'limit':limit}
 if prefix:params['prefix']=token(prefix)
 j,url,digest=data('/search',params);icons=j.get('icons');collections=j.get('collections',{})
 if not isinstance(icons,list) or len(icons)>1000 or not isinstance(collections,dict):raise ValueError('Malformed search response')
 for item in icons:icon_id(item)
 selected=icons[:limit];prefixes=sorted({icon_id(x)[0] for x in selected})
 return {'icons':selected,'collections':{p:metadata(collections[p]) for p in prefixes if p in collections},'source_url':url,'response_sha256':digest,'state':'candidates-not-selected'}

def get(value):
 prefix,name=icon_id(value);info=collection(prefix);license=info['info']['license']
 if not license.get('title') or not license.get('url'):raise ValueError('License metadata unavailable; inspect rights before retrieval')
 raw,url=fetch('/'+prefix+'/'+name+'.svg',svg=True);svg=passive_svg(raw)
 return {'id':value,'svg':svg,'collection':info,'source_url':url,'source_sha256':hashlib.sha256(raw).hexdigest(),'svg_sha256':hashlib.sha256(svg.encode()).hexdigest(),'retrieved_utc':datetime.now(timezone.utc).isoformat(),'state':'retrieved-passive-subset-not-visually-reviewed','rights':'Collection metadata is evidence, not permission certification; inspect actual license and trademark terms before use.'}

def main():
 ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='command',required=True)
 s=sub.add_parser('search');s.add_argument('query');s.add_argument('--prefix');s.add_argument('--limit',type=int,default=12)
 i=sub.add_parser('info');i.add_argument('prefix')
 g=sub.add_parser('get');g.add_argument('icon_id')
 args=ap.parse_args()
 try:
  result=search(args.query,args.prefix,args.limit) if args.command=='search' else collection(args.prefix) if args.command=='info' else get(args.icon_id)
  print(json.dumps(result,ensure_ascii=True,indent=2));return 0
 except (ValueError,OSError,ET.ParseError,RecursionError) as error:
  print(json.dumps({'state':'failed','error':str(error)},ensure_ascii=True),file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
