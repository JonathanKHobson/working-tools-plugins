"""Read-only MCP Design Library and self-contained local HTML export."""

from __future__ import annotations

import argparse
import base64
import json
import sys
import os
from pathlib import Path

from catalog import CatalogError, OWNER, ROOT, browse, handoff, load_catalog, source_status


RESOURCE_URI = "ui://design-library/gallery-prompt-v2.html"
RESOURCE_MIME = "text/html;profile=mcp-app"


def _json_for_script(value: object) -> str:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def _image_data_url(item_id: str, size: str, root: Path) -> str:
    path = root / "assets" / f"{item_id}-{size}.png"
    if path.is_symlink() or not path.is_file():
        raise CatalogError(f"Missing safe {size} preview for {item_id}")
    raw = path.read_bytes()
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise CatalogError(f"Invalid PNG preview for {item_id}")
    return "data:image/png;base64," + base64.b64encode(raw).decode("ascii")


def ui_data(*, root: Path = ROOT, codex_home: Path | None = None) -> dict:
    items = []
    catalog_path = Path(os.environ["DESIGN_LIBRARY_CATALOG"]) if root == ROOT and "DESIGN_LIBRARY_CATALOG" in os.environ else root / "catalog.json"
    for item in load_catalog(catalog_path):
        status, _ = source_status(item, codex_home)
        items.append({
            **{key: item[key] for key in (
                "id", "name", "summary", "category", "tags", "bestFor", "avoidWhen",
                "interactions", "limitations", "skillName", "sourceHash"
            )},
            "availability": status,
            "desktopPreview": _image_data_url(item["id"], "desktop", catalog_path.parent),
            "mobilePreview": _image_data_url(item["id"], "mobile", catalog_path.parent),
        })
    return {"schemaVersion": 1, "owner": OWNER, "items": items}


def render_html(*, root: Path = ROOT, codex_home: Path | None = None) -> str:
    ui = root / "ui"
    try:
        template = (ui / "index.html").read_text(encoding="utf-8")
        replacements = {
            "__LIBRARY_DATA__": _json_for_script(ui_data(root=root, codex_home=codex_home)),
            "__LIBRARY_CSS__": (ui / "styles.css").read_text(encoding="utf-8"),
            "__LIBRARY_BRIDGE__": (ui / "bridge.js").read_text(encoding="utf-8"),
            "__LIBRARY_JS__": (ui / "adapter.js").read_text(encoding="utf-8") + "\n" + (ui / "app.js").read_text(encoding="utf-8"),
        }
    except OSError as exc:
        raise CatalogError(f"Gallery UI file is unavailable: {exc.filename}") from exc
    for marker, value in replacements.items():
        if template.count(marker) != 1:
            raise CatalogError(f"Gallery UI must contain exactly one {marker} marker")
        template = template.replace(marker, value, 1)
    return template


def create_server():
    # Import the SDK only for MCP mode. The standalone exporter needs stdlib alone.
    from mcp.server.fastmcp import FastMCP
    from mcp.types import CallToolResult, TextContent, ToolAnnotations

    server = FastMCP("Design Library")
    from feedback import register_feedback
    register_feedback(server, 'design')
    ui_meta = {"ui": {"resourceUri": RESOURCE_URI}, "openai/outputTemplate": RESOURCE_URI}
    read_only = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)

    @server.tool(
        name="browse_design_library", title="Browse Design Library",
        description="Open the interactive chooser only for human browsing, choosing or inspecting intentionally presented options. For AI-only retrieval use search_design_library. Browse registered Site templates and their source availability. Read only. If no useful match, use record_library_search_miss when available with sanitized evidence; reuse task/need keys across retries. Zero results do not prove missing content.",
        annotations=read_only, meta=ui_meta,
    )
    def browse_design_library(query: str = "", category: str = "all"):
        result = browse(query, category)
        summary = f"{len(result['items'])} Design Library template(s): " + ", ".join(
            f"{item['name']} ({item['availability']})" for item in result["items"]
        )
        return CallToolResult(content=[TextContent(type="text", text=summary)], structuredContent=result)

    @server.tool(
        name="search_design_library", title="Search Design Library",
        description="Assistant-only structured retrieval of Design Library templates. Use for independent AI search or selection; never opens a widget. Use browse_design_library only when intentionally presenting options for a human to browse. Optional search-miss logging remains available.",
        annotations=read_only,
    )
    def search_design_library(query: str = "", category: str = "all"):
        return browse_design_library(query, category)

    @server.tool(
        name="prepare_design_handoff", title="Prepare Design Handoff",
        description="Validate a registered Site template's current source and prepare a version-bound selection without opening a widget. Read only.",
        annotations=read_only,
    )
    def prepare_design_handoff(template_id: str, brief: str = ""):
        result = handoff(template_id, brief)
        return CallToolResult(content=[TextContent(type="text", text=result["handoffText"])], structuredContent=result)

    @server.resource(
        RESOURCE_URI, name="Design Library gallery", title="Design Library gallery",
        description="Self-contained visual gallery for registered Site templates.",
        mime_type=RESOURCE_MIME,
    )
    def gallery() -> str:
        return render_html()

    return server


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Design Library MCP server and local gallery exporter")
    parser.add_argument("--export-html", metavar="PATH", type=Path, help="Write a self-contained local gallery")
    args = parser.parse_args(argv)
    try:
        if args.export_html:
            target = args.export_html.expanduser()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render_html(), encoding="utf-8")
            print(f"Design Library gallery exported to {target}")
            return 0
        create_server().run(transport="stdio")
        return 0
    except (CatalogError, OSError) as exc:
        print(f"Design Library: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
