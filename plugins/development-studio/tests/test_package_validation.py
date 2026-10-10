"""Negative integrity cases for the authored, read-only validator."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("package_validation", ROOT / "scripts/validate_package.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class PackageIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="development-studio-validation-")
        self.root = Path(self.scratch.name) / "package"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))

    def tearDown(self):
        self.scratch.cleanup()

    def test_baseline_is_valid(self):
        result = validator.check(self.root)
        self.assertTrue(result["ok"], result["errors"])

    def test_import_tampering_fails(self):
        file = self.root / "libraries/superpowers-6.4.2/skills/systematic-debugging/SKILL.md"
        file.write_text(file.read_text() + "\nChanged after admission.\n")
        self.assertTrue(any("import hash mismatch" in x for x in validator.check(self.root)["errors"]))

    def test_missing_full_method_fails(self):
        file = self.root / "libraries/superpowers-6.4.2/skills/writing-plans/SKILL.md"
        file.unlink()
        self.assertFalse(validator.check(self.root)["ok"])

    def test_local_mcp_adaptation_tampering_fails(self):
        file = self.root / "libraries/local-mcp-methods/local-data-mcp-builder/SKILL.md"
        file.write_text(file.read_text() + "\nUnreviewed adaptation.\n")
        self.assertTrue(any("import hash mismatch" in x for x in validator.check(self.root)["errors"]))

    def test_untracked_vendor_asset_fails(self):
        file = self.root / "libraries/alpic-1.0.1/unreviewed.txt"
        file.write_text("extra content not in source inventory\n")
        self.assertTrue(any("support closure" in x for x in validator.check(self.root)["errors"]))

    def test_accidental_runtime_declaration_fails(self):
        file = self.root / ".codex-plugin/plugin.json"
        manifest = json.loads(file.read_text())
        manifest["mcpServers"] = "./.mcp.json"
        file.write_text(json.dumps(manifest))
        self.assertTrue(any("runtime/provider" in x for x in validator.check(self.root)["errors"]))

    def test_unknown_provider_fails(self):
        file = self.root / "docs/routes.json"
        routes = json.loads(file.read_text())
        routes["provider_routes"]["build-web-software"].append("imaginary-execution-provider")
        file.write_text(json.dumps(routes))
        self.assertTrue(any("uninventoried provider" in x for x in validator.check(self.root)["errors"]))

    def test_standalone_query_engine_tampering_fails(self):
        file = self.root / "skills/golang-effective/scripts/query_chunk_index.py"
        file.write_text(file.read_text() + "\nUnreviewed adaptation.\n")
        self.assertTrue(any("import hash mismatch" in x for x in validator.check(self.root)["errors"]))

    def test_reference_escape_fails(self):
        file = self.root / "README.md"
        file.write_text(file.read_text() + "\n[private host configuration](../outside.json)\n")
        self.assertTrue(any("escaping link" in x for x in validator.check(self.root)["errors"]))


if __name__ == "__main__":
    unittest.main()
