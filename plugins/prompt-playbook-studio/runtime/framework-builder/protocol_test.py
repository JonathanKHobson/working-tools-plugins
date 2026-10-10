"""Fresh stdio server test. This does not refresh the running Codex connection."""
import asyncio
import hashlib
import json
from pathlib import Path
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent


async def main():
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / 'server.py')], env={'PYTHONDONTWRITEBYTECODE': '1'})
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            initialized = await session.initialize()
            tools = {t.name: t for t in (await session.list_tools()).tools}
            assert set(tools) == {'search_prompt_frameworks', 'read_prompt_framework', 'browse_prompt_frameworks',
                                  'read_framework_preferences', 'save_framework_preferences', 'prepare_framework_prompt'}
            assert not tools['search_prompt_frameworks'].meta
            assert not tools['read_prompt_framework'].meta
            for name in ('read_framework_preferences', 'save_framework_preferences'):
                assert tools[name].meta['ui']['visibility'] == ['app']
            uri = tools['browse_prompt_frameworks'].meta['ui']['resourceUri']
            assert tools['prepare_framework_prompt'].meta['ui']['resourceUri'] == uri
            found = await session.call_tool('search_prompt_frameworks', {'query': 'clear path'})
            assert not found.isError and found.structuredContent['total'] >= 1
            selected = found.structuredContent['items'][0]
            detail = await session.call_tool('read_prompt_framework', {'framework_id': selected['id']})
            assert not detail.isError and detail.structuredContent['item']['fields']
            invalid = await session.call_tool('read_prompt_framework', {'framework_id': '../../unknown'})
            assert invalid.isError
            browse = await session.call_tool('browse_prompt_frameworks', {'query': 'clear path'})
            assert not browse.isError and browse.structuredContent['query'] == 'clear path'
            prepared = await session.call_tool('prepare_framework_prompt', {
                'framework_id': 'clear-prompting-method',
                'field_values': {'clarity': 'Explain a course choice', 'ctx': 'Adult learners'},
                'additional_instructions': 'Use plain language.',
                'rationale': 'This framework fits the requested communication task.',
            })
            assert not prepared.isError
            prefill = prepared.structuredContent['prefill']
            assert prefill['frameworkId'] == 'clear-prompting-method'
            assert prefill['values'] == {'clarity': 'Explain a course choice', 'ctx': 'Adult learners'}
            assert prefill['additionalInstructions'] == 'Use plain language.'
            assert prefill['rationale'].startswith('This framework fits')
            assert isinstance(prefill['id'], str) and prefill['id']
            bad_prefill = await session.call_tool('prepare_framework_prompt', {
                'framework_id': 'clear-prompting-method', 'field_values': {'unknown': 'value'},
            })
            assert bad_prefill.isError
            resource = await session.read_resource(uri)
            html = resource.contents[0].text
            assert 'PromptAssembly' in html and 'FrameworkBuilderEditor' in html and 'FrameworkAdditions' in html
            assert '__LIBRARY_' not in html
            receipt = {'scope': 'fresh-subprocess MCP, not native host', 'protocol': initialized.protocolVersion,
                       'tools': list(tools), 'resource': uri, 'resource_bytes': len(html.encode()),
                       'resource_sha256': hashlib.sha256(html.encode()).hexdigest(), 'passed': True}
            (ROOT / 'qa').mkdir(exist_ok=True)
            (ROOT / 'qa/protocol-receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
            print(json.dumps(receipt))


asyncio.run(main())
