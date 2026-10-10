from pathlib import Path

from video_workflow.utils import resolve_tool, run


def _fake_tool(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("#!/bin/sh\nprintf 'resolved-tool\\n'\n", encoding="utf-8")
    path.chmod(0o755)
    return path


def test_resolve_tool_prefers_explicit_environment_override(tmp_path: Path, monkeypatch) -> None:
    fake = _fake_tool(tmp_path / "custom-ffmpeg")
    monkeypatch.setenv("VIDEO_WORKFLOW_FFMPEG", str(fake))
    assert resolve_tool("ffmpeg") == str(fake.resolve())


def test_resolve_tool_uses_plugin_runtime_directory(tmp_path: Path, monkeypatch) -> None:
    fake = _fake_tool(tmp_path / ".runtime" / "bin" / "ffprobe")
    monkeypatch.delenv("VIDEO_WORKFLOW_FFPROBE", raising=False)
    monkeypatch.delenv("FFPROBE", raising=False)
    monkeypatch.setenv("VIDEO_WORKFLOW_HOME", str(tmp_path))
    assert resolve_tool("ffprobe") == str(fake.resolve())


def test_run_resolves_named_media_tool_before_execution(tmp_path: Path, monkeypatch) -> None:
    fake = _fake_tool(tmp_path / "ffmpeg")
    monkeypatch.setenv("VIDEO_WORKFLOW_FFMPEG", str(fake))
    result = run(["ffmpeg"], capture=True)
    assert result.stdout.strip() == "resolved-tool"
