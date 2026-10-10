"""HTML serialization and model-visible result checks."""

from __future__ import annotations

import asyncio
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from server import RESOURCE_URI, create_server, render_html  # noqa: E402
import feedback  # noqa: E402


class ServerTests(unittest.TestCase):
    def test_render_escapes_catalog_strings_inside_script(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            ui = root / "ui"
            ui.mkdir()
            (ui / "index.html").write_text(
                "<style>__LIBRARY_CSS__</style>"
                '<script type="application/json" id="library-data">__LIBRARY_DATA__</script>'
                "<script>__LIBRARY_BRIDGE__</script>"
                "<script>__LIBRARY_JS__</script>", encoding="utf-8"
            )
            for name in ("styles.css", "bridge.js", "adapter.js", "app.js"):
                (ui / name).write_text("/* self-contained */", encoding="utf-8")
            injected = '</script><script>alert("x")</script>\u2028&'
            with patch("server.ui_data", return_value={"items": [{"name": injected}]}):
                html = render_html(root=root)
            self.assertEqual(html.count("</script>"), 3)
            self.assertNotIn(injected, html)
            payload = html.split('id="library-data">', 1)[1].split("</script>", 1)[0]
            self.assertEqual(json.loads(payload)["items"][0]["name"], injected)
            self.assertNotIn("__LIBRARY_", html)

    def test_sdk_tool_result_is_compact_with_structured_data(self):
        try:
            with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {"DESIGN_LIBRARY_FEEDBACK_DB": str(Path(folder) / "feedback.sqlite")}):
                server = create_server()
        except ImportError:
            self.skipTest("MCP SDK is not installed in this Python")
        tools = asyncio.run(server.list_tools())
        by_name = {tool.name: tool for tool in tools}
        self.assertEqual(set(by_name), {"search_design_library", "browse_design_library", "prepare_design_handoff",
                                        "record_library_search_miss", "review_library_search_misses"})
        for name in ("browse_design_library",):
            tool = by_name[name]
            self.assertEqual(tool.meta["ui"]["resourceUri"], RESOURCE_URI)
            self.assertTrue(tool.annotations.readOnlyHint)
        for name in ("search_design_library", "prepare_design_handoff"):
            self.assertFalse(by_name[name].meta)
        self.assertFalse(by_name["record_library_search_miss"].annotations.readOnlyHint)
        self.assertFalse(by_name["record_library_search_miss"].annotations.destructiveHint)
        self.assertTrue(by_name["review_library_search_misses"].annotations.readOnlyHint)
        result = asyncio.run(server.call_tool("browse_design_library", {}))
        self.assertFalse(result.isError)
        catalog = json.loads((Path(__file__).resolve().parents[1] / "catalog.json").read_text(encoding="utf-8"))
        expected_ids = [item["id"] for item in catalog["items"]]
        self.assertEqual([item["id"] for item in result.structuredContent["items"]], expected_ids)
        self.assertNotIn("data:image", result.content[0].text)
        self.assertNotIn("desktopPreview", str(result.structuredContent))

    def test_missing_optional_feedback_binding_keeps_search_usable(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(feedback.Path, "home", return_value=Path(folder)):
                server = create_server()
            tools = asyncio.run(server.list_tools())
            self.assertEqual({tool.name for tool in tools},
                             {"search_design_library", "browse_design_library", "prepare_design_handoff"})
            result = asyncio.run(server.call_tool("browse_design_library", {}))
            self.assertFalse(result.isError)
            self.assertEqual(result.structuredContent["items"], [])


if __name__ == "__main__":
    unittest.main()
