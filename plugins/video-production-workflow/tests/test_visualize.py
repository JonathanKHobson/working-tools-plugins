from pathlib import Path
from PIL import Image

from video_workflow.visualize import make_contact_sheet, make_timeline_view, make_waveform


def test_visual_evidence_generation(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    video = root / "examples/music-slideshow/output/preview.mp4"
    audio = root / "examples/music-slideshow/assets/music.wav"
    contact = make_contact_sheet(video, tmp_path / "contact.png", count=6, frame_width=240)
    waveform = make_waveform(audio, tmp_path / "wave.png", width=800, height=180)
    timeline = make_timeline_view(video, tmp_path / "timeline.png", start=1.0, end=3.0, count=5, frame_width=200)
    for path in (contact, waveform, timeline):
        assert path.exists() and path.stat().st_size > 1000
        with Image.open(path) as image:
            assert image.width > 200 and image.height > 100
