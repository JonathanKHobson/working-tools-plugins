from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from survey_io import SurveyValidationError, iter_questions, load_survey, validate_survey  # noqa: E402


class SurveyIOTests(unittest.TestCase):
    def setUp(self) -> None:
        self.valid = {
            "survey": {
                "id": "pulse-01",
                "title": "Product experience pulse",
                "version": "1.0.0",
                "objective": "Decide which onboarding friction to investigate next.",
                "target_audience": "People who completed onboarding in the past 14 days.",
                "mode": "web",
                "estimated_minutes": 3,
                "consent": {
                    "required": True,
                    "text": "Your participation is voluntary.",
                    "contact": "research@example.com",
                },
                "privacy": {
                    "identifiability": "pseudonymous",
                    "collects_pii": False,
                    "retention": "Delete raw responses after 12 months.",
                    "jurisdictions": ["US"],
                },
            },
            "analysis_plan": {
                "decisions": ["Choose the next onboarding problem for discovery research."],
                "primary_metrics": ["task_ease"],
                "segments": [],
                "exclusions": ["test responses"],
            },
            "blocks": [
                {
                    "id": "experience",
                    "title": "Your recent experience",
                    "questions": [
                        {
                            "id": "task_ease",
                            "type": "rating",
                            "text": "How easy or difficult was it to finish onboarding?",
                            "required": True,
                            "rationale": "Measures perceived onboarding effort.",
                            "construct": "task ease",
                            "analysis_use": "Primary metric; report its distribution.",
                            "scale": {
                                "min": 1,
                                "max": 7,
                                "step": 1,
                                "anchors": {"1": "Very difficult", "7": "Very easy"},
                            },
                        }
                    ],
                }
            ],
        }

    def test_loads_json_and_iterates_questions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "survey.json"
            path.write_text(json.dumps(self.valid), encoding="utf-8")
            survey = load_survey(path)
        self.assertEqual([q["id"] for q in iter_questions(survey)], ["task_ease"])

    def test_validates_complete_survey(self) -> None:
        validate_survey(self.valid)

    def test_rejects_missing_objective(self) -> None:
        del self.valid["survey"]["objective"]
        with self.assertRaises(SurveyValidationError) as ctx:
            validate_survey(self.valid)
        self.assertIn("objective", str(ctx.exception))

    def test_rejects_duplicate_question_ids(self) -> None:
        duplicate = dict(self.valid["blocks"][0]["questions"][0])
        self.valid["blocks"][0]["questions"].append(duplicate)
        with self.assertRaises(SurveyValidationError) as ctx:
            validate_survey(self.valid)
        self.assertIn("duplicate question id", str(ctx.exception).lower())

    def test_rejects_choice_question_without_choices(self) -> None:
        question = self.valid["blocks"][0]["questions"][0]
        question["type"] = "single_choice"
        question.pop("scale")
        with self.assertRaises(SurveyValidationError) as ctx:
            validate_survey(self.valid)
        self.assertIn("choices", str(ctx.exception).lower())

    def test_rejects_duplicate_choice_values(self) -> None:
        question = self.valid["blocks"][0]["questions"][0]
        question["type"] = "single_choice"
        question.pop("scale")
        question["choices"] = [
            {"id": "yes", "label": "Yes", "value": 1},
            {"id": "no", "label": "No", "value": 1},
        ]
        with self.assertRaises(SurveyValidationError) as ctx:
            validate_survey(self.valid)
        self.assertIn("duplicate choice value", str(ctx.exception).lower())


if __name__ == "__main__":
    unittest.main()
