"""Real stock-bootstrap MCP execution against explicit authored external data."""
import asyncio
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sample", ROOT / "scripts/create_sample_collection.py")
sample = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sample)

async def verify():
    with tempfile.TemporaryDirectory(prefix="design-public-runtime-") as folder:
        external = Path(folder)
        fixture = sample.create(external / "collection")
        env = {**os.environ, "DESIGN_LIBRARY_PYTHON": sys.executable,
            "DESIGN_LIBRARY_CATALOG": fixture["DESIGN_LIBRARY_CATALOG"],
            "DESIGN_TEMPLATES_DATA_ROOT": fixture["DESIGN_TEMPLATES_DATA_ROOT"],
            "DESIGN_LIBRARY_FEEDBACK_DB": str(external / "feedback.sqlite"),
            "PYTHONDONTWRITEBYTECODE": "1"}
        bootstrap = os.environ.get("DESIGN_BOOTSTRAP_PYTHON", sys.executable)
        params = StdioServerParameters(command=bootstrap,
            args=[str(ROOT / "scripts/design_library_mcp.py")], env=env, cwd=str(external))
        async with stdio_client(params) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                await session.initialize()
                tools = await session.list_tools()
                expected = {"search_design_library", "browse_design_library", "prepare_design_handoff",
                    "record_library_search_miss", "review_library_search_misses"}
                assert {tool.name for tool in tools.tools} == expected
                result = await session.call_tool("search_design_library", {"query": "synthetic"})
                assert not result.isError and result.structuredContent["items"][0]["availability"] == "ready"
                selected = await session.call_tool("prepare_design_handoff", {"template_id": "synthetic-example", "brief": "Preserve the synthetic limitation."})
                assert not selected.isError
                assert selected.structuredContent["sourceHash"] == fixture["item"]["sourceHash"]
                assert len(selected.structuredContent["guidanceRefs"]) == 3
                resources = await session.list_resources()
                assert [str(resource.uri) for resource in resources.resources] == ["ui://design-library/gallery-prompt-v2.html"]
                result = await session.read_resource("ui://design-library/gallery-prompt-v2.html")
                html = result.contents[0].text
                assert "__LIBRARY_" not in html and "Synthetic source-integrity example" in html
                if target := os.environ.get("DESIGN_PUBLIC_FIXTURE_HTML"):
                    Path(target).write_text(html)
                source = external / "collection/templates/artifact-template-studio-synthetic-example/assets/source/index.html"
                original = source.read_bytes()
                source.write_text("Changed fixture source")
                rejected = await session.call_tool("prepare_design_handoff", {"template_id": "synthetic-example"})
                assert rejected.isError
                source.write_bytes(original)
                assert not (external / "feedback.sqlite").exists()
                return {"transport": "stdio", "bootstrap": bootstrap, "tools": sorted(expected), "resources": 1,
                    "external_synthetic_source": True, "ready_search": True, "source_and_guidance_handoff": True,
                    "changed_source_rejected": True, "real_resource_html": True, "private_feedback_untouched": True}

if __name__ == "__main__":
    print(json.dumps(asyncio.run(verify()), indent=2))
