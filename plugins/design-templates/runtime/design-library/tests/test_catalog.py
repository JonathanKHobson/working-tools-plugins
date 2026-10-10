"""Catalog integrity and handoff behavior with isolated installed packages."""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from catalog import CatalogError, browse, handoff, source_fingerprint  # noqa: E402


class CatalogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / "codex"
        self.package = self.home / "skills" / "artifact-template-studio-example"
        self.source = self.package / "assets" / "source"
        self.source.mkdir(parents=True)
        (self.source / "index.html").write_text("<h1>Example</h1>", encoding="utf-8")
        (self.package / "artifact-template.json").write_text(
            json.dumps({"kind": "site", "reference": "assets/source"}), encoding="utf-8"
        )
        (self.package / "DESIGN.md").write_text("Keep the source hierarchy.", encoding="utf-8")
        (self.package / "WORKFLOW.md").write_text("Adapt a working copy.", encoding="utf-8")
        (self.package / "design").mkdir()
        # Foundations deliberately uses a different source-hash scope from the catalog.
        (self.package / "design" / "foundations.json").write_text(json.dumps({
            "sourceHash": "a" * 64, "sourceHashScope": "visual source files only"
        }), encoding="utf-8")
        (self.package / "design" / "ADAPTATION.md").write_text("Retain unknown facts.", encoding="utf-8")
        self.provenance = self.root / "provenance.json"
        self.seed_provenance()
        self.item = {
            "id": "example", "name": "Example", "summary": "An illustrative Site template",
            "category": "Research", "tags": ["editorial"], "bestFor": ["Stories"],
            "avoidWhen": ["Dashboards"], "interactions": ["Read"], "limitations": ["Example"],
            "skillName": "artifact-template-studio-example", "sourceHash": source_fingerprint(self.source),
            "sourceKind": "site", "desktopPreview": "assets/example-desktop.png",
            "mobilePreview": "assets/example-mobile.png",
        }
        self.catalog = self.root / "catalog.json"
        self.save()

    def save(self) -> None:
        self.catalog.write_text(json.dumps({"schemaVersion": 1, "owner": "Design Templates", "items": [self.item]}), encoding="utf-8")

    def seed_provenance(self) -> None:
        files = [{
            "path": f"templates/{self.package.name}/{path.relative_to(self.package).as_posix()}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        } for path in self.package.rglob("*") if path.is_file()]
        self.provenance.write_text(json.dumps({"schemaVersion": 1, "files": files}), encoding="utf-8")

    def browse(self, **kwargs):
        return browse(catalog_path=self.catalog, codex_home=self.home, **kwargs)

    def handoff(self, template_id="example", brief=""):
        return handoff(template_id, brief, catalog_path=self.catalog, codex_home=self.home,
                       guidance_manifest_path=self.provenance)

    def test_registered_ready_and_filtered_results(self):
        result = self.browse(query="EDITORIAL", category="research")
        self.assertEqual(result["items"][0]["availability"], "ready")
        self.assertNotIn("desktopPreview", result["items"][0])
        self.assertEqual(self.browse(query="none")["items"], [])
        self.assertEqual(self.browse(category="unrelated")["items"], [])
        selected = self.handoff(brief="Use a short source list")
        self.assertEqual(selected["sourceHash"], self.item["sourceHash"])
        self.assertIn("copy the source into a new working directory", selected["instructions"])

    def test_handoff_has_exact_verified_refs_and_leaves_source_unchanged(self):
        before = {path.relative_to(self.package).as_posix(): path.read_bytes()
                  for path in self.package.rglob("*") if path.is_file()}
        selected = self.handoff(brief="Keep approved findings and flag unknown values")
        expected_names = ("artifact-template.json", "DESIGN.md", "WORKFLOW.md",
                          "design/foundations.json", "design/ADAPTATION.md")
        self.assertEqual(selected["guidanceRefs"], [{
            "path": str(self.package / name),
            "sha256": hashlib.sha256((self.package / name).read_bytes()).hexdigest(),
        } for name in expected_names])
        self.assertIn("read the selected authoritative guidanceRefs before adapting", selected["handoffText"])
        self.assertIn("Preserve approved facts, explicit unknowns and the current design", selected["handoffText"])
        self.assertIn("unless the brief authorizes change", selected["handoffText"])
        for ref in selected["guidanceRefs"]:
            self.assertIn(f"{ref['path']} | {ref['sha256']}", selected["handoffText"])
        self.assertNotIn("Keep the source hierarchy.", selected["handoffText"])
        self.assertEqual(before, {path.relative_to(self.package).as_posix(): path.read_bytes()
                                  for path in self.package.rglob("*") if path.is_file()})
        self.assertNotIn("guidanceRefs", self.browse()["items"][0])

    def test_missing_and_tampered_guidance_refuse_ready_source_handoff(self):
        for name in ("DESIGN.md", "WORKFLOW.md", "design/foundations.json", "design/ADAPTATION.md"):
            with self.subTest(name=name):
                path = self.package / name
                original = path.read_bytes()
                path.unlink()
                self.assertEqual(self.browse()["items"][0]["availability"], "ready")
                with self.assertRaisesRegex(CatalogError, "Missing file"):
                    self.handoff()
                path.write_text("arbitrary replacement", encoding="utf-8")
                with self.assertRaisesRegex(CatalogError, "guidance has changed"):
                    self.handoff()
                path.write_bytes(original)

    def test_optional_guidance_absent_from_package_and_baseline_is_omitted(self):
        for name in ("design/foundations.json", "design/ADAPTATION.md"):
            (self.package / name).unlink()
        self.seed_provenance()
        self.assertEqual(len(self.handoff()["guidanceRefs"]), 3)

    def test_unanchored_present_or_mandatory_guidance_is_rejected(self):
        baseline = json.loads(self.provenance.read_text())
        for name in ("DESIGN.md", "WORKFLOW.md", "design/foundations.json", "design/ADAPTATION.md"):
            with self.subTest(name=name):
                document = {**baseline, "files": [entry for entry in baseline["files"]
                            if entry["path"] != f"templates/{self.package.name}/{name}"]}
                self.provenance.write_text(json.dumps(document), encoding="utf-8")
                with self.assertRaisesRegex(CatalogError, "no provenance hash"):
                    self.handoff()

    def test_provenance_source_binding_rejects_catalog_rehash(self):
        (self.source / "index.html").write_text("changed but recatalogued", encoding="utf-8")
        self.item["sourceHash"] = source_fingerprint(self.source)
        self.save()
        self.assertEqual(self.browse()["items"][0]["availability"], "ready")
        with self.assertRaisesRegex(CatalogError, "does not match the selected sourceHash"):
            self.handoff()

    def test_tampered_manifest_is_rejected_even_with_valid_kind_and_reference(self):
        (self.package / "artifact-template.json").write_text(json.dumps({
            "kind": "site", "reference": "assets/source", "extra": "unapproved"
        }), encoding="utf-8")
        with self.assertRaisesRegex(CatalogError, "guidance has changed: artifact-template.json"):
            self.handoff()

    def test_guidance_and_design_directory_symlinks_are_rejected(self):
        outside = self.root / "outside.md"
        original = (self.package / "DESIGN.md").read_bytes()
        outside.write_bytes(original)  # Matching bytes must not make a link acceptable.
        (self.package / "DESIGN.md").unlink()
        (self.package / "DESIGN.md").symlink_to(outside)
        with self.assertRaisesRegex(CatalogError, "regular file"):
            self.handoff()
        (self.package / "DESIGN.md").unlink()
        (self.package / "DESIGN.md").write_bytes(original)
        (self.package / "design").rename(self.root / "outside-design")
        (self.package / "design").symlink_to(self.root / "outside-design", target_is_directory=True)
        with self.assertRaisesRegex(CatalogError, "real directory"):
            self.handoff()

    def test_invalid_and_escaping_provenance_entries_are_rejected(self):
        baseline = json.loads(self.provenance.read_text())
        for entry in ({"path": f"templates/{self.package.name}/../outside.md", "sha256": "a" * 64},
                      {"path": f"templates/{self.package.name}/DESIGN.md", "sha256": "invalid"},
                      baseline["files"][0]):
            with self.subTest(entry=entry):
                self.provenance.write_text(json.dumps({**baseline, "files": [*baseline["files"], entry]}))
                with self.assertRaises(CatalogError):
                    self.handoff()

    def test_changed_file_and_new_file_refuse_handoff(self):
        (self.source / "index.html").write_text("changed", encoding="utf-8")
        self.assertEqual(self.browse()["items"][0]["availability"], "changed")
        with self.assertRaisesRegex(CatalogError, "changed"):
            self.handoff()
        (self.source / "index.html").write_text("<h1>Example</h1>", encoding="utf-8")
        (self.source / "new.css").write_text("body{}", encoding="utf-8")
        with self.assertRaisesRegex(CatalogError, "changed"):
            self.handoff()

    def test_missing_manifest_and_changed_kind_refuse_handoff(self):
        manifest = self.package / "artifact-template.json"
        manifest.unlink()
        self.assertEqual(self.browse()["items"][0]["availability"], "missing")
        with self.assertRaises(CatalogError):
            self.handoff()
        manifest.write_text(json.dumps({"kind": "document", "reference": "assets/source"}), encoding="utf-8")
        self.assertEqual(self.browse()["items"][0]["availability"], "changed")
        with self.assertRaises(CatalogError):
            self.handoff()

    def test_symlink_inside_source_and_package_refuse_handoff(self):
        outside = self.root / "outside.txt"
        outside.write_text("secret", encoding="utf-8")
        (self.source / "outside.txt").symlink_to(outside)
        self.assertEqual(self.browse()["items"][0]["availability"], "changed")
        with self.assertRaises(CatalogError):
            self.handoff()
        (self.source / "outside.txt").unlink()
        (self.package / "artifact-template.json").unlink()
        (self.package / "artifact-template.json").symlink_to(outside)
        with self.assertRaises(CatalogError):
            self.handoff()

    def test_unknown_and_escaping_ids_never_resolve_paths(self):
        for template_id in ("../example", "unknown", "/tmp/a"):
            with self.subTest(template_id=template_id), self.assertRaises(CatalogError):
                self.handoff(template_id)
        self.item["skillName"] = "../../other"
        self.save()
        with self.assertRaises(CatalogError):
            self.browse()

    def test_malformed_catalog_and_duplicate_ids(self):
        self.item["desktopPreview"] = "../../private.png"
        self.save()
        with self.assertRaises(CatalogError):
            self.browse()
        self.item["desktopPreview"] = "assets/example-desktop.png"
        self.catalog.write_text(json.dumps({"schemaVersion": 1, "owner": "Design Templates", "items": [self.item, self.item]}), encoding="utf-8")
        with self.assertRaises(CatalogError):
            self.browse()


if __name__ == "__main__":
    unittest.main()
