#!/usr/bin/env python3
"""Run offline citation-integrity checks for prose, Markdown, and wikitext."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit


URL_RE = re.compile(r"https?://[^\s<>\]\[\"')]+")
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
ISBN_LABEL_RE = re.compile(r"\bISBN(?:-1[03])?\s*:?[\s-]*([0-9Xx][0-9Xx\s-]{8,20}[0-9Xx])")
PLACEHOLDER_RE = re.compile(r"\b(?:20\d{2}-[Xx]{2}-[Xx]{2}|YYYY-MM-DD|INSERT_[A-Z0-9_]+|PASTE_[A-Z0-9_]+_HERE|SOURCE_PUBLISHER|URL)\b")
AI_ARTIFACT_RE = re.compile(r"(?:contentReference|oaicite|oai_citation|turn\d+(?:search|file|news)\d+|attributableIndex|\[cite:\s*\d|grok_render_citation_card_json|【\d+†L\d|\[(?:attached_file|web):\d+\])", re.IGNORECASE)
REF_DEF_RE = re.compile(r"<ref\s+name\s*=\s*[\"']?([^\s\"'/>]+)[\"']?\s*>", re.IGNORECASE)
REF_USE_RE = re.compile(r"<ref\s+name\s*=\s*[\"']?([^\s\"'/>]+)[\"']?\s*/>", re.IGNORECASE)


def read_text(path: str) -> tuple[str, str]:
    if path == "-":
        return sys.stdin.read(), "stdin"
    source = Path(path)
    return source.read_text(encoding="utf-8"), str(source)


def isbn_status(raw: str) -> tuple[str, str]:
    value = re.sub(r"[^0-9Xx]", "", raw).upper()
    if len(value) == 10:
        if not re.fullmatch(r"\d{9}[\dX]", value):
            return value, "invalid characters"
        total = sum((10 - i) * (10 if ch == "X" else int(ch)) for i, ch in enumerate(value))
        return value, "valid checksum" if total % 11 == 0 else "invalid checksum"
    if len(value) == 13:
        if not value.isdigit():
            return value, "invalid characters"
        total = sum(int(ch) * (1 if i % 2 == 0 else 3) for i, ch in enumerate(value))
        return value, "valid checksum" if total % 10 == 0 else "invalid checksum"
    return value, "invalid length"


def location(text: str, index: int) -> str:
    before = text[:index]
    return f"{before.count(chr(10)) + 1}:{index - before.rfind(chr(10))}"


def audit(text: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for match in PLACEHOLDER_RE.finditer(text):
        findings.append({"severity": "high", "category": "placeholder", "location": location(text, match.start()), "value": match.group(0), "check": "Replace with a verified value or remove the dependent claim."})
    for match in AI_ARTIFACT_RE.finditer(text):
        findings.append({"severity": "high", "category": "internal_citation_artifact", "location": location(text, match.start()), "value": match.group(0), "check": "Recover and verify the intended source before removing the artifact."})
    for match in URL_RE.finditer(text):
        url = match.group(0).rstrip(".,;:")
        query = dict(parse_qsl(urlsplit(url).query))
        flagged = [key for key in ("utm_source", "referrer") if key in query and query[key] in {"chatgpt.com", "openai", "copilot.com", "grok.com"}]
        if flagged or "ppl-ai-file-upload" in url:
            findings.append({"severity": "medium", "category": "tracking_or_tool_url", "location": location(text, match.start()), "value": url, "check": "Verify the clean stable URL, then remove unnecessary tracking or temporary upload paths."})
    for match in DOI_RE.finditer(text):
        doi = match.group(0).rstrip(".,;:")
        findings.append({"severity": "info", "category": "doi", "location": location(text, match.start()), "value": doi, "check": f"Resolve https://doi.org/{doi} and compare title, authors, venue, date, and supported claim."})
    for match in ISBN_LABEL_RE.finditer(text):
        value, status = isbn_status(match.group(1))
        severity = "info" if status == "valid checksum" else "high"
        findings.append({"severity": severity, "category": "isbn", "location": location(text, match.start()), "value": value, "check": f"{status}; also compare title, author, edition, and publisher."})
    defined = set(REF_DEF_RE.findall(text))
    used = set(REF_USE_RE.findall(text))
    for name in sorted(defined - used):
        findings.append({"severity": "medium", "category": "named_ref_declared_not_reused", "location": "document", "value": name, "check": "Confirm the definition is cited inline; remove it if unused."})
    for name in sorted(used - defined):
        findings.append({"severity": "high", "category": "named_ref_used_not_defined", "location": "document", "value": name, "check": "Add the verified definition or remove the unsupported citation use."})
    return sorted(findings, key=lambda item: (item["location"], item["category"], item["value"]))


def render_markdown(source: str, findings: list[dict[str, str]]) -> str:
    lines = [f"# Citation audit: `{source}`", "", "Offline checks only. Verify source existence and claim support manually.", ""]
    if not findings:
        return "\n".join(lines + ["No configured citation cues found."])
    lines += ["| Location | Severity | Category | Value | Required check |", "| --- | --- | --- | --- | --- |"]
    for item in findings:
        value = item["value"].replace("|", "\\|")
        check = item["check"].replace("|", "\\|")
        lines.append(f"| {item['location']} | {item['severity']} | {item['category']} | {value} | {check} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit common citation-integrity failures without inventing replacements.")
    parser.add_argument("path", help="UTF-8 text file, or - for stdin")
    parser.add_argument("--format", choices=("text", "markdown", "json"), default="text")
    args = parser.parse_args()
    text, source = read_text(args.path)
    results = audit(text)
    if args.format == "json":
        print(json.dumps({"source": source, "findings": results}, indent=2))
    elif args.format == "markdown":
        print(render_markdown(source, results))
    else:
        print(f"{source}: {len(results)} citation cue(s).")
        for item in results:
            print(f"{item['location']} [{item['severity']}] {item['category']}: {item['value']} — {item['check']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
