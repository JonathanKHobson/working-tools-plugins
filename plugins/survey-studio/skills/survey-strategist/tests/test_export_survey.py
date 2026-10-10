from __future__ import annotations

import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
from html.parser import HTMLParser
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from export_survey import export_to_path  # noqa: E402
from survey_io import load_survey  # noqa: E402


class FormInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.label_fors: set[str] = set()
        self.names: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if attr.get("id"):
            self.ids.add(str(attr["id"]))
        if tag == "label" and attr.get("for"):
            self.label_fors.add(str(attr["for"]))
        if attr.get("name"):
            self.names.add(str(attr["name"]))


class ExportSurveyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.survey = load_survey(ROOT / "assets" / "survey-template.json")

    def test_exports_textual_formats_with_stable_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            paths = {
                "markdown": tmp_path / "survey.md",
                "text": tmp_path / "survey.txt",
                "html": tmp_path / "survey.html",
                "xml": tmp_path / "survey.xml",
                "json": tmp_path / "survey.json",
                "yaml": tmp_path / "survey.yaml",
            }
            for fmt, path in paths.items():
                export_to_path(self.survey, fmt, path)
                self.assertTrue(path.exists(), fmt)
                self.assertIn("outcome_metric", path.read_text(encoding="utf-8"), fmt)
            self.assertEqual(load_survey(paths["json"])["survey"]["id"], "example-survey")
            self.assertEqual(load_survey(paths["yaml"])["survey"]["id"], "example-survey")
            ET.parse(paths["xml"])

    def test_html_uses_labels_and_stable_names(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "survey.html"
            export_to_path(self.survey, "html", path)
            parser = FormInspector()
            parser.feed(path.read_text(encoding="utf-8"))
            self.assertIn("outcome_metric", parser.names)
            self.assertTrue(parser.label_fors.issubset(parser.ids))
            self.assertGreater(len(parser.label_fors), 0)

    def test_exports_docx_and_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            docx_path = Path(tmp) / "survey.docx"
            pdf_path = Path(tmp) / "survey.pdf"
            export_to_path(self.survey, "docx", docx_path)
            export_to_path(self.survey, "pdf", pdf_path)
            self.assertTrue(zipfile.is_zipfile(docx_path))
            with zipfile.ZipFile(docx_path) as archive:
                document_xml = archive.read("word/document.xml").decode("utf-8")
                self.assertIn("outcome_metric", document_xml)
            self.assertTrue(pdf_path.read_bytes().startswith(b"%PDF"))
            self.assertGreater(pdf_path.stat().st_size, 1000)

    def test_unknown_format_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                export_to_path(self.survey, "unknown", Path(tmp) / "x.bin")


if __name__ == "__main__":
    unittest.main()
