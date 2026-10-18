"""Bounded local workflow activity recorder checks."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/work_activity_record.py"
spec = importlib.util.spec_from_file_location("work_activity_record", SCRIPT)
activity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(activity)


class ActivityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "project"
        self.root.mkdir()
        self.state = self.base / "state"
        self.config = {"state_dir": str(self.state), "project_roots": [
            {"name": "demo", "root": str(self.root), "globs": ["receipts/*.json", "docs/*.md"]}
        ], "max_files": 20, "max_bytes": 10000}

    def journal(self):
        return json.loads((self.state / "activity.json").read_text())

    def test_baseline_edit_unchanged_and_exclusions(self):
        receipt = self.root / "receipts/r.json"
        receipt.parent.mkdir()
        receipt.write_text('{"ok": true}')
        (self.root / "build").mkdir()
        (self.root / "build/r.json").write_text("ignored")
        self.assertEqual(activity.scan(self.config)["status"], "recorded")
        self.assertEqual(activity.scan(self.config)["status"], "unchanged")
        self.assertEqual(self.journal()["activities"], [])
        receipt.write_text('{"ok": false}')
        result = activity.scan(self.config)
        self.assertEqual((result["status"], result["changed"]), ("changed", 1))
        row = self.journal()["activities"][0]
        self.assertEqual((row["path"], row["status"]), ("receipts/r.json", "changed_unverified"))
        self.assertEqual(activity.scan(self.config)["status"], "unchanged")

    def test_unavailable_root_preserves_prior_state_and_corrupt_is_untouched(self):
        doc = self.root / "docs/a.md"
        doc.parent.mkdir(); doc.write_text("a")
        activity.scan(self.config)
        before_files = self.journal()["files"]
        self.root.rename(self.base / "detached")
        result = activity.scan(self.config)
        self.assertEqual(result["unavailable"], ["demo"])
        self.assertEqual(self.journal()["files"], before_files)
        self.assertEqual(self.journal()["last_unavailable"], ["demo"])
        path = self.state / "activity.json"
        path.write_bytes(b"{bad")
        with self.assertRaisesRegex(ValueError, "corrupt"):
            activity.scan(self.config)
        self.assertEqual(path.read_bytes(), b"{bad")

    def test_structured_record_hashes_evidence_and_suppresses_duplicate(self):
        evidence = self.base / "evidence.txt"
        evidence.write_text("receipt")
        payload = {"workflow": "release", "method": "review", "outcome": "ready",
                   "status": "tested", "evidence_refs": [str(evidence)]}
        self.assertEqual(activity.record(self.config, payload)["status"], "recorded")
        self.assertEqual(activity.record(self.config, payload)["status"], "duplicate")
        row = self.journal()["activities"][0]
        self.assertEqual((row["status_source"], row["human_accepted"]), ("caller_declared", False))
        self.assertIn("sha256", row["evidence"][0])
        self.assertNotIn("receipt", json.dumps(row))

    def test_touch_does_not_duplicate_and_completion_status_requires_evidence(self):
        evidence = self.base / "evidence.txt"
        evidence.write_text("receipt")
        payload = {"workflow": "release", "method": "review", "outcome": "ready",
                   "status": "tested", "evidence_refs": [str(evidence)]}
        activity.record(self.config, payload)
        evidence.touch()
        self.assertEqual(activity.record(self.config, payload)["status"], "duplicate")
        with self.assertRaisesRegex(ValueError, "evidence_refs"):
            activity.record(self.config, {"workflow": "x", "method": "y", "outcome": "z",
                                          "status": "published"})

    def test_isolated_subprocess_tracker_runs_opt_in_activity_capture(self):
        plugins = self.base / "plugins/p/.codex-plugin"
        plugins.mkdir(parents=True)
        (plugins / "plugin.json").write_text("{}")
        project = self.base / "tracked/docs"
        project.mkdir(parents=True)
        (project / "a.md").write_text("a")
        activity_config = self.base / "activity-config.json"
        activity_config.write_text(json.dumps({"state_dir": str(self.base / "activity-state"),
            "project_roots": [{"name": "tracked", "root": str(self.base / "tracked"),
                               "globs": ["docs/*.md"]}]}))
        tracker_config = self.base / "tracker-config.json"
        tracker_config.write_text(json.dumps({"canonical_root": str(self.base / "plugins"),
            "state_dir": str(self.base / "plugin-state"),
            "work_activity_config": str(activity_config)}))
        result = subprocess.run([sys.executable, "-I", str(Path(__file__).parents[1] / "scripts/plugin_change_record.py"),
                                 "--config", str(tracker_config)], capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.base / "activity-state/activity.json").exists())

    def test_query_aggregates_plugin_events_without_copying_source_store(self):
        activity.scan(self.config)
        plugin = self.base / "plugin.json"
        plugin.write_text(json.dumps({"events": [{"at": "2026-10-15T12:00:00+00:00", "changes": []}]}))
        result = activity.query({**self.config, "plugin_journal": str(plugin)},
                                "2026-10-15T00:00:00+00:00", "2026-10-16T00:00:00+00:00")
        self.assertEqual(result["plugin_events"][0]["type"], "plugin_source_changed")
        self.assertTrue(result["limitations"])


if __name__ == "__main__":
    unittest.main()
