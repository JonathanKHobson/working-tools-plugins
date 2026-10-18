"""Offline invariants for the portable bounded Claude subscription helper."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
import subprocess
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "claude_worker.py"
SPEC = importlib.util.spec_from_file_location("claude_worker", SCRIPT)
claude_worker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(claude_worker)


class ClaudeWorkerTests(unittest.TestCase):
    def invoke(self, response, cli_args):
        calls = []
        auth = {
            "loggedIn": True,
            "authMethod": "claude.ai",
            "apiProvider": "firstParty",
            "subscriptionType": "pro",
        }

        def fake_run_json(cli, command, env, cwd, timeout, prompt=None):
            calls.append((cli, command, env, cwd, timeout, prompt))
            return auth if command == ["auth", "status"] else response

        stdout = io.StringIO()
        with (
            mock.patch.object(sys, "argv", [str(SCRIPT), "--cli", sys.executable, *cli_args]),
            mock.patch.object(sys.stdin, "isatty", return_value=False),
            mock.patch.object(claude_worker, "read_prompt", return_value="bounded task"),
            mock.patch.object(claude_worker, "run_json", side_effect=fake_run_json),
            mock.patch.dict("os.environ", {
                "ANTHROPIC_API_KEY": "must-not-pass",
                "CLAUDE_CODE_TOKEN": "must-not-pass",
                "CLAUDE_CONFIG_DIR": "/private/config",
                "CLAUDECODE": "1",
                "KEEP_ME": "ok",
            }, clear=True),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            claude_worker.main()
        return calls, stdout.getvalue()

    def test_effort_model_receipt_and_isolation(self):
        calls, output = self.invoke(
            {"subtype": "success", "result": "Reviewed result", "modelUsage": {"actual-model": {}}},
            ["--model", "opus", "--effort", "max", "--json"],
        )
        cli, command, env = calls[1][0], calls[1][1], calls[1][2]
        self.assertEqual(cli, Path(sys.executable))
        self.assertEqual(command[command.index("--model") + 1], "opus")
        self.assertEqual(command[command.index("--effort") + 1], "max")
        for key in ("ANTHROPIC_API_KEY", "CLAUDE_CODE_TOKEN", "CLAUDE_CONFIG_DIR", "CLAUDECODE"):
            self.assertNotIn(key, env)
        self.assertEqual(env["KEEP_ME"], "ok")
        self.assertIn("--tools", command)
        self.assertEqual(command[command.index("--tools") + 1], "")
        self.assertIn("--strict-mcp-config", command)
        self.assertEqual(command[command.index("--mcp-config") + 1], '{"mcpServers":{}}')
        receipt = json.loads(output)
        self.assertEqual(receipt["requestedModel"], "opus")
        self.assertEqual(receipt["requestedEffort"], "max")
        self.assertEqual(receipt["models"], ["actual-model"])

    def test_default_effort_remains_low(self):
        calls, _ = self.invoke({"subtype": "success", "result": "Done"}, [])
        command = calls[1][1]
        self.assertEqual(command[command.index("--effort") + 1], "low")

    def test_empty_success_response_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "successful text result"):
            self.invoke({"subtype": "success", "result": "  \n"}, [])

    def test_unsupported_effort_is_rejected(self):
        with self.assertRaises(SystemExit):
            self.invoke({"subtype": "success", "result": "unused"}, ["--effort", "minimal"])

    def test_run_json_timeout_returns_promptly(self):
        with tempfile.TemporaryDirectory(prefix="claude-worker-timeout-test-") as folder:
            cli = Path(folder) / "slow-cli"
            cli.write_text("#!/bin/sh\nsleep 60\n")
            cli.chmod(0o700)
            started = time.monotonic()
            with self.assertRaises(subprocess.TimeoutExpired):
                claude_worker.run_json(cli, ["ignored"], {}, folder, 0.05, "prompt")
            self.assertLess(time.monotonic() - started, 2.0)


if __name__ == "__main__":
    unittest.main()
