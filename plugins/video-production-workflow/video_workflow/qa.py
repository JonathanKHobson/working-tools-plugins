from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .probe import probe_media
from .utils import run


def _analysis_log(path: Path, *, video_filter: str | None = None, audio_filter: str | None = None) -> str:
    cmd = ["ffmpeg", "-hide_banner", "-nostats", "-i", str(path)]
    if video_filter:
        cmd += ["-vf", video_filter, "-an"]
    elif audio_filter:
        cmd += ["-af", audio_filter, "-vn"]
    cmd += ["-f", "null", "-"]
    proc = run(cmd, capture=True)
    return (proc.stderr or "") + (proc.stdout or "")


def _parse_black(log: str) -> list[dict[str, float]]:
    pattern = re.compile(r"black_start:(?P<start>-?\d+(?:\.\d+)?)\s+black_end:(?P<end>-?\d+(?:\.\d+)?)\s+black_duration:(?P<duration>\d+(?:\.\d+)?)")
    return [{key: round(float(value), 4) for key, value in match.groupdict().items()} for match in pattern.finditer(log)]


def _parse_freeze(log: str) -> list[dict[str, float | None]]:
    starts = [float(v) for v in re.findall(r"freeze_start:\s*(-?\d+(?:\.\d+)?)", log)]
    ends = [float(v) for v in re.findall(r"freeze_end:\s*(-?\d+(?:\.\d+)?)", log)]
    durations = [float(v) for v in re.findall(r"freeze_duration:\s*(\d+(?:\.\d+)?)", log)]
    count = max(len(starts), len(ends), len(durations))
    return [
        {
            "start": round(starts[i], 4) if i < len(starts) else None,
            "end": round(ends[i], 4) if i < len(ends) else None,
            "duration": round(durations[i], 4) if i < len(durations) else None,
        }
        for i in range(count)
    ]


def _parse_silence(log: str) -> list[dict[str, float | None]]:
    starts = [float(v) for v in re.findall(r"silence_start:\s*(-?\d+(?:\.\d+)?)", log)]
    ends = [float(v) for v in re.findall(r"silence_end:\s*(-?\d+(?:\.\d+)?)", log)]
    durations = [float(v) for v in re.findall(r"silence_duration:\s*(\d+(?:\.\d+)?)", log)]
    count = max(len(starts), len(ends), len(durations))
    return [
        {
            "start": round(starts[i], 4) if i < len(starts) else None,
            "end": round(ends[i], 4) if i < len(ends) else None,
            "duration": round(durations[i], 4) if i < len(durations) else None,
        }
        for i in range(count)
    ]


def _parse_peak(log: str) -> float | None:
    match = re.search(r"max_volume:\s*(-?inf|-?\d+(?:\.\d+)?)\s*dB", log)
    if not match or match.group(1) == "-inf":
        return None
    return float(match.group(1))


def validate_video(
    path: str | Path,
    *,
    expected_width: int | None = None,
    expected_height: int | None = None,
    expected_duration: float | None = None,
    deep: bool = False,
) -> dict[str, Any]:
    source = Path(path)
    info = probe_media(source)
    checks: list[dict[str, Any]] = []
    video = info.get("video")
    audio = info.get("audio")
    checks.append({"name": "playable", "status": "pass" if info["format"]["duration"] > 0 else "fail"})
    checks.append({"name": "video-stream", "status": "pass" if video else "fail"})
    if expected_width is not None and expected_height is not None and video:
        checks.append({
            "name": "dimensions",
            "status": "pass" if (video["width"], video["height"]) == (expected_width, expected_height) else "fail",
            "actual": [video["width"], video["height"]],
            "expected": [expected_width, expected_height],
        })
    if expected_duration is not None:
        delta = abs(info["format"]["duration"] - expected_duration)
        checks.append({"name": "duration", "status": "pass" if delta <= 0.15 else "fail", "delta_s": round(delta, 4)})
    checks.append({"name": "audio-stream", "status": "pass" if audio else "warning"})

    if deep and video:
        black = _parse_black(_analysis_log(source, video_filter="blackdetect=d=0.4:pix_th=0.10"))
        freeze = _parse_freeze(_analysis_log(source, video_filter="freezedetect=n=-55dB:d=1.2"))
        checks.append({"name": "black-segments", "status": "warning" if black else "pass", "segments": black})
        checks.append({"name": "freeze-segments", "status": "warning" if freeze else "pass", "segments": freeze})
    elif deep:
        checks.extend([
            {"name": "black-segments", "status": "warning", "segments": [], "reason": "no video stream"},
            {"name": "freeze-segments", "status": "warning", "segments": [], "reason": "no video stream"},
        ])

    if deep and audio:
        silence = _parse_silence(_analysis_log(source, audio_filter="silencedetect=noise=-50dB:d=0.8"))
        peak = _parse_peak(_analysis_log(source, audio_filter="volumedetect"))
        peak_status = "warning" if peak is not None and peak > -0.1 else "pass"
        checks.append({"name": "silence-segments", "status": "warning" if silence else "pass", "segments": silence})
        checks.append({"name": "audio-peak", "status": peak_status, "max_volume_db": peak})
    elif deep:
        checks.extend([
            {"name": "silence-segments", "status": "warning", "segments": [], "reason": "no audio stream"},
            {"name": "audio-peak", "status": "warning", "max_volume_db": None, "reason": "no audio stream"},
        ])

    return {
        "path": str(source.resolve()),
        "probe": info,
        "checks": checks,
        "deep": deep,
        "passed": not any(item["status"] == "fail" for item in checks),
        "interpretation_warning": "Temporal detectors flag candidate defects; intentional black, freeze, and silence require human review.",
    }


def save_report(report: dict[str, Any], path: str | Path) -> None:
    Path(path).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
