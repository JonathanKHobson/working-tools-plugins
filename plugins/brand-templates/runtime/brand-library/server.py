"""Read-only Brand Library MCP app and standalone export."""
from pathlib import Path
import argparse
import base64
import json
from catalog import ROOT, catalog, search, handoff

RESOURCE_URI = 'ui://brand-library/gallery-prompt-v2.html'


def script_json(value):
    return json.dumps(value,ensure_ascii=False).replace('&','\\u0026').replace('<','\\u003c').replace('>','\\u003e').replace('\u2028','\\u2028').replace('\u2029','\\u2029')


def render_html():
    items=[]
    for item in catalog():
        preview=ROOT/'library'/item['previews'][0]['src']
        if preview.is_symlink() or not preview.resolve().is_relative_to((ROOT/'library').resolve()):
            raise ValueError('Unsafe preview')
        items.append({**item,'preview':'data:image/webp;base64,'+base64.b64encode(preview.read_bytes()).decode()})
    ui=Path(__file__).parent/'ui'
    body=(ui/'index.html').read_text()
    for token,value in {
        '__LIBRARY_DATA__':script_json({'items':items}),
        '__LIBRARY_CSS__':(ui/'styles.css').read_text(),
        '__LIBRARY_BRIDGE__':(ui/'bridge.js').read_text(),
        '__LIBRARY_JS__':(ui/'adapter.js').read_text()+'\n'+(ui/'app.js').read_text(),
    }.items():
        if body.count(token)!=1:raise ValueError('Invalid UI marker')
        body=body.replace(token,value,1)
    return body


def create_server():
    from mcp.server.fastmcp import FastMCP
    from mcp.types import CallToolResult, TextContent, ToolAnnotations
    mcp=FastMCP('Brand Library')
    readonly=ToolAnnotations(readOnlyHint=True,destructiveHint=False,idempotentHint=True,openWorldHint=False)
    def result(data):
        return CallToolResult(content=[TextContent(type='text',text=data.get('handoffText') or json.dumps(data,ensure_ascii=False))],structuredContent=data)
    @mcp.tool(name='search_brand_library',description='Assistant-only search of reusable brand kits, names, categories and source design IDs. Read-only; no widget.',annotations=readonly)
    def search_brand_library(query:str='',category:str='all'):
        return result(search(query,category))
    @mcp.tool(name='browse_brand_library',description='Open the Brand Templates picker when the human wants to browse or choose a reusable identity. Read-only.',annotations=readonly,meta={'ui':{'resourceUri':RESOURCE_URI},'openai/outputTemplate':RESOURCE_URI})
    def browse_brand_library(query:str='',category:str='all'):
        return result(search(query,category))
    @mcp.tool(name='prepare_brand_handoff',description='Verify the selected brand source closure and prepare a version-bound prompt. Read-only; no widget, installation or publishing.',annotations=readonly)
    def prepare_brand_handoff(brand_id:str,brief:str=''):
        return result(handoff(brand_id,brief))
    @mcp.resource(RESOURCE_URI,name='Brand Library gallery',mime_type='text/html;profile=mcp-app')
    def gallery()->str:
        return render_html()
    return mcp

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--export-html',type=Path);a=p.parse_args()
    if a.export_html:
        a.export_html.parent.mkdir(parents=True,exist_ok=True);a.export_html.write_text(render_html())
    else:create_server().run(transport='stdio')
