from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from generate_codebook import codebook_rows, write_codebook  # noqa: E402
from survey_io import load_survey  # noqa: E402


class CodebookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.survey = load_survey(ROOT / "assets" / "survey-template.json")

    def test_codebook_has_question_and_scale_rows(self) -> None:
        rows = codebook_rows(self.survey)
        records = {(row["record_type"], row["question_id"]) for row in rows}
        self.assertIn(("question", "outcome_metric"), records)
        self.assertIn(("scale_anchor", "outcome_metric"), records)
        self.assertIn(("question", "why"), records)

    def test_writes_csv_markdown_and_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for fmt, suffix in (("csv", ".csv"), ("markdown", ".md"), ("json", ".json")):
                path = Path(tmp) / f"codebook{suffix}"
                write_codebook(self.survey, path, fmt)
                self.assertTrue(path.exists())
                self.assertIn("outcome_metric", path.read_text(encoding="utf-8"))
            with (Path(tmp) / "codebook.csv").open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertTrue(any(row["question_id"] == "why" for row in rows))


if __name__ == "__main__":
    unittest.main()
