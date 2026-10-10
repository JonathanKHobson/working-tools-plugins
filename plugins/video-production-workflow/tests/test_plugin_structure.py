from pathlib import Path
import json

EXPECTED = {
    "plan-video-production",
    "install-video-toolchain",
    "ingest-video-assets",
    "analyze-video-content",
    "analyze-music-pacing",
    "design-video-storyboards",
    "compose-slideshow-video",
    "edit-dialogue-footage",
    "edit-davinci-resolve",
    "create-video-typography",
    "create-motion-graphics",
    "mix-video-audio",
    "render-video-project",
    "exchange-video-timelines",
    "conform-video-delivery",
    "validate-video-quality",
    "evolve-video-workflow",
}


def test_plugin_manifest_and_skill_structure() -> None:
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / ".codex-plugin/plugin.json").read_text())
    assert manifest["name"] == "video-production-workflow"
    skills = root / "skills"
    assert {p.name for p in skills.iterdir() if p.is_dir()} == EXPECTED
    for skill in EXPECTED:
        path = skills / skill
        assert (path / "SKILL.md").is_file()
        assert (path / "agents/openai.yaml").is_file()
        if skill != "edit-davinci-resolve":
            assert any((path / "agents").glob("*.md"))
            assert any((path / "scripts").glob("*"))
        assert any((path / "references").glob("*.md"))
        assert (path / "references/sources/source-index.md").is_file()
