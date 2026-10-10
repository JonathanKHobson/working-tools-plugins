"""Focused, filesystem-isolated checks for the professional-agent installer."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest

try:
    import install_professional_agents as installer
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    import install_professional_agents as installer


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name).resolve() / "home"
        self.owner = self.home / "plugins" / "studio-test"
        (self.owner / ".codex-plugin").mkdir(parents=True)
        (self.owner / ".codex-plugin" / "plugin.json").write_text('{"name":"studio-test"}\n')
        self.skill = self.owner / "skills" / "inspect" / "SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text("# Existing method\n\nKeep this authored text.\n")
        self.provider_file = self.home / "plugins/work-management/references/professional-agents/providers.json"
        self.provider_file.parent.mkdir(parents=True)
        self.provider_file.write_text(json.dumps([{
            "name": "studio-test", "root": str(self.owner), "enabled": True
        }]))
        self.role = {
            "id": "test-reviewer", "title": "Test Reviewer", "owner_plugin": "studio-test",
            "description": "Inspect a bounded test artifact and report findings.",
            "mission": "Inspect the assigned artifact.",
            "triggers": ["A review is assigned."], "inputs": ["Artifact and scope."],
            "outputs": ["Findings with evidence."], "decisions": ["Whether evidence supports a finding."],
            "boundaries": ["Do not implement fixes."], "skills": ["studio-test:inspect"],
            "review_only": True, "collaboration_class": "reviewer",
        }
        self.catalog = self.home / "catalog.json"
        self.catalog.write_text(json.dumps({"roles": [self.role]}))
        self.backup = Path(self.temp.name) / "backups"
        self.receipt = Path(self.temp.name) / "receipt.json"
        self.args = SimpleNamespace(apply=True, backup=self.backup, receipt=self.receipt)

    def generated(self):
        roles = installer.load_roles(self.catalog)
        paths = installer.skill_paths(self.home)
        return installer.outputs(self.home, roles, paths, set())

    def test_unmanaged_registration_collision_is_rejected_without_writes(self):
        target = self.home / ".codex/agents/studio-test-reviewer.toml"
        target.parent.mkdir(parents=True)
        target.write_text("# Human-owned registration\n")
        with self.assertRaisesRegex(ValueError, "Refusing unmanaged output"):
            installer.commit(self.generated(), self.args)
        self.assertEqual(target.read_text(), "# Human-owned registration\n")
        self.assertFalse(self.receipt.exists())
        self.assertEqual(self.skill.read_text(), "# Existing method\n\nKeep this authored text.\n")

    def test_managed_update_creates_exact_backup_and_receipt(self):
        target = self.home / ".codex/agents/studio-test-reviewer.toml"
        target.parent.mkdir(parents=True)
        previous = f"# {installer.MARKER}\nname = 'stale'\n".encode()
        target.write_bytes(previous)
        generated = self.generated()
        self.assertTrue(installer.commit(generated, self.args))
        self.assertEqual(target.read_text(), generated[target])
        entry = next(x for x in json.loads(self.receipt.read_text()) if x["path"] == str(target))
        self.assertEqual(Path(entry["backup"]).read_bytes(), previous)
        self.assertEqual(entry["before_sha256"], installer.digest(previous))
        self.assertEqual(entry["after_sha256"], installer.digest(target.read_bytes()))

    def test_second_apply_is_idempotent(self):
        self.assertTrue(installer.commit(self.generated(), self.args))
        self.assertFalse(installer.commit(self.generated(), self.args))
        self.assertEqual(json.loads(self.receipt.read_text()), [])
        self.assertEqual(self.skill.read_text().count(installer.BEGIN), 1)

    def test_missing_enabled_skill_aborts_check_without_outputs(self):
        self.role["skills"] = ["studio-test:missing"]
        self.catalog.write_text(json.dumps({"roles": [self.role]}))
        script = Path(installer.__file__)
        run = subprocess.run(
            [sys.executable, str(script), "--home", str(self.home),
             "--catalog", str(self.catalog), "--check"],
            capture_output=True, text=True, check=False,
        )
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("Missing enabled methods: ['studio-test:missing']", run.stderr)
        self.assertFalse((self.home / ".codex/agents").exists())

    def test_reviewer_field_sets_read_only_and_review_boundary(self):
        generated = self.generated()
        codex = generated[self.home / ".codex/agents/studio-test-reviewer.toml"]
        claude = generated[self.home / ".claude/agents/studio-test-reviewer.md"]
        self.assertIn('sandbox_mode = "read-only"', codex)
        self.assertIn("do not implement fixes or approve your own work", codex)
        self.assertIn("do not implement fixes or approve your own work", claude)
        self.role["review_only"] = False
        self.catalog.write_text(json.dumps({"roles": [self.role]}))
        codex = self.generated()[self.home / ".codex/agents/studio-test-reviewer.toml"]
        self.assertNotIn("sandbox_mode", codex)

    def test_existing_source_text_survives_append_and_refresh(self):
        readme = self.owner / "README.md"
        readme.write_text("# Studio Test\n\nHuman-authored context.\n")
        self.assertTrue(installer.commit(self.generated(), self.args))
        self.assertTrue(self.skill.read_text().startswith("# Existing method\n\nKeep this authored text.\n"))
        self.assertTrue(readme.read_text().startswith("# Studio Test\n\nHuman-authored context.\n"))
        self.assertEqual(self.skill.read_text().count(installer.BEGIN), 1)
        self.assertEqual(readme.read_text().count(installer.BEGIN), 1)
        self.skill.write_text(self.skill.read_text().replace("Keep this authored text.", "Keep this revised authored text."))
        self.role["description"] = "Inspect a revised bounded test artifact and report findings."
        self.catalog.write_text(json.dumps({"roles": [self.role]}))
        self.assertTrue(installer.commit(self.generated(), self.args))
        self.assertIn("Keep this revised authored text.", self.skill.read_text())
        self.assertEqual(self.skill.read_text().count(installer.BEGIN), 1)


if __name__ == "__main__":
    unittest.main()
