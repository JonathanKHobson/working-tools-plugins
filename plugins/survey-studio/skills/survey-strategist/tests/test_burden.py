from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_burden import estimate_burden  # noqa: E402


class BurdenTests(unittest.TestCase):
    def test_open_text_costs_more_than_closed_question(self) -> None:
        survey = json.loads((ROOT / "assets" / "survey-template.json").read_text(encoding="utf-8"))
        report = estimate_burden(survey)
        by_id = {item["question_id"]: item["seconds"] for item in report["questions"]}
        self.assertGreater(by_id["why"], by_id["outcome_metric"])

    def test_reports_total_minutes_and_hotspots(self) -> None:
        survey = json.loads((ROOT / "assets" / "survey-template.json").read_text(encoding="utf-8"))
        report = estimate_burden(survey)
        self.assertGreater(report["estimated_seconds"], 0)
        self.assertGreater(report["estimated_minutes"], 0)
        self.assertIn("questions", report)


if __name__ == "__main__":
    unittest.main()
