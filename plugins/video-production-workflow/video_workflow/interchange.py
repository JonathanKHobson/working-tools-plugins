from __future__ import annotations

from pathlib import Path
from typing import Any

from .manifest import load_project


def _tc(seconds: float, fps: int) -> str:
    frames = round(seconds * fps)
    h, rem = divmod(frames, fps * 3600)
    m, rem = divmod(rem, fps * 60)
    s, f = divmod(rem, fps)
    return f"{h:02d}:{m:02d}:{s:02d}:{f:02d}"


def export_cmx3600(manifest: str | Path, output: str | Path) -> Path:
    project = load_project(manifest)
    fps = int(project["delivery"]["fps"])
    lines = [f"TITLE: {project['project'].get('title', project['project']['id'])}", "FCM: NON-DROP FRAME", ""]
    event = 1
    for item in sorted(project["timeline"], key=lambda entry: float(entry["start"])):
        if item["kind"] not in {"video", "animation"}:
            continue
        source_start = float(item.get("source_start", 0.0))
        duration = float(item["duration"])
        record_start = float(item["start"])
        asset_id = str(item.get("asset", "SOURCE"))[:8].upper()
        lines.append(f"{event:03d}  {asset_id:<8} V     C        {_tc(source_start, fps)} {_tc(source_start+duration, fps)} {_tc(record_start, fps)} {_tc(record_start+duration, fps)}")
        lines.append(f"* FROM CLIP NAME: {project['assets'][item['asset']]['path']}")
        lines.append("")
        event += 1
    Path(output).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return Path(output)


def export_otio(manifest: str | Path, output: str | Path) -> Path:
    try:
        import opentimelineio as otio
    except ImportError as exc:
        raise RuntimeError("OpenTimelineIO is optional. Install with: pip install 'video-production-workflow[interchange]'") from exc
    project = load_project(manifest)
    rate = float(project["delivery"]["fps"])
    timeline = otio.schema.Timeline(name=project["project"].get("title", project["project"]["id"]))
    track = otio.schema.Track(name="V1", kind=otio.schema.TrackKind.Video)
    timeline.tracks.append(track)
    for item in sorted(project["timeline"], key=lambda entry: float(entry["start"])):
        if item["kind"] not in {"video", "animation", "image"}:
            continue
        asset = project["assets"][item["asset"]]
        duration = otio.opentime.RationalTime(float(item["duration"]) * rate, rate)
        start = otio.opentime.RationalTime(float(item.get("source_start", 0.0)) * rate, rate)
        media_ref = otio.schema.ExternalReference(target_url=str(asset["path"]), available_range=otio.opentime.TimeRange(start, duration))
        clip = otio.schema.Clip(name=str(item["id"]), media_reference=media_ref, source_range=otio.opentime.TimeRange(start, duration))
        clip.metadata["video-production-workflow"] = {"record_start_s": float(item["start"]), "kind": item["kind"]}
        track.append(clip)
    otio.adapters.write_to_file(timeline, str(output))
    return Path(output)
