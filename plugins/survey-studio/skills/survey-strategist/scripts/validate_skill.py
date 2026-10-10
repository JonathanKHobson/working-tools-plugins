#!/usr/bin/env python3
"""Validate survey-strategist structure, metadata, links, assets, examples, and scripts."""

from __future__ import annotations

import argparse
import json
import os
import py_compile
import re
import sys
import tempfile
from pathlib import Path
from typing import Iterable, Sequence

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install dependencies with: python -m pip install -r requirements.txt") from exc

Issue = tuple[str, str]
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FORBIDDEN_AUXILIARY = {"README.md", "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md", "CHANGELOG.md"}
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|FIXME)\b|fill\s+in\s+later", re.I)
CLI_SCRIPTS = {
    "estimate_burden.py",
    "export_survey.py",
    "generate_codebook.py",
    "survey_lint.py",
    "validate_qualtrics_txt.py",
    "validate_skill.py",
}


def _frontmatter(text: str) -> tuple[dict, str] | tuple[None, str]:
    if not text.startswith("---\n"):
        return None, "SKILL.md must start with YAML frontmatter delimited by --- lines."
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, "SKILL.md frontmatter closing delimiter is missing."
    raw = text[4:end]
    try:
        metadata = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return None, f"SKILL.md frontmatter is invalid YAML: {exc}"
    if not isinstance(metadata, dict):
        return None, "SKILL.md frontmatter must be a mapping."
    return metadata, text[end + 5 :]


def _markdown_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return LINK_RE.findall(text)


def _relative_target(source: Path, raw: str) -> Path | None:
    target = raw.strip().split()[0].strip("<>")
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None
    return (source.parent / target).resolve()


def _validate_frontmatter(root: Path, issues: list[Issue]) -> dict | None:
    skill = root / "SKILL.md"
    if not skill.is_file():
        issues.append(("error", "Missing required SKILL.md."))
        return None
    try:
        text = skill.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        issues.append(("error", f"SKILL.md must be UTF-8: {exc}"))
        return None
    result, detail = _frontmatter(text)
    if result is None:
        issues.append(("error", detail))
        return None
    metadata = result
    extra = set(metadata) - {"name", "description"}
    if extra:
        issues.append(("error", f"SKILL.md frontmatter contains unsupported fields: {', '.join(sorted(extra))}."))
    name = metadata.get("name")
    description = metadata.get("description")
    if not isinstance(name, str) or not name:
        issues.append(("error", "Frontmatter name is required and must be a string."))
    else:
        if not NAME_RE.fullmatch(name) or len(name) > 64:
            issues.append(("error", "Frontmatter name must be <=64 characters using lowercase letters, digits, and hyphens."))
        if root.name != name:
            issues.append(("error", f"Skill folder name '{root.name}' does not match frontmatter name '{name}'."))
    if not isinstance(description, str) or not description.strip():
        issues.append(("error", "Frontmatter description is required and must be a string."))
    else:
        desc = " ".join(description.split())
        if len(desc) > 1024:
            issues.append(("error", f"Frontmatter description is {len(desc)} characters; maximum is 1024."))
        if not desc.startswith("Use when"):
            issues.append(("error", "Frontmatter description should start with 'Use when' for trigger-oriented discovery."))
    line_count = len(text.splitlines())
    if line_count > 500:
        issues.append(("error", f"SKILL.md has {line_count} lines; keep it under 500 and use references."))
    return metadata


def _validate_agents(root: Path, name: str | None, issues: list[Issue]) -> None:
    path = root / "agents" / "openai.yaml"
    if not path.is_file():
        issues.append(("error", "Missing recommended agents/openai.yaml UI metadata."))
        return
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        issues.append(("error", f"agents/openai.yaml is invalid: {exc}"))
        return
    interface = data.get("interface") if isinstance(data, dict) else None
    if not isinstance(interface, dict):
        issues.append(("error", "agents/openai.yaml must contain an interface mapping."))
        return
    for key in ("display_name", "short_description", "default_prompt"):
        if not isinstance(interface.get(key), str) or not interface[key].strip():
            issues.append(("error", f"agents/openai.yaml interface.{key} is required and must be a quoted string."))
    short = interface.get("short_description", "")
    if isinstance(short, str) and not 25 <= len(short) <= 64:
        issues.append(("error", f"interface.short_description must be 25–64 characters; found {len(short)}."))
    prompt = interface.get("default_prompt", "")
    if name and isinstance(prompt, str) and f"${name}" not in prompt:
        issues.append(("error", f"interface.default_prompt must explicitly mention '${name}'."))


