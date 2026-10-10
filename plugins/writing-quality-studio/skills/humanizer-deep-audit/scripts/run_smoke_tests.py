#!/usr/bin/env python3
"""Run dependency-free smoke tests for Humanizer helpers."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SAMPLE = """# Key Challenges And Future Prospects
Of course! The project marked a pivotal moment — highlighting its enduring legacy.
Experts argue that it is not just vibrant, but also crucial to the evolving landscape.
- **Impact:** It maintains an active social media presence.
As of my last knowledge update, details are not widely documented.
Source: :contentReference[oaicite:1]{index=1} https://example.com/?utm_source=chatgpt.com
Contact [Your Name] by 2026-XX-XX.
"""
CITATIONS = """Claim.<ref name=alpha />
<references><ref name=beta>https://example.com</ref></references>
ISBN 978-0-306-40615-7. DOI 10.18653/v1/2025.acl-long.267.
"""


def run_json(*args: str) -> dict:
    result = subprocess.run([sys.executable, *args], capture_output=True, text=True, check=True)
    return json.loads(result.stdout)


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        sample = root / "sample.md"
        citation = root / "citation.wiki"
        baseline = root / "baseline.txt"
        sample.write_text(SAMPLE, encoding="utf-8")
        citation.write_text(CITATIONS, encoding="utf-8")
        baseline.write_text("I write short notes. I use plain words. I don't add a preamble. " * 12, encoding="utf-8")

        lint = run_json(str(ROOT / "humanizer_lint.py"), str(sample), "--format", "json")
        categories = {item["category"] for item in lint["findings"]}
        expected = {"em_dash", "unsupported_significance", "generic_analysis", "vague_attribution", "negative_parallelism", "inline_header_list", "cutoff_disclaimer", "unsupported_absence", "ai_markup", "tracking_parameter", "placeholder"}
        assert expected <= categories, sorted(expected - categories)

        listed = subprocess.run([sys.executable, str(ROOT / "humanizer_lint.py"), "--list-rules"], capture_output=True, text=True, check=True)
        assert "ai_markup\thigh" in listed.stdout

        citation_result = run_json(str(ROOT / "citation_audit.py"), str(citation), "--format", "json")
        citation_categories = {item["category"] for item in citation_result["findings"]}
        assert {"doi", "isbn", "named_ref_used_not_defined", "named_ref_declared_not_reused"} <= citation_categories

        baseline_result = run_json(str(ROOT / "style_baseline.py"), str(sample), "--format", "json")
        assert baseline_result["words"] > 0

        drift_result = run_json(str(ROOT / "style_drift.py"), str(baseline), str(sample), "--format", "json")
        assert drift_result["comparisons"]

    print("Humanizer smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
