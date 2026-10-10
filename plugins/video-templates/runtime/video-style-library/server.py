"""Read-only Video Style Library MCP App and local gallery exporter."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
from pathlib import Path

from catalog import library_handoff, library_item, library_items, library_search
from storyboards import StoryboardError, StoryboardStore, draw_payload, _revision
from storyboard_media import reference_image, render_sketch

ROOT = Path(__file__).resolve().parents[2]
# Bundled pinned projection of the canonical Design Templates chooser.
SHARED_UI = Path(os.environ.get("VIDEO_TEMPLATES_CHOOSER", ROOT / "runtime/library-chooser"))
URI = "ui://video-production-studio/style-library-v1.html"
STORYBOARD_URI = "ui://video-production-studio/storyboard-v2.html"


def _script_json(value: object) -> str:
    return (json.dumps(value, ensure_ascii=False, separators=(",", ":"))
            .replace("&", "\\u0026").replace("<", "\\u003c")
            .replace(">", "\\u003e").replace("\u2028", "\\u2028")
            .replace("\u2029", "\\u2029"))


def _redact_references(board: dict) -> dict:
    """Keep media provenance in AI text without transporting image bytes."""
    for shot in board["shots"]:
        if "reference" in shot:
            ref = shot["reference"]
            mime, encoded = reference_image(ref)
            raw = base64.b64decode(encoded)
            shot["reference"] = {"name": ref.get("name", ""), "description": ref.get("description", ""),
                                 "mime_type": "image/" + mime, "bytes": len(raw),
                                 "sha256": hashlib.sha256(raw).hexdigest()}
    return board


def render_html(shared_ui: Path = SHARED_UI) -> str:
    """Use UX Design Studio's single maintained chooser and bridge, plus Video adapter."""
    own_ui = Path(__file__).resolve().parent / "ui"
    replacements = {
        "__LIBRARY_DATA__": _script_json({"schemaVersion": 2,
                                          "items": library_items(preview=True)}),
        "__LIBRARY_CSS__": (shared_ui / "styles.css").read_text(encoding="utf-8") + "\n" +
                           (own_ui / "video.css").read_text(encoding="utf-8"),
        "__LIBRARY_BRIDGE__": (shared_ui / "bridge.js").read_text(encoding="utf-8"),
        "__LIBRARY_JS__": (own_ui / "adapter.js").read_text(encoding="utf-8") + "\n" +
                          (shared_ui / "app.js").read_text(encoding="utf-8"),
    }
    html = (shared_ui / "index.html").read_text(encoding="utf-8")
    for marker, value in replacements.items():
        if html.count(marker) != 1:
            raise ValueError(f"Shared library chooser marker mismatch: {marker}")
        html = html.replace(marker, value, 1)
    return html


def render_storyboard_html(shared_ui: Path = SHARED_UI) -> str:
    own_ui = Path(__file__).resolve().parent / "ui"
    html = (own_ui / "storyboard.html").read_text(encoding="utf-8")
    replacements = {
        "__STORYBOARD_CSS__": (own_ui / "storyboard.css").read_text(encoding="utf-8"),
        "__LIBRARY_BRIDGE__": (shared_ui / "bridge.js").read_text(encoding="utf-8"),
        "__STORYBOARD_MEDIA_JS__": (own_ui / "storyboard-media.js").read_text(encoding="utf-8"),
        "__STORYBOARD_JS__": (own_ui / "storyboard.js").read_text(encoding="utf-8"),
    }
    for marker, value in replacements.items():
        if html.count(marker) != 1:
            raise ValueError(f"Storyboard template marker mismatch: {marker}")
        html = html.replace(marker, value, 1)
    return html


