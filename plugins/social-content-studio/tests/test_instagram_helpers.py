import importlib.util
import hashlib
import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

reel = load("skills/short-form-video/scripts/reel_tools.py", "reel_tools")
research = load("skills/short-form-video/scripts/reel_research.py", "reel_research")
caption = load("skills/social-content/scripts/caption_check.py", "caption_check")


class InstagramHelperTests(unittest.TestCase):
    def test_beats_literal_diagnostics_and_no_score(self):
        got = reel._beats("This will change everything.\n$18,000 later.", 120, 3)
        self.assertGreater(got["total_seconds"], 0)
        self.assertTrue(any(x["kind"] == "literal_feature" for x in got["diagnostics"]))
        self.assertNotIn("score", got); self.assertNotIn("winner", got)

    def test_beats_rejects_invalid_rates(self):
        for value in (0, -1, float("nan"), float("inf"), True):
            with self.assertRaises(ValueError): reel._beats("hello", value)
        with self.assertRaises(ValueError): reel._beats("hello", 165, 0)
        with self.assertRaises(ValueError): reel._beats("hello", 5e-324)

    def test_beats_flags_non_space_delimited_scripts(self):
        got = reel._beats("这是一段很长很长很长很长很长的文字描述内容", 165)
        self.assertTrue(got["unsupported"])
        self.assertIsNone(got["total_seconds"])

    def test_hooks_abstain_without_literal_source(self):
        got = reel._hooks("A quiet demonstration of folding paper")
        self.assertTrue(got["abstained"])

    def test_hooks_known_literal_is_review_cue_not_score(self):
        got = reel._hooks("Nobody tells you the answer")
        self.assertFalse(got["abstained"])
        self.assertEqual(got["matches"][0]["id"], 3)
        self.assertEqual(got["matches"][0]["matched_literals"], ["nobody tells you"])
        self.assertNotIn("score", got)

    def row(self, **changes):
        row = {"source_url": "https://example.test/a", "account": "acct", "platform": "instagram", "views": 100, "baseline_views": 20, "metric": "views", "window": "7d", "cohort": "niche"}
        row.update(changes); return row

    def test_research_preserves_missing_and_zero_baselines(self):
        got = research.analyse([self.row(), self.row(source_url="https://example.test/b", baseline_views=None), self.row(source_url="https://example.test/c", baseline_views=0)])
        self.assertEqual(got["rows"][0]["relative_multiple"], 5.0)
        self.assertEqual(got["rows"][1]["baseline_status"], "missing baseline")
        self.assertEqual(got["rows"][2]["baseline_status"], "zero baseline")
        self.assertIsNone(got["ranking"])

    def test_research_rejects_bad_numbers_and_duplicates(self):
        for value in (-1, float("nan"), float("inf"), True, "20"):
            with self.assertRaises(ValueError): research.analyse([self.row(views=value)])
        with self.assertRaises(ValueError): research.analyse([self.row(), self.row()])

    def test_research_keeps_cohorts_separate(self):
        got = research.analyse([self.row(), self.row(source_url="https://example.test/b", cohort="other", metric="likes")])
        self.assertEqual(len(got["comparable_groups"]), 2)

    def test_research_keeps_platforms_separate_and_median_samples(self):
        got = research.analyse([self.row(baseline_views=None, baseline_samples=[10, 20, 30], baseline_source="recent", baseline_window="7d"), self.row(source_url="https://example.test/b", platform="tiktok")])
        self.assertEqual(got["rows"][0]["baseline_views"], 20.0)
        self.assertEqual(got["rows"][0]["baseline_count"], 3)
        self.assertEqual(len(got["comparable_groups"]), 2)

    def test_research_rejects_huge_or_unavailable_arithmetic(self):
        with self.assertRaises(ValueError): research.analyse([self.row(views=10**400)])
        got = research.analyse([self.row(views=1e308, baseline_views=1e-308)])
        self.assertIsNone(got["rows"][0]["relative_multiple"])
        self.assertIn("ratio unavailable", got["rows"][0]["baseline_status"])

    def test_research_rejects_conflicting_explicit_baseline_and_samples(self):
        with self.assertRaises(ValueError): research.analyse([self.row(baseline_views=0, baseline_samples=[10, 20])])

    def test_research_required_number_error_is_truthful(self):
        with self.assertRaisesRegex(ValueError, r"finite nonnegative number$"):
            research.analyse([self.row(baseline_samples=[None])])

    def test_research_missing_views_stays_unranked(self):
        got = research.analyse([self.row(views=None)])
        self.assertEqual(got["rows"][0]["views_status"], "missing views")
        self.assertIsNone(got["rows"][0]["relative_multiple"])

    def test_research_validates_optional_provenance_fields(self):
        with self.assertRaises(ValueError): research.analyse([self.row(baseline_count=True)])
        with self.assertRaises(ValueError): research.analyse([self.row(baseline_source=3)])
        got = research.analyse([self.row(baseline_count=0)])
        self.assertTrue(any("baseline_count" in warning for warning in got["warnings"]))

    def test_caption_preserves_unicode_zwj_and_exact_preview(self):
        text = "👩‍💻 café #éducation\n第二行"
        got = caption.analyse(text, preview_budget=8, platform="instagram")
        self.assertEqual(got["text"], text)
        self.assertEqual(got["preview"], text[:8])
        self.assertIn("#éducation", got["hashtags"])

    def test_caption_empty_and_optional_keywords(self):
        got = caption.analyse("", keywords=[])
        self.assertEqual(got["characters"], 0); self.assertEqual(got["keywords"], {"found": [], "missing": []})
        self.assertIsNone(caption.analyse("hello")["keywords"])

    def test_caption_limits_are_observations(self):
        got = caption.analyse("a #one #two #three", limit=3, max_hashtags=2)
        self.assertEqual(got["max_hashtags"], 2)
        self.assertEqual(len(got["warnings"]), 2)
        self.assertNotIn("verdict", got)

    def test_caption_platform_never_invents_a_limit(self):
        got = caption.analyse("#one #two #three #four #five #six", platform="instagram")
        self.assertIsNone(got["max_hashtags"])
        self.assertEqual(got["warnings"], [])

    def test_caption_cli_preserves_crlf_zwj_file_and_stdin(self):
        script = ROOT / "skills/social-content/scripts/caption_check.py"
        original_hash = hashlib.sha256(script.read_bytes()).hexdigest()
        payload = "👩‍💻 café\r\n#éducation\r\n"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "caption.txt"
            path.write_bytes(payload.encode("utf-8"))
            file_run = subprocess.run([sys.executable, str(script), str(path)], check=True, capture_output=True)
            stdin_run = subprocess.run([sys.executable, str(script), "-"], input=payload.encode("utf-8"), check=True, capture_output=True)
        self.assertEqual(json.loads(file_run.stdout)["text"], payload)
        self.assertEqual(json.loads(stdin_run.stdout)["text"], payload)
        self.assertEqual(hashlib.sha256(script.read_bytes()).hexdigest(), original_hash)


if __name__ == "__main__":
    unittest.main()
