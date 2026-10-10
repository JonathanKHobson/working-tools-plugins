from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from .fonts import resolve_font_file
from .layout import safe_rect_from_style, wrap_text_to_width
from .manifest import load_project, validate_project
from .timeline import project_duration
from .utils import require_tool, run


def _resolve_asset(project: dict[str, Any], asset_id: str, manifest_dir: Path) -> Path:
    asset = project["assets"].get(asset_id)
    if not asset:
        raise ValueError(f"Unknown asset: {asset_id}")
    path = Path(asset["path"])
    return path if path.is_absolute() else (manifest_dir / path).resolve()


def _escape_filter_path(path: Path) -> str:
    value = str(path.resolve()).replace("\\", "/")
    return value.replace(":", "\\:").replace("'", "\\'")


def _fit_filter(width: int, height: int, mode: str) -> str:
    if mode == "contain":
        return f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"
    return f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}"


def _motion_filter(motion: str, width: int, height: int, fps: int, duration: float, fit: str = "cover") -> str:
    frames = max(1, round(duration * fps))
    if motion == "none":
        return ""
    if fit == "contain":
        # Animate the already letterboxed canvas so mixed-orientation assets remain fully visible.
        base = _fit_filter(width, height, "contain")
        zoom_max = 1.04
        pan_zoom = 1.03
    else:
        # Overscale first so cover-mode pan expressions never expose borders.
        base = f"scale={round(width * 1.12)}:{round(height * 1.12)}:force_original_aspect_ratio=increase,crop={round(width * 1.12)}:{round(height * 1.12)}"
        zoom_max = 1.12
        pan_zoom = 1.08
    if motion == "zoom-in":
        zp = f"zoompan=z='min({zoom_max},1+({zoom_max}-1)*on/{frames})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={width}x{height}:fps={fps}"
    elif motion == "zoom-out":
        zp = f"zoompan=z='max(1,{zoom_max}-({zoom_max}-1)*on/{frames})':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={width}x{height}:fps={fps}"
    elif motion == "pan-left":
        zp = f"zoompan=z='{pan_zoom}':x='(iw-iw/zoom)*(1-on/{frames})':y='ih/2-(ih/zoom/2)':d={frames}:s={width}x{height}:fps={fps}"
    elif motion == "pan-right":
        zp = f"zoompan=z='{pan_zoom}':x='(iw-iw/zoom)*(on/{frames})':y='ih/2-(ih/zoom/2)':d={frames}:s={width}x{height}:fps={fps}"
    else:
        return ""
    return f"{base},{zp}"


def _text_filter(text_file: Path, project: dict[str, Any], item: dict[str, Any], *, kind: str, font_file: Path) -> str:
    style = project.get("style", {})
    font_size = int(item.get("font_size") or round(project["delivery"]["height"] * 0.075))
    color = (item.get("text_color") or style.get("foreground", "#FFFFFF")).lstrip("#")
    box_color = (item.get("text_box_color") or "#000000").lstrip("#")
    width = int(project["delivery"]["width"])
    height = int(project["delivery"]["height"])
    safe_x, safe_y, safe_w, safe_h = safe_rect_from_style(width, height, style)
    offset_x = int(item.get("text_offset_x", 0))
    offset_y = int(item.get("text_offset_y", 0))
    align = str(item.get("text_align", "center"))
    if align == "left":
        x = f"{safe_x + offset_x}"
    elif align == "right":
        x = f"{safe_x + safe_w}-text_w+{offset_x}"
    else:
        x = f"{safe_x}+({safe_w}-text_w)/2+{offset_x}"

    position = str(item.get("text_position") or ("center" if kind == "card" else "lower"))
    if "text_y" in item:
        y = str(item["text_y"])
    elif position == "top":
        y = f"{safe_y + offset_y}"
    elif position in {"middle", "center"}:
        y = f"{safe_y}+({safe_h}-text_h)/2+{offset_y}"
    elif position == "bottom":
        y = f"{safe_y + safe_h}-text_h+{offset_y}"
    else:
        y = f"{safe_y}+{safe_h}*0.68-text_h/2+{offset_y}"
    return (
        f"drawtext=fontfile='{_escape_filter_path(font_file)}':textfile='{_escape_filter_path(text_file)}':"
        f"fontsize={font_size}:fontcolor=0x{color}:borderw=3:bordercolor=black@0.85:"
        f"box=1:boxcolor=0x{box_color}@0.35:boxborderw=18:"
        f"line_spacing={max(4, round(font_size * 0.12))}:x={x}:y={y}"
    )


