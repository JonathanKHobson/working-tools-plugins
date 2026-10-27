"""Maintenance fixtures: never call an AI provider or real installation."""
import fcntl
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/provider_sync.py"
spec = importlib.util.spec_from_file_location("provider_sync", SCRIPT)
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.adapter = self.root / "sync_antigravity.py"
        self.adapter.write_text("# reviewed offline adapter\n")
        adapter_config = self.root / "adapter.json"
        adapter_config.write_text("{}")
        self.journal = self.root / "journal.json"
        self.write_source("a")
        self.config = {"schema_version": 1, "enabled": True, "required_mounts": [],
                       "state_dir": str(self.root / "state"), "storage_root": str(self.root),
                       "journal": str(self.journal), "adapters": {"gemini": {
                           "owners": ["example"],
                           "argv": [sys.executable, str(self.adapter), "--config",
                                    str(adapter_config), "--apply"],
                           "reviewed_files": {str(self.adapter): sync.digest(self.adapter),
                                              str(adapter_config): sync.digest(adapter_config)}}}}
        self.calls = []

    def write_source(self, sha):
        self.journal.write_text(json.dumps({"revision": 1, "products": {"example": {
            "files": {"skills/test/SKILL.md": {"sha256": sha}}}}}))

    def runner(self, argv, timeout, output):
        self.calls.append(argv)
        return 0

    def test_check_read_only_and_noop_does_not_invoke(self):
        self.assertEqual(sync.reconcile(self.config)["status"], "pending")
        self.assertFalse((self.root / "state").exists())
        sync.reconcile(self.config, "baseline", self.runner)
        stamp = (self.root / "state/state.json").stat().st_mtime_ns
        result = sync.reconcile(self.config, "apply", self.runner)
        self.assertEqual(result["status"], "unchanged")
        self.assertEqual(self.calls, [])
        self.assertEqual((self.root / "state/state.json").stat().st_mtime_ns, stamp)

    def test_change_one_run_repeated_event_noop(self):
        sync.reconcile(self.config, "baseline", self.runner)
        self.write_source("b")
        sync.reconcile(self.config, "apply", self.runner)
        sync.reconcile(self.config, "apply", self.runner)
        self.assertEqual(len(self.calls), 1)

    def test_failure_preserves_cursor_for_retry(self):
        sync.reconcile(self.config, "baseline", self.runner)
        self.write_source("b")
        prior = json.loads((self.root / "state/state.json").read_text())["adapters"]["gemini"]["signature"]
        self.assertEqual(sync.reconcile(self.config, "apply", lambda *_: 2)["status"], "failed")
        after = json.loads((self.root / "state/state.json").read_text())
        self.assertEqual(after["adapters"]["gemini"]["signature"], prior)
        self.assertEqual(sync.reconcile(self.config)["status"], "attention_required")
        sync.reconcile(self.config, "apply", self.runner)
        self.assertEqual(self.calls, [])
        sync.reconcile(self.config, "apply", self.runner, retry_failed=True)
        self.assertEqual(len(self.calls), 1)

    def test_changed_adapter_path_escape_and_provider_cli_rejected(self):
        self.adapter.write_text("unreviewed")
        with self.assertRaises(ValueError):
            sync.reconcile(self.config, "apply", self.runner)
        self.assertEqual(self.calls, [])
        self.config["adapters"]["gemini"]["reviewed_files"][str(self.adapter)] = sync.digest(self.adapter)
        self.config["adapters"]["../outside"] = self.config["adapters"].pop("gemini")
        with self.assertRaises(ValueError):
            sync.reconcile(self.config, "apply", self.runner)
        self.config["adapters"]["gemini"] = self.config["adapters"].pop("../outside")
        self.config["adapters"]["gemini"]["argv"] = ["/usr/bin/claude", "-p", "run model"]
        with self.assertRaises(ValueError):
            sync.reconcile(self.config, "apply", self.runner)

    def test_mount_loss_no_write_or_invocation(self):
        self.config["required_mounts"] = [str(self.root / "absent")]
        with self.assertRaises(ValueError):
            sync.reconcile(self.config, "apply", self.runner)
        self.assertEqual(self.calls, [])
        self.assertFalse((self.root / "state").exists())

    def test_outer_deadline_can_cover_native_batch_and_recovery(self):
        self.config["adapters"]["gemini"]["timeout_seconds"] = 7200
        self.assertEqual(sync.reconcile(self.config)["status"], "pending")
        self.config["adapters"]["gemini"]["timeout_seconds"] = 21601
        with self.assertRaisesRegex(ValueError, "timeout"):
            sync.reconcile(self.config)

    def test_enqueuing_unchanged_never_launches_process(self):
        sync.reconcile(self.config, "baseline", self.runner)
        path = self.root / "config.json"
        path.write_text(json.dumps(self.config))
        with patch.object(sync.subprocess, "Popen") as popen:
            self.assertEqual(sync.enqueue(path)["status"], "unchanged")
            popen.assert_not_called()

    def test_adapter_configuration_change_requires_review(self):
        sync.reconcile(self.config, "baseline", self.runner)
        adapter_config = Path(self.config["adapters"]["gemini"]["argv"][3])
        adapter_config.write_text('{"changed":true}')
        with self.assertRaises(ValueError):
            sync.reconcile(self.config, "apply", self.runner)
        self.assertEqual(self.calls, [])
        self.config["adapters"]["gemini"]["reviewed_files"][str(adapter_config)] = sync.digest(adapter_config)
        self.assertEqual(sync.reconcile(self.config)["status"], "pending")

    def test_adapter_configuration_must_have_a_reviewed_hash(self):
        config_path = self.config["adapters"]["gemini"]["argv"][3]
        del self.config["adapters"]["gemini"]["reviewed_files"][config_path]
        with self.assertRaisesRegex(ValueError, "configuration need reviewed hashes"):
            sync.reconcile(self.config, "apply", self.runner)
        self.assertEqual(self.calls, [])

    def test_inherited_lock_fd_must_identify_real_sync_lock(self):
        state = self.root / "state"
        state.mkdir()
        with (state / "sync.lock").open("a") as genuine, (self.root / "other.lock").open("a") as other:
            fcntl.flock(genuine, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaisesRegex(ValueError, "not the expected lock file"):
                sync.reconcile(self.config, "apply", self.runner, lock_fd=other.fileno())
            self.assertEqual(self.calls, [])
            # The inherited descriptor points at the locked open file description.
            result = sync.reconcile(self.config, "apply", self.runner, lock_fd=genuine.fileno())
        self.assertEqual(result["status"], "synchronized")
        self.assertEqual(len(self.calls), 1)

    def test_held_and_new_adapter_remains_attention_required(self):
        sync.reconcile(self.config, "baseline", self.runner)
        self.write_source("b")
        sync.reconcile(self.config, "apply", lambda *_: 2)
        self.config["adapters"]["codex"] = json.loads(json.dumps(self.config["adapters"]["gemini"]))
        second = self.root / "sync_codex_plugins.py"
        second.write_text("# other reviewed offline adapter\n")
        self.config["adapters"]["codex"]["argv"][1] = str(second)
        self.config["adapters"]["codex"]["reviewed_files"][str(second)] = sync.digest(second)
        result = sync.reconcile(self.config, "apply", self.runner)
        self.assertEqual(result["status"], "attention_required")
        self.assertEqual(result["held"], ["gemini"])
        self.assertEqual(len(self.calls), 1)


if __name__ == "__main__":
    unittest.main()
