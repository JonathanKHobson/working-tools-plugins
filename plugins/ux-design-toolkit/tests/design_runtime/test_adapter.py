from __future__ import annotations

import hashlib
import io
import json
import os
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stdout

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))

from design_runtime import cli, config, engine, hooks, scope  # noqa: E402


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.plugin = self.base / "plugin"
        runtime = self.plugin / "runtime" / "impeccable"
        (runtime / "bin").mkdir(parents=True)
        (runtime / "skill").mkdir()
        self.binary = runtime / "bin" / "impeccable"
        self.binary.write_text(f"#!{sys.executable}\nimport sys, time\nif 'sleep' in sys.argv: time.sleep(5)\nprint('[]')\n", encoding="utf-8")
        self.binary.chmod(0o700)
        self.manifest = runtime / "manifest.json"
        self._manifest()
        self.project = self.base / "project"
        self.project.mkdir()
        (self.project / "src").mkdir()
        self.frontend = self.project / "src" / "screen.tsx"
        self.frontend.write_text("export default () => null;", encoding="utf-8")
        self.home_patch = patch.object(Path, "home", return_value=self.base)
        self.home_patch.start()
        self.addCleanup(self.home_patch.stop)

    def _manifest(self):
        self.manifest.write_text(json.dumps({
            "schemaVersion": 1,
            "engine": {"path": "bin/impeccable", "sha256": hashlib.sha256(self.binary.read_bytes()).hexdigest(),
                       "arch": engine.platform.machine(), "platform": engine.platform.system().lower()},
            "skillDir": "skill",
            "skillAssetsSha256": hashlib.sha256(b"").hexdigest(),
        }), encoding="utf-8")

    def test_manifest_missing_hash_and_architecture_refuse_execution(self):
        with patch.object(engine, "_binary_arch_ok", return_value=True):
            self.assertEqual(engine.verified_engine(self.plugin)[0], self.binary)
            self.binary.write_text(self.binary.read_text() + "#changed\n")
            with self.assertRaisesRegex(engine.RuntimeErrorWithMessage, "SHA-256"):
                engine.verified_engine(self.plugin)
            self._manifest()
            self.binary.unlink()
            with self.assertRaisesRegex(engine.RuntimeErrorWithMessage, "missing"):
                engine.verified_engine(self.plugin)
        self.binary.write_text("test")
        self.binary.chmod(0o700)
        self._manifest()
        with patch.object(engine, "_binary_arch_ok", return_value=False):
            with self.assertRaisesRegex(engine.RuntimeErrorWithMessage, "architecture"):
                engine.verified_engine(self.plugin)

    def test_source_only_runtime_reports_explicit_overlay_setup(self):
        self.binary.unlink()
        with self.assertRaises(engine.RuntimeErrorWithMessage) as failure:
            engine.verified_engine(self.plugin)
        message = str(failure.exception)
        self.assertIn("executable is missing:", message)
        self.assertIn("Source-only packages", message)
        self.assertIn("reviewed runtime overlay", message)
        self.assertIn(str(self.plugin / "docs" / "design-runtime.md"), message)
        self.assertIn("Design methods remain available", message)
        self.assertIn("no download was attempted", message)
        self.assertNotIn("not executable:", message)

    def test_present_nonexecutable_runtime_reports_permissions_separately(self):
        self.binary.chmod(0o600)
        with self.assertRaises(engine.RuntimeErrorWithMessage) as failure:
            engine.verified_engine(self.plugin)
        message = str(failure.exception)
        self.assertIn("executable is not executable:", message)
        self.assertIn("restore its executable mode", message)
        self.assertIn("refusing to execute", message)
        self.assertNotIn("executable is missing:", message)

    def test_private_environment_and_timeout(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "must-not-pass", "AWS_SECRET_ACCESS_KEY": "must-not-pass", "IMPECCABLE_BROWSER": "/tmp/untrusted"}):
            env = engine.private_env(self.plugin / "runtime" / "impeccable" / "skill", self.plugin / "scripts" / "design_runtime.py")
            self.assertNotIn("OPENAI_API_KEY", env)
            self.assertNotIn("AWS_SECRET_ACCESS_KEY", env)
            self.assertNotIn("IMPECCABLE_BROWSER", env)
            self.assertEqual(env["IMPECCABLE_NO_UPDATE_CHECK"], "1")
        with patch.object(engine, "_binary_arch_ok", return_value=True):
            with self.assertRaisesRegex(engine.RuntimeErrorWithMessage, "timed out"):
                engine.invoke(["sleep"], root=self.plugin, timeout=1, cwd=self.project)

    def test_changed_packaged_asset_refuses_execution(self):
        asset = self.plugin / "runtime" / "impeccable" / "skill" / "reference.md"
        asset.write_text("changed")
        with self.assertRaisesRegex(engine.RuntimeErrorWithMessage, "asset SHA-256"):
            engine.verified_engine(self.plugin)

    def test_pinned_nonempty_asset_closure_refuses_edit_add_delete_and_rename(self):
        runtime = self.plugin / "runtime" / "impeccable"
        asset = runtime / "skill" / "reference.md"
        asset.write_text("reviewed reference")
        manifest = json.loads(self.manifest.read_text())
        manifest["skillAssetsSha256"] = engine._asset_digest(runtime, runtime / "skill")
        self.manifest.write_text(json.dumps(manifest))
        with patch.object(engine, "_binary_arch_ok", return_value=True):
            self.assertEqual(engine.verified_engine(self.plugin)[1], runtime / "skill")
            asset.write_text("unreviewed reference")
            with self.assertRaisesRegex(engine.RuntimeErrorWithMessage, "asset SHA-256"):
                engine.verified_engine(self.plugin)
            asset.write_text("reviewed reference")
            added = runtime / "skill" / "new.md"
            added.write_text("new asset")
            with self.assertRaisesRegex(engine.RuntimeErrorWithMessage, "asset SHA-256"):
                engine.verified_engine(self.plugin)
            added.unlink()
            asset.rename(added)
            with self.assertRaisesRegex(engine.RuntimeErrorWithMessage, "asset SHA-256"):
                engine.verified_engine(self.plugin)
            added.unlink()
            with self.assertRaisesRegex(engine.RuntimeErrorWithMessage, "asset SHA-256"):
                engine.verified_engine(self.plugin)
            asset.write_text("reviewed reference")
            self.assertEqual(engine.verified_engine(self.plugin)[0], self.binary)

    def test_packaged_asset_symlink_refuses_execution_even_with_same_bytes(self):
        runtime = self.plugin / "runtime" / "impeccable"
        asset = runtime / "skill" / "reference.md"
        asset.write_text("reviewed reference")
        manifest = json.loads(self.manifest.read_text())
        manifest["skillAssetsSha256"] = engine._asset_digest(runtime, runtime / "skill")
        self.manifest.write_text(json.dumps(manifest))
        target = self.base / "reference.md"
        target.write_bytes(asset.read_bytes())
        asset.unlink()
        asset.symlink_to(target)
        with self.assertRaisesRegex(engine.RuntimeErrorWithMessage, "symlink"):
            engine.verified_engine(self.plugin)

    def test_manual_targets_are_explicit_and_scoped(self):
        self.assertEqual(scope.explicit_target(self.project, "src/screen.tsx", allow_url=False), str(self.frontend))
        with self.assertRaises(ValueError):
            scope.explicit_target(self.project, "https://example.com", allow_url=False)
        self.assertEqual(scope.explicit_target(self.project, "https://example.com", allow_url=True), "https://example.com")
        with self.assertRaises(ValueError):
            scope.loopback_url("https://example.com")
        (self.project / ".env.tsx").write_text("secret")
        self.assertIsNone(scope.allowed_file(self.project, ".env.tsx"))
        outside = self.base / "outside.tsx"
        outside.write_text("outside")
        (self.project / "src" / "escape.tsx").symlink_to(outside)
        self.assertIsNone(scope.allowed_file(self.project, "src/escape.tsx"))

    def test_events_queue_bounded_files_and_stop_once(self):
        scope.enable(self.project)
        event = {"session_id": "session-1", "cwd": str(self.project), "tool_name": "apply_patch",
                 "tool_input": {"patch": "*** Begin Patch\n*** Update File: src/screen.tsx\n@@\n"}}
        with patch.object(hooks, "_scan", return_value="finding") as scan:
            self.assertEqual(hooks.handle("post", event, str(self.project)), "finding")
            self.assertEqual(scan.call_count, 1)
            self.assertEqual(hooks.handle("post", event, str(self.project)), "")
            self.assertEqual(hooks.handle("stop", {"session_id": "session-1", "cwd": str(self.project)}, str(self.project)), "finding")
            self.assertEqual(scan.call_count, 2)
            self.assertEqual(hooks.handle("stop", {"session_id": "session-1", "cwd": str(self.project)}, str(self.project)), "")
            self.assertEqual(scan.call_count, 2)

    def test_reentry_disabled_malformed_and_out_of_root_skip(self):
        scope.enable(self.project)
        event = {"session_id": "session-1", "cwd": str(self.project), "tool_name": "Write", "tool_input": {"file_path": str(self.frontend)}}
        with patch.object(hooks, "_scan", return_value="finding") as scan:
            with patch.dict(os.environ, {"IMPECCABLE_HOOK_DEPTH": "1"}):
                self.assertEqual(hooks.handle("post", event, str(self.project)), "")
            self.assertEqual(hooks.handle("post", {**event, "cwd": str(self.base)}, str(self.project)), "")
            self.assertEqual(hooks.handle("post", {**event, "session_id": ""}, str(self.project)), "")
            self.assertEqual(hooks.handle("stop", {**event, "stop_hook_active": True}, str(self.project)), "")
            self.assertEqual(scan.call_count, 0)
        self.assertEqual(hooks.event_paths({"tool_name": "Bash", "tool_input": {"command": "cat src/screen.tsx"}}), [])
        scope.disable(self.project)
        self.assertFalse(scope.enabled(self.project))

    def test_detector_exit_contract_and_url_mode(self):
        for native_code in (0, 2, 1):
            result = subprocess.CompletedProcess([], native_code, '[{"rule":"x"}]\n', "")
            stdout = io.StringIO()
            with patch.object(cli, "invoke", return_value=result) as call, redirect_stdout(stdout):
                code = cli.main(["detect", "--project", str(self.project), "src/screen.tsx"])
            self.assertEqual(code, native_code)
            self.assertEqual(stdout.getvalue(), result.stdout)
            self.assertEqual(call.call_args.args[0][:2], ["detect", "--json"])
        with patch.object(cli, "invoke", return_value=subprocess.CompletedProcess([], 0, "[]\n", "")) as call, redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["detect", "--project", str(self.project), "--url", "http://localhost:3000"]), 0)
            self.assertEqual(call.call_args.args[0][-1], "http://localhost:3000")

    def test_patch_string_and_sensitive_generated_paths(self):
        patch_event = {"tool_name": "functions.apply_patch", "tool_input": "*** Update File: src/screen.tsx\n*** Add File: src/new.tsx\n"}
        self.assertEqual(hooks.event_paths(patch_event), ["src/screen.tsx", "src/new.tsx"])
        (self.project / "node_modules").mkdir()
        (self.project / "node_modules" / "library.tsx").write_text("x")
        self.assertIsNone(scope.allowed_file(self.project, "node_modules/library.tsx"))
        (self.project / "src" / "credentials.tsx").write_text("x")
        self.assertIsNone(scope.allowed_file(self.project, "src/credentials.tsx"))

    def test_codex_stop_is_nonblocking_message(self):
        event = {"turn_id": "turn-1", "session_id": "session-1", "cwd": str(self.project)}
        output = io.StringIO()
        with patch("sys.stdin", io.StringIO(json.dumps(event))), patch.object(cli, "handle", return_value="Review a finding"), redirect_stdout(output):
            self.assertEqual(cli.main(["hook", "stop", "--project", str(self.project)]), 0)
        self.assertEqual(json.loads(output.getvalue()), {"systemMessage": "Review a finding"})

    def test_project_hook_install_preserves_other_entries_and_is_idempotent(self):
        codex = self.project / ".codex" / "hooks.json"
        claude = self.project / ".claude" / "settings.json"
        codex.parent.mkdir()
        claude.parent.mkdir()
        original_codex = {"custom": {"keep": True}, "hooks": {"PostToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "echo keep"}]}]}}
        original_claude = {"permissions": {"allow": ["Read"]}, "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo another"}]}]}}
        codex.write_text(json.dumps(original_codex))
        claude.write_text(json.dumps(original_claude))
        with patch.object(config, "verified_engine"), patch.object(config, "plugin_root", return_value=self.plugin):
            config.install_hooks(self.project, "both")
            first_codex = codex.read_text()
            first_claude = claude.read_text()
            config.install_hooks(self.project, "both")
            self.assertEqual(codex.read_text(), first_codex)
            self.assertEqual(claude.read_text(), first_claude)
            self.assertTrue(scope.enabled(self.project))
            self.assertIn("echo keep", first_codex)
            self.assertIn("echo another", first_claude)
            self.assertIn("Read", first_claude)
            self.assertIn("--project " + str(self.project), first_codex)
            config.remove_hooks(self.project, "both")
        self.assertEqual(json.loads(codex.read_text()), original_codex)
        self.assertEqual(json.loads(claude.read_text()), original_claude)
        self.assertFalse(scope.enabled(self.project))
        self.assertGreaterEqual(len(list(codex.parent.glob("hooks.json.bak-*"))), 1)

    def test_hook_migration_replaces_only_exact_owned_commands_and_keeps_venv_path(self):
        codex = self.project / ".codex" / "hooks.json"
        codex.parent.mkdir()
        launcher = self.plugin / "scripts" / "design_runtime.py"
        old = f"/opt/homebrew/bin/python3.12 {launcher} hook post --project {self.project}"
        other = old + " --other-owner"
        codex.write_text(json.dumps({"hooks": {"PostToolUse": [
            {"hooks": [{"type": "command", "command": old},
                       {"type": "command", "command": other},
                       {"type": "command", "command": "echo keep"}]}
        ]}}))
        venv_python = self.base / "venv" / "bin" / "python3"
        with patch.object(config, "verified_engine"), patch.object(config, "plugin_root", return_value=self.plugin), \
             patch.object(config.sys, "executable", str(venv_python)):
            config.install_hooks(self.project, "codex")
            handlers = [handler for group in json.loads(codex.read_text())["hooks"]["PostToolUse"]
                        for handler in group["hooks"]]
            commands = [handler["command"] for handler in handlers]
            self.assertNotIn(old, commands)
            self.assertIn(other, commands)
            self.assertIn("echo keep", commands)
            self.assertEqual(sum(command.startswith(str(venv_python) + " ") for command in commands), 1)
            config.remove_hooks(self.project, "codex")
            remaining = [handler["command"] for group in json.loads(codex.read_text())["hooks"]["PostToolUse"]
                         for handler in group["hooks"]]
            self.assertEqual(remaining, [other, "echo keep"])
            self.assertEqual(shlex.split(config.owned_command(self.project, "post"))[0], str(venv_python))

    def test_marker_only_detects_legacy_owned_command(self):
        codex = self.project / ".codex" / "hooks.json"
        codex.parent.mkdir()
        old = f"/opt/homebrew/bin/python3.12 {self.plugin}/scripts/design_runtime.py hook stop --project {self.project}"
        codex.write_text(json.dumps({"hooks": {"Stop": [{"hooks": [{"type": "command", "command": old}]}]}}))
        with patch.object(config, "verified_engine"), patch.object(config, "plugin_root", return_value=self.plugin):
            with self.assertRaisesRegex(ValueError, "Owned project-local hooks already exist"):
                config.install_marker_only(self.project)

    def test_marker_only_opt_in_preserves_host_configs_and_is_reversible(self):
        codex = self.project / ".codex" / "hooks.json"
        codex.parent.mkdir()
        original = '{"hooks":{"Stop":[{"hooks":[{"type":"command","command":"echo keep"}]}]}}'
        codex.write_text(original)
        with patch.object(config, "verified_engine") as verify, redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["install-hooks", "--project", str(self.project), "--marker-only"]), 0)
            self.assertEqual(cli.main(["install-hooks", "--project", str(self.project), "--marker-only"]), 0)
            self.assertEqual(cli.main(["remove-hooks", "--project", str(self.project), "--marker-only"]), 0)
        self.assertEqual(verify.call_count, 2)
        self.assertFalse(scope.enabled(self.project))
        self.assertEqual(codex.read_text(), original)
        self.assertFalse((self.project / ".claude" / "settings.json").exists())
        self.assertEqual(list(codex.parent.glob("hooks.json.bak-*")), [])

    def test_marker_only_refuses_duplicate_owned_project_hooks(self):
        with patch.object(config, "verified_engine"), patch.object(config, "plugin_root", return_value=self.plugin):
            config.install_hooks(self.project, "codex")
            with self.assertRaisesRegex(ValueError, "Owned project-local hooks already exist"):
                config.install_marker_only(self.project)
            config.remove_hooks(self.project, "codex")
            self.assertTrue(config.install_marker_only(self.project).is_file())

    def test_invalid_existing_host_config_prevents_install(self):
        codex = self.project / ".codex" / "hooks.json"
        codex.parent.mkdir()
        codex.write_text("{ invalid")
        with patch.object(config, "verified_engine"):
            with self.assertRaises(ValueError):
                config.install_hooks(self.project, "codex")
        self.assertFalse(scope.enabled(self.project))
        self.assertEqual(codex.read_text(), "{ invalid")


if __name__ == "__main__":
    unittest.main()
