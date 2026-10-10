from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from survey_lint import lint_survey  # noqa: E402


class SurveyLintTests(unittest.TestCase):
    def setUp(self) -> None:
        self.survey = json.loads((ROOT / "assets" / "survey-template.json").read_text(encoding="utf-8"))

    def codes(self, survey: dict) -> set[str]:
        return {issue.code for issue in lint_survey(survey, include_info=True)}

    def test_clean_template_has_no_errors(self) -> None:
        issues = lint_survey(self.survey, include_info=True)
        self.assertFalse([issue for issue in issues if issue.severity == "error"])

    def test_flags_leading_and_double_barreled_wording(self) -> None:
        question = self.survey["blocks"][0]["questions"][0]
        question["text"] = "Don't you agree that onboarding is clear and easy to complete?"
        codes = self.codes(self.survey)
        self.assertIn("WORDING_LEADING", codes)
        self.assertIn("WORDING_DOUBLE_BARRELED", codes)

    def test_flags_required_sensitive_question(self) -> None:
        question = self.survey["blocks"][0]["questions"][1]
        question["sensitive"] = True
        question["required"] = True
        self.assertIn("SENSITIVE_REQUIRED", self.codes(self.survey))

    def test_flags_privacy_mismatch_for_pii(self) -> None:
        question = self.survey["blocks"][0]["questions"][1]
        question["pii"] = True
        self.assertIn("PII_PRIVACY_MISMATCH", self.codes(self.survey))

    def test_flags_overlapping_numeric_ranges(self) -> None:
        question = self.survey["blocks"][0]["questions"][0]
        question.clear()
        question.update(
            {
                "id": "age",
                "type": "single_choice",
                "text": "What is your age?",
                "required": False,
                "rationale": "Supports age-based subgroup analysis.",
                "construct": "age band",
                "analysis_use": "Compare outcomes across prespecified age bands.",
                "choices": [
                    {"id": "a", "label": "18-25", "value": "18-25"},
                    {"id": "b", "label": "25-34", "value": "25-34"},
                    {"id": "c", "label": "35 or older", "value": "35+"}
                ]
            }
        )
        self.survey["analysis_plan"]["primary_metrics"] = []
        self.assertIn("OPTIONS_OVERLAP", self.codes(self.survey))

    def test_flags_large_matrix(self) -> None:
        question = self.survey["blocks"][0]["questions"][0]
        question.clear()
        question.update(
            {
                "id": "feature_matrix",
                "type": "matrix",
                "text": "How satisfied are you with each feature?",
                "required": False,
                "rationale": "Measures satisfaction across major features.",
                "construct": "feature satisfaction",
                "analysis_use": "Compare item distributions; do not average unless reliability supports it.",
                "rows": [
                    {"id": f"r{i}", "label": f"Feature {i}", "value": i}
                    for i in range(1, 10)
                ],
                "columns": [
                    {"id": f"c{i}", "label": str(i), "value": i}
                    for i in range(1, 8)
                ]
            }
        )
        self.survey["analysis_plan"]["primary_metrics"] = []
        self.assertIn("MATRIX_OVERLOAD", self.codes(self.survey))

    def test_flags_future_logic_reference(self) -> None:
        first, second = self.survey["blocks"][0]["questions"]
        first["display_if"] = {"question_id": second["id"], "operator": "answered"}
        self.assertIn("LOGIC_FORWARD_REFERENCE", self.codes(self.survey))

    def test_flags_demographics_too_early(self) -> None:
        q = self.survey["blocks"][0]["questions"][0]
        q["id"] = "gender"
        q["construct"] = "demographic gender"
        self.survey["analysis_plan"]["primary_metrics"] = []
        self.assertIn("DEMOGRAPHIC_EARLY", self.codes(self.survey))

    def test_balanced_bipolar_wording_is_not_double_barreled(self) -> None:
        question = self.survey["blocks"][0]["questions"][0]
        question["text"] = "How easy or difficult was this task?"
        self.assertNotIn("WORDING_DOUBLE_BARRELED", self.codes(self.survey))

    def test_does_not_treat_manageable_as_age_demographic(self) -> None:
        question = self.survey["blocks"][0]["questions"][0]
        question["id"] = "workload_manageable"
        question["text"] = "My workload was manageable during the past 2 weeks."
        question["construct"] = "workload manageability"
        self.assertNotIn("DEMOGRAPHIC_EARLY", self.codes(self.survey))

    def test_required_sensitive_question_with_necessity_is_warning_not_error(self) -> None:
        question = self.survey["blocks"][0]["questions"][1]
        question["sensitive"] = True
        question["required"] = True
        question["required_justification"] = "The service cannot route the request without a short problem description."
        issues = lint_survey(self.survey, include_info=True)
        codes = {issue.code for issue in issues}
        self.assertNotIn("SENSITIVE_REQUIRED", codes)
        justified = [issue for issue in issues if issue.code == "SENSITIVE_REQUIRED_JUSTIFIED"]
        self.assertEqual(1, len(justified))
        self.assertEqual("warning", justified[0].severity)

    def test_nps_scale_must_be_zero_to_ten(self) -> None:
        survey = deepcopy(self.survey)
        q = survey["blocks"][0]["questions"][0]
        q["type"] = "nps"
        q["scale"] = {"min": 1, "max": 5, "step": 1, "anchors": {"1": "Not likely", "5": "Very likely"}}
        self.assertIn("NPS_SCALE", self.codes(survey))


if __name__ == "__main__":
    unittest.main()
