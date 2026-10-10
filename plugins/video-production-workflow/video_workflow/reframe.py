from __future__ import annotations


def crop_from_anchor(
    source_width: int,
    source_height: int,
    target_width: int,
    target_height: int,
    *,
    anchor_x: float = 0.5,
    anchor_y: float = 0.5,
) -> tuple[float, float, float, float]:
    """Return a cover crop (x, y, width, height) centered on a normalized anchor."""
    if min(source_width, source_height, target_width, target_height) <= 0:
        raise ValueError("Dimensions must be positive")
    anchor_x = min(1.0, max(0.0, float(anchor_x)))
    anchor_y = min(1.0, max(0.0, float(anchor_y)))
    target_ratio = target_width / target_height
    source_ratio = source_width / source_height
    if source_ratio > target_ratio:
        crop_height = float(source_height)
        crop_width = crop_height * target_ratio
    else:
        crop_width = float(source_width)
        crop_height = crop_width / target_ratio
    center_x = anchor_x * source_width
    center_y = anchor_y * source_height
    x = min(max(0.0, center_x - crop_width / 2), source_width - crop_width)
    y = min(max(0.0, center_y - crop_height / 2), source_height - crop_height)
    return (x, y, crop_width, crop_height)
