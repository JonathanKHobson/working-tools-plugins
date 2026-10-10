"""Exercise the actual manifest without generating images, uploading or saving data."""
import asyncio,json,os,sys,subprocess,hashlib
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
ROOT=Path(__file__).resolve().parents[1]
async def main():
    portable='--portable' in sys.argv
    manifest_path=ROOT/('mcp.json' if portable else '.mcp.json')
    manifest=json.loads(manifest_path.read_text())['mcpServers']['image-workflows']
    argv=[a.replace('${CLAUDE_PLUGIN_ROOT}',str(ROOT)).replace('${PLUGIN_ROOT}',str(ROOT)) for a in manifest['args']]
    env=dict(os.environ,**manifest['env'],IMAGE_WORKFLOWS_PYTHON=sys.executable)
    bootstrap=subprocess.run([manifest['command'],'-c','import sys;print(sys.version)'],capture_output=True,text=True,check=True).stdout.strip()
    async with stdio_client(StdioServerParameters(command=manifest['command'],args=argv,env=env)) as (reader,writer):
        async with ClientSession(reader,writer) as session:
            await session.initialize()
            tools=await session.list_tools();names=[t.name for t in tools.tools]
            assert set(names)=={'search_image_workflows','read_image_workflow','browse_image_workflows','prepare_image_workflow_handoff'}
            found=await session.call_tool('search_image_workflows',{'query':'poster','domain':'graphic'});assert not found.isError and found.structuredContent['total']>0
            row=found.structuredContent['items'][0];revision=found.structuredContent['revision']
            read=await session.call_tool('read_image_workflow',{'workflow_id':row['id']});assert not read.isError
            prepared=await session.call_tool('prepare_image_workflow_handoff',{'workflow_id':row['id'],'subject':'A fictional paper moon workshop','aspect_ratio':'2:3','revision':revision});assert not prepared.isError and prepared.structuredContent['status']=='prepared';assert 'official imagegen' in prepared.structuredContent['handoffText']
            stale=await session.call_tool('prepare_image_workflow_handoff',{'workflow_id':row['id'],'subject':'fictional','revision':'stale'});assert stale.isError
            browse=await session.call_tool('browse_image_workflows',{'domain':'graphic'});assert not browse.isError
            resources=await session.list_resources();assert len(resources.resources)==1
            resource=await session.read_resource(resources.resources[0].uri);html=resource.contents[0].text;assert 'window.ImageWorkflowEditor' in html and 'data:image' in html
            print(json.dumps({'status':'passed','manifest':manifest_path.name,'bootstrap_python':bootstrap,'runtime_python':sys.version,'tools':names,'actual_task':'search/read/prepare fictional poster request; reject stale revision; browse/read actual app resource','resource_bytes':len(html.encode()),'resource_sha256':hashlib.sha256(html.encode()).hexdigest(),'generated':False,'native_host_verified':False}))
asyncio.run(main())
