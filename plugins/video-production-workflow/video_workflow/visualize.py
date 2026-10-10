from __future__ import annotations

import math
import tempfile
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont

from .probe import probe_media
from .utils import require_tool, run


def _font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/Library/Fonts/Arial.ttf"),
        Path("C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _extract_frame(video: Path, timestamp: float, output: Path, width: int) -> None:
    run([
        "ffmpeg", "-y", "-v", "error", "-ss", f"{max(0.0, timestamp):.6f}", "-i", str(video),
        "-frames:v", "1", "-vf", f"scale={width}:-2", str(output),
    ])


def _timestamp(seconds: float) -> str:
    total_ms = max(0, round(seconds * 1000))
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"


def _sheet_from_timestamps(
    video: Path,
    timestamps: Iterable[float],
    output: Path,
    *,
    frame_width: int,
    columns: int | None = None,
) -> Path:
    values = list(timestamps)
    if not values:
        raise ValueError("At least one timestamp is required")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="video-workflow-contact-") as temp_raw:
        temp = Path(temp_raw)
        frames: list[tuple[float, Image.Image]] = []
        for index, timestamp in enumerate(values):
            frame_path = temp / f"frame-{index:03d}.png"
            _extract_frame(video, timestamp, frame_path, frame_width)
            frames.append((timestamp, Image.open(frame_path).convert("RGB")))
        frame_height = max(image.height for _, image in frames)
        label_height = max(24, round(frame_width * 0.075))
        cols = columns or max(1, min(4, math.ceil(math.sqrt(len(frames) * 16 / 9))))
        rows = math.ceil(len(frames) / cols)
        gap = max(4, round(frame_width * 0.02))
        canvas = Image.new(
            "RGB",
            (cols * frame_width + (cols + 1) * gap, rows * (frame_height + label_height) + (rows + 1) * gap),
            "#111111",
        )
        draw = ImageDraw.Draw(canvas)
        font = _font(max(12, round(label_height * 0.56)))
        for index, (timestamp, image) in enumerate(frames):
            row, col = divmod(index, cols)
            x = gap + col * (frame_width + gap)
            y = gap + row * (frame_height + label_height + gap)
            if image.height != frame_height:
                cell = Image.new("RGB", (frame_width, frame_height), "black")
                cell.paste(image, (0, (frame_height - image.height) // 2))
                image = cell
            canvas.paste(image, (x, y))
            draw.rectangle((x, y + frame_height, x + frame_width, y + frame_height + label_height), fill="#000000")
            draw.text((x + 6, y + frame_height + 3), _timestamp(timestamp), fill="white", font=font)
        canvas.save(output)
        for _, image in frames:
            image.close()
    return output


def make_contact_sheet(
    video: str | Path,
    output: str | Path,
    *,
    count: int = 12,
    frame_width: int = 320,
    timestamps: Iterable[float] | None = None,
) -> Path:
    require_tool("ffmpeg")
    source = Path(video).resolve()
    target = Path(output).resolve()
    if timestamps is None:
        duration = float(probe_media(source)["format"]["duration"])
        if count <= 0:
            raise ValueError("count must be positive")
        if count == 1:
            values = [duration / 2]
        else:
            edge = min(0.05, duration / 20)
            values = [edge + i * max(0.0, duration - 2 * edge) / (count - 1) for i in range(count)]
    else:
        values = [float(value) for value in timestamps]
    return _sheet_from_timestamps(source, values, target, frame_width=frame_width)


def make_waveform(
    audio_or_video: str | Path,
    output: str | Path,
    *,
    width: int = 1200,
    height: int = 300,
    start: float | None = None,
    end: float | None = None,
) -> Path:
    require_tool("ffmpeg")
    source = Path(audio_or_video).resolve()
    target = Path(output).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    filters = []
    if start is not None or end is not None:
        start_value = 0.0 if start is None else max(0.0, float(start))
        trim = f"atrim=start={start_value}"
        if end is not None:
            trim += f":end={max(start_value, float(end))}"
        filters.extend([trim, "asetpts=N/SR/TB"])
    filters.append(f"showwavespic=s={int(width)}x{int(height)}:colors=white:scale=sqrt")
    run([
        "ffmpeg", "-y", "-v", "error", "-i", str(source), "-filter_complex", ",".join(filters),
        "-frames:v", "1", str(target),
    ])
    return target


def make_timeline_view(
    video: str | Path,
    output: str | Path,
    *,
    start: float,
    end: float,
    count: int = 6,
    frame_width: int = 240,
) -> Path:
    if end <= start:
        raise ValueError("end must be greater than start")
    source = Path(video).resolve()
    target = Path(output).resolve()
    values = [start + (end - start) * i / max(1, count - 1) for i in range(count)]
    with tempfile.TemporaryDirectory(prefix="video-workflow-timeline-") as temp_raw:
        temp = Path(temp_raw)
        sheet_path = _sheet_from_timestamps(source, values, temp / "sheet.png", frame_width=frame_width)
        with Image.open(sheet_path).convert("RGB") as sheet:
            waveform_path = make_waveform(source, temp / "waveform.png", width=sheet.width, height=max(120, sheet.height // 4), start=start, end=end)
            with Image.open(waveform_path).convert("RGB") as waveform:
                header_h = 42
                canvas = Image.new("RGB", (sheet.width, header_h + sheet.height + waveform.height), "#111111")
                canvas.paste(sheet, (0, header_h))
                canvas.paste(waveform, (0, header_h + sheet.height))
                draw = ImageDraw.Draw(canvas)
                draw.text((12, 10), f"TIMELINE VIEW  {_timestamp(start)} → {_timestamp(end)}", font=_font(18), fill="white")
                target.parent.mkdir(parents=True, exist_ok=True)
                canvas.save(target)
    return target
