"""Validate and preview registered, image-generated sprite pose sequences.

This module deliberately does not invent motion. It only holds supplied poses for
the exact frame counts in a manifest and records the resulting frame ranges.

Manifest shape: ``{"fps": 24, "canvas": [W, H], "poses": {"idle":
{"path": "poses/idle.png", "sha256": "..."}}, "timeline":
[{"pose": "idle", "frames": 4, "reason": "settle"}],
"expected_frames": 4}``.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image


class SpriteSequenceError(ValueError):
    """A manifest or supplied pose failed deterministic validation."""


def _fail(message: str) -> None:
    raise SpriteSequenceError(message)


def _path_inside(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative:
        _fail("pose path must be a non-empty string")
    lexical = Path(relative)
    if lexical.is_absolute() or ".." in lexical.parts:
        _fail(f"pose path must be a relative path without '..': {relative}")
    candidate = (root / lexical).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        _fail(f"pose path must resolve within manifest root: {relative}")
    return candidate


def validate_manifest(manifest: dict[str, Any], root: Path | str) -> dict[str, Any]:
    """Validate a manifest against its supplied pose files and return evidence."""
    root = Path(root).resolve()
    if not isinstance(manifest, dict):
        _fail("manifest must be an object")
    fps = manifest.get("fps")
    if isinstance(fps, bool) or not isinstance(fps, int) or fps <= 0:
        _fail("fps must be a positive integer")
    canvas = manifest.get("canvas")
    if not isinstance(canvas, list) or len(canvas) != 2 or any(isinstance(v, bool) or not isinstance(v, int) or v <= 0 for v in canvas):
        _fail("canvas must be [positive width, positive height]")
    poses = manifest.get("poses")
    if not isinstance(poses, dict) or not poses:
        _fail("poses must be a non-empty object")
    pose_images: dict[str, Image.Image] = {}
    for pose_id, spec in poses.items():
        if not isinstance(pose_id, str) or not pose_id or not isinstance(spec, dict):
            _fail("each pose needs an id and object specification")
        path = _path_inside(root, spec.get("path"))
        if not path.is_file():
            _fail(f"pose file does not exist: {spec.get('path')}")
        expected = spec.get("sha256")
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if not isinstance(expected, str) or expected.lower() != actual_hash:
            _fail(f"pose hash mismatch for {pose_id}")
        try:
            source = Image.open(path)
            if source.mode != "RGBA":
                _fail(f"pose must be an RGBA image for {pose_id}, got {source.mode}")
            image = source.copy()
            image.load()
        except Exception as exc:
            _fail(f"pose is not a readable image for {pose_id}: {exc}")
        if list(image.size) != canvas:
            _fail(f"pose canvas mismatch for {pose_id}: {image.size} != {tuple(canvas)}")
        if image.getchannel("A").getbbox() is None:
            _fail(f"pose has no visible alpha for {pose_id}")
        if image.getchannel("A").getextrema() == (255, 255):
            _fail(f"pose must include transparent padding for {pose_id}")
        pose_images[pose_id] = image

    timeline = manifest.get("timeline")
    if not isinstance(timeline, list) or not timeline:
        _fail("timeline must be a non-empty list")
    cursor = 0
    evidence = []
    unique = []
    for entry in timeline:
        if not isinstance(entry, dict):
            _fail("timeline entries must be objects")
        pose = entry.get("pose")
        frames = entry.get("frames")
        reason = entry.get("reason")
        if not isinstance(pose, str) or not pose:
            _fail("timeline pose must be a non-empty string")
        if pose not in pose_images:
            _fail(f"timeline references unknown pose: {pose}")
        if isinstance(frames, bool) or not isinstance(frames, int) or frames <= 0:
            _fail(f"frames must be a positive integer for pose {pose}")
        if not isinstance(reason, str) or not reason.strip():
            _fail(f"timeline reason must be a non-empty string for pose {pose}")
        if pose not in unique:
            unique.append(pose)
        evidence.append({"pose": pose, "frames": frames, "frame_start": cursor, "frame_end": cursor + frames - 1,
                         "reason": reason.strip()})
        cursor += frames
    expected_frames = manifest.get("expected_frames")
    if isinstance(expected_frames, bool) or not isinstance(expected_frames, int) or expected_frames <= 0:
        _fail("expected_frames must be a positive integer")
    if cursor != expected_frames:
        _fail(f"timeline has {cursor} frames; expected {expected_frames}")
    used_hashes = {poses[pose]["sha256"].lower() for pose in unique}
    return {"fps": fps, "canvas": canvas, "frame_count": cursor, "unique_poses": unique,
            "distinct_artwork_count": len(used_hashes),
            "timeline": evidence, "pose_files": {k: str(_path_inside(root, poses[k]["path"])) for k in poses}}


def render_sequence(manifest: dict[str, Any], root: Path | str, output_dir: Path | str) -> dict[str, Any]:
    """Render supplied poses as a GIF and timestamped stills; never alters source poses."""
    root = Path(root).resolve()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    evidence = validate_manifest(manifest, root)
    images = {pose: Image.open(path).convert("RGBA") for pose, path in evidence["pose_files"].items()}
    frames = [images[item["pose"]].copy() for item in evidence["timeline"] for _ in range(item["frames"])]
    gif_path = output_dir / "sequence.gif"
    # GIF stores centiseconds. Allocate durations by cumulative rounding so total
    # duration follows the exact source frame ledger as closely as GIF permits.
    boundaries = [round(i * 100 / evidence["fps"]) for i in range(len(frames) + 1)]
    durations = [max(1, boundaries[i + 1] - boundaries[i]) * 10 for i in range(len(frames))]
    # Quantize against a constant review backdrop; do not request palette index 0
    # transparency, which can erase arbitrary sprite colors.
    backdrop = Image.new("RGBA", tuple(evidence["canvas"]), (28, 32, 40, 255))
    gif_frames = [Image.alpha_composite(backdrop, frame).convert("RGB") for frame in frames]
    gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:], duration=durations, loop=0, disposal=2)
    stills = []
    indexes = sorted(set([0, len(frames) // 3, (2 * len(frames)) // 3, len(frames) - 1]))
    for i, frame_index in enumerate(indexes):
        path = output_dir / f"still-{i+1:02d}-frame-{frame_index:04d}.png"
        frames[frame_index].save(path)
        stills.append(str(path))
    return {"gif": str(gif_path), "stills": stills, "frame_count": len(frames),
            "distinct_artwork_count": evidence["distinct_artwork_count"],
            "gif_timing": {"source_fps": evidence["fps"], "duration_ms_total": sum(durations), "duration_ms_per_frame": durations, "note": "GIF duration is centisecond-quantized; use source frame accounting for exact timing."},
            "still_limitations": None if len(stills) >= 4 else f"Only {len(stills)} unique frame(s) available; four distinct stills require at least four source frames.",
            "timeline": evidence["timeline"]}


def load_manifest(path: Path | str) -> tuple[dict[str, Any], Path]:
    path = Path(path).resolve()
    try:
        return json.loads(path.read_text()), path.parent
    except Exception as exc:
        _fail(f"could not read manifest: {exc}")

