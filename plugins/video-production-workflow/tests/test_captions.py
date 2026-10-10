from pathlib import Path

from video_workflow.captions import parse_srt, cue_reading_speed, write_ass


def test_parse_srt_and_reading_speed(tmp_path: Path) -> None:
    srt = tmp_path / "in.srt"
    srt.write_text("1\n00:00:01,000 --> 00:00:03,000\nHello there friend.\n", encoding="utf-8")
    cues = parse_srt(srt)
    assert cues[0]["start"] == 1.0
    assert cues[0]["end"] == 3.0
    assert cue_reading_speed(cues[0]) == 1.5


def test_write_ass_contains_style_and_dialogue(tmp_path: Path) -> None:
    out = tmp_path / "captions.ass"
    cues = [{"start": 0.0, "end": 1.5, "text": "Hello"}]
    write_ass(cues, out, width=1080, height=1920, style={"font": "DejaVu Sans", "font_size": 72})
    text = out.read_text(encoding="utf-8")
    assert "[V4+ Styles]" in text
    assert "Dialogue:" in text
    assert "Hello" in text
