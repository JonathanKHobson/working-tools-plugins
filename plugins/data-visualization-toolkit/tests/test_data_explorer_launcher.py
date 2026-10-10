"""Unit tests for the Data Explorer launcher (scripts/data_explorer_mcp.py).

Tests dynamically import the sibling launcher script and exercise
``launch_spec`` directly. No process is ever executed and no data directory
is ever created.
"""

import importlib.util
import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
LAUNCHER_PATH = THIS_DIR.parent / "scripts/data_explorer_mcp.py"


def _load_launcher_module():
    spec = importlib.util.spec_from_file_location("data_explorer_mcp", LAUNCHER_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


launcher = _load_launcher_module()


def _make_executable(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("#!/bin/sh\n")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def _make_root_with_server(root: Path) -> Path:
    server = root / "runtime" / "data-explorer" / "server.py"
    server.parent.mkdir(parents=True, exist_ok=True)
    server.write_text("# bundled server\n")
    return server


def _make_bundled_venv_python(root: Path) -> Path:
    rel = ("Scripts", "python.exe") if os.name == "nt" else ("bin", "python")
    python = root / ".runtime" / "venv" / rel[0] / rel[1]
    _make_executable(python)
    return python


class LaunchSpecTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self.root = self.base / "pkg"
        self.home = self.base / "home"
        self.root.mkdir()
        self.home.mkdir()
        self.server = _make_root_with_server(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def write_config(self, payload) -> Path:
        config_dir = self.home / ".config" / "studio-tools"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path = config_dir / "data-explorer.json"
        config_path.write_text(json.dumps(payload))
        return config_path

    def assertNoDataDirCreated(self, data_dir: Path):
        self.assertFalse(data_dir.exists(), f"data dir must not be created: {data_dir}")

    def test_legacy_private_binding_preserves_interpreter_and_data_dir_with_bundled_server(self):
        private_interpreter = self.base / "venvs" / "legacy" / "bin" / "python"
        _make_executable(private_interpreter)
        private_data_dir = self.base / "legacy-data"

        self.write_config(
            {
                "interpreter": str(private_interpreter),
                "server": "/old/server/path.py",  # must be read but never executed
                "data_dir": str(private_data_dir),
            }
        )

        interpreter, argv, child_env = launcher.launch_spec(
            root=self.root, env={}, home=self.home
        )

        self.assertEqual(interpreter, str(private_interpreter))
        self.assertEqual(
            argv,
            [
                str(private_interpreter),
                str(self.server),
                "--data-dir",
                str(private_data_dir),
                "--stdio",
            ],
        )
        self.assertNotIn("/old/server/path.py", argv)
        self.assertEqual(child_env["PYTHONDONTWRITEBYTECODE"], "1")
        self.assertNoDataDirCreated(private_data_dir)

    def test_full_environment_override_wins_over_binding_and_bundled_defaults(self):
        binding_interpreter = self.base / "venvs" / "binding" / "bin" / "python"
        _make_executable(binding_interpreter)
        self.write_config(
            {
                "interpreter": str(binding_interpreter),
                "server": "/unused.py",
                "data_dir": str(self.base / "binding-data"),
            }
        )

        override_interpreter = self.base / "override" / "bin" / "python"
        _make_executable(override_interpreter)
        override_data_dir = self.base / "override-data"

        env = {
            "DATA_EXPLORER_PYTHON": str(override_interpreter),
            "DATA_EXPLORER_DATA_DIR": str(override_data_dir),
        }

        interpreter, argv, _ = launcher.launch_spec(root=self.root, env=env, home=self.home)

        self.assertEqual(interpreter, str(override_interpreter))
        self.assertEqual(
            argv,
            [
                str(override_interpreter),
                str(self.server),
                "--data-dir",
                str(override_data_dir),
                "--stdio",
            ],
        )
        self.assertNoDataDirCreated(override_data_dir)

    def test_complete_environment_overrides_ignore_malformed_default_but_not_explicit_binding(self):
        config_path = self.write_config({})
        config_path.write_text("not valid JSON")
        interpreter_path = self.base / "override" / "bin" / "python"
        _make_executable(interpreter_path)
        data_dir = self.base / "override-data"
        env = {"DATA_EXPLORER_PYTHON": str(interpreter_path),
               "DATA_EXPLORER_DATA_DIR": str(data_dir)}
        interpreter, argv, _ = launcher.launch_spec(root=self.root, env=env, home=self.home)
        self.assertEqual(interpreter, str(interpreter_path))
        self.assertIn(str(data_dir), argv)
        self.assertNoDataDirCreated(data_dir)
        with self.assertRaises(launcher.LaunchError):
            launcher.launch_spec(root=self.root, env=dict(env, DATA_EXPLORER_BINDING=str(config_path)), home=self.home)

    def test_no_binding_file_uses_bundled_interpreter_and_default_data_dir(self):
        bundled_python = _make_bundled_venv_python(self.root)

        interpreter, argv, _ = launcher.launch_spec(root=self.root, env={}, home=self.home)

        expected_data_dir = self.home / ".local" / "share" / "working-tools" / "data-explorer"
        self.assertEqual(interpreter, str(bundled_python))
        self.assertEqual(
            argv,
            [
                str(bundled_python),
                str(self.server),
                "--data-dir",
                str(expected_data_dir),
                "--stdio",
            ],
        )
        self.assertNoDataDirCreated(expected_data_dir)

    def test_xdg_data_home_used_when_set_and_no_binding(self):
        _make_bundled_venv_python(self.root)
        xdg = self.base / "xdg"
        _, argv, _ = launcher.launch_spec(
            root=self.root, env={"XDG_DATA_HOME": str(xdg)}, home=self.home
        )
        expected = xdg / "working-tools" / "data-explorer"
        self.assertIn(str(expected), argv)
        self.assertNoDataDirCreated(expected)

    def test_malformed_binding_raises_launch_error(self):
        self.write_config(["not", "an", "object"])
        with self.assertRaises(launcher.LaunchError):
            launcher.launch_spec(root=self.root, env={}, home=self.home)

    def test_explicit_missing_binding_is_rejected(self):
        self.write_config(
            {
                "interpreter": str(self.base / "irrelevant"),
                "server": "/unused.py",
                "data_dir": str(self.base / "irrelevant-data"),
            }
        )
        with self.assertRaises(launcher.LaunchError):
            launcher.launch_spec(
                root=self.root, env={"DATA_EXPLORER_BINDING": str(self.base / "missing.json")}, home=self.home
            )

    def test_explicit_missing_binding_with_no_config_file_is_rejected(self):
        with self.assertRaises(launcher.LaunchError):
            launcher.launch_spec(
                root=self.root, env={"DATA_EXPLORER_BINDING": str(self.base / "missing.json")}, home=self.home
            )

    def test_relative_interpreter_override_is_rejected(self):
        with self.assertRaises(launcher.LaunchError):
            launcher.launch_spec(
                root=self.root,
                env={"DATA_EXPLORER_PYTHON": "relative/python"},
                home=self.home,
            )

    def test_relative_binding_interpreter_is_rejected(self):
        self.write_config(
            {
                "interpreter": "relative/python",
                "server": "/unused.py",
                "data_dir": str(self.base / "data"),
            }
        )
        with self.assertRaises(launcher.LaunchError):
            launcher.launch_spec(root=self.root, env={}, home=self.home)

    def test_symlink_interpreter_spelling_is_preserved_not_resolved(self):
        real_interpreter = self.base / "real-venv" / "bin" / "python3.11"
        _make_executable(real_interpreter)

        symlink_dir = self.base / "symlinked-venv" / "bin"
        symlink_dir.mkdir(parents=True)
        symlink_path = symlink_dir / "python"
        os.symlink(real_interpreter, symlink_path)

        self.write_config(
            {
                "interpreter": str(symlink_path),
                "server": "/unused.py",
                "data_dir": str(self.base / "data"),
            }
        )

        interpreter, argv, _ = launcher.launch_spec(root=self.root, env={}, home=self.home)

        self.assertEqual(interpreter, str(symlink_path))
        self.assertNotEqual(interpreter, str(real_interpreter))
        self.assertEqual(argv[0], str(symlink_path))


    def test_launch_spec_does_not_mutate_injected_env(self):
        _make_bundled_venv_python(self.root)
        original_env = {"SOME_VAR": "value"}
        launcher.launch_spec(root=self.root, env=original_env, home=self.home)
        self.assertEqual(original_env, {"SOME_VAR": "value"})


    def test_explicit_binding_is_a_file_path_and_environment_is_unchanged(self):
        interpreter_path = self.base / "selected" / "python"
        _make_executable(interpreter_path)
        binding = self.base / "alternate.json"
        data_dir = self.base / "selected-data"
        binding.write_text(json.dumps({"interpreter": str(interpreter_path), "data_dir": str(data_dir)}))
        env = {"DATA_EXPLORER_BINDING": str(binding), "EXISTING_SETTING": "kept"}
        before = dict(env)
        interpreter, argv, child = launcher.launch_spec(root=self.root, env=env, home=self.home)
        self.assertEqual(interpreter, str(interpreter_path))
        self.assertEqual(argv[3], str(data_dir))
        self.assertEqual(env, before)
        self.assertEqual(child["EXISTING_SETTING"], "kept")
        self.assertNoDataDirCreated(data_dir)

    def test_empty_override_and_relative_data_root_are_rejected(self):
        _make_bundled_venv_python(self.root)
        for env in ({"DATA_EXPLORER_PYTHON": ""}, {"DATA_EXPLORER_DATA_DIR": "relative"}, {"XDG_DATA_HOME": "relative"}):
            with self.subTest(env=env), self.assertRaises(launcher.LaunchError):
                launcher.launch_spec(root=self.root, env=env, home=self.home)


if __name__ == "__main__":
    unittest.main()
