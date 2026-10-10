import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock


LAUNCH_PATH = Path(__file__).resolve().parents[1] / "scripts" / "launch.py"
SPEC = importlib.util.spec_from_file_location("discord_launch", LAUNCH_PATH)
launch = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(launch)


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.python = self.root / "python"
        self.server = self.root / "server.py"
        self.database = self.root / "discord.sqlite"
        self.python.touch()
        self.python.chmod(0o755)
        self.server.touch()
        self.database.touch()
        self.config = self.root / "config.json"
        self.config.write_text(json.dumps({
            "python": str(self.python),
            "server_path": str(self.server),
            "db_path": str(self.database),
        }))

    def test_config_launches_existing_server_with_database_argument(self):
        with mock.patch.dict(os.environ, {"DISCORD_CONNECTOR_CONFIG": str(self.config)}, clear=True):
            with mock.patch.object(launch.os, "execv") as execv:
                self.assertEqual(launch.main(), 0)
        execv.assert_called_once_with(str(self.python.resolve()), [
            str(self.python.resolve()), str(self.server.resolve()), "--db-path", str(self.database.resolve())
        ])

    def test_environment_overrides_config_paths(self):
        other_server = self.root / "other-server.py"
        other_server.touch()
        with mock.patch.dict(os.environ, {
            "DISCORD_CONNECTOR_CONFIG": str(self.config),
            "DISCORD_CONNECTOR_SERVER": str(other_server),
        }, clear=True):
            with mock.patch.object(launch.os, "execv") as execv:
                self.assertEqual(launch.main(), 0)
        self.assertEqual(execv.call_args.args[1][1], str(other_server.resolve()))

    def test_missing_config_fails_without_launching_or_exposing_secrets(self):
        missing = self.root / "missing.json"
        stderr = io.StringIO()
        with mock.patch.dict(os.environ, {"DISCORD_CONNECTOR_CONFIG": str(missing)}, clear=True):
            with mock.patch.object(launch.os, "execv") as execv:
                with contextlib.redirect_stderr(stderr):
                    self.assertEqual(launch.main(), 2)
        execv.assert_not_called()
        self.assertIn("Missing Discord connector settings", stderr.getvalue())
        self.assertNotIn("token", stderr.getvalue().lower())


if __name__ == "__main__":
    unittest.main()