def _validate_links(root: Path, issues: list[Issue]) -> None:
    for path in root.rglob("*.md"):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        for raw in _markdown_links(path):
            target = _relative_target(path, raw)
            if target is not None and not target.exists():
                issues.append(("error", f"Broken relative link in {path.relative_to(root)}: {raw}"))

    # Full reference closure may be reached through the shared index in the
    # maintained modular package. Follow only local Markdown within its declared
    # package boundary; a historical external file cannot satisfy the contract.
    boundary = root.resolve()
    manifest = root.parents[1] / ".codex-plugin" / "plugin.json"
    if manifest.is_file():
        try:
            package = json.loads(manifest.read_text())
        except (OSError, ValueError):
            package = {}
        if package.get("name") == "survey-studio" and package.get("skills") == "./skills/":
            boundary = root.parents[1].resolve()
    pending = [root / "SKILL.md"]
    reached: set[Path] = set()
    while pending:
        source = pending.pop().resolve()
        if source in reached:
            continue
        reached.add(source)
        for raw in _markdown_links(source):
            target = _relative_target(source, raw)
            if target is None:
                continue
            if not target.is_relative_to(boundary):
                issues.append(("error", f"Reference escapes declared package: {raw}"))
            elif target.is_file() and target.suffix == ".md" and target not in reached:
                pending.append(target)
    for ref in sorted((root / "references").glob("*.md")):
        if ref.resolve() not in reached:
            issues.append(("error", f"Reference is not reachable from SKILL.md: {ref.relative_to(root).as_posix()}"))


def _validate_files(root: Path, issues: list[Issue]) -> None:
    for forbidden in FORBIDDEN_AUXILIARY:
        if (root / forbidden).exists():
            issues.append(("error", f"Extraneous top-level file is not part of the skill contract: {forbidden}"))
    for path in root.rglob("*"):
        if path.is_symlink() and not path.exists():
            issues.append(("error", f"Broken symlink: {path.relative_to(root)}"))
        if path.name == "__pycache__" or path.suffix == ".pyc":
            issues.append(("warning", f"Generated Python cache should be removed before packaging: {path.relative_to(root)}"))
    for path in list(root.glob("SKILL.md")) + list((root / "references").glob("*.md")) + list((root / "agents" / "roles").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if PLACEHOLDER_RE.search(text):
            issues.append(("error", f"Unresolved authoring placeholder in {path.relative_to(root)}."))


def _validate_structured_files(root: Path, issues: list[Issue]) -> None:
    for path in root.rglob("*.json"):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            issues.append(("error", f"Invalid JSON in {path.relative_to(root)}: {exc}"))
    for path in list(root.rglob("*.yaml")) + list(root.rglob("*.yml")):
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, yaml.YAMLError) as exc:
            issues.append(("error", f"Invalid YAML in {path.relative_to(root)}: {exc}"))


def _validate_scripts(root: Path, issues: list[Issue]) -> None:
    scripts = root / "scripts"
    if not scripts.is_dir():
        issues.append(("error", "Missing scripts directory."))
        return
    with tempfile.TemporaryDirectory() as tmp:
        for path in scripts.glob("*.py"):
            try:
                py_compile.compile(str(path), cfile=str(Path(tmp) / f"{path.stem}.pyc"), doraise=True)
            except py_compile.PyCompileError as exc:
                issues.append(("error", f"Python compile failure in {path.relative_to(root)}: {exc.msg}"))
            first = path.read_text(encoding="utf-8").splitlines()[:1]
            if not first or not first[0].startswith("#!"):
                issues.append(("error", f"Executable script lacks a shebang: {path.relative_to(root)}"))
            if not os.access(path, os.X_OK):
                issues.append(("error", f"Script is not executable: {path.relative_to(root)}"))
    for name in CLI_SCRIPTS:
        if not (scripts / name).is_file():
            issues.append(("error", f"Missing expected CLI script: scripts/{name}"))