def _render_segment(project: dict[str, Any], item: dict[str, Any], manifest_dir: Path, out: Path, text_dir: Path) -> None:
    delivery = project["delivery"]
    width, height, fps = int(delivery["width"]), int(delivery["height"]), int(delivery["fps"])
    duration = float(item["duration"])
    kind = item["kind"]
    filters: list[str] = []
    if kind == "card":
        background = (item.get("background") or project.get("style", {}).get("background", "#000000")).replace("#", "0x")
        cmd = ["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"color=c={background}:s={width}x{height}:r={fps}:d={duration}"]
    else:
        source = _resolve_asset(project, str(item["asset"]), manifest_dir)
        if kind == "image":
            cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(fps), "-i", str(source), "-t", f"{duration:.6f}"]
            motion = str(item.get("motion", "none"))
            motion_filter = _motion_filter(motion, width, height, fps, duration, str(item.get("fit", "cover")))
            if motion_filter:
                filters.append(motion_filter)
            else:
                filters.append(_fit_filter(width, height, str(item.get("fit", "cover"))))
        elif kind in {"video", "animation"}:
            source_start = float(item.get("source_start", 0.0))
            cmd = ["ffmpeg", "-y", "-v", "error", "-ss", f"{source_start:.6f}", "-i", str(source), "-t", f"{duration:.6f}"]
            filters.append(_fit_filter(width, height, str(item.get("fit", "cover"))))
        else:
            raise ValueError(f"Unsupported kind: {kind}")
    if item.get("text"):
        text_file = text_dir / f"{item['id']}.txt"
        style = project.get("style", {})
        _, _, safe_w, _ = safe_rect_from_style(width, height, style)
        font_size = int(item.get("font_size") or round(height * 0.075))
        max_width = int(item.get("text_max_width_px") or max(80, safe_w - 48))
        max_width = min(max_width, max(80, safe_w - 24))
        font_file = resolve_font_file(str(item.get("font") or style.get("font", "DejaVu Sans")), base_dir=manifest_dir)
        wrapped = wrap_text_to_width(
            str(item["text"]),
            max_width=max_width,
            font_size=font_size,
            font=str(font_file),
        )
        text_file.write_text(wrapped, encoding="utf-8")
        filters.append(_text_filter(text_file, project, item, kind=kind, font_file=font_file))
    # Gentle edge fades prevent abrupt flashes, but preserve actual editorial overlap math.
    fade_duration = min(0.12, duration / 10)
    filters.extend([f"fade=t=in:st=0:d={fade_duration}", f"fade=t=out:st={max(0, duration-fade_duration):.6f}:d={fade_duration}", "setsar=1", "format=yuv420p"])
    cmd += [
        "-vf", ",".join(filters), "-an", "-r", str(fps), "-c:v", delivery.get("video_codec", "libx264"),
        "-preset", "veryfast", "-crf", "20", "-pix_fmt", delivery.get("pixel_format", "yuv420p"), "-movflags", "+faststart", str(out)
    ]
    run(cmd)


def _combine_segments(project: dict[str, Any], segments: list[Path], timeline: list[dict[str, Any]], out: Path) -> None:
    if len(segments) == 1:
        shutil.copy2(segments[0], out)
        return
    transitions = [float((timeline[i].get("transition") or {}).get("duration", 0.0)) for i in range(len(segments) - 1)]
    if not any(value > 0 for value in transitions):
        concat_file = out.parent / "concat.txt"
        concat_file.write_text("".join(f"file '{path.resolve()}'\n" for path in segments), encoding="utf-8")
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(out)])
        return
    inputs: list[str] = []
    for path in segments:
        inputs.extend(["-i", str(path)])
    filters: list[str] = []
    current_label = "[0:v]"
    cumulative = float(timeline[0]["duration"])
    for index in range(1, len(segments)):
        transition = timeline[index - 1].get("transition") or {}
        duration = max(0.001, float(transition.get("duration", 0.001)))
        transition_type = str(transition.get("type", "fade"))
        supported = {"fade", "wipeleft", "wiperight", "slideleft", "slideright", "smoothleft", "smoothright", "circleopen", "circleclose", "dissolve"}
        if transition_type not in supported:
            transition_type = "fade"
        offset = max(0.0, cumulative - duration)
        output_label = f"[v{index}]"
        filters.append(f"{current_label}[{index}:v]xfade=transition={transition_type}:duration={duration:.6f}:offset={offset:.6f}{output_label}")
        current_label = output_label
        cumulative = offset + float(timeline[index]["duration"])
    filters.append(f"{current_label}format=yuv420p[vout]")
    run([
        "ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters), "-map", "[vout]",
        "-an", "-c:v", project["delivery"].get("video_codec", "libx264"), "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", project["delivery"].get("pixel_format", "yuv420p"), str(out)
    ])


