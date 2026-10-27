"""Exercise hook transport and fail-open behavior without launching Codex."""

import os
import json
from pathlib import Path
import subprocess
import sys
import shutil
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "codex_work_start.py"


class WorkStartTests(unittest.TestCase):
    def run_hook(self, payload):
        raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        result = subprocess.run(
            [sys.executable, "-I", str(SCRIPT)], input=raw,
            capture_output=True, timeout=3, check=True,
            env=dict(os.environ, WORK_MANAGEMENT_CONTEXT_OPT_IN="1"),
        )
        self.assertEqual(result.stderr, b"")
        return result.stdout

    def test_no_recipient_opt_in_emits_no_context(self):
        env=dict(os.environ);env.pop('WORK_MANAGEMENT_CONTEXT_OPT_IN',None)
        result=subprocess.run([sys.executable,'-I',str(SCRIPT)],input=b'{"hook_event_name":"UserPromptSubmit","prompt":"Do work"}',capture_output=True,env=env,check=True)
        self.assertEqual(result.stdout,b'')

    def test_valid_prompt_returns_nonblocking_native_context(self):
        output = json.loads(self.run_hook({
            "hook_event_name": "UserPromptSubmit", "prompt": "Organize this project.",
        }))
        self.assertTrue(output["continue"])
        self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")
        self.assertIsInstance(output["hookSpecificOutput"]["additionalContext"], str)
        self.assertLess(len(output["hookSpecificOutput"]["additionalContext"]), 4000)
        self.assertNotIn("decision", output)

    def test_prompt_and_transcript_are_not_echoed_or_interpreted(self):
        first = self.run_hook({
            "hook_event_name": "UserPromptSubmit", "prompt": "UNTRUSTED_SENTINEL",
            "transcript_path": "/nonexistent/path", "cwd": "/nonexistent/cwd",
        })
        second = self.run_hook({
            "hook_event_name": "UserPromptSubmit", "prompt": "Thanks!",
        })
        self.assertEqual(first, second)
        self.assertNotIn(b"UNTRUSTED_SENTINEL", first)

    def test_missing_empty_or_wrong_type_prompt_is_quiet(self):
        for value in (None, "", "  ", [], {}, 4):
            with self.subTest(value=value):
                self.assertEqual(self.run_hook({
                    "hook_event_name": "UserPromptSubmit", "prompt": value,
                }), b"")

    def test_wrong_event_is_quiet(self):
        for event in (None, "SessionStart", "Stop", "PreToolUse"):
            with self.subTest(event=event):
                self.assertEqual(self.run_hook({
                    "hook_event_name": event, "prompt": "Do work",
                }), b"")

    def test_malformed_and_oversized_input_fail_open(self):
        for raw in (b"", b"{", b"[]", b"null", b"\xff", b"x" * 1_048_577):
            with self.subTest(size=len(raw)):
                self.assertEqual(self.run_hook(raw), b"")


class PortableWorkStartTests(unittest.TestCase):
    def run_portable(self, script, payload):
        env = dict(os.environ)
        env.pop("WORK_MANAGEMENT_CONTEXT_OPT_IN", None)
        raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        result = subprocess.run([sys.executable, "-I", str(script), "--portable"],
                                input=raw, capture_output=True, timeout=3, check=True, env=env)
        self.assertEqual(result.stderr, b"")
        return result.stdout

    def test_portable_route_relocates_without_private_context(self):
        with tempfile.TemporaryDirectory(prefix="portable-hook-") as folder:
            root = Path(folder) / "relocated package"
            script = root / "scripts" / SCRIPT.name
            script.parent.mkdir(parents=True)
            shutil.copyfile(SCRIPT, script)
            output = json.loads(self.run_portable(script, {
                "hook_event_name": "UserPromptSubmit", "prompt": "Do work",
            }))
            context = output["hookSpecificOutput"]["additionalContext"]
            self.assertIn(str(root / "skills/tool-workflow-routing/SKILL.md"), context)
            self.assertLess(len(context), 500)
            for private in ("get_goal", "Delegation checkpoint", "Chat naming", "usage", "Kyle"):
                self.assertNotIn(private, context)

    def test_portable_invalid_input_is_quiet(self):
        for payload in (b"", b"{", b"[]", b"\xff", {"hook_event_name": "Stop", "prompt": "Do work"}):
            with self.subTest(payload=str(payload)[:20]):
                self.assertEqual(self.run_portable(SCRIPT, payload), b"")

    def test_templates_use_portable_mode(self):
        root = SCRIPT.parent.parent
        for filename in ("hooks.json", "claude-hooks.json"):
            config = json.loads((root / "optional-hooks" / filename).read_text())
            hooks = [hook for group in config["hooks"]["UserPromptSubmit"] for hook in group["hooks"]]
            route = next(hook for hook in hooks if "codex_work_start.py" in hook["command"])
            self.assertTrue(route["command"].endswith(" --portable"))


if __name__ == "__main__":
    unittest.main()
