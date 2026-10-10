from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from export_survey import export_to_path  # noqa: E402
from qualtrics_txt import export_advanced_txt, export_simple_txt  # noqa: E402
from survey_io import load_survey  # noqa: E402
from validate_qualtrics_txt import validate_file, validate_text  # noqa: E402


class QualtricsTXTTests(unittest.TestCase):
    def setUp(self) -> None:
        self.survey = load_survey(ROOT / "assets" / "survey-template.json")

    def test_advanced_export_preserves_ids_and_warns_on_scale_mapping(self) -> None:
        text, warnings = export_advanced_txt(self.survey)
        self.assertTrue(text.startswith("[[AdvancedFormat]]"))
        self.assertIn("[[ID:outcome_metric]]", text)
        self.assertIn("[[Question:MC:SingleAnswer:Horizontal]]", text)
        self.assertIn("[[Question:TE:Essay]]", text)
        self.assertTrue(any("outcome_metric" in warning and "multiple-choice" in warning.lower() for warning in warnings))
        self.assertFalse([issue for issue in validate_text(text) if issue.severity == "error"])

    def test_export_to_path_writes_utf8_lf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "advanced.txt"
            export_to_path(self.survey, "qualtrics-advanced", path)
            raw = path.read_bytes()
            self.assertNotIn(b"\r\n", raw)
            self.assertNotIn(b"\xff\xfe", raw)
            self.assertIn(b"[[AdvancedFormat]]", raw)

    def test_export_writes_warning_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "advanced.txt"
            warnings = export_to_path(self.survey, "qualtrics-advanced", path)
            manifest = path.with_suffix(".warnings.json")
            self.assertTrue(warnings)
            self.assertTrue(manifest.exists())
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual("qualtrics-advanced", payload["format"])
            self.assertEqual(warnings, payload["warnings"])

    def test_simple_export_supports_multiple_choice_and_matrix(self) -> None:
        survey = json.loads(json.dumps(self.survey))
        survey["blocks"][0]["questions"] = [
            {
                "id": "channel",
                "type": "single_choice",
                "text": "Which channel did you use most recently?",
                "required": True,
                "rationale": "Identifies the experience channel.",
                "construct": "channel",
                "analysis_use": "Segment the primary outcome by channel.",
                "choices": [
                    {"id": "web", "label": "Website", "value": 1},
                    {"id": "app", "label": "Mobile app", "value": 2}
                ]
            },
            {
                "id": "feature_matrix",
                "type": "matrix",
                "text": "How satisfied were you with each area?",
                "required": False,
                "rationale": "Measures area-level satisfaction.",
                "construct": "area satisfaction",
                "analysis_use": "Report distributions for each row.",
                "rows": [
                    {"id": "speed", "label": "Speed", "value": 1},
                    {"id": "clarity", "label": "Clarity", "value": 2}
                ],
                "columns": [
                    {"id": "low", "label": "Dissatisfied", "value": 1},
                    {"id": "high", "label": "Satisfied", "value": 2}
                ]
            }
        ]
        survey["analysis_plan"]["primary_metrics"] = []
        text, warnings = export_simple_txt(survey)
        self.assertIn("channel. Which channel", text)
        self.assertIn("feature_matrix. How satisfied", text)
        self.assertTrue(any("Required-response" in warning for warning in warnings))
        self.assertFalse([issue for issue in validate_text(text) if issue.severity == "error"])

    def test_validator_rejects_utf16(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.txt"
            path.write_bytes("[[AdvancedFormat]]\n".encode("utf-16"))
            issues = validate_file(path)
            self.assertIn("ENCODING_UTF16", {issue.code for issue in issues})

    def test_validator_rejects_duplicate_ids_and_unknown_tags(self) -> None:
        text = """[[AdvancedFormat]]

[[Question:TE:SingleLine]]
[[ID:q1]]
First

[[Question:TE:SingleLine]]
[[ID:q1]]
Second

[[MagicTag]]
"""
        codes = {issue.code for issue in validate_text(text)}
        self.assertIn("DUPLICATE_ID", codes)
        self.assertIn("UNKNOWN_TAG", codes)

    def test_simple_validator_warns_about_colons_in_choices(self) -> None:
        text = """q1. Choose one.

Choice: A
Choice B
"""
        self.assertIn("SIMPLE_CHOICE_COLON", {issue.code for issue in validate_text(text)})


if __name__ == "__main__":
    unittest.main()
