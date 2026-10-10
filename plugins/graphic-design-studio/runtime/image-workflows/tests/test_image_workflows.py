"""Image workflow catalog and resource contract tests."""

import sys
import asyncio
import json
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from catalog import RATIOS, catalog, handoff, item, search
from server import URI, create_server, render_html


class ImageWorkflowTests(unittest.TestCase):
    def test_catalog_ids_and_domain_filter(self):
        data = catalog()
        self.assertEqual(data["schemaVersion"], 1)
        self.assertEqual(len(data["items"]), 16)
        self.assertEqual(len({row["id"] for row in data["items"]}), 16)
        for row in data["items"]:
            self.assertEqual(item(row["id"])["item"], row)
        filtered = search(domain="video")
        self.assertTrue(filtered["items"])
        self.assertTrue(all("video" in row["domains"] for row in filtered["items"]))
        self.assertEqual(search(query="impossible-workflow-999")["total"], 0)

    def test_exact_id_revision_and_bounds(self):
        selected = catalog()["items"][0]
        with self.assertRaises(ValueError):
            item("../catalog.json")
        with self.assertRaises(ValueError):
            search(domain="../../graphic")
        with self.assertRaises(ValueError):
            search(limit=101)
        with self.assertRaises(ValueError):
            handoff(selected["id"], "subject", revision="stale")
        with self.assertRaises(ValueError):
            handoff(selected["id"], "subject", aspect_ratio="1024x1024")
        with self.assertRaises(ValueError):
            handoff(selected["id"], " ")
        with self.assertRaises(ValueError):
            handoff(selected["id"], "x" * 1001)

    def test_catalog_rejects_preview_path_escape(self):
        import catalog as source
        data = catalog()
        data["items"][0]["previewAsset"] = "../private.png"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "catalog.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            previous = source.SOURCE
            try:
                source.SOURCE = path
                with self.assertRaisesRegex(ValueError, "Invalid preview asset"):
                    source.catalog()
            finally:
                source.SOURCE = previous

    def test_handoff_is_generation_request_with_reference_guard(self):
        required = next(row for row in catalog()["items"] if row["reference"] == "required")
        result = handoff(required["id"], "restore the supplied portrait", aspect_ratio="4:5",
                         background="Transparent", reference_notes="keep the glasses",
                         prompt_override="Retain expression and lighting.",
                         additional_instructions="No text.")
        prompt = result["handoffText"]
        self.assertEqual(result["status"], "prepared")
        self.assertIn("official imagegen", prompt)
        self.assertIn("transparent_background=true", prompt)
        self.assertIn("ask the user to attach it and stop", prompt)
        self.assertIn("view_image", prompt)
        self.assertIn("Never use both mechanisms", prompt)
        self.assertIn("Retain expression and lighting.", prompt)
        self.assertNotIn(required["prompt"], prompt)
        self.assertIn("Reference notes (description only", prompt)
        self.assertEqual(len(RATIOS), 7)

    def test_export_injects_shared_chooser_without_source_copy(self):
        html = render_html()
        self.assertIn("window.LibraryBridge", html)
        self.assertIn("window.ImageWorkflowEditor", html)
        self.assertIn("window.LibraryAdapter", html)
        self.assertIn("Send to conversation", html)
        self.assertIn(catalog()["revision"], html)
        self.assertNotIn("__LIBRARY_", html)
        self.assertTrue(URI.endswith("-v2.html"))
        self.assertIn('data:image/png;base64,', html)

    def test_tool_metadata_and_structured_search(self):
        async def inspect():
            server = create_server()
            tools = {tool.name: tool for tool in await server.list_tools()}
            self.assertEqual(set(tools), {"search_image_workflows", "read_image_workflow",
                                          "browse_image_workflows", "prepare_image_workflow_handoff"})
            self.assertEqual(tools["browse_image_workflows"].meta["ui"]["resourceUri"], URI)
            for name in ("search_image_workflows", "read_image_workflow", "prepare_image_workflow_handoff"):
                self.assertFalse(tools[name].meta)
            response = await server.call_tool("search_image_workflows", {"domain": "video"})
            self.assertFalse(response.isError)
            self.assertTrue(all("video" in row["domains"] for row in response.structuredContent["items"]))
            self.assertNotIn("data:image", response.content[0].text)
        asyncio.run(inspect())


if __name__ == "__main__":
    unittest.main()
