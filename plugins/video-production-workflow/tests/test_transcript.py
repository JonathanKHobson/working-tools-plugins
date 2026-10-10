from video_workflow.transcript import pack_phrases, snap_ranges


def test_pack_phrases_breaks_on_silence_and_speaker() -> None:
    data = {"words": [
        {"text": "Hello", "start": 0.0, "end": 0.3, "speaker": "A", "type": "word"},
        {"text": "there", "start": 0.35, "end": 0.6, "speaker": "A", "type": "word"},
        {"text": "Again", "start": 1.3, "end": 1.6, "speaker": "A", "type": "word"},
        {"text": "Yes", "start": 1.7, "end": 1.9, "speaker": "B", "type": "word"},
    ]}
    phrases = pack_phrases(data, silence_threshold=0.5)
    assert [p["text"] for p in phrases] == ["Hello there", "Again", "Yes"]
    assert phrases[2]["speaker"] == "B"


def test_snap_ranges_uses_word_edges_and_padding() -> None:
    data = {"words": [
        {"text": "One", "start": 1.0, "end": 1.25, "type": "word"},
        {"text": "two", "start": 1.4, "end": 1.65, "type": "word"},
        {"text": "three", "start": 1.9, "end": 2.2, "type": "word"},
    ]}
    result = snap_ranges([{"start": 1.12, "end": 2.05}], data, pad_before=0.05, pad_after=0.08)
    assert result[0]["start"] == 0.95
    assert result[0]["end"] == 2.28
