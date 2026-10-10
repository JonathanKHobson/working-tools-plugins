import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "provider_source", Path(__file__).resolve().parents[1] / "scripts/resolve_provider_source.py")
provider = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(provider)


class ProviderSourceTest(unittest.TestCase):
    def test_absent_binding_is_an_explicit_gap_without_creation(self):
        with tempfile.TemporaryDirectory() as directory:
            binding = Path(directory) / "absent.json"
            self.assertEqual(provider.resolve_source("visualize", binding)["reason"], "binding_missing")
            self.assertFalse(binding.exists())

    def test_entry_is_located_without_support_completeness_or_runtime_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "source"
            entry = root / "skills/visualize/SKILL.md"
            entry.parent.mkdir(parents=True)
            entry.write_text("Fictional test procedure")
            binding = Path(directory) / "binding.json"
            binding.write_text(json.dumps({"visualize": str(root)}))
            result = provider.resolve_source("visualize", binding)
            self.assertEqual(result["procedure"], str(entry.resolve()))
            self.assertTrue(result["available"])
            self.assertFalse(result["supporting_sources_verified"])
            self.assertFalse(result["runtime_verified"])
            self.assertFalse(result["redistribution_permission_verified"])
            self.assertEqual(entry.read_text(), "Fictional test procedure")
            self.assertEqual(provider.resolve_source("scientific", binding)["reason"], "provider_not_configured")

    def test_relative_source_and_escaping_symlink_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            binding = base / "binding.json"
            binding.write_text(json.dumps({"visualize": "relative/source"}))
            with self.assertRaises(ValueError):
                provider.resolve_source("visualize", binding)
            root = base / "source"
            entry = root / "skills/visualize/SKILL.md"
            entry.parent.mkdir(parents=True)
            outside = base / "outside.md"
            outside.write_text("Not an authorized procedure")
            entry.symlink_to(outside)
            binding.write_text(json.dumps({"visualize": str(root)}))
            with self.assertRaises(ValueError):
                provider.resolve_source("visualize", binding)

    def test_malformed_binding_is_not_silently_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            binding = Path(directory) / "binding.json"
            for content in ("not json", "[]", '{"scientific": 3}'):
                binding.write_text(content)
                with self.assertRaises(ValueError):
                    provider.resolve_source("scientific", binding)


if __name__ == "__main__":
    unittest.main()
