from __future__ import annotations

import importlib.util
import platform
import re
import subprocess
from typing import Any

from .utils import resolve_tool

TOOLS = {
    "ffmpeg": {"tier": "core", "purpose": "media decode, filters, encode, mux"},
    "ffprobe": {"tier": "core", "purpose": "machine-readable media inspection"},
    "python3": {"tier": "core", "purpose": "orchestration and analysis"},
    "git": {"tier": "recommended", "purpose": "plugin/source versioning"},
    "mediainfo": {"tier": "recommended", "purpose": "deep container, stream, HDR and timecode inspection"},
    "exiftool": {"tier": "recommended", "purpose": "camera and media metadata inspection"},
    "yt-dlp": {"tier": "optional-rights-sensitive", "purpose": "acquire user-authorized online media"},
    "packager": {"tier": "optional", "purpose": "Shaka Packager DASH/HLS packaging and encryption"},
    "mediaconch": {"tier": "optional", "purpose": "policy and implementation conformance checks"},
    "qcli": {"tier": "optional-gpl-executable", "purpose": "QCTools audiovisual signal analysis reports"},
    "magick": {"tier": "optional", "purpose": "ImageMagick batch image preparation"},
    "sox": {"tier": "optional", "purpose": "audio conversion, measurement and utility processing"},
    "node": {"tier": "optional", "purpose": "Remotion, HyperFrames, Motion Canvas"},
    "npm": {"tier": "optional", "purpose": "JavaScript renderer packages"},
    "blender": {"tier": "optional", "purpose": "3D, compositing, VSE automation"},
    "aubio": {"tier": "optional-gpl-executable", "purpose": "beat/onset/pitch analysis"},
    "docker": {"tier": "optional", "purpose": "reproducible isolated renderer and analysis environments"},
}

PYTHON_PACKAGES = [
    "yaml",
    "numpy",
    "PIL",
    "jsonschema",
    "librosa",
    "soundfile",
    "pyloudnorm",
    "moviepy",
    "scenedetect",
    "opentimelineio",
    "faster_whisper",
    "mediapipe",
    "av",
]

VERSION_ARGUMENTS = {
    "ffmpeg": ["-version"],
    "ffprobe": ["-version"],
    "exiftool": ["-ver"],
    "mediainfo": ["--Version"],
    "packager": ["--version"],
    "blender": ["--version"],
    "magick": ["-version"],
    "sox": ["--version"],
    "python3": ["--version"],
}

FILTERS_OF_INTEREST = [
    "libvmaf",
    "subtitles",
    "ass",
    "loudnorm",
    "xfade",
    "acrossfade",
    "blackdetect",
    "freezedetect",
    "silencedetect",
    "cropdetect",
    "scdet",
    "showwavespic",
    "zscale",
    "tonemap",
]

ENCODERS_OF_INTEREST = [
    "libx264",
    "libx265",
    "libsvtav1",
    "libaom-av1",
    "prores_ks",
    "aac",
    "h264_nvenc",
    "hevc_nvenc",
    "h264_videotoolbox",
    "hevc_videotoolbox",
    "h264_qsv",
    "hevc_qsv",
    "h264_amf",
    "hevc_amf",
]


def _capture(cmd: list[str], timeout: int = 8) -> str:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
    except Exception:
        return ""
    return "\n".join(part for part in (proc.stdout, proc.stderr) if part)


def _listed(name: str, listing: str) -> bool:
    return bool(re.search(rf"(?<![A-Za-z0-9_-]){re.escape(name)}(?![A-Za-z0-9_-])", listing))


def _ffmpeg_capabilities(ffmpeg_path: str | None) -> dict[str, Any]:
    if not ffmpeg_path:
        return {
            "filters": {name: False for name in FILTERS_OF_INTEREST},
            "encoders": {name: False for name in ENCODERS_OF_INTEREST},
            "hardware_acceleration": [],
        }

    filters_text = _capture([ffmpeg_path, "-hide_banner", "-filters"])
    encoders_text = _capture([ffmpeg_path, "-hide_banner", "-encoders"])
    hw_text = _capture([ffmpeg_path, "-hide_banner", "-hwaccels"])
    hw_lines = [line.strip() for line in hw_text.splitlines()]
    try:
        start = hw_lines.index("Hardware acceleration methods:") + 1
        hardware = [line for line in hw_lines[start:] if line and " " not in line]
    except ValueError:
        hardware = []

    return {
        "filters": {name: _listed(name, filters_text) for name in FILTERS_OF_INTEREST},
        "encoders": {name: _listed(name, encoders_text) for name in ENCODERS_OF_INTEREST},
        "hardware_acceleration": hardware,
    }


def check_toolchain() -> dict[str, Any]:
    binaries: dict[str, dict[str, Any]] = {}
    for name, metadata in TOOLS.items():
        path = resolve_tool(name, required=False)
        version = None
        if path:
            output = _capture([path, *VERSION_ARGUMENTS.get(name, ["--version"])], timeout=5)
            version = next((line.strip()[:200] for line in output.splitlines() if line.strip()), "present")
        binaries[name] = {**metadata, "available": bool(path), "path": path, "version": version}

    packages = {name: bool(importlib.util.find_spec(name)) for name in PYTHON_PACKAGES}
    ffmpeg_capabilities = _ffmpeg_capabilities(binaries["ffmpeg"]["path"])
    return {
        "platform": platform.platform(),
        "python": platform.python_version(),
        "binaries": binaries,
        "python_packages": packages,
        "ffmpeg_capabilities": ffmpeg_capabilities,
        "can_render_baseline": binaries["ffmpeg"]["available"] and binaries["ffprobe"]["available"],
        "can_burn_captions": ffmpeg_capabilities["filters"]["subtitles"] or ffmpeg_capabilities["filters"]["ass"],
        "can_measure_vmaf": ffmpeg_capabilities["filters"]["libvmaf"],
    }