def create_server(storyboard_db: Path | None = None):
    from mcp.server.fastmcp import FastMCP
    from mcp.types import CallToolResult, TextContent, ImageContent, ToolAnnotations

    server = FastMCP("Video Style Library")
    def board_store(*, create: bool = False):
        return StoryboardStore(storyboard_db, create=create) if storyboard_db is not None else StoryboardStore(create=create)
    readonly = ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                               idempotentHint=True, openWorldHint=False)
    ui_meta = {"ui": {"resourceUri": URI}, "openai/outputTemplate": URI}
    storyboard_meta = {"ui": {"resourceUri": STORYBOARD_URI}, "openai/outputTemplate": STORYBOARD_URI}
    app_write_meta = {"ui": {"visibility": ["app", "model"]}, "openai/widgetAccessible": True}
    write = ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False, openWorldHint=False)

    def storyboard_result(action):
        try:
            data = action()
            summary = ({"storyboard_id": data["storyboard_id"], "title": data["title"],
                        "revision": data["revision"], "shot_count": len(data["shots"])}
                       if "storyboard_id" in data and "shots" in data else data)
            return CallToolResult(content=[TextContent(type="text", text=json.dumps(summary, ensure_ascii=False))],
                                  structuredContent=data)
        except StoryboardError as exc:
            data = {"error": {"code": exc.code, "message": str(exc)}}
            if exc.current is not None:
                data["current"] = exc.current
            return CallToolResult(content=[TextContent(type="text", text=f"{exc.code}: {exc}")],
                                  structuredContent=data, isError=True)

    @server.tool(name="search_video_styles", title="Search video styles",
                 description="Assistant-only read-only search of public Video Library families and seven distinct staged reference methods. Returns example identities, source hashes, review and availability. Does not open a widget. Use browse_video_styles for visual browsing.",
                 annotations=readonly)
    def search_video_styles(query: str = "", limit: int = 50):
        data = library_search(query, limit)
        return CallToolResult(content=[TextContent(type="text", text=json.dumps(data, ensure_ascii=False))],
                              structuredContent=data)

    @server.tool(name="read_video_style", title="Read video style",
                 description="Read one exact Video Library family ID (family/<id>) or staged method ID (method/<id> or legacy bare ID). Methods include pinned STYLE.md rules and hash. Read only; no widget.", annotations=readonly)
    def read_video_style(style_id: str):
        data = library_item(style_id, full=True)
        return CallToolResult(content=[TextContent(type="text", text=json.dumps(data, ensure_ascii=False))],
                              structuredContent=data)

    @server.tool(name="browse_video_styles", title="Browse video styles",
                 description="Open the visual Video Library with public film families, selectable examples and seven distinct staged reference methods. For assistant-only retrieval use search_video_styles.",
                 annotations=readonly, meta=ui_meta)
    def browse_video_styles(query: str = ""):
        data = library_search(query)
        return CallToolResult(content=[TextContent(type="text", text=f"{data['total']} video style(s): " + ", ".join(x["name"] for x in data["items"]))],
                              structuredContent=data)

    @server.tool(name="prepare_video_style_handoff", title="Prepare video style handoff",
                 description="Validate an exact selected family example master hash or pinned staged method source hash and prepare a source-bound video/storyboard prompt. Read only; does not create or open a board.",
                 annotations=readonly)
    def prepare_video_style_handoff(style_id: str, source_hash: str, brief: str = "", example_id: str = ""):
        data = library_handoff(style_id, source_hash, brief, example_id)
        return CallToolResult(content=[TextContent(type="text", text=data["handoffText"])],
                              structuredContent=data)

    @server.resource(URI, name="Video style gallery", title="Video style gallery",
                     description="Video Library chooser with public family examples and staged reference methods.",
                     mime_type="text/html;profile=mcp-app",
                     meta={"ui": {"csp": {"connectDomains": ["https://activity-atlas.jkylehobson.chatgpt.site"],
                                           "resourceDomains": ["https://activity-atlas.jkylehobson.chatgpt.site"],
                                           "frameDomains": []}}})
    def gallery() -> str:
        return render_html()

    @server.tool(name="create_video_storyboard", title="Create video storyboard",
                 description="Create a private Video Studio storyboard of ordered shot cards. Each shot needs id, visual, duration_seconds, narration; optional sketch={strokes:[{points:[[x,y],...]}]} uses normalized coordinates with max 64 strokes and 512 points each. Optional reference={data_url,name?,description?} accepts base64 PNG/JPEG/WebP up to 1 MiB decoded; entire board max 8 MiB; use a unique operation_id and repeat that same ID only for the identical retry. Creating does not create a Draw and Think board.",
                 annotations=write)
    def create_video_storyboard(title: str, shots: list[dict], operation_id: str):
        return storyboard_result(lambda: board_store(create=True).create(title, shots, operation_id))

    @server.tool(name="read_video_storyboard", title="Read video storyboard",
                 description="Read exact storyboard shots and revision without opening a widget. Reference images default to metadata only; include_media=true returns complete data URLs for app hydration. Use patch_video_storyboard for assistant changes so metadata reads cannot overwrite images. Use read_video_storyboard_media for actual visual inspection.",
                 annotations=readonly)
    def read_video_storyboard(storyboard_id: str, include_media: bool = False):
        def read():
            board = board_store().read(storyboard_id)
            if not include_media:
                _redact_references(board)
                board["media_included"] = False
            return board
        return storyboard_result(read)

    @server.tool(name="open_video_storyboard", title="Open video storyboard",
                 description="Open the dedicated shot-card storyboard widget for human editing. Omit ID for a new unsaved three-shot scaffold; existing IDs load the saved revision. Does not open Draw and Think.",
                 annotations=readonly, meta=storyboard_meta)
    def open_video_storyboard(storyboard_id: str = ""):
        if storyboard_id:
            return storyboard_result(lambda: board_store().read(storyboard_id))
        draft = {"storyboard_id": "", "title": "Untitled storyboard", "revision": 0,
                 "shots": [{"id": name.lower(), "visual": "", "duration_seconds": 5, "narration": ""}
                           for name in ("Opening", "Development", "Resolution")],
                 "state": "unsaved scaffold; durations are provisional"}
        return CallToolResult(content=[TextContent(type="text", text="New unsaved three-shot storyboard scaffold. Five-second durations are provisional.")],
                              structuredContent=draft)

    @server.tool(name="save_video_storyboard", title="Save video storyboard",
                 description="Assistant and widget revisioned save of the whole ordered shot list; preserve optional sketch/reference fields when editing. Use a unique operation ID per intended change; retry the identical request with the same ID.",
                 annotations=write, meta=app_write_meta)
    def save_video_storyboard(storyboard_id: str, expected_revision: int,
                              operation_id: str, title: str, shots: list[dict]):
        return storyboard_result(lambda: board_store().save(storyboard_id, expected_revision, operation_id, title, shots))

    @server.tool(name="patch_video_storyboard", title="Patch video storyboard",
                 description="Assistant and app bounded revisioned edits by stable shot ID. operations (1–40) use {op:update,shot_id,changes:{visual/duration_seconds/narration/sketch/reference}}, {op:add,shot,after_shot_id?:id|null} (omitted appends, null first), {op:remove,shot_id}, {op:reorder,shot_ids:[every ID exactly once]}, {op:title,title}. Null sketch/reference changes remove media. Preserve other shot fields. Retry only identical operations with the same operation_id; stale expected_revision returns current board. Inspect images with read_video_storyboard_media before visual claims.",
                 annotations=write, meta=app_write_meta)
    def patch_video_storyboard(storyboard_id: str, expected_revision: int,
                               operation_id: str, operations: list[dict]):
        return storyboard_result(lambda: board_store().patch(storyboard_id, expected_revision, operation_id, operations))

    @server.tool(name="read_video_storyboard_media", title="View storyboard shot media",
                 description="Read one exact shot at expected_revision and return its attached reference image and rendered sketch as actual image content for visual inspection. Offline; no remote retrieval. Text descriptions alone do not establish visual inspection.",
                 annotations=readonly)
    def read_video_storyboard_media(storyboard_id: str, shot_id: str, expected_revision: int):
        def read_media():
            _revision(expected_revision)
            board = board_store().read(storyboard_id)
            if board["revision"] != expected_revision:
                raise StoryboardError("revision_conflict", "Storyboard changed; reload before media inspection", board)
            shot = next((shot for shot in board["shots"] if shot["id"] == shot_id), None)
            if shot is None:
                raise StoryboardError("not_found", "Shot was not found")
            data = {"storyboard_id": storyboard_id, "shot_id": shot_id, "revision": expected_revision,
                    "has_reference": "reference" in shot, "has_sketch": "sketch" in shot}
            content = [TextContent(type="text", text=json.dumps(data))]
            if "reference" in shot:
                ref = shot["reference"]
                mime, encoded = reference_image(ref)
                content.extend([TextContent(type="text", text="Shot reference image: " + ref.get("name", "") + "\n" + ref.get("description", "")),
                                ImageContent(type="image", data=encoded, mimeType="image/" + mime)])
            if "sketch" in shot:
                content.extend([TextContent(type="text", text="Shot sketch rendered on a 16:9 white canvas."),
                                ImageContent(type="image", data=render_sketch(shot["sketch"]), mimeType="image/png")])
            return CallToolResult(content=content, structuredContent=data)
        try:
            return read_media()
        except StoryboardError as exc:
            return storyboard_result(lambda: (_ for _ in ()).throw(exc))

    @server.tool(name="prepare_video_storyboard_draw_handoff", title="Prepare Draw and Think storyboard handoff",
                 description="Read and revision-check an exact saved Video storyboard; return editable Draw and Think elements and a handoff prompt. Read only. Does not create/open a drawing board.",
                 annotations=readonly)
    def prepare_video_storyboard_draw_handoff(storyboard_id: str, expected_revision: int):
        def prepare():
            board = board_store().read(storyboard_id)
            if board["revision"] != expected_revision:
                raise StoryboardError("revision_conflict", "Storyboard changed; reload before handoff", board)
            draw = draw_payload(board)
            _redact_references(board)
            prompt = ("Create a new Draw and Think board from this saved Video Studio storyboard. "
                      "Call draw_create_board with the title and elements below, then draw_open_board with "
                      "the returned board_id. Verify the created board and keep the source storyboard ID/revision "
                      "in the production notes. Board notes are concise; full visual and narration text is in "
                      "the source shots below. Reference images and sketches remain in the source Video storyboard and are not transferred to Draw and Think. Inspect them using read_video_storyboard_media at this exact revision. Do not overwrite an existing board.\n\n" +
                      "Draw board payload:\n" + json.dumps(draw, ensure_ascii=False, indent=2) +
                      "\n\nFull source shots:\n" + json.dumps(board["shots"], ensure_ascii=False, indent=2))
            return {"storyboardId": storyboard_id, "revision": expected_revision,
                    "drawPayload": draw, "handoffText": prompt}
        return storyboard_result(prepare)

    @server.resource(STORYBOARD_URI, name="Video storyboard editor", title="Video storyboard editor",
                     description="Private ordered shot-card editor with Draw and Think handoff.",
                     mime_type="text/html;profile=mcp-app",
                     meta={"ui": {"csp": {"connectDomains": [], "resourceDomains": [], "frameDomains": []}}})
    def storyboard_resource() -> str:
        return render_storyboard_html()

    return server


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export-html", type=Path)
    parser.add_argument("--export-storyboard-html", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.export_html or args.export_storyboard_html:
            target = (args.export_html or args.export_storyboard_html).expanduser().resolve()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render_html() if args.export_html else render_storyboard_html(), encoding="utf-8")
            print(target)
        else:
            create_server().run(transport="stdio")
        return 0
    except (OSError, ValueError) as exc:
        print(f"Video Style Library: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
