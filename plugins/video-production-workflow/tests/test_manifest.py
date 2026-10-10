from pathlib import Path

from video_workflow.manifest import default_project, load_project, save_project, validate_project
from video_workflow.timeline import project_duration


def test_default_project_is_valid(tmp_path: Path) -> None:
    project = default_project("demo", width=1080, height=1920, fps=30)
    validate_project(project)
    assert project["delivery"]["aspect_ratio"] == "9:16"
    out = tmp_path / "project.json"
    save_project(project, out)
    loaded = load_project(out)
    assert loaded["project"]["id"] == "demo"


def test_project_duration_accounts_for_overlaps() -> None:
    project = default_project("duration")
    project["timeline"] = [
        {"id": "a", "kind": "card", "start": 0.0, "duration": 3.0, "text": "A"},
        {"id": "b", "kind": "card", "start": 2.5, "duration": 2.0, "text": "B"},
    ]
    assert project_duration(project) == 4.5
