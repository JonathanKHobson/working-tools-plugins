from video_workflow.reframe import crop_from_anchor


def test_crop_from_anchor_stays_inside_source() -> None:
    crop = crop_from_anchor(1920, 1080, 1080, 1920, anchor_x=0.9, anchor_y=0.5)
    assert crop[2] / crop[3] == 1080 / 1920
    assert crop[0] + crop[2] <= 1920
    assert crop[1] + crop[3] <= 1080
    assert crop[0] > 800
