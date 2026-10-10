"""Loopback-only QA harness; not evidence of actual MCP host acceptance."""
import argparse
import asyncio
import json
import secrets
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs,urlparse
from server import create_server,render_html

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,required=True)
    parser.add_argument('--port',type=int,default=0)
    args=parser.parse_args()
    mcp=create_server(args.data_dir);token=secrets.token_urlsafe(32)
    allowed={'data_create_dataset','data_open_explorer','data_read_view','data_save_view'}
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args): pass
        def reply(self,status,body,ctype='application/json'):
            self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(body.encode())
        def valid_host(self): return self.headers.get('Host')==f'127.0.0.1:{self.server.server_port}'
        def do_GET(self):
            parsed=urlparse(self.path)
            if not self.valid_host() or parsed.path!='/':return self.reply(404,'{}')
            data=None;did=parse_qs(parsed.query).get('dataset',[None])[0]
            if did:
                result=asyncio.run(mcp.call_tool('data_open_explorer',{'dataset_id':did}))
                if result.isError:return self.reply(404,'{}')
                data=result.structuredContent
            encoded=json.dumps({'token':token,'data':data}).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
            html=render_html().replace('<head>','<head><script>window.DATA_PREVIEW='+encoded+';</script>',1)
            theme=parse_qs(parsed.query).get('theme',[''])[0]
            if theme in ('dark','light'): html=html.replace('<html lang="en">','<html lang="en" data-theme="'+theme+'">',1)
            self.reply(200,html,'text/html; charset=utf-8')
        def do_POST(self):
            origin=f'http://127.0.0.1:{self.server.server_port}'
            if not self.valid_host() or self.path!='/api/tool' or self.headers.get('Origin')!=origin or not secrets.compare_digest(self.headers.get('X-Explorer-Token',''),token):return self.reply(403,'{}')
            try:
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<=700_000:return self.reply(413,'{}')
                payload=json.loads(self.rfile.read(size))
                if payload.get('name') not in allowed or not isinstance(payload.get('arguments'),dict):return self.reply(400,'{}')
                result=asyncio.run(mcp.call_tool(payload['name'],payload['arguments']))
                self.reply(200,result.model_dump_json(by_alias=True,exclude_none=True))
            except Exception as error:self.reply(400,json.dumps({'isError':True,'content':[{'type':'text','text':str(error)}]}))
    httpd=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    print(f'http://127.0.0.1:{httpd.server_port}',flush=True)
    try:httpd.serve_forever()
    except KeyboardInterrupt:pass
    finally:httpd.server_close()
if __name__=='__main__':main()
