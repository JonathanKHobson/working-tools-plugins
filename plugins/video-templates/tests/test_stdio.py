"""Actual stdio acceptance from a relocated package and an empty private home.

Run directly using an MCP-equipped Python. The synthetic board lives only in a
TemporaryDirectory; this test never reads or writes the user's live board DB.
"""
import asyncio
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]
TOOLS = {'search_video_styles', 'read_video_style', 'browse_video_styles',
         'prepare_video_style_handoff', 'create_video_storyboard',
         'read_video_storyboard', 'open_video_storyboard', 'save_video_storyboard',
         'patch_video_storyboard', 'read_video_storyboard_media',
         'prepare_video_storyboard_draw_handoff'}
URIS = {'ui://video-production-studio/style-library-v1.html',
        'ui://video-production-studio/storyboard-v2.html'}


async def verify():
    with tempfile.TemporaryDirectory(prefix='video-template-portability-') as temp:
        base = Path(temp)
        package = base / 'video-templates'
        shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns('__pycache__', '.pytest_cache', '*.pyc'))
        private_home = base / 'fresh-home'
        private_home.mkdir()
        db = private_home / 'boards.sqlite3'
        env = dict(os.environ, HOME=str(private_home), PYTHONDONTWRITEBYTECODE='1',
                   VIDEO_TEMPLATES_PYTHON=sys.executable, VIDEO_STORYBOARD_DB=str(db))
        for key in ('VIDEO_TEMPLATES_BINDINGS', 'VIDEO_LIBRARY_CATALOG', 'VIDEO_TEMPLATES_CHOOSER'):
            env.pop(key, None)
        bootstrap = os.environ.get("VIDEO_TEMPLATES_BOOTSTRAP_PYTHON", sys.executable)
        params = StdioServerParameters(command=bootstrap,
            args=[str(package / 'scripts/video_style_library_mcp.py')], env=env, cwd=str(private_home))
        async with stdio_client(params) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                initialized = await session.initialize()
                assert initialized.serverInfo.name == 'Video Style Library'
                listed = await session.list_tools()
                assert {t.name for t in listed.tools} == TOOLS
                resources = await session.list_resources()
                assert {str(r.uri) for r in resources.resources} == URIS
                for uri in URIS:
                    result = await session.read_resource(uri)
                    assert len(result.contents) == 1
                    assert result.contents[0].mimeType == 'text/html;profile=mcp-app'
                    assert '__LIBRARY_' not in result.contents[0].text
                result = await session.call_tool('search_video_styles', {})
                assert not result.isError
                data = result.structuredContent
                assert data['familyCount'] == 30 and data['methodCount'] == 7 and data['total'] == 37
                assert sum(r.get('exampleCount', 0) for r in data['items']) == 38
                family = next(r for r in data['items'] if r['kind'] == 'video-family')
                example = family['examples'][0]
                args = {'style_id': family['id'], 'source_hash': example['masterSha256'],
                        'example_id': example['id'], 'brief': 'Explain one process.'}
                selected = await session.call_tool('prepare_video_style_handoff', args)
                assert not selected.isError and selected.structuredContent['exampleId'] == example['id']
                assert selected.structuredContent['sourceHash'] == example['masterSha256']
                assert 'draw_create_board' in selected.structuredContent['handoffText']
                stale = await session.call_tool('prepare_video_style_handoff', {**args, 'source_hash': 'stale'})
                assert stale.isError
                methods = next(r for r in data['items'] if r['kind'] == 'staged-method')
                handoff = await session.call_tool('prepare_video_style_handoff', {'style_id': methods['id'], 'source_hash': methods['sourceHash']})
                assert not handoff.isError
                scaffold = await session.call_tool('open_video_storyboard', {})
                assert scaffold.structuredContent['revision'] == 0 and not db.exists()
                shots = [{'id':'opening','visual':'A book opens','duration_seconds':3.5,'narration':'Start here.',
                          'sketch':{'strokes':[{'points':[[0.2,0.2],[0.7,0.7]]}]}}]
                created = await session.call_tool('create_video_storyboard', {'title':'Synthetic portability test','shots':shots,'operation_id':'create-one'})
                assert not created.isError and created.structuredContent['revision'] == 1
                sid = created.structuredContent['storyboard_id']
                args_patch = {'storyboard_id':sid,'expected_revision':1,'operation_id':'patch-one',
                              'operations':[{'op':'update','shot_id':'opening','changes':{'visual':'The book closes'}}]}
                patched = await session.call_tool('patch_video_storyboard', args_patch)
                assert patched.structuredContent['revision'] == 2
                retry = await session.call_tool('patch_video_storyboard', args_patch)
                assert retry.structuredContent == patched.structuredContent
                conflict = await session.call_tool('patch_video_storyboard', {**args_patch,'operation_id':'stale-patch'})
                assert conflict.isError and conflict.structuredContent['error']['code'] == 'revision_conflict'
                readback = await session.call_tool('read_video_storyboard', {'storyboard_id':sid})
                assert readback.structuredContent['shots'][0]['visual'] == 'The book closes'
                assert readback.structuredContent['shots'][0]['sketch'] == shots[0]['sketch']
                media = await session.call_tool('read_video_storyboard_media', {'storyboard_id':sid,'shot_id':'opening','expected_revision':2})
                assert any(c.type == 'image' for c in media.content)
                drawing = await session.call_tool('prepare_video_storyboard_draw_handoff', {'storyboard_id':sid,'expected_revision':2})
                assert drawing.structuredContent['revision'] == 2
                assert drawing.structuredContent['drawPayload']['sourceStoryboardId'] == sid
                assert db.is_file() and not list(package.rglob('*.sqlite3'))
        return {'transport':'stdio', 'relocatedPackage':True, 'freshHome':True, 'bootstrapInterpreter':bootstrap,
                'tools':sorted(TOOLS), 'resources':sorted(URIS), 'families':30, 'examples':38,
                'methods':7, 'familyMethodHandoff':'passed', 'staleHashRejected':True,
                'storyboardRevisionRetryConflictMediaDraw':'passed', 'privateStateExternal':True}


if __name__ == '__main__':
    print(json.dumps(asyncio.run(verify()), indent=2))
