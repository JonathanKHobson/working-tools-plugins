"""Gateway framing, native content pass-through, and process cleanup."""

import json
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


GATEWAY = Path(__file__).resolve().parents[1] / "scripts/artcraft_gateway.py"
SPEC = importlib.util.spec_from_file_location("artcraft_gateway", GATEWAY)
gateway = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gateway)
FAKE_CLI = '''#!/usr/bin/env python3
import json,sys
for line in sys.stdin:
    msg=json.loads(line)
    if "id" not in msg: continue
    ident=msg["id"]
    if msg["method"] == "initialize":
        print(json.dumps({"jsonrpc":"2.0","method":"notifications/message","params":{"level":"info","data":"ready"}}),flush=True)
        result={"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"fake","version":"1"}}
    elif msg["method"] == "tools/list":
        result={"tools":[{"name":"picture","inputSchema":{"type":"object","properties":{}}}]}
    else:
        result={"content":[{"type":"image","mimeType":"image/png","data":"aGVsbG8="}],"isError":False}
    print(json.dumps({"jsonrpc":"2.0","id":ident,"result":result}),flush=True)
'''


class GatewayProtocolTest(unittest.TestCase):
    def test_new_app_native_routes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            expected = {
                "wordcraft": (["mcp"], ["mcp", "--connect", "127.0.0.1:7981"]),
                "soundcraft": (["mcp"], ["mcp", "--connect", "7801"]),
                "cadcraft": (["mcp"], ["mcp", "--connect", "127.0.0.1:7979"]),
            }
            for app, (headless, live) in expected.items():
                with self.subTest(app=app):
                    self.assertIn(app, gateway.APPS)
                    self.assertEqual(gateway.native_args(app, "headless", root, {}), headless)
                    self.assertEqual(gateway.native_args(app, "live", root, {}), live)
                    self.assertIn("run", gateway.CLI_COMMANDS[app])
            self.assertEqual(gateway.native_args("soundcraft", "headless", root, {"demo": True}),
                             ["mcp", "--demo"])
            self.assertEqual(gateway.native_args("wordcraft", "headless", root, {"author": "Kyle"}),
                             ["mcp", "--author", "Kyle"])

    def test_new_app_session_cleanup(self):
        for app in ("wordcraft", "soundcraft", "cadcraft"):
            with self.subTest(app=app), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                binary = root / "cli" / app / f"{app}-cli"
                binary.parent.mkdir(parents=True)
                binary.write_text(FAKE_CLI)
                binary.chmod(0o755)
                project = root / "project"
                project.mkdir()
                env = dict(os.environ, ARTCRAFT_HOME=str(root), PYTHONDONTWRITEBYTECODE="1")
                proc = subprocess.Popen(["python3", str(GATEWAY)], stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
                try:
                    proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                                 "params": {"name": "open_session", "arguments": {
                                                     "app": app, "mode": "headless", "project_root": str(project)}}}) + "\n")
                    proc.stdin.flush()
                    opened = json.loads(proc.stdout.readline())["result"]
                    child_pid = json.loads(opened["content"][0]["text"])["pid"]
                    proc.stdin.close()
                    self.assertEqual(proc.wait(timeout=8), 0)
                    with self.assertRaises(ProcessLookupError):
                        os.kill(child_pid, 0)
                    if app == "cadcraft":
                        self.assertTrue((project / ".artcraft-config/cadcraft").is_dir())
                finally:
                    if proc.poll() is None:
                        proc.terminate()
                        proc.wait(timeout=5)
                    proc.stdout.close()
                    proc.stderr.close()
                    if not proc.stdin.closed:
                        proc.stdin.close()

    def test_native_notification_image_and_eof_cleanup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            binary = root / "cli/pdfcraft/pdfcraft-cli"
            binary.parent.mkdir(parents=True)
            binary.write_text(FAKE_CLI)
            binary.chmod(0o755)
            project = root / "project"
            project.mkdir()
            env = dict(os.environ, ARTCRAFT_HOME=str(root), PYTHONDONTWRITEBYTECODE="1")
            proc = subprocess.Popen(["python3", str(GATEWAY)], stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)

            def call(ident, method, params):
                proc.stdin.write(json.dumps({"jsonrpc": "2.0", "id": ident,
                                             "method": method, "params": params}) + "\n")
                proc.stdin.flush()
                reply = json.loads(proc.stdout.readline())
                self.assertEqual(reply["id"], ident)
                return reply["result"]

            try:
                call(1, "initialize", {"protocolVersion": "2024-11-05"})
                opened = call(2, "tools/call", {"name": "open_session", "arguments": {
                    "app": "pdfcraft", "mode": "headless", "project_root": str(project)}})
                child_pid = json.loads(opened["content"][0]["text"])["pid"]
                tools = call(3, "tools/call", {"name": "native_tools", "arguments": {}})
                self.assertEqual(json.loads(tools["content"][0]["text"])["tools"][0]["name"], "picture")
                output = call(4, "tools/call", {"name": "native_call", "arguments": {
                    "name": "picture", "arguments": {}}})
                self.assertEqual(output["content"], [{"type": "image", "mimeType": "image/png", "data": "aGVsbG8="}])
                proc.stdin.close()
                self.assertEqual(proc.wait(timeout=8), 0)
                with self.assertRaises(ProcessLookupError):
                    os.kill(child_pid, 0)
            finally:
                if proc.poll() is None:
                    proc.terminate()
                    proc.wait(timeout=5)
                proc.stdout.close()
                proc.stderr.close()
                if not proc.stdin.closed:
                    proc.stdin.close()


if __name__ == "__main__":
    unittest.main()
