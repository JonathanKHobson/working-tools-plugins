from video_workflow.layout import (
    contrast_ratio,
    fit_rect,
    safe_rect,
    safe_rect_sides,
    wrap_text_to_width,
)


def test_wcag_contrast_examples() -> None:
    assert round(contrast_ratio("#000000", "#ffffff"), 1) == 21.0
    assert contrast_ratio("#777777", "#ffffff") >= 4.4


def test_fit_rect_contain_and_cover() -> None:
    contain = fit_rect(1920, 1080, 1080, 1920, mode="contain")
    assert contain[2] == 1080
    assert contain[3] < 1920
    cover = fit_rect(1920, 1080, 1080, 1920, mode="cover")
    assert cover[3] == 1920
    assert cover[2] > 1080


def test_safe_rect_is_inset() -> None:
    x, y, w, h = safe_rect(1080, 1920, margin_pct=0.1)
    assert (x, y) == (108, 192)
    assert (w, h) == (864, 1536)


def test_asymmetric_safe_rect_preserves_vertical_control_lane() -> None:
    x, y, w, h = safe_rect_sides(
        1080,
        1920,
        left_pct=0.056,
        right_pct=0.20,
        top_pct=0.08,
        bottom_pct=0.18,
    )
    assert x == 60
    assert x + w == 864
    assert y == 154
    assert y + h == 1574


def test_text_wrap_preserves_explicit_breaks_and_bounds() -> None:
    wrapped = wrap_text_to_width(
        "Pick a vibe\nnot homework",
        max_width=420,
        font_size=64,
    )
    assert "\n" in wrapped
    assert wrapped.splitlines()[0] == "Pick a vibe"
