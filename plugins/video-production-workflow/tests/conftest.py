"""Synthetic media fixtures for portable package tests."""
from pathlib import Path
import subprocess
import pytest
from video_workflow.utils import require_tool

@pytest.fixture
def sample_video(tmp_path: Path):
    def make(*, width: int = 640, height: int = 360, duration: int = 8) -> Path:
        out = tmp_path / f"sample-{width}x{height}.mp4"
        subprocess.run([require_tool("ffmpeg"), "-y", "-f", "lavfi", "-i",
                        f"testsrc2=size={width}x{height}:rate=24",
                        "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=44100",
                        "-t", str(duration), "-c:v", "mpeg4", "-q:v", "4",
                        "-c:a", "aac", "-shortest", str(out)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return out
    return make
