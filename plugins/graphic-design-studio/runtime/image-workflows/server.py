"""Local Image Workflow MCP App and standalone chooser exporter."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path

from catalog import catalog, handoff, item, search

def shared_ui_path() -> Path:
    declared = os.environ.get("DESIGN_TEMPLATES_ROOT")
    owners = ([Path(declared).expanduser().absolute()] if declared else [
        Path(__file__).resolve().parents[3] / "design-templates",
        Path.home() / "plugins/ux-design-toolkit",
    ])
    for owner in owners:
        shared = owner / "runtime/library-chooser"
        if all((shared / name).is_file() for name in ("index.html", "styles.css", "bridge.js", "app.js")):
            return shared
    raise ValueError("Install design-templates or set DESIGN_TEMPLATES_ROOT to its package root; see docs/installation.md")
URI = "ui://graphic-design-studio/image-workflows-v2.html"


def _script_json(value: object) -> str:
    return (json.dumps(value, ensure_ascii=False, separators=(",", ":"))
            .replace("&", "\\u0026").replace("<", "\\u003c")
            .replace(">", "\\u003e").replace("\u2028", "\\u2028")
            .replace("\u2029", "\\u2029"))


def render_html(shared_ui: Path | None = None) -> str:
    """Read the maintained chooser and bridge at render time; inject only this domain's editor."""
    shared_ui = shared_ui or shared_ui_path()
    own_ui = Path(__file__).resolve().parent / "ui"
    data = catalog()
    # Only catalog-authored basenames inside this fixed directory can become previews.
    # No request field can select a file.
    for row in data["items"]:
        filename = row.get("previewAsset")
        if not filename:
            continue
        path = own_ui / "previews" / filename
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Preview missing: {filename}")
        raw = path.read_bytes()
        if len(raw) > 2_000_000:
            raise ValueError(f"Preview exceeds 2 MB: {filename}")
        mime = "image/png" if filename.endswith(".png") else "image/jpeg"
        if not raw.startswith(b"\x89PNG\r\n\x1a\n" if mime == "image/png" else b"\xff\xd8"):
            raise ValueError(f"Invalid preview image: {filename}")
        row["preview"] = "data:" + mime + ";base64," + base64.b64encode(raw).decode("ascii")
    replacements = {
        "__LIBRARY_DATA__": _script_json(data),
        "__LIBRARY_CSS__": (shared_ui / "styles.css").read_text(encoding="utf-8") + "\n" +
                           (own_ui / "editor.css").read_text(encoding="utf-8"),
        "__LIBRARY_BRIDGE__": (shared_ui / "bridge.js").read_text(encoding="utf-8"),
        "__LIBRARY_JS__": (own_ui / "editor.js").read_text(encoding="utf-8") + "\n" +
                          (own_ui / "adapter.js").read_text(encoding="utf-8") + "\n" +
                          (shared_ui / "app.js").read_text(encoding="utf-8"),
    }
    html = (shared_ui / "index.html").read_text(encoding="utf-8")
    for marker, value in replacements.items():
        if html.count(marker) != 1:
            raise ValueError(f"Shared library chooser marker mismatch: {marker}")
        html = html.replace(marker, value, 1)
    return html


def create_server():
    from mcp.server.fastmcp import FastMCP
    from mcp.types import CallToolResult, TextContent, ToolAnnotations

    server = FastMCP("Image Gen Templates")
    readonly = ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                               idempotentHint=True, openWorldHint=False)
    ui_meta = {"ui": {"resourceUri": URI}, "openai/outputTemplate": URI}

    def result(data: dict, *, text: str | None = None):
        return CallToolResult(content=[TextContent(type="text", text=text or json.dumps(data, ensure_ascii=False))],
                              structuredContent=data)

    @server.tool(name="search_image_workflows", title="Search image templates",
                 description="Assistant-only search of the local image recipe catalog. Structured data; does not open a widget. Use browse_image_workflows when the person wants to choose visually.", annotations=readonly)
    def search_image_workflows(query: str = "", domain: str = "all", limit: int = 30):
        return result(search(query, domain, limit))

    @server.tool(name="read_image_workflow", title="Read image template",
                 description="Read one exact local image workflow ID and its current catalog revision. Does not open a widget.", annotations=readonly)
    def read_image_workflow(workflow_id: str):
        return result(item(workflow_id))

    @server.tool(name="browse_image_workflows", title="Browse image templates",
                 description="Open the image recipe chooser for deliberate browsing. Filter by graphic, ux, creative, or video domain and optional search query.",
                 annotations=readonly, meta=ui_meta)
    def browse_image_workflows(query: str = "", domain: str = "all"):
        data = search(query, domain)
        return result(data, text=f"{data['total']} image template(s) found for {domain}: " +
                      ", ".join(row["name"] for row in data["items"]))

    @server.tool(name="prepare_image_workflow_handoff", title="Prepare image template request",
                 description="Validate a selected workflow and prepare a generation request for the assistant. Does not generate, edit, upload, or save an image.", annotations=readonly)
    def prepare_image_workflow_handoff(workflow_id: str, subject: str, aspect_ratio: str = "Auto",
                                       detail: str = "Balanced", reference_notes: str = "",
                                       background: str = "Scene", prompt_override: str = "",
                                       additional_instructions: str = "", revision: str = ""):
        data = handoff(workflow_id, subject, aspect_ratio, detail, reference_notes,
                       background, prompt_override, additional_instructions, revision)
        return result(data, text=data["handoffText"])

    @server.resource(URI, name="Image Gen Templates", title="Image Gen Templates",
                     description="Local image recipe chooser with an editable generation brief.",
                     mime_type="text/html;profile=mcp-app",
                     meta={"ui": {"csp": {"connectDomains": [], "resourceDomains": [], "frameDomains": []}}})
    def gallery() -> str:
        return render_html()

    return server


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export-html", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.export_html:
            target = args.export_html.expanduser().resolve()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render_html(), encoding="utf-8")
            print(target)
        else:
            create_server().run(transport="stdio")
        return 0
    except (OSError, ValueError) as exc:
        print(f"Image Gen Templates: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
