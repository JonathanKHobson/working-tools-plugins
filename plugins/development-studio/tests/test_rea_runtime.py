"""Synthetic, non-executing checks for the pinned REA launcher boundary."""

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/rea_runtime.py"
spec = importlib.util.spec_from_file_location("rea_runtime_under_test", SCRIPT)
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


class ReaRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="rea-launcher-test-")
        self.addCleanup(self.scratch.cleanup)
        self.base = Path(self.scratch.name).resolve()
        self.root = self.base / "runtime"
        self.package = self.root / "node_modules/rea-agents"
        self.cli = self.package / "scripts/rea.mjs"
        self.cli.parent.mkdir(parents=True)
        self.cli.write_text("// inert fixture\n")
        (self.package / "package.json").write_text(
            json.dumps({"name": "rea-agents", "version": runtime.VERSION})
        )
        (self.root / "package.json").write_text("{}\n")
        (self.root / "package-lock.json").write_text("{}\n")
        self.node = self.base / "node-fixture"
        self.node.write_text("inert node fixture\n")
        self.inventory = self.base / "inventory.json"
        self.binding = {
            "version": runtime.VERSION,
            "runtime_root": str(self.root),
            "node": str(self.node),
            "cli": str(self.cli),
            "node_sha256": runtime.sha256(self.node),
            "integrity_file": str(self.inventory),
            "environment": {},
            "tool_path": [],
        }
        self.refresh_inventory()

    def refresh_inventory(self):
        paths = sorted(
            [p for p in (self.root / "node_modules").rglob("*") if p.is_file() or p.is_symlink()]
            + [self.root / "package.json", self.root / "package-lock.json"]
        )
        files = []
        for path in paths:
            files.append({
                "path": str(path.relative_to(self.root)),
                "kind": "symlink" if path.is_symlink() else "file",
                "value": os.readlink(path) if path.is_symlink() else runtime.sha256(path),
            })
        self.inventory.write_text(json.dumps({"files": files}))
        self.binding["integrity_sha256"] = runtime.sha256(self.inventory)

    def assert_refused(self):
        with self.assertRaises((ValueError, OSError)):
            runtime.verify(self.binding)

    def test_baseline_fixture_verifies_without_real_binding_or_runtime(self):
        self.assertEqual(runtime.verify(self.binding), (self.root, self.node, self.cli))

    def test_changed_node_is_rejected(self):
        self.node.write_text("changed interpreter\n")
        self.assert_refused()

    def test_changed_package_file_is_rejected(self):
        self.cli.write_text("// changed launcher\n")
        self.assert_refused()

    def test_added_package_file_is_rejected(self):
        (self.package / "extra.js").write_text("// unreviewed\n")
        self.assert_refused()

    def test_added_symlink_is_rejected(self):
        (self.package / "extra-link").symlink_to("scripts/rea.mjs")
        self.assert_refused()

    def test_symlink_replacing_hashed_file_is_rejected(self):
        other = self.package / "scripts/other.mjs"
        other.write_text("// inert\n")
        self.refresh_inventory()
        self.cli.unlink()
        self.cli.symlink_to("other.mjs")
        self.assert_refused()

    def test_declared_symlink_must_retain_its_target(self):
        target = self.package / "scripts/link.mjs"
        target.symlink_to("rea.mjs")
        other = self.package / "scripts/other.mjs"
        other.write_text("// inert\n")
        self.refresh_inventory()
        target.unlink()
        target.symlink_to("other.mjs")
        self.assert_refused()

    def test_symlink_escape_is_rejected_even_when_rehashed(self):
        outside = self.base / "outside.js"
        outside.write_text("// outside runtime\n")
        link = self.package / "escape.js"
        link.symlink_to(outside)
        self.refresh_inventory()
        self.assert_refused()

    def test_inventory_path_traversal_is_rejected_even_when_rehashed(self):
        data = json.loads(self.inventory.read_text())
        data["files"][0]["path"] = "../outside"
        self.inventory.write_text(json.dumps(data))
        self.binding["integrity_sha256"] = runtime.sha256(self.inventory)
        self.assert_refused()

    def test_clean_environment_excludes_inherited_decoy_secrets(self):
        inherited = {
            "OPENAI_API_KEY": "decoy-secret",
            "NODE_OPTIONS": "--require=/tmp/untrusted.js",
            "HOPPER_TARGET_PATH": "/tmp/private-target",
            "HTTPS_PROXY": "http://decoy.invalid",
            "HOME": "/tmp/decoy-home",
        }
        with mock.patch.dict(os.environ, inherited, clear=True):
            env = runtime.clean_environment(self.binding, self.root)
        for key in inherited:
            self.assertNotIn(key, env)
        self.assertEqual(env["TMPDIR"], str(self.root / "tmp"))

    def test_unreviewed_environment_key_and_nul_are_rejected(self):
        self.binding["environment"] = {"NODE_OPTIONS": "--require=/tmp/untrusted.js"}
        with self.assertRaises(ValueError):
            runtime.clean_environment(self.binding, self.root)
        self.binding["environment"] = {"REA_ANALYSIS_PROVIDER": "ghidra\x00evil"}
        with self.assertRaises(ValueError):
            runtime.clean_environment(self.binding, self.root)

    def test_tool_path_must_be_an_existing_absolute_directory(self):
        for bad in ("relative/bin", str(self.base / "missing"), str(self.node)):
            with self.subTest(path=bad):
                self.binding["tool_path"] = [bad]
                with self.assertRaises(ValueError):
                    runtime.clean_environment(self.binding, self.root)

    def test_tool_path_cannot_contain_path_separator(self):
        # A literal colon is legal in a macOS directory name, but PATH treats
        # it as two entries and would search directories absent from binding.
        directory = self.base / "reviewed:unreviewed"
        directory.mkdir()
        self.binding["tool_path"] = [str(directory)]
        with self.assertRaises(ValueError):
            runtime.clean_environment(self.binding, self.root)

    def test_tmp_symlink_and_world_readable_directory_block_launch(self):
        home, plugin = self.prepare_main()
        tmp = self.root / "tmp"
        outside = self.base / "outside-tmp"
        outside.mkdir()
        with mock.patch.object(runtime.Path, "home", return_value=home), \
             mock.patch.object(runtime, "__file__", str(plugin / "scripts/rea_runtime.py")), \
             mock.patch.object(runtime.os, "chdir"), \
             mock.patch.object(runtime.os, "execve") as execve:
            tmp.symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                runtime.main(["--mcp"])
            execve.assert_not_called()
            tmp.unlink()
            tmp.mkdir(mode=0o755)
            tmp.chmod(0o755)
            with self.assertRaises(ValueError):
                runtime.main(["--mcp"])
            execve.assert_not_called()

    def prepare_main(self):
        home = self.base / "home"
        config = home / ".config/studio-tools/rea.json"
        config.parent.mkdir(parents=True)
        config.write_text(json.dumps(self.binding))
        plugin = self.base / "plugin"
        (plugin / "scripts").mkdir(parents=True)
        (plugin / "docs").mkdir()
        (plugin / "docs/rea-tool-catalog.json").write_text(
            json.dumps({"cli_commands": ["analyze", "decompile",
                                         "analyze-javascript-application"]})
        )
        self.binding["catalog_sha256"] = runtime.sha256(plugin / "docs/rea-tool-catalog.json")
        config.write_text(json.dumps(self.binding))
        return home, plugin

    def test_changed_catalog_cannot_enable_administrative_cli(self):
        home, plugin = self.prepare_main()
        (plugin / "docs/rea-tool-catalog.json").write_text(json.dumps({"cli_commands": ["setup"]}))
        with mock.patch.object(runtime.Path, "home", return_value=home), \
             mock.patch.object(runtime, "__file__", str(plugin / "scripts/rea_runtime.py")), \
             mock.patch.object(runtime.os, "execve") as execve:
            with self.assertRaises(ValueError):
                runtime.main(["cli", "setup"])
            execve.assert_not_called()

    def test_special_file_is_rejected_without_reading_it(self):
        self.cli.unlink()
        os.mkfifo(self.cli)
        self.assert_refused()

    def test_mcp_launch_passes_only_clean_environment_and_fixed_command(self):
        home, plugin = self.prepare_main()
        with mock.patch.object(runtime.Path, "home", return_value=home), \
             mock.patch.object(runtime, "__file__", str(plugin / "scripts/rea_runtime.py")), \
             mock.patch.object(runtime.os, "chdir"), \
             mock.patch.object(runtime.os, "execve") as execve, \
             mock.patch.dict(os.environ, {"OPENAI_API_KEY": "decoy-secret"}, clear=True):
            self.assertEqual(runtime.main(["--mcp"]), None)
        executable, args, env = execve.call_args.args
        self.assertEqual(executable, str(self.node))
        self.assertEqual(args, [str(self.node), str(self.cli), "--mcp"])
        self.assertNotIn("OPENAI_API_KEY", env)
        self.assertNotIn("HOPPER_TARGET_PATH", env)

    def test_cli_allows_analysis_but_refuses_administration(self):
        home, plugin = self.prepare_main()
        with mock.patch.object(runtime.Path, "home", return_value=home), \
             mock.patch.object(runtime, "__file__", str(plugin / "scripts/rea_runtime.py")), \
             mock.patch.object(runtime.os, "chdir"), \
             mock.patch.object(runtime.os, "execve") as execve:
            runtime.main(["cli", "analyze-javascript-application", "--target", "owned.js"])
            self.assertEqual(execve.call_args.args[1][-4:],
                             [str(self.cli), "analyze-javascript-application", "--target", "owned.js"])
            for command in ("analyze", "decompile"):
                with self.subTest(command=command):
                    runtime.main(["cli", command, "owned.js"])
                    self.assertEqual(execve.call_args.args[1][-2:], [command, "owned.js"])
            execve.reset_mock()
            for bad in (["cli", "setup"], ["cli", "update"],
                        ["cli", "install"], ["cli", "uninstall"],
                        ["cli", "doctor"], ["cli", "completions"],
                        ["cli", "mcp"], ["cli"], ["--mcp", "setup"],
                        ["cli", "analyze", "--update"],
                        ["cli", "analyze", "--update=all"],
                        ["cli", "decompile", "--mcp"],
                        ["cli", "decompile", "--mcp=true"],
                        ["cli", "--help", "--update"]):
                with self.subTest(args=bad), self.assertRaises(ValueError):
                    runtime.main(bad)
                execve.assert_not_called()


if __name__ == "__main__":
    unittest.main()
