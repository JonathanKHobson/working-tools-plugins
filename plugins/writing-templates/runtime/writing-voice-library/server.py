"""Writing Voice Library MCP tools and self-contained HTML resource."""
from __future__ import annotations
import argparse
import base64
import json
import re
import sys
from pathlib import Path
from catalog import CatalogError, ROOT, DATA_ROOT, browse, handoff, load_catalog, public_item, verified_file

RESOURCE_URI = 'ui://writing-voice-library/gallery-prompt-v2.html'
RESOURCE_MIME = 'text/html;profile=mcp-app'
# Catalog IDs are currently V01–V24/P25–P48, but future entries should still
# render when they have not received artwork yet. Keep this a basename-only
# allowlist so the optional cover lookup cannot escape the UI asset directory.
_COVER_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$')

def _json_for_script(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('&','\\u0026').replace('<','\\u003c').replace('>','\\u003e').replace('\u2028','\\u2028').replace('\u2029','\\u2029')

def _cover_data_url(item_id: str) -> str:
    """Embed the Writing Library's published cover artwork in the MCP resource.

    The resource is self-contained, so the chooser does not depend on the public
    site being reachable or on relative URLs resolving from a ui:// document.
    The fixed ID allowlist also prevents catalog data from selecting arbitrary
    files during HTML generation.
    """
    if not _COVER_ID.fullmatch(item_id):
        raise CatalogError('Writing cover ID is invalid')
    path = ROOT / 'ui' / 'previews' / f'{item_id}.svg'
    if path.is_symlink() or not path.is_file():
        return ''
    raw = path.read_bytes()
    if b'<svg' not in raw[:256]:
        return ''
    return 'data:image/svg+xml;base64,' + base64.b64encode(raw).decode('ascii')

def ui_data(data_root: Path = DATA_ROOT) -> dict:
    items = []
    for record in load_catalog(data_root):
        item = public_item(record, data_root, samples=True)
        item['coverImage'] = _cover_data_url(record['id'])
        items.append(item)
    briefs_text = verified_file(data_root, 'records/briefs.md').decode('utf-8')
    briefs = [{'id':'E-B01','name':'Feature explanation · Draftline'},
              {'id':'E-B02','name':'Workshop invitation · Clearer Notes'},
              {'id':'E-B03','name':'Service incident · Draftline'}]
    if (data_root / 'records/structure-briefs.json').is_file():
        extra = json.loads(verified_file(data_root, 'records/structure-briefs.json'))
        known = {brief['id'] for brief in briefs}
        for brief in extra['briefs']:
            if brief['id'] in known:
                continue
            briefs.append({'id': brief['id'], 'name': brief['task']})
            briefs_text += ('\n\n## ' + brief['id'] + ' · fictional exercise\n\n' + brief['task']
                            + '\n\n' + '\n'.join('- ' + fact for fact in brief['facts'])
                            + '\n\nUnknowns:\n' + '\n'.join('- ' + item for item in brief['unknowns']))
    return {'schemaVersion': 1, 'owner': 'Writing Templates', 'items': items,
            'briefsText': briefs_text, 'briefs': briefs}

def render_html(data_root: Path = DATA_ROOT) -> str:
    ui = ROOT / 'ui'
    html = (ui/'index.html').read_text(encoding='utf-8')
    values = {'__LIBRARY_DATA__': _json_for_script(ui_data(data_root)), '__LIBRARY_CSS__': (ui/'styles.css').read_text(), '__LIBRARY_BRIDGE__': (ui/'bridge.js').read_text(), '__LIBRARY_JS__': (ui/'adapter.js').read_text() + '\n' + (ui/'app.js').read_text()}
    for marker, value in values.items():
        if html.count(marker) != 1:
            raise CatalogError('Gallery template marker is invalid')
        html = html.replace(marker, value, 1)
    return html

def create_server(data_root: Path = DATA_ROOT):
    from mcp.server.fastmcp import FastMCP
    from mcp.types import CallToolResult, TextContent, ToolAnnotations
    server = FastMCP('Writing Voice Library')
    from feedback import register_feedback
    register_feedback(server, 'writing')
    meta = {'ui': {'resourceUri': RESOURCE_URI}, 'openai/outputTemplate': RESOURCE_URI}
    annotations = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)
    def result(payload):
        return CallToolResult(content=[TextContent(type='text', text=payload['handoffText'])], structuredContent=payload)
    def error(exc):
        return CallToolResult(content=[TextContent(type='text',text=str(exc))], isError=True)
    @server.tool(name='browse_writing_voice_library', title='Browse Writing Voice Library', description='Open the interactive chooser only for human browsing, choosing or inspecting intentionally presented options. For AI-only retrieval use search_writing_voice_library. Browse reviewed synthetic writing examples and their actual base/module routes. Read only; profiles, candidates, modules, aliases and merges are distinct. If no useful match, use record_library_search_miss when available with sanitized evidence; reuse task/need keys across retries. Zero results do not prove missing content.', annotations=annotations, meta=meta)
    def browse_writing_voice_library(query: str = '', type: str = 'all'):
        try:
            payload = browse(query, type, data_root=data_root)
            summary = f"{len(payload['items'])} writing resources. " + '; '.join(f"{r['id']} {r['name']} ({r['resource_type']}, v{r['version']}, {r['availability']})" for r in payload['items'])
            return CallToolResult(content=[TextContent(type='text',text=summary)],structuredContent=payload)
        except CatalogError as exc:
            return error(exc)
    @server.tool(name='search_writing_voice_library', title='Search Writing Templates', description='Assistant-only structured retrieval. Use for independent AI search or selection; never opens a widget. Use browse_writing_voice_library only for intentionally presented human browsing. Optional search-miss logging remains available.', annotations=annotations)
    def search_writing_voice_library(query: str = '', type: str = 'all'):
        return browse_writing_voice_library(query, type)
    @server.tool(name='prepare_writing_voice_handoff', title='Prepare Writing Voice Handoff', description='Validate a registered writing resource, its real base/modules, versions and source hashes; prepare a portable brief-bound writing handoff. No writing, sending or publication occurs. Optional modifiers must share the base. Does not open a widget.', annotations=annotations)
    def prepare_writing_voice_handoff(profile_id: str, brief: str = '', modifier_ids: list[str] | None = None):
        try:
            return result(handoff(profile_id, brief, modifier_ids, data_root=data_root))
        except CatalogError as exc:
            return error(exc)
    @server.resource(RESOURCE_URI, name='Writing Voice Library gallery', title='Writing Voice Library gallery', description='Read actual prose, inspect routes and compare two or three resources on the same fictional brief.', mime_type=RESOURCE_MIME)
    def gallery() -> str:
        return render_html(data_root)
    return server

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Writing Voice Library MCP server and local gallery exporter')
    parser.add_argument('--export-html', type=Path, metavar='PATH')
    args = parser.parse_args(argv)
    try:
        if args.export_html:
            target = args.export_html.expanduser()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render_html(),encoding='utf-8')
            print(f'Writing Voice Library gallery exported to {target}')
        else:
            create_server().run(transport='stdio')
        return 0
    except (CatalogError, OSError) as exc:
        print(f'Writing Voice Library: {exc}',file=sys.stderr)
        return 1
if __name__ == '__main__':
    raise SystemExit(main())
