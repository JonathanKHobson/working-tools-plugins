import json
from pathlib import Path
import subprocess
import sys
import shutil
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/editorial_context.py"


class EditorialContextTests(unittest.TestCase):
    def run_hook(self, payload):
        result = subprocess.run([sys.executable, str(SCRIPT)], input=payload,
                                text=True, capture_output=True, timeout=3)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_semantic_route_without_keyword_requirement(self):
        for prompt in ("Make this less crowded.", "Turn these notes into something clients can use."):
            data = json.loads(self.run_hook(json.dumps({
                "hook_event_name": "UserPromptSubmit", "prompt": prompt})))
            context = data["hookSpecificOutput"]["additionalContext"]
            self.assertIn("natural-prose-editor", context)
            self.assertIn("any medium", context)
            self.assertIn(str(SCRIPT.parent.parent / "skills/natural-prose-editor/SKILL.md"), context)
            self.assertNotIn(prompt, context)
            self.assertLess(len(context), 750)
            self.assertNotIn("decision", data)

    def test_other_events_are_silent(self):
        for event in ("Stop", "PreToolUse", "SessionStart"):
            self.assertEqual(self.run_hook(json.dumps({"hook_event_name": event})), "")

    def test_malformed_and_oversized_inputs_are_silent(self):
        for value in ("", "oops", "[]", '{"hook_event_name":"UserPromptSubmit",' + " " * 64000):
            self.assertEqual(self.run_hook(value), "")

    def test_claude_prompt_hook_uses_portable_package_root_and_existing_script(self):
        root = SCRIPT.parent.parent
        hook_file = root / "hooks/claude-hooks.json"
        config = json.loads(hook_file.read_text())
        self.assertEqual(set(config["hooks"]), {"UserPromptSubmit"})
        command = config["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
        self.assertEqual(command, 'python3 -I "${CLAUDE_PLUGIN_ROOT}/scripts/editorial_context.py"')
        self.assertTrue((root / "scripts/editorial_context.py").is_file())
        self.assertNotIn("/Users/", command)
        self.assertNotIn("gate.py", command)

    def test_editorial_route_computes_relocated_skill_path(self):
        with tempfile.TemporaryDirectory(prefix="editorial hook ") as folder:
            root = Path(folder).resolve() / "Writing Quality Studio"
            (root / "scripts").mkdir(parents=True)
            script = root / "scripts/editorial_context.py"
            shutil.copyfile(SCRIPT, script)
            result = subprocess.run([sys.executable, "-I", str(script)],
                                    input=json.dumps({"hook_event_name": "UserPromptSubmit", "prompt": "Draft copy"}),
                                    text=True, capture_output=True, timeout=3, check=True)
            self.assertEqual(result.stderr, "")
            context = json.loads(result.stdout)["hookSpecificOutput"]["additionalContext"]
            self.assertIn(str(root / "skills/natural-prose-editor/SKILL.md"), context)
            self.assertNotIn(str(SCRIPT.parent.parent), context)

    def test_codex_public_hook_contains_only_portable_editorial_route(self):
        config = json.loads((SCRIPT.parent.parent / "optional-hooks/codex-hooks.json").read_text())
        self.assertEqual(set(config["hooks"]), {"UserPromptSubmit"})
        entries = config["hooks"]["UserPromptSubmit"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(len(entries[0]["hooks"]), 1)
        hook = entries[0]["hooks"][0]
        self.assertEqual(hook["command"], 'python3 -I "${PLUGIN_ROOT}/scripts/editorial_context.py"')
        self.assertEqual(hook["commandWindows"], 'python -I "${PLUGIN_ROOT}/scripts/editorial_context.py"')
        text = json.dumps(config)
        for private_value in ("/Users/", "/opt/", "gmail", "gate.py", "PreToolUse"):
            self.assertNotIn(private_value, text)


if __name__ == "__main__":
    unittest.main()
