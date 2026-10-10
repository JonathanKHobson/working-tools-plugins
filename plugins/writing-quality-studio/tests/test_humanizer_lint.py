"""Focused checks for the advisory Humanizer compound cue and CLI contract."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


LINTER = Path(__file__).resolve().parents[1] / "skills/humanizer-deep-audit/scripts/humanizer_lint.py"


class HumanizerLintTests(unittest.TestCase):
    def lint(self, content, *options):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "draft.txt"
            source.write_text(content, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-B", str(LINTER), str(source), "--format", "json", *options],
                capture_output=True, text=True, check=False,
            )
        self.assertFalse(result.stderr, result.stderr)
        return result, json.loads(result.stdout)

    def compounds(self, report):
        return [item for item in report["findings"] if item["category"] == "compound_stack"]

    def test_four_compounds_trigger_but_three_do_not(self):
        three = "A well-known, research-backed, reader-focused method works."
        four = "A well-known, research-backed, reader-focused, task-specific method works."
        self.assertFalse(self.compounds(self.lint(three)[1]))
        result, report = self.lint(four)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(self.compounds(report)), 1)
        self.assertEqual(self.compounds(report)[0]["severity"], "low")
        self.assertNotIn("score", report)

    def test_sliding_window_finds_stack_across_fixed_chunk_boundary(self):
        text = "x" * 210 + " a well-known, research-backed, reader-focused, task-specific method."
        self.assertEqual(len(self.compounds(self.lint(text)[1])), 1)

    def test_compounds_farther_than_window_do_not_trigger(self):
        text = "A well-known, research-backed, reader-focused " + "ordinary " * 30 + "task-specific method."
        self.assertFalse(self.compounds(self.lint(text)[1]))

    def test_separate_sentences_do_not_combine_compounds(self):
        text = "A well-known, research-backed method. A reader-focused, task-specific method."
        self.assertFalse(self.compounds(self.lint(text)[1]))

    def test_ranges_and_bare_hyphens_do_not_count(self):
        text = "A well-known, research-backed, reader-focused plan covers 10-20 pages, 2025-2026, and a - marker."
        self.assertFalse(self.compounds(self.lint(text)[1]))

    def test_existing_cli_filters_exit_gate_and_em_dash_severity(self):
        text = "A well-known, research-backed, reader-focused, task-specific plan—clear enough. Delve."
        result, report = self.lint(text)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(self.compounds(report)), 1)
        self.assertEqual(next(item["severity"] for item in report["findings"] if item["category"] == "em_dash"), "info")
        self.assertTrue(any(item["category"] == "ai_vocabulary" for item in report["findings"]))
        self.assertEqual(self.lint(text, "--fail-on", "low")[0].returncode, 1)
        self.assertEqual(len(self.lint(text, "--only", "compound_stack")[1]["findings"]), 1)
        self.assertFalse(self.compounds(self.lint(text, "--ignore", "compound_stack")[1]))


if __name__ == "__main__":
    unittest.main()
