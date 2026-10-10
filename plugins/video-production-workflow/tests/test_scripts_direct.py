import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_check_environment_runs_without_editable_install():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "check_environment.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(proc.stdout)
    assert "binaries" in report
    assert "ffmpeg_capabilities" in report


def test_skill_entry_point_can_show_help_without_editable_install():
    script = ROOT / "skills" / "validate-video-quality" / "scripts" / "run.py"
    proc = subprocess.run(
        [sys.executable, str(script), "--help"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "usage:" in proc.stdout.lower()


def test_toolchain_installer_has_non_destructive_json_plan():
    script = ROOT / "scripts" / "install_toolchain.py"
    proc = subprocess.run(
        [sys.executable, str(script), "--profile", "production", "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    plan = json.loads(proc.stdout)
    assert plan["apply"] is False
    assert plan["profile"] == "production"
    assert plan["commands"]
    assert plan["manual_steps"]


def test_runtime_configurator_copies_verified_media_tools(tmp_path):
    tool = tmp_path / "fake-media-tool"
    tool.write_text("#!/bin/sh\nprintf 'fake version 1\\n'\n")
    tool.chmod(0o755)
    runtime = tmp_path / "runtime"
    script = ROOT / "scripts" / "configure_runtime.py"
    subprocess.run(
        [
            sys.executable,
            str(script),
            "--ffmpeg",
            str(tool),
            "--ffprobe",
            str(tool),
            "--mode",
            "copy",
            "--runtime-root",
            str(runtime),
        ],
        check=True,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert (runtime / "bin" / "ffmpeg").is_file()
    assert (runtime / "bin" / "ffprobe").is_file()
    report = json.loads((runtime / "runtime-report.json").read_text())
    assert report["mode"] == "copy"
