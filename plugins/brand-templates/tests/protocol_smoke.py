"""Run with an existing Python that has MCP installed; launches a fresh server."""
import asyncio,json,sys,tempfile
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
ROOT=Path(__file__).resolve().parents[1]

async def main():
    home=tempfile.TemporaryDirectory()
    params=StdioServerParameters(command=sys.executable,args=[str(ROOT/'scripts/brand_library_mcp.py')],env={'HOME':home.name,'BRAND_TEMPLATES_PYTHON':sys.executable,'PYTHONDONTWRITEBYTECODE':'1'})
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            init=await session.initialize()
            tools={t.name:t for t in (await session.list_tools()).tools}
            assert set(tools)=={'browse_brand_library','search_brand_library','prepare_brand_handoff'}
            assert not tools['search_brand_library'].meta
            assert tools['browse_brand_library'].meta['ui']['resourceUri']=='ui://brand-library/gallery-prompt-v2.html'
            result=await session.call_tool('search_brand_library',{'query':'Pattern Practice'})
            assert not result.isError and result.structuredContent['total']==1
            item=result.structuredContent['items'][0]
            prepared=await session.call_tool('prepare_brand_handoff',{'brand_id':item['id'],'brief':'A teaching card'})
            assert not prepared.isError and prepared.structuredContent['verifiedFiles']>20
            bad=await session.call_tool('prepare_brand_handoff',{'brand_id':'../secret'})
            assert bad.isError
            resources=await session.list_resources()
            resource=await session.read_resource(resources.resources[0].uri)
            assert 'Brand Templates' in resource.contents[0].text
            print(json.dumps({'protocol':init.protocolVersion,'tools':list(tools),'searchItems':result.structuredContent['total'],'handoffFiles':prepared.structuredContent['verifiedFiles'],'resourceBytes':len(resource.contents[0].text.encode()),'nativeHostVerified':False,'freshHome':True}))

    home.cleanup()

asyncio.run(main())
