"""Public method availability and held-runtime boundaries without upstream execution."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("public_motion_sources", ROOT / "scripts/motion_sources.py")
motion = importlib.util.module_from_spec(spec)
spec.loader.exec_module(motion)


class PublicMotionSourceTests(unittest.TestCase):
    def test_catalog_is_available_and_does_not_claim_runtime_bundles(self):
        for source, expected in [("huashu-motion", 10), ("motion-anything", 218)]:
            with self.subTest(source=source):
                library = motion.SourceLibrary(source)
                rows = library.catalog()
                self.assertEqual(len(rows), expected)
                self.assertTrue(all(row["public_bundle_available"] is False for row in rows))

    def test_complete_original_methods_can_be_read(self):
        for source, relative in [("huashu-motion", "skills/huashu-motion/SKILL.md"),
                                 ("motion-anything", "skills/motion-anything/SKILL.md")]:
            result = motion.SourceLibrary(source).read(relative)
            self.assertEqual(result["content_as_quoted_data"],
                             (ROOT / "libraries" / source / relative).read_text())
            self.assertIn("runtime closures held", result["boundary"])

    def test_held_likeness_and_recipe_code_are_not_readable(self):
        for source, relative in [("huashu-motion", "runtime/clip/lib/toon.js"),
                                 ("motion-anything", "recipes/animxyz/_runtime/animxyz.css")]:
            with self.assertRaisesRegex(ValueError, "not admitted"):
                motion.SourceLibrary(source).read(relative)
            self.assertFalse((ROOT / "libraries" / source / relative).exists())

    def test_valid_selection_fails_before_bundle_output_or_retrieval(self):
        for source in motion.SOURCES:
            library = motion.SourceLibrary(source)
            selection = library.catalog()[0]["id"]
            with tempfile.TemporaryDirectory() as folder:
                with self.assertRaisesRegex(ValueError, "Public method-only edition"):
                    library.bundle(selection, folder, "output")
                self.assertEqual(list(Path(folder).iterdir()), [])

    def test_unknown_and_unsafe_inputs_remain_rejected(self):
        library = motion.SourceLibrary("huashu-motion")
        with self.assertRaisesRegex(ValueError, "exact catalog ID"):
            library.plan("not-a-selection")
        for value in ["../LICENSE", "/LICENSE", ".private/file", "a\\b"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                library.read(value)

    def test_every_admitted_source_hash_is_verified(self):
        for source in motion.SOURCES:
            library = motion.SourceLibrary(source)
            admitted = [path for path, row in library.rows.items() if row["retained_in_owner"]]
            self.assertTrue(admitted)
            for relative in admitted:
                library.read_bytes(relative)

    def test_changed_source_cannot_be_read(self):
        with tempfile.TemporaryDirectory() as folder:
            owner = Path(folder).resolve()
            root = owner / "libraries/huashu-motion"
            docs = owner / "docs/motion-source-admission"
            root.mkdir(parents=True)
            docs.mkdir(parents=True)
            (root / "LICENSE").write_text("changed")
            (docs / "huashu-motion-files.json").write_text(json.dumps([
                {"path": "LICENSE", "retained_in_owner": True, "sha256": "0" * 64}]))
            (docs / "huashu-motion-catalog.json").write_text("[]")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                motion.SourceLibrary("huashu-motion", owner).read("LICENSE")


if __name__ == "__main__":
    unittest.main()
