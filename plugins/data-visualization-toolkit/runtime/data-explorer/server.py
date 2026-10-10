"""Private interactive data explorer MCP App over stdio."""
from __future__ import annotations
import argparse
import sqlite3
import sys
from pathlib import Path
from store import ExplorerError, ExplorerStore
ROOT=Path(__file__).resolve().parent
RESOURCE_URI='ui://data-explorer/explorer.html'
RESOURCE_MIME='text/html;profile=mcp-app'

def render_html(root=ROOT):
    path=root/'dist'/'widget.html'
    if not path.is_file() or path.is_symlink(): raise FileNotFoundError(f'Built widget unavailable: {path}')
    return path.read_text(encoding='utf-8')

def create_server(data_dir=None):
    from mcp.server.fastmcp import FastMCP
    from mcp.types import CallToolResult, TextContent, ToolAnnotations
    store=ExplorerStore(data_dir if data_dir is not None else Path.home()/'.local/share/working-tools/data-explorer')
    server=FastMCP('Data Explorer')
    ui_meta={'ui':{'resourceUri':RESOURCE_URI},'openai/outputTemplate':RESOURCE_URI}
    app_only={'ui':{'visibility':['app']},'openai/widgetAccessible':True}
    read=ToolAnnotations(readOnlyHint=True,destructiveHint=False,idempotentHint=True,openWorldHint=False)
    write=ToolAnnotations(readOnlyHint=False,destructiveHint=False,idempotentHint=False,openWorldHint=False)
    def result(action,summary):
        try:
            data=action()
            return CallToolResult(content=[TextContent(type='text',text=f"{summary}: {data['title']} · revision {data['revision']} · {data['aggregate']['row_count']} filtered rows")],structuredContent=data)
        except ExplorerError as exc:
            error={'error':{'code':exc.code,'message':str(exc)}}
            if exc.current is not None: error['current']=exc.current
            return CallToolResult(content=[TextContent(type='text',text=f'{exc.code}: {exc}')],structuredContent=error,isError=True)
        except (sqlite3.Error,OSError):
            return CallToolResult(content=[TextContent(type='text',text='storage_error: private explorer storage unavailable')],structuredContent={'error':{'code':'storage_error','message':'private explorer storage unavailable'}},isError=True)
    @server.tool(name='data_create_dataset',title='Create private dataset',description='Create an immutable private tabular dataset with explicit source title/revision and synthetic flag. Supply 1–12 typed columns and up to 500 rows, each {id,values} with exact column keys. At least one numeric column. No import, file reading, queries, inference or cleaning. Returns saved view metadata and aggregate, without raw rows.',annotations=write)
    def data_create_dataset(title:str,source_revision:str,synthetic:bool,columns:list[dict],rows:list[dict]):
        return result(lambda:store.create(title,source_revision,synthetic,columns,rows),'Dataset created')
    @server.tool(name='data_open_explorer',title='Open data explorer',description='Open the private dataset in the interactive explorer. The view includes source rows for the app; use data_read_view for model-only summary.',annotations=read,meta=ui_meta)
    def data_open_explorer(dataset_id:str):
        return result(lambda:store.read(dataset_id,True),'Explorer opened')
    @server.tool(name='data_read_view',title='Read saved data view',description='Read the saved filters, measure, sort, selected row IDs, source metadata and computed aggregate. Does not return raw rows. Saved view is the source of truth; unsaved UI controls are not included.',annotations=read)
    def data_read_view(dataset_id:str):
        return result(lambda:store.read(dataset_id,False),'Saved view')
    @server.tool(name='data_save_view',title='Save explorer view',description='App-only save of validated view state with compare-and-swap expected revision and idempotent operation id. Immutable dataset rows are unchanged.',annotations=write,meta=app_only)
    def data_save_view(dataset_id:str,expected_revision:int,operation_id:str,view:dict):
        return result(lambda:store.save(dataset_id,expected_revision,operation_id,view),'View saved')
    @server.resource(RESOURCE_URI,name='Data Explorer',title='Data Explorer',description='Private responsive data explorer.',mime_type=RESOURCE_MIME,meta={'ui':{'csp':{'connectDomains':[],'resourceDomains':[],'frameDomains':[]}}})
    def resource()->str: return render_html()
    return server

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,default=Path.home()/'.local/share/working-tools/data-explorer')
    parser.add_argument('--stdio',action='store_true')
    parser.add_argument('--export-html',type=Path)
    args=parser.parse_args(argv)
    try:
        if args.export_html:
            html=render_html(); args.export_html.parent.mkdir(parents=True,exist_ok=True);args.export_html.write_text(html,encoding='utf-8');print(args.export_html);return 0
        create_server(args.data_dir).run(transport='stdio');return 0
    except (OSError,ExplorerError,FileNotFoundError) as exc:
        print(f'Data Explorer: {exc}',file=sys.stderr);return 1
if __name__=='__main__': raise SystemExit(main())
