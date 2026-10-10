"""Check universal hook transport without asserting model comprehension."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "decision_review_hint.py"

class DecisionHintTests(unittest.TestCase):
    def call(self, payload):
        raw = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        with tempfile.TemporaryDirectory() as cwd:
            p = subprocess.run([sys.executable, "-I", str(SCRIPT)], input=raw,
                               cwd=cwd, capture_output=True, timeout=3, check=True)
            self.assertEqual(list(Path(cwd).iterdir()), [])
        self.assertEqual(p.stderr, b"")
        return p.stdout

    def prompt(self, text):
        return self.call({"hook_event_name":"UserPromptSubmit", "prompt":text,
                          "transcript_path":"/DO_NOT_READ", "cwd":"/DO_NOT_READ"})

    def test_no_phrase_gate_including_implicit_and_nonenglish_ideas(self):
        first = self.prompt("A shared library could save us rebuilding assets.")
        for text in ["Maybe a weekend workshop.", "Podríamos ofrecer un curso.",
                     "Let's put the examples before the theory.", "What about this?",
                     "I have an idea", "x" * 40000]:
            self.assertEqual(self.prompt(text), first)
        data = json.loads(first)
        self.assertTrue(data["continue"])
        self.assertEqual(data["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")
        ctx = data["hookSpecificOutput"]["additionalContext"]
        self.assertLess(len(ctx), 1400)
        self.assertIn("regardless of wording", ctx)
        self.assertNotIn("decision", data)

    def test_context_delivered_even_when_host_should_omit_visible_review(self):
        first = self.prompt("A new direction")
        for text in ["Thanks", "Continue", "Fix the typo", "No critique, just brainstorm",
                     'Transcribe this: "a new idea"', "[decision-review:off]"]:
            self.assertEqual(self.prompt(text), first)
        ctx = json.loads(first)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("no visible review", ctx)
        self.assertIn("no-critique", ctx)
        self.assertIn("quoted/source material", ctx)

    def test_untrusted_input_never_echoed_interpreted_or_read(self):
        output = self.prompt("SECRET_SENTINEL $(touch pwned)")
        self.assertEqual(output, self.prompt("Hello"))
        self.assertNotIn(b"SECRET_SENTINEL", output)

    def test_invalid_input_and_events_fail_open(self):
        for raw in [b"", b"{", b"[]", b"null", b"\xff", b"x" * 1048577]:
            self.assertEqual(self.call(raw), b"")
        for event in [None, "Stop", "SessionStart", "PreToolUse"]:
            self.assertEqual(self.call({"hook_event_name":event,"prompt":"Anything"}), b"")
        for value in [None, [], {}, 42, "", "  "]:
            self.assertEqual(self.call({"hook_event_name":"UserPromptSubmit","prompt":value}), b"")

if __name__ == "__main__":
    unittest.main()
