from __future__ import annotations

import re
from pathlib import Path
from typing import Any

_TIMESTAMP_RE = re.compile(r"(\d{2}):(\d{2}):(\d{2})[,.](\d{3})")


def _seconds(value: str) -> float:
    match = _TIMESTAMP_RE.fullmatch(value.strip())
    if not match:
        raise ValueError(f"Invalid subtitle timestamp: {value}")
    h, m, s, ms = map(int, match.groups())
    return h * 3600 + m * 60 + s + ms / 1000.0


def parse_srt(path: str | Path) -> list[dict[str, Any]]:
    text = Path(path).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    cues: list[dict[str, Any]] = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [line.strip("\ufeff") for line in block.splitlines()]
        if len(lines) < 2:
            continue
        timing_index = 1 if re.fullmatch(r"\d+", lines[0].strip()) else 0
        if "-->" not in lines[timing_index]:
            continue
        start_text, end_text = [part.strip().split(" ")[0] for part in lines[timing_index].split("-->", 1)]
        cue_text = "\\N".join(line.strip() for line in lines[timing_index + 1 :] if line.strip())
        cues.append({"start": _seconds(start_text), "end": _seconds(end_text), "text": cue_text})
    return cues


def cue_reading_speed(cue: dict[str, Any]) -> float:
    duration = max(0.001, float(cue["end"]) - float(cue["start"]))
    words = len(re.findall(r"\b[\w’'-]+\b", str(cue.get("text", ""))))
    return round(words / duration, 3)


def _ass_time(seconds: float) -> str:
    centiseconds = max(0, round(seconds * 100))
    h, rem = divmod(centiseconds, 360000)
    m, rem = divmod(rem, 6000)
    s, cs = divmod(rem, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def _ass_color(hex_color: str, alpha: str = "00") -> str:
    value = hex_color.lstrip("#")
    if len(value) != 6:
        raise ValueError("ASS colors require #RRGGBB")
    rr, gg, bb = value[0:2], value[2:4], value[4:6]
    return f"&H{alpha}{bb}{gg}{rr}"


def write_ass(
    cues: list[dict[str, Any]],
    path: str | Path,
    *,
    width: int,
    height: int,
    style: dict[str, Any] | None = None,
) -> None:
    style = style or {}
    font = style.get("font", "DejaVu Sans")
    font_size = int(style.get("font_size", round(height * 0.05)))
    primary = _ass_color(style.get("color", "#FFFFFF"))
    outline = _ass_color(style.get("outline_color", "#000000"))
    margin_v = int(style.get("margin_v", round(height * 0.08)))
    alignment = int(style.get("alignment", 2))
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
ScaledBorderAndShadow: yes
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font},{font_size},{primary},{primary},{outline},&H64000000,-1,0,0,0,100,100,0,0,1,3,0,{alignment},40,40,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = [header]
    for cue in cues:
        text = str(cue.get("text", "")).replace("\n", "\\N").replace("{", "\\{").replace("}", "\\}")
        lines.append(f"Dialogue: 0,{_ass_time(float(cue['start']))},{_ass_time(float(cue['end']))},Default,,0,0,0,,{text}\n")
    Path(path).write_text("".join(lines), encoding="utf-8")


def validate_cues(cues: list[dict[str, Any]], *, max_words_per_second: float = 4.0) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    previous_end = 0.0
    for index, cue in enumerate(cues):
        start, end = float(cue["start"]), float(cue["end"])
        if end <= start:
            issues.append({"cue": index + 1, "severity": "error", "code": "nonpositive-duration"})
        if start < previous_end:
            issues.append({"cue": index + 1, "severity": "warning", "code": "overlap"})
        speed = cue_reading_speed(cue)
        if speed > max_words_per_second:
            issues.append({"cue": index + 1, "severity": "warning", "code": "fast-reading", "words_per_second": speed})
        previous_end = max(previous_end, end)
    return issues
