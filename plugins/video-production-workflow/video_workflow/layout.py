from __future__ import annotations

from math import floor
from pathlib import Path
from typing import Any

from PIL import ImageFont


def _parse_hex(color: str) -> tuple[int, int, int]:
    value = color.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    if len(value) != 6:
        raise ValueError(f"Expected #RRGGBB color, got {color!r}")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _relative_luminance(color: str) -> float:
    channels = []
    for channel in _parse_hex(color):
        value = channel / 255.0
        channels.append(value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast_ratio(foreground: str, background: str) -> float:
    a = _relative_luminance(foreground)
    b = _relative_luminance(background)
    lighter, darker = max(a, b), min(a, b)
    return (lighter + 0.05) / (darker + 0.05)


def safe_rect(width: int, height: int, *, margin_pct: float = 0.08) -> tuple[int, int, int, int]:
    if not 0 <= margin_pct < 0.5:
        raise ValueError("margin_pct must be between 0 and 0.5")
    x = round(width * margin_pct)
    y = round(height * margin_pct)
    return x, y, width - 2 * x, height - 2 * y


def safe_rect_sides(
    width: int,
    height: int,
    *,
    left_pct: float,
    right_pct: float,
    top_pct: float,
    bottom_pct: float,
) -> tuple[int, int, int, int]:
    values = (left_pct, right_pct, top_pct, bottom_pct)
    if any(value < 0 or value >= 0.5 for value in values):
        raise ValueError("safe-area percentages must be between 0 and 0.5")
    if left_pct + right_pct >= 1 or top_pct + bottom_pct >= 1:
        raise ValueError("opposing safe-area percentages must leave positive space")
    left = round(width * left_pct)
    right = round(width * right_pct)
    top = round(height * top_pct)
    bottom = round(height * bottom_pct)
    return left, top, width - left - right, height - top - bottom


def safe_rect_from_style(width: int, height: int, style: dict[str, Any] | None) -> tuple[int, int, int, int]:
    style = style or {}
    area = style.get("safe_area")
    if isinstance(area, dict):
        fallback = float(style.get("safe_margin_pct", 0.08))
        return safe_rect_sides(
            width,
            height,
            left_pct=float(area.get("left_pct", fallback)),
            right_pct=float(area.get("right_pct", fallback)),
            top_pct=float(area.get("top_pct", fallback)),
            bottom_pct=float(area.get("bottom_pct", fallback)),
        )
    return safe_rect(width, height, margin_pct=float(style.get("safe_margin_pct", 0.08)))


def _measurement_font(font_size: int, font: str | None = None) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    from .fonts import resolve_font_file
    try:
        return ImageFont.truetype(str(resolve_font_file(font)), font_size)
    except ValueError:
        # Nonrendering layout checks can run without an installed system font.
        # Rendering resolves a real font first and fails explicitly if absent.
        return ImageFont.load_default(size=font_size)


def _line_width(text: str, font: ImageFont.FreeTypeFont | ImageFont.ImageFont) -> float:
    left, _, right, _ = font.getbbox(text or " ")
    return float(right - left)


def wrap_text_to_width(
    text: str,
    *,
    max_width: int,
    font_size: int,
    font: str | None = None,
) -> str:
    """Wrap text against measured pixel width while preserving explicit breaks."""
    if max_width <= 0:
        raise ValueError("max_width must be positive")
    face = _measurement_font(font_size, font)
    output: list[str] = []
    for paragraph in str(text).replace("\r\n", "\n").split("\n"):
        words = paragraph.split()
        if not words:
            output.append("")
            continue
        line = words[0]
        for word in words[1:]:
            candidate = f"{line} {word}"
            if _line_width(candidate, face) <= max_width:
                line = candidate
            else:
                output.append(line)
                line = word
        output.append(line)
    return "\n".join(output)


def fit_rect(source_width: int, source_height: int, target_width: int, target_height: int, *, mode: str = "contain") -> tuple[int, int, int, int]:
    if mode not in {"contain", "cover"}:
        raise ValueError("mode must be contain or cover")
    scale_x = target_width / source_width
    scale_y = target_height / source_height
    scale = min(scale_x, scale_y) if mode == "contain" else max(scale_x, scale_y)
    width = max(1, round(source_width * scale))
    height = max(1, round(source_height * scale))
    x = floor((target_width - width) / 2)
    y = floor((target_height - height) / 2)
    return x, y, width, height


def recommended_text_size(frame_height: int, role: str = "body") -> int:
    ratios = {"caption": 0.050, "body": 0.055, "subtitle": 0.065, "title": 0.095, "display": 0.13}
    if role not in ratios:
        raise ValueError(f"Unknown text role: {role}")
    return max(18, round(frame_height * ratios[role]))
