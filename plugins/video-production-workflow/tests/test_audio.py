from pathlib import Path
import subprocess

from video_workflow.audio import analyze_music
from video_workflow.utils import require_tool


def test_click_track_bpm_is_reasonable(tmp_path: Path) -> None:
    wav = tmp_path / "click.wav"
    subprocess.run([
        require_tool("ffmpeg"), "-y", "-f", "lavfi", "-i",
        "aevalsrc='if(lt(mod(t,0.5),0.01),0.9*sin(2*PI*1000*t),0)':s=22050:d=8",
        str(wav),
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    result = analyze_music(wav, use_librosa=True)
    assert 110 <= result["tempo_bpm"] <= 130
    assert len(result["beats_s"]) >= 10
