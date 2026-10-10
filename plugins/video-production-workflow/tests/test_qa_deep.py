from pathlib import Path
from video_workflow.qa import validate_video


def test_deep_qa_emits_temporal_and_peak_checks() -> None:
    root=Path(__file__).resolve().parents[1]
    report=validate_video(root/'examples/music-slideshow/output/preview.mp4', expected_width=640, expected_height=360, expected_duration=8, deep=True)
    names={item['name'] for item in report['checks']}
    assert {'black-segments','freeze-segments','silence-segments','audio-peak'} <= names
    assert report['passed']
