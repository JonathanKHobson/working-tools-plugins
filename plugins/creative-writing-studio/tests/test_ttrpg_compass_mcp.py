"""Privacy and binding checks for the packaged TTRPG Compass launcher."""

import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


BRIDGE = Path(__file__).resolve().parents[1] / "scripts/ttrpg_compass_mcp.py"


class Launched(Exception):
    pass


class TtrpgBridgeTest(unittest.TestCase):
    def test_uses_fixed_binding_and_drops_inherited_personal_slot(self):
        spec = importlib.util.spec_from_file_location("ttrpg_bridge", BRIDGE)
        bridge = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bridge)
        with tempfile.TemporaryDirectory() as temporary_home:
            config_dir = Path(temporary_home) / ".config/studio-tools"
            config_dir.mkdir(parents=True)
            server = Path(temporary_home) / "server.py"
            server.write_text("# stub")
            (config_dir / "compass.json").write_text(json.dumps({
                "other-compass": {"server": "/wrong/server"},
                "ttrpg-compass": {"interpreter": sys.executable, "server": str(server), "args": ["--db-path", "/private/db"]},
            }))
            with patch.dict(os.environ, {"HOME": temporary_home, "TTRPG_COMPASS_PERSONAL_CAMPAIGN_CONFIG": "/inherited/private"}), \
                    patch.object(sys, "argv", [str(BRIDGE)]), \
                    patch.object(bridge.os, "chdir"), \
                    patch.object(bridge.os, "execve", side_effect=Launched) as launch:
                with self.assertRaises(Launched):
                    bridge.main()
        executable, argv, environment = launch.call_args.args
        self.assertEqual(executable, sys.executable)
        self.assertEqual(argv, [sys.executable, str(server.resolve()), "--db-path", "/private/db"])
        self.assertNotIn("TTRPG_COMPASS_PERSONAL_CAMPAIGN_CONFIG", environment)


if __name__ == "__main__":
    unittest.main()
