from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .utils import parse_fraction, require_tool, run


def probe_media(path: str | Path) -> dict[str, Any]:
    require_tool("ffprobe")
    source = Path(path)
    proc = run([
        "ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(source)
    ], capture=True)
    data = json.loads(proc.stdout)
    video_stream = next((stream for stream in data.get("streams", []) if stream.get("codec_type") == "video"), None)
    audio_stream = next((stream for stream in data.get("streams", []) if stream.get("codec_type") == "audio"), None)
    fmt = data.get("format", {})
    result: dict[str, Any] = {
        "path": str(source.resolve()),
        "format": {
            "name": fmt.get("format_name"),
            "duration": float(fmt.get("duration") or 0.0),
            "size_bytes": int(fmt.get("size") or 0),
            "bit_rate": int(fmt.get("bit_rate") or 0),
        },
        "video": None,
        "audio": None,
        "streams": data.get("streams", []),
    }
    if video_stream:
        result["video"] = {
            "codec": video_stream.get("codec_name"),
            "width": int(video_stream.get("width") or 0),
            "height": int(video_stream.get("height") or 0),
            "fps": parse_fraction(video_stream.get("avg_frame_rate")) or parse_fraction(video_stream.get("r_frame_rate")),
            "pixel_format": video_stream.get("pix_fmt"),
            "color_space": video_stream.get("color_space"),
            "color_transfer": video_stream.get("color_transfer"),
            "color_primaries": video_stream.get("color_primaries"),
            "duration": float(video_stream.get("duration") or fmt.get("duration") or 0.0),
        }
    if audio_stream:
        result["audio"] = {
            "codec": audio_stream.get("codec_name"),
            "sample_rate": int(audio_stream.get("sample_rate") or 0),
            "channels": int(audio_stream.get("channels") or 0),
            "channel_layout": audio_stream.get("channel_layout"),
            "duration": float(audio_stream.get("duration") or fmt.get("duration") or 0.0),
        }
    return result
