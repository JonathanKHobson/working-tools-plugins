"""Static package checks. Does not execute candidate skills, helpers, or providers."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    manifest = load(".codex-plugin/plugin.json")
    routes = load("docs/routes.json")
    cases = load("tests/route-cases.json")
    coverage = load("provenance/coverage.json")
    assert manifest["name"] == "game-creation-studio"
    assert manifest["version"].split("+", 1)[0] == "0.2.0"
    assert manifest["skills"] == "./skills/"
    assert not any(manifest.get(key) for key in ("mcpServers", "hooks", "apps"))
    assert not (ROOT / ".mcp.json").exists()
    local = routes["localSkills"]
    official = routes["officialBrowserGameProvider"]["skills"]
    assert len(local) == 10 and len({item["id"] for item in local}) == 10
    assert len(official) == 9 and len({item["id"] for item in official}) == 9
    local_ids = {item["id"] for item in local}
    assert local_ids == {path.parent.name for path in ROOT.glob("skills/*/SKILL.md")}
    official_ids = {item["id"] for item in official}
    for item in local:
        skill = ROOT / item["skill"]
        content = skill.read_text(encoding="utf-8")
        assert content.startswith("---\n"), skill
        assert re.search(rf"(?m)^name: {re.escape(item['id'])}$", content), skill
        assert re.search(r"(?m)^description: .+", content), skill
    assert len(cases["cases"]) >= 18
    for case in cases["cases"]:
        assert case["expectedLocal"] is None or case["expectedLocal"] in local_ids
        if "expectedOfficial" in case:
            assert case["expectedOfficial"] in official_ids
    # Check local Markdown links only. External links and fragment targets are not files.
    for path in [ROOT / "README.md", ROOT / "docs/project-map.md", *ROOT.glob("skills/**/*.md")]:
        content = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", content):
            if target.startswith(("https://", "http://", "#")):
                continue
            assert (path.parent / target.split("#", 1)[0]).exists(), (path, target)
    vendored = {p.relative_to(ROOT).as_posix() for p in (ROOT / "vendor/game-development-studio-1.0.2").rglob("*") if p.is_file()}
    covered = {item["source"] for item in coverage["files"]}
    assert vendored == covered, ("source coverage mismatch", sorted(vendored - covered), sorted(covered - vendored))
    for item in coverage["files"]:
        source = ROOT / item["source"]
        assert source.is_file(), source
        assert hashlib.sha256(source.read_bytes()).hexdigest() == item["sha256"], source
        if item.get("activeCopy"):
            active = ROOT / item["activeCopy"]
            assert active.is_file(), active
            assert active.read_bytes() == source.read_bytes(), active
    assert len(coverage["files"]) == 38
    for path in ROOT.rglob("*"):
        assert not path.is_symlink(), ("symlink in distribution", path)
        assert path.name != ".DS_Store" and path.suffix != ".pyc", ("host artifact", path)
        if path.is_file() and path.suffix in {".md", ".json", ".yaml", ".toml", ".txt"}:
            text = path.read_text(encoding="utf-8")
            pattern = "/" + r"(?:Users|home)/[A-Za-z][A-Za-z0-9_.-]*/|" + "/" + "Volumes/" + r"[A-Za-z][^\n`\"']+"
            assert not re.search(pattern, text), ("concrete host path", path)
    print(f"PASS: 10 local skills, 9 official routes, {len(cases['cases'])} route cases, 38 upstream files, links and hashes")


if __name__ == "__main__":
    main()
