"""Private interactive data explorer MCP App over stdio."""
from __future__ import annotations
import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from store import ExplorerError, ExplorerStore
ROOT=Path(__file__).resolve().parent
RESOURCE_URI='ui://data-explorer/explorer.html'
RESOURCE_MIME='text/html;profile=mcp-app'


class ColumnDefinition(BaseModel):
    """Disclose the nested column contract without coercing caller values."""
    model_config = ConfigDict(extra='forbid', strict=True)
    key: StrictStr = Field(description="Unique safe column identifier, other than id; every row values object must use this exact key.")
    label: StrictStr = Field(description="Human-readable column label. Use label, not name.")
    type: Literal['number', 'category', 'text'] = Field(description="At least one column must have type number.")
    unit: StrictStr | None = Field(default=None, description="Optional unit for a number column only, at most 30 characters; omit for category/text.")

class DatasetRow(BaseModel):
    """Rows retain arbitrary exact values until the existing store validates them."""
    model_config = ConfigDict(extra='forbid', strict=True)
    id: StrictStr = Field(description="Unique stable row identifier, at most 80 characters; letters, digits, underscore, period, colon and hyphen.")
    values: dict[str, Any] = Field(description="Object containing exactly all declared column keys. Number values are finite numbers or null; category/text values are strings or null. Zero is known; null is missing.", json_schema_extra={"additionalProperties": {"type": ["string", "number", "null"]}})

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
    @server.tool(name='data_create_dataset',title='Create private dataset',description='Create an immutable private tabular dataset with explicit source title/revision and synthetic flag. Supply 1–12 columns, each {key,label,type,optional unit}, with type number/category/text. Use label, not name. Rows are {id,values} with exact column keys; at most 500 rows. Zero is known and null is missing. At least one numeric column. No import, file reading, queries, inference or cleaning. Returns saved view metadata and aggregate, without raw rows.',annotations=write)
    def data_create_dataset(title:str,source_revision:str,synthetic:bool,columns:list[ColumnDefinition]=Field(min_length=1,max_length=12),rows:list[DatasetRow]=Field(max_length=500)):
        return result(lambda:store.create(title,source_revision,synthetic,[column.model_dump(exclude_unset=True) for column in columns],[row.model_dump() for row in rows]),'Dataset created')
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