def _validate_domain_assets(root: Path, issues: list[Issue]) -> None:
    required = [
        "assets/survey.schema.json",
        "assets/survey-template.json",
        "assets/survey-template.yaml",
        "assets/qualtrics-advanced-example.txt",
        "assets/qualtrics-simple-example.txt",
    ]
    for rel in required:
        if not (root / rel).is_file():
            issues.append(("error", f"Missing required bundled resource: {rel}"))

    sys.path.insert(0, str(root / "scripts"))
    try:
        from survey_io import SurveyValidationError, load_survey
        from validate_qualtrics_txt import validate_file
    except Exception as exc:  # pragma: no cover - surfaced as validation issue
        issues.append(("error", f"Cannot import bundled validators: {exc}"))
        return

    survey_files = [root / "assets" / "survey-template.json", root / "assets" / "survey-template.yaml"]
    survey_files.extend(sorted((root / "examples").glob("*.json")))
    survey_files.extend(sorted((root / "examples").glob("*.yaml")))
    survey_files.extend(sorted((root / "examples").glob("*.yml")))
    for path in survey_files:
        try:
            load_survey(path)
        except (FileNotFoundError, SurveyValidationError) as exc:
            issues.append(("error", f"Canonical survey validation failed for {path.relative_to(root)}: {exc}"))

    for path in (root / "assets").glob("qualtrics-*.txt"):
        qissues = validate_file(path)
        for issue in qissues:
            if issue.severity == "error":
                issues.append(("error", f"Qualtrics validation failed for {path.relative_to(root)} line {issue.line}: {issue.code} {issue.message}"))


def validate_skill(path: str | Path, *, deep: bool = True) -> list[Issue]:
    root = Path(path).resolve()
    issues: list[Issue] = []
    if not root.is_dir():
        return [("error", f"Skill directory does not exist: {root}")]
    metadata = _validate_frontmatter(root, issues)
    if not deep:
        return issues
    name = metadata.get("name") if isinstance(metadata, dict) else None
    _validate_agents(root, name if isinstance(name, str) else None, issues)
    _validate_links(root, issues)
    _validate_files(root, issues)
    _validate_structured_files(root, issues)
    _validate_scripts(root, issues)
    _validate_domain_assets(root, issues)
    # Stable, readable ordering while preserving discovery context.
    return sorted(dict.fromkeys(issues), key=lambda item: (0 if item[0] == "error" else 1, item[1]))


def _render(issues: Iterable[Issue]) -> str:
    rows = list(issues)
    errors = sum(severity == "error" for severity, _ in rows)
    warnings = sum(severity == "warning" for severity, _ in rows)
    if not rows:
        return "Skill validation: PASS — 0 errors, 0 warnings.\n"
    lines = [f"Skill validation: {'FAIL' if errors else 'PASS'} — {errors} errors, {warnings} warnings.", ""]
    for severity, message in rows:
        lines.append(f"{severity.upper():7} {message}")
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a Codex survey-strategist skill directory.")
    parser.add_argument("skill", nargs="?", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--format", choices=("text", "json"), default="text", dest="output_format")
    parser.add_argument("--shallow", action="store_true", help="Validate only SKILL.md frontmatter and naming")
    parser.add_argument("--fail-on-warning", action="store_true")
    args = parser.parse_args(argv)
    issues = validate_skill(args.skill, deep=not args.shallow)
    if args.output_format == "json":
        print(json.dumps({"issues": [{"severity": s, "message": m} for s, m in issues]}, indent=2, ensure_ascii=False))
    else:
        print(_render(issues), end="")
    has_errors = any(severity == "error" for severity, _ in issues)
    has_warnings = any(severity == "warning" for severity, _ in issues)
    return 1 if has_errors or (args.fail_on_warning and has_warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
