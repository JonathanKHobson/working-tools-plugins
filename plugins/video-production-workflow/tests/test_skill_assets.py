from __future__ import annotations

import json
import py_compile
import re
from pathlib import Path
from urllib.parse import unquote


def test_skill_scripts_compile_and_scenarios_cover_all_skills() -> None:
    root = Path(__file__).resolve().parents[1]
    skills = {p.name for p in (root / "skills").iterdir() if p.is_dir()}
    for path in (root / "skills").glob("*/scripts/*.py"):
        py_compile.compile(str(path), doraise=True)
    rows = [json.loads(line) for line in (root / "evaluations/scenarios.jsonl").read_text().splitlines() if line.strip()]
    external = [row for row in rows if ":" in row["expected_skill"]]
    # The existing source-to-static-visual negative case deliberately bypasses Video.
    assert all(row["expected_skill"] == "graphic-design-studio:graphic-design" and row["type"] == "negative" for row in external)
    covered = {row["expected_skill"] for row in rows if ":" not in row["expected_skill"]}
    assert covered == skills
    for skill in skills:
        minimum = 1 if skill == "edit-davinci-resolve" else 3
        assert sum(1 for row in rows if row["expected_skill"] == skill and row["type"] == "positive") >= minimum


def test_legacy_skill_agents_and_references_and_compact_editor_routes() -> None:
    root = Path(__file__).resolve().parents[1]
    for skill in (root / "skills").iterdir():
        if not skill.is_dir():
            continue
        if skill.name != "edit-davinci-resolve":
            assert len(list((skill / "agents").glob("*.md"))) >= 2
            assert len(list((skill / "references").glob("*.md"))) >= 6
            assert len(list((skill / "references/sources").glob("*.md"))) >= 5
        else:
            # The native editor owner reuses existing stage implementations and
            # shared role contracts; its required support is one operation guide.
            assert (skill / "references/resolve-control-and-finishing.md").is_file()
        # Both layouts must lead agents to existing support rather than dead links.
        for path in (skill / "SKILL.md", skill / "references/sources/source-index.md"):
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if target.startswith(("https:", "http:", "#", "mailto:")):
                    continue
                resolved = path.parent / unquote(target.split("#", 1)[0])
                assert resolved.exists(), f"{path.relative_to(root)} -> {target}"
