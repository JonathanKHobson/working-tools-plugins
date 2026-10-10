"""Execute a fictional saved-table task through the actual manifest stdio route."""
import asyncio,json,os,sys,tempfile
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
ROOT=Path(__file__).resolve().parents[1]
async def main():
    config="mcp.json" if "--portable" in sys.argv[1:] else ".mcp.json"
    manifest=json.loads((ROOT/config).read_text())["mcpServers"]["data-explorer"]
    args=[x.replace("${CLAUDE_PLUGIN_ROOT}",str(ROOT)).replace("${PLUGIN_ROOT}",str(ROOT)) for x in manifest["args"]]
    with tempfile.TemporaryDirectory(prefix="public-data-example-") as state:
        env=dict(os.environ,**manifest["env"],DATA_EXPLORER_PYTHON=sys.executable,DATA_EXPLORER_DATA_DIR=state)
        async with stdio_client(StdioServerParameters(command=manifest["command"],args=args,env=env,cwd=str(ROOT))) as (read,write):
            async with ClientSession(read,write) as session:
                await session.initialize();tools=await session.list_tools();assert len(tools.tools)==4
                create_tool=next(tool for tool in tools.tools if tool.name=="data_create_dataset")
                schema=create_tool.inputSchema
                column=schema["$defs"][schema["properties"]["columns"]["items"]["$ref"].split("/")[-1]]
                row=schema["$defs"][schema["properties"]["rows"]["items"]["$ref"].split("/")[-1]]
                assert set(column["required"])=={"key","label","type"} and "name" not in column["properties"]
                assert set(column["properties"]["type"]["enum"])=={"number","category","text"}
                assert set(row["required"])=={"id","values"}
                resources=await session.list_resources();assert len(resources.resources)==1
                resource=await session.read_resource(resources.resources[0].uri);assert "Data Explorer" in resource.contents[0].text
                payload=json.loads((ROOT/"examples/sample-dataset.json").read_text())
                wrong=json.loads(json.dumps(payload));wrong["columns"][0]["name"]=wrong["columns"][0].pop("label")
                rejected=await session.call_tool("data_create_dataset",wrong);assert rejected.isError
                assert "label" in rejected.content[0].text and "name" in rejected.content[0].text
                created=await session.call_tool("data_create_dataset",payload);assert not created.isError
                did=created.structuredContent["dataset_id"]
                opened=await session.call_tool("data_open_explorer",{"dataset_id":did});assert len(opened.structuredContent["rows"])==4
                saved=await session.call_tool("data_read_view",{"dataset_id":did});data=saved.structuredContent;assert "rows" not in data
                assert data["aggregate"]["mean"]==20 and data["aggregate"]["known_count"]==3 and data["aggregate"]["missing_count"]==1
                print(json.dumps({"status":"passed","nested_schema":"exact required column/row fields and type enum","wrong_name_rejected":True,"source_revision":data["source_revision"],"synthetic":True,"aggregate":data["aggregate"],"scope":"actual stdio task;native app rendering and host delivery not tested"},indent=2))
asyncio.run(main())