def _add_audio(project: dict[str, Any], manifest_dir: Path, video: Path, out: Path) -> None:
    audio = project.get("audio") or {}
    music_cfg = audio.get("music")
    voice_cfg = audio.get("voiceover")
    duration = project_duration(project)
    if not music_cfg and not voice_cfg:
        shutil.copy2(video, out)
        return
    inputs = ["-i", str(video)]
    filters: list[str] = []
    labels: list[str] = []
    input_index = 1
    music_label = None
    voice_label = None
    if music_cfg:
        music_path = _resolve_asset(project, str(music_cfg["asset"]), manifest_dir)
        music_start = max(0.0, float(music_cfg.get("start", 0.0) or 0.0))
        inputs += ["-stream_loop", "-1"]
        if music_start:
            inputs += ["-ss", f"{music_start:.6f}"]
        inputs += ["-i", str(music_path)]
        volume = float(music_cfg.get("volume", 0.25))
        trim_duration = duration
        if music_cfg.get("end") is not None:
            trim_duration = min(duration, max(0.001, float(music_cfg["end"]) - music_start))
        music_filters = [
            f"atrim=0:{trim_duration:.6f}",
            "asetpts=N/SR/TB",
            f"volume={volume}",
        ]
        fade_in = max(0.0, float(music_cfg.get("fade_in_s", 0.0) or 0.0))
        fade_out = max(0.0, float(music_cfg.get("fade_out_s", 0.0) or 0.0))
        if fade_in:
            music_filters.append(f"afade=t=in:st=0:d={min(fade_in, trim_duration):.6f}")
        if fade_out:
            music_filters.append(
                f"afade=t=out:st={max(0.0, trim_duration-fade_out):.6f}:d={min(fade_out, trim_duration):.6f}"
            )
        if trim_duration < duration:
            music_filters.append(f"apad=pad_dur={duration-trim_duration:.6f}")
        filters.append(f"[{input_index}:a]{','.join(music_filters)}[music]")
        music_label = "[music]"
        input_index += 1
    if voice_cfg:
        voice_path = _resolve_asset(project, str(voice_cfg["asset"]), manifest_dir)
        inputs += ["-i", str(voice_path)]
        volume = float(voice_cfg.get("volume", 1.0))
        delay_ms = max(0, round(float(voice_cfg.get("start", 0.0)) * 1000))
        filters.append(f"[{input_index}:a]adelay={delay_ms}|{delay_ms},volume={volume}[voice]")
        voice_label = "[voice]"
    if music_label and voice_label:
        filters.append(f"{music_label}{voice_label}sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350[ducked]")
        filters.append("[ducked][voice]amix=inputs=2:duration=longest:normalize=0[mix]")
        output_audio = "[mix]"
    else:
        output_audio = music_label or voice_label
    if not output_audio:
        shutil.copy2(video, out)
        return
    loudness = audio.get("loudness") or {}
    if loudness.get("enabled"):
        target = float(loudness.get("target_lufs", -16.0))
        tp = float(loudness.get("true_peak_db", -1.5))
        lra = float(loudness.get("lra", 11.0))
        filters.append(f"{output_audio}loudnorm=I={target}:TP={tp}:LRA={lra}[master]")
        output_audio = "[master]"
    run([
        "ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", ";".join(filters),
        "-map", "0:v:0", "-map", output_audio, "-c:v", "copy", "-c:a", project["delivery"].get("audio_codec", "aac"),
        "-b:a", "192k", "-ar", "48000", "-t", f"{duration:.6f}", "-movflags", "+faststart", str(out)
    ])


def _burn_captions(project: dict[str, Any], manifest_dir: Path, video: Path, out: Path) -> None:
    cfg = project.get("captions") or {}
    source = cfg.get("source")
    if not cfg.get("enabled") or not cfg.get("burn_in") or not source:
        shutil.copy2(video, out)
        return
    caption_path = Path(source)
    if not caption_path.is_absolute():
        caption_path = (manifest_dir / caption_path).resolve()
    escaped = _escape_filter_path(caption_path)
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(video), "-vf", f"subtitles='{escaped}'", "-c:v", project["delivery"].get("video_codec", "libx264"),
        "-preset", "veryfast", "-crf", "19", "-c:a", "copy", "-pix_fmt", project["delivery"].get("pixel_format", "yuv420p"), str(out)
    ])


def render_project(manifest: str | Path, output: str | Path, *, work_dir: str | Path | None = None) -> Path:
    require_tool("ffmpeg")
    project = load_project(manifest)
    validate_project(project)
    timeline = sorted(project["timeline"], key=lambda item: float(item["start"]))
    if not timeline:
        raise ValueError("Timeline is empty")
    manifest_path = Path(manifest).resolve()
    manifest_dir = manifest_path.parent
    output_path = Path(output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    work = Path(work_dir).resolve() if work_dir else output_path.parent / f".{output_path.stem}-work"
    segments_dir = work / "segments"
    text_dir = work / "text"
    segments_dir.mkdir(parents=True, exist_ok=True)
    text_dir.mkdir(parents=True, exist_ok=True)
    segments: list[Path] = []
    for index, item in enumerate(timeline):
        segment = segments_dir / f"{index:03d}-{re.sub(r'[^a-zA-Z0-9_-]+', '-', str(item['id']))}.mp4"
        _render_segment(project, item, manifest_dir, segment, text_dir)
        segments.append(segment)
    visual = work / "visual.mp4"
    _combine_segments(project, segments, timeline, visual)
    with_audio = work / "with-audio.mp4"
    _add_audio(project, manifest_dir, visual, with_audio)
    _burn_captions(project, manifest_dir, with_audio, output_path)
    return output_path
