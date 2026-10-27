"""Native installer fakes verify preservation and recovery without Codex calls."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location(
    "codex_sync", Path(__file__).resolve().parents[1] / "scripts/sync_codex_plugins.py")
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)


class CodexSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source, self.cache = self.root / "source", self.root / "cache"
        (self.source / ".codex-plugin").mkdir(parents=True)
        (self.source / ".codex-plugin/plugin.json").write_text('{"version":"1.0"}')
        (self.source / "method.md").write_text("original")
        shutil.copytree(self.source, self.cache)
        self.config = {"storage_root": str(self.root), "state_dir": str(self.root / "state"),
                       "cli": "never-invoked", "packages": {"example@personal": {
                           "source": str(self.source), "cache": str(self.cache), "version": "1.0"}}}
        self.adds = 0
        self.failure = None

    def native(self, cli, args):
        if args[0] == "list":
            return {"installed": [{"pluginId": "example@personal", "enabled": True, "version": "1.0"}]}
        self.adds += 1
        for p in self.source.rglob("*"):
            if p.is_file():
                target = self.cache / p.relative_to(self.source)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, target)
        if self.failure == "extra":
            (self.cache / "unexpected.txt").write_text("installer-added")
        if self.failure == "delete":
            (self.cache / ".codex-plugin/plugin.json").unlink()
        if self.failure == "timeout":
            raise subprocess.TimeoutExpired(["native", "add"], timeout=90)
        return {"installedPath": str(self.cache)}

    def baseline(self):
        sync.synchronize(self.config, "baseline", self.native)

    def test_noop_drift_and_repeated_apply(self):
        self.baseline()
        state = self.root / "state/state.json"
        stamp = state.stat().st_mtime_ns
        sync.synchronize(self.config, "apply", self.native)
        self.assertEqual(self.adds, 0)
        self.assertEqual(state.stat().st_mtime_ns, stamp)
        (self.source / "method.md").write_text("new source")
        result = sync.synchronize(self.config, "apply", self.native)
        self.assertEqual(len(result["updated"]), 1)
        self.assertEqual((self.cache / "method.md").read_text(), "new source")
        sync.synchronize(self.config, "apply", self.native)
        self.assertEqual(self.adds, 1)

    def test_user_cache_edit_and_missing_baseline_are_preserved(self):
        self.baseline()
        (self.cache / "method.md").write_text("user edit")
        self.assertTrue(sync.synchronize(self.config, "apply", self.native)["conflicts"])
        self.assertEqual((self.cache / "method.md").read_text(), "user edit")
        (self.root / "state/state.json").write_text("{}")
        self.assertTrue(sync.synchronize(self.config, "apply", self.native)["conflicts"])
        self.assertEqual(self.adds, 0)

    def test_partial_native_failure_restores_extra_and_missing_files(self):
        for failure in ("extra", "delete", "timeout"):
            with self.subTest(failure=failure):
                self.baseline()
                (self.source / "method.md").write_text("new source")
                self.failure = failure
                result = sync.synchronize(self.config, "apply", self.native)
                self.assertTrue(result["rollback_verified"])
                self.assertEqual((self.cache / "method.md").read_text(), "original")
                self.assertFalse((self.cache / "unexpected.txt").exists())
                self.assertTrue((self.cache / ".codex-plugin/plugin.json").is_file())
                (self.source / "method.md").write_text("original")


if __name__ == "__main__":
    unittest.main()
