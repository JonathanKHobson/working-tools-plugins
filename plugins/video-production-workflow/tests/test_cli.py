from pathlib import Path
import json

from video_workflow.cli import main


def test_cli_new_project(tmp_path: Path) -> None:
    out = tmp_path / "project.json"
    rc = main(["new", str(out), "--id", "cli-test", "--preset", "vertical-1080"])
    assert rc == 0
    data = json.loads(out.read_text())
    assert data["delivery"]["width"] == 1080
    assert data["delivery"]["height"] == 1920
