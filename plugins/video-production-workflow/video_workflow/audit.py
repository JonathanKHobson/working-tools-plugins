from __future__ import annotations

import re
from collections import Counter
from typing import Any

from .manifest import validate_project
from .timeline import project_duration


def _issue(
    issues: list[dict[str, Any]],
    code: str,
    message: str,
    *,
    severity: str = "warning",
    item_id: str | None = None,
) -> None:
    entry: dict[str, Any] = {"code": code, "severity": severity, "message": message}
    if item_id:
        entry["item_id"] = item_id
    issues.append(entry)


def audit_project(project: dict[str, Any]) -> dict[str, Any]:
    """Audit editorial constraints that JSON Schema alone cannot express."""
    validate_project(project)
    issues: list[dict[str, Any]] = []
    style = project.get("style") or {}
    qa = project.get("qa") or {}
    delivery = project.get("delivery") or {}

    safe_area = style.get("safe_area")
    if delivery.get("platform"):
        reviewed = isinstance(safe_area, dict) and safe_area.get("reviewed_at") and safe_area.get("source")
        if not reviewed:
            _issue(
                issues,
                "platform-safe-area-unreviewed",
                "Platform delivery requires a dated safe-area review and source.",
            )

    max_asset_uses = int(qa.get("max_asset_uses_per_video", 0) or 0)
    if max_asset_uses > 0:
        usage = Counter(
            str(item["asset"])
            for item in project.get("timeline", [])
            if item.get("asset") is not None
        )
        for asset, count in sorted(usage.items()):
            if count > max_asset_uses:
                _issue(
                    issues,
                    "asset-reuse-exceeded",
                    f"Asset {asset!r} appears {count} times; configured maximum is {max_asset_uses}.",
                )

    reading = style.get("reading") or {}
    words_per_second = max(0.1, float(reading.get("words_per_second", 3.0)))
    minimum_text_hold = max(0.0, float(reading.get("minimum_text_hold_s", 2.5)))
    copy_constraints = style.get("copy_constraints") or {}
    disallowed = [str(value) for value in copy_constraints.get("disallowed_characters", [])]
    minimum_cta_hold = max(0.0, float(qa.get("minimum_cta_hold_s", 2.5)))

    for item in project.get("timeline", []):
        text = str(item.get("text") or "")
        item_id = str(item.get("id") or "")
        duration = float(item.get("duration") or 0.0)
        if text:
            words = len(re.findall(r"\b[\w’'-]+\b", text))
            required = max(minimum_text_hold, words / words_per_second)
            if duration + 1e-6 < required:
                _issue(
                    issues,
                    "text-hold-too-short",
                    f"Text needs approximately {required:.2f}s but the item lasts {duration:.2f}s.",
                    item_id=item_id,
                )
            for character in disallowed:
                if character and character in text:
                    _issue(
                        issues,
                        "copy-constraint",
                        f"Text contains disallowed character {character!r}.",
                        item_id=item_id,
                    )
        if item.get("role") == "cta" and duration + 1e-6 < minimum_cta_hold:
            _issue(
                issues,
                "cta-hold-too-short",
                f"Call-to-action hold is {duration:.2f}s; minimum is {minimum_cta_hold:.2f}s.",
                severity="error",
                item_id=item_id,
            )

    music = (project.get("audio") or {}).get("music")
    if isinstance(music, dict) and (float(music.get("start", 0.0) or 0.0) > 0 or music.get("end") is not None):
        review = music.get("boundary_review")
        valid = (
            isinstance(review, dict)
            and review.get("start_natural") is True
            and review.get("end_natural") is True
            and bool(str(review.get("method") or "").strip())
        )
        if not valid:
            _issue(
                issues,
                "music-boundary-review-missing",
                "A trimmed music segment requires confirmed natural start/end boundaries and a review method.",
                severity="error",
            )
        if music.get("end") is not None:
            segment_duration = float(music["end"]) - float(music.get("start", 0.0) or 0.0)
            video_duration = project_duration(project)
            if segment_duration + 0.15 < video_duration:
                _issue(
                    issues,
                    "music-segment-too-short",
                    f"Music excerpt is {segment_duration:.2f}s but the video timeline is {video_duration:.2f}s.",
                    severity="error",
                )

    return {
        "passed": not any(issue["severity"] == "error" for issue in issues),
        "issues": issues,
        "summary": {
            "errors": sum(issue["severity"] == "error" for issue in issues),
            "warnings": sum(issue["severity"] == "warning" for issue in issues),
        },
    }
