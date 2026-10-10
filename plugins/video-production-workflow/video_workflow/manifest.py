from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

from .errors import ManifestError

PRESETS = {
    "landscape-1080": (1920, 1080, 30),
    "cinema-1080": (1920, 1080, 24),
    "vertical-1080": (1080, 1920, 30),
    "square-1080": (1080, 1080, 30),
    "portrait-4x5": (1080, 1350, 30),
    "uhd-4k": (3840, 2160, 24),
}


def aspect_ratio_label(width: int, height: int) -> str:
    from math import gcd

    divisor = gcd(width, height)
    return f"{width // divisor}:{height // divisor}"


def default_project(project_id: str, *, width: int = 1920, height: int = 1080, fps: int = 30) -> dict[str, Any]:
    clean_id = re.sub(r"[^a-zA-Z0-9_-]+", "-", project_id).strip("-") or "video-project"
    return {
        "version": 1,
        "project": {
            "id": clean_id,
            "title": clean_id.replace("-", " ").title(),
            "intent": "",
            "audience": "",
            "status": "draft",
        },
        "delivery": {
            "width": int(width),
            "height": int(height),
            "fps": int(fps),
            "aspect_ratio": aspect_ratio_label(int(width), int(height)),
            "video_codec": "libx264",
            "audio_codec": "aac",
            "pixel_format": "yuv420p",
            "color_space": "bt709",
            "container": "mp4",
        },
        "style": {
            "background": "#0B0D12",
            "foreground": "#FFFFFF",
            "accent": "#7C6CFF",
            "font": "DejaVu Sans",
            "safe_margin_pct": 0.08,
            "safe_area": {
                "left_pct": 0.08,
                "right_pct": 0.08,
                "top_pct": 0.08,
                "bottom_pct": 0.08,
            },
            "reading": {
                "words_per_second": 3.0,
                "minimum_text_hold_s": 2.5,
            },
            "copy_constraints": {"disallowed_characters": []},
            "motion_intensity": "moderate",
        },
        "assets": {},
        "timeline": [],
        "audio": {
            "music": None,
            "voiceover": None,
            "loudness": {"enabled": True, "target_lufs": -16.0, "true_peak_db": -1.5, "lra": 11.0},
        },
        "captions": {"enabled": False, "source": None, "format": "ass", "burn_in": True},
        "render": {"quality": "preview", "cache": True, "faststart": True},
        "qa": {
            "required": ["probe", "duration", "streams", "frame-samples", "audio-peak"],
            "max_asset_uses_per_video": 0,
            "minimum_cta_hold_s": 2.5,
        },
        "provenance": {"sources": [], "decisions": []},
    }


def project_from_preset(project_id: str, preset: str) -> dict[str, Any]:
    try:
        width, height, fps = PRESETS[preset]
    except KeyError as exc:
        raise ManifestError(f"Unknown preset {preset!r}. Choose from: {', '.join(sorted(PRESETS))}") from exc
    return default_project(project_id, width=width, height=height, fps=fps)


def validate_project(project: dict[str, Any]) -> None:
    if project.get("version") != 1:
        raise ManifestError("Manifest version must be 1")
    for section in ("project", "delivery", "assets", "timeline"):
        if section not in project:
            raise ManifestError(f"Missing required section: {section}")
    delivery = project["delivery"]
    for key in ("width", "height", "fps"):
        if not isinstance(delivery.get(key), int) or delivery[key] <= 0:
            raise ManifestError(f"delivery.{key} must be a positive integer")
    style = project.get("style") or {}
    area = style.get("safe_area")
    if area is not None:
        if not isinstance(area, dict):
            raise ManifestError("style.safe_area must be an object")
        values = {
            name: float(area.get(name, style.get("safe_margin_pct", 0.08)))
            for name in ("left_pct", "right_pct", "top_pct", "bottom_pct")
        }
        if any(value < 0 or value >= 0.5 for value in values.values()):
            raise ManifestError("style.safe_area percentages must be between 0 and 0.5")
        if values["left_pct"] + values["right_pct"] >= 1:
            raise ManifestError("style.safe_area horizontal percentages leave no usable width")
        if values["top_pct"] + values["bottom_pct"] >= 1:
            raise ManifestError("style.safe_area vertical percentages leave no usable height")
    ids: set[str] = set()
    for index, item in enumerate(project["timeline"]):
        if not isinstance(item, dict):
            raise ManifestError(f"timeline[{index}] must be an object")
        item_id = str(item.get("id", ""))
        if not item_id:
            raise ManifestError(f"timeline[{index}] is missing id")
        if item_id in ids:
            raise ManifestError(f"Duplicate timeline id: {item_id}")
        ids.add(item_id)
        if float(item.get("start", -1)) < 0 or float(item.get("duration", 0)) <= 0:
            raise ManifestError(f"timeline item {item_id} requires start >= 0 and duration > 0")
        kind = item.get("kind")
        if kind not in {"image", "video", "card", "animation"}:
            raise ManifestError(f"Unsupported timeline kind {kind!r} in {item_id}")
        if item.get("text_align") not in {None, "left", "center", "right"}:
            raise ManifestError(f"Unsupported text_align in {item_id}")
        if item.get("text_position") not in {None, "top", "middle", "center", "lower", "bottom"}:
            raise ManifestError(f"Unsupported text_position in {item_id}")
        asset = item.get("asset")
        if kind in {"image", "video", "animation"} and asset not in project["assets"]:
            raise ManifestError(f"Timeline item {item_id} references unknown asset {asset!r}")


def load_project(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    text = source.read_text(encoding="utf-8")
    if source.suffix.lower() in {".yaml", ".yml"}:
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ManifestError("Project manifest must contain an object")
    validate_project(data)
    data.setdefault("_manifest_path", str(source.resolve()))
    return data


def save_project(project: dict[str, Any], path: str | Path) -> None:
    target = Path(path)
    data = {k: v for k, v in project.items() if not k.startswith("_")}
    validate_project(data)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.suffix.lower() in {".yaml", ".yml"}:
        target.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
    else:
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
