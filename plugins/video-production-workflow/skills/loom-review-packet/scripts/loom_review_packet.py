#!/usr/bin/env python3
"""Extract Loom transcript timestamps and assemble a UX review packet."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


TIMESTAMP_RE = re.compile(r"(?<!\d)(?P<stamp>(?:\d+:)?\d{1,2}:\d{2})(?!\d)")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}


def timestamp_seconds(value: str) -> int:
    parts = value.strip().split(":")
    if len(parts) not in (2, 3) or not all(part.isdigit() for part in parts):
        raise ValueError(f"invalid timestamp: {value!r}")
    numbers = [int(part) for part in parts]
    if numbers[-1] >= 60 or (len(numbers) == 3 and numbers[-2] >= 60):
        raise ValueError(f"invalid timestamp: {value!r}")
    if len(numbers) == 2:
        return numbers[0] * 60 + numbers[1]
    return numbers[0] * 3600 + numbers[1] * 60 + numbers[2]


def canonical_timestamp(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def safe_timestamp(seconds: int) -> str:
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}-{minutes:02d}-{secs:02d}"
    return f"{minutes:02d}-{secs:02d}"


def slugify(value: str, fallback: str = "frame") -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:60].rstrip("-") or fallback


def extract_segments(text: str) -> list[dict[str, object]]:
    matches = list(TIMESTAMP_RE.finditer(text))
    rows: list[dict[str, object]] = []
    for index, match in enumerate(matches, start=1):
        seconds = timestamp_seconds(match.group("stamp"))
        end = matches[index].start() if index < len(matches) else len(text)
        transcript = " ".join(text[match.end() : end].split())
        rows.append(
            {
                "sequence": index,
                "timestamp": canonical_timestamp(seconds),
                "seconds": seconds,
                "transcript": transcript,
            }
        )
    return rows


def write_timestamp_csv(rows: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["sequence", "timestamp", "seconds", "transcript"]
        )
        writer.writeheader()
        writer.writerows(rows)


def read_cues(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "timestamp" not in reader.fieldnames:
            raise ValueError("cue CSV must contain a timestamp column")
        cues = []
        for row_number, row in enumerate(reader, start=2):
            cleaned = {key: (value or "").strip() for key, value in row.items() if key}
            if not cleaned["timestamp"]:
                raise ValueError(f"cue CSV row {row_number} has no timestamp")
            cleaned["seconds"] = str(timestamp_seconds(cleaned["timestamp"]))
            cues.append(cleaned)
    if not cues:
        raise ValueError("cue CSV has no cues")
    cues.sort(key=lambda row: int(row["seconds"]))
    return cues


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def nearest_transcript(rows: list[dict[str, object]], seconds: int) -> str:
    prior = [row for row in rows if int(row["seconds"]) <= seconds]
    if prior:
        return str(prior[-1]["transcript"])
    return str(rows[0]["transcript"]) if rows else ""


def resolve_screenshot(name: str, screenshots_dir: Path | None) -> Path:
    source = Path(name).expanduser()
    if not source.is_absolute():
        if screenshots_dir is None:
            raise ValueError(
                f"relative screenshot {name!r} requires --screenshots-dir"
            )
        source = screenshots_dir / source
    source = source.resolve()
    if not source.is_file():
        raise FileNotFoundError(f"screenshot not found: {source}")
    if source.suffix.lower() not in IMAGE_SUFFIXES:
        raise ValueError(f"unsupported screenshot type: {source}")
    return source


def capture_frame(video: Path, seconds: int, output: Path, ffmpeg: str) -> None:
    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-ss",
        str(seconds),
        "-i",
        str(video),
        "-frames:v",
        "1",
        "-y",
        str(output),
    ]
    subprocess.run(command, check=True)


def markdown_value(value: str) -> str:
    return value if value else "_Not recorded._"


def build_packet(args: argparse.Namespace) -> int:
    transcript_path = args.transcript.expanduser().resolve()
    cues_path = args.cues.expanduser().resolve()
    output = args.output.expanduser().resolve()
    screenshots_dir = (
        args.screenshots_dir.expanduser().resolve() if args.screenshots_dir else None
    )
    video = args.video.expanduser().resolve() if args.video else None

    if output.exists():
        raise FileExistsError(f"output already exists: {output}")
    if not transcript_path.is_file():
        raise FileNotFoundError(f"transcript not found: {transcript_path}")
    if not cues_path.is_file():
        raise FileNotFoundError(f"cues not found: {cues_path}")
    if video and not video.is_file():
        raise FileNotFoundError(f"video not found: {video}")

    transcript_text = transcript_path.read_text(encoding="utf-8")
    transcript_rows = extract_segments(transcript_text)
    if not transcript_rows:
        raise ValueError("no timestamps found in transcript")
    cues = read_cues(cues_path)

    plan: list[dict[str, object]] = []
    needs_capture = False
    for index, cue in enumerate(cues, start=1):
        seconds = int(cue["seconds"])
        topic = cue.get("topic", "")
        base = f"{index:03d}-{safe_timestamp(seconds)}-{slugify(topic)}"
        screenshot_name = cue.get("screenshot", "")
        if screenshot_name:
            source = resolve_screenshot(screenshot_name, screenshots_dir)
            destination_name = base + source.suffix.lower()
            mode = "copied-screenshot"
        elif video:
            source = video
            destination_name = base + ".png"
            mode = "captured-video-frame"
            needs_capture = True
        else:
            source = None
            destination_name = ""
            mode = "missing"
        plan.append(
            {
                "index": index,
                "cue": cue,
                "source": source,
                "destination_name": destination_name,
                "mode": mode,
            }
        )

    missing = [item for item in plan if item["mode"] == "missing"]
    if missing and not args.allow_missing:
        stamps = ", ".join(str(item["cue"]["timestamp"]) for item in missing)
        raise ValueError(
            f"no frame source for cue(s) {stamps}; map screenshots, provide --video, "
            "or explicitly use --allow-missing"
        )

    ffmpeg = shutil.which("ffmpeg") if needs_capture else None
    if needs_capture and not ffmpeg:
        raise RuntimeError("ffmpeg is required to capture frames from --video")

    transcript_dir = output / "transcript"
    frames_dir = output / "frames"
    transcript_dir.mkdir(parents=True)
    frames_dir.mkdir()
    shutil.copy2(transcript_path, transcript_dir / "raw.txt")
    write_timestamp_csv(transcript_rows, transcript_dir / "timestamps.csv")

    manifest_cues = []
    review_sections = []
    for item in plan:
        cue = item["cue"]
        seconds = int(cue["seconds"])
        destination_name = str(item["destination_name"])
        destination = frames_dir / destination_name if destination_name else None
        source = item["source"]
        mode = str(item["mode"])
        if mode == "copied-screenshot":
            shutil.copy2(source, destination)
        elif mode == "captured-video-frame":
            capture_frame(source, seconds, destination, str(ffmpeg))

        frame_relative = f"frames/{destination_name}" if destination else None
        frame_hash = sha256(destination) if destination else None
        transcript_excerpt = nearest_transcript(transcript_rows, seconds)
        manifest_cues.append(
            {
                "sequence": item["index"],
                "timestamp": canonical_timestamp(seconds),
                "seconds": seconds,
                "topic": cue.get("topic", ""),
                "frame": frame_relative,
                "frameSource": str(source) if source else None,
                "frameMode": mode,
                "frameSha256": frame_hash,
            }
        )

        title = cue.get("topic", "") or "Untitled cue"
        frame_markdown = (
            f"![{title}](frames/{destination_name})" if destination else "_Frame missing._"
        )
        review_sections.append(
            "\n".join(
                [
                    f"## {int(item['index']):02d} — {canonical_timestamp(seconds)} — {title}",
                    "",
                    frame_markdown,
                    "",
                    f"**Transcript:** {markdown_value(transcript_excerpt)}",
                    "",
                    f"**Observation:** {markdown_value(cue.get('observation', ''))}",
                    "",
                    f"**Question:** {markdown_value(cue.get('question', ''))}",
                    "",
                    f"**Recommendation:** {markdown_value(cue.get('recommendation', ''))}",
                ]
            )
        )

    frame_count = sum(1 for item in manifest_cues if item["frame"])
    status = "complete" if frame_count == len(manifest_cues) else "partial"
    manifest = {
        "schemaVersion": 1,
        "status": status,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "title": args.title,
        "author": args.author or None,
        "sourceUrl": args.source_url or None,
        "transcriptSource": str(transcript_path),
        "cueCount": len(manifest_cues),
        "frameCount": frame_count,
        "cues": manifest_cues,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    heading = f"# {args.title} — Loom UX Review"
    byline = f"\n\nAuthor: {args.author}" if args.author else ""
    source_line = f"\n\nSource: {args.source_url}" if args.source_url else ""
    review = heading + byline + source_line + "\n\n" + "\n\n".join(review_sections) + "\n"
    (output / "ux-feedback.md").write_text(review, encoding="utf-8")

    print(
        json.dumps(
            {
                "output": str(output),
                "status": status,
                "cueCount": len(manifest_cues),
                "frameCount": frame_count,
            }
        )
    )
    return 0 if status == "complete" else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract = subparsers.add_parser("extract", help="extract timestamped transcript rows")
    extract.add_argument("--transcript", type=Path, required=True)
    extract.add_argument("--output", type=Path, required=True)

    build = subparsers.add_parser("build", help="assemble a Loom UX review packet")
    build.add_argument("--title", required=True)
    build.add_argument("--author", default="")
    build.add_argument("--source-url", default="")
    build.add_argument("--transcript", type=Path, required=True)
    build.add_argument("--cues", type=Path, required=True)
    build.add_argument("--screenshots-dir", type=Path)
    build.add_argument("--video", type=Path)
    build.add_argument("--output", type=Path, required=True)
    build.add_argument("--allow-missing", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "extract":
            transcript = args.transcript.expanduser().resolve()
            if not transcript.is_file():
                raise FileNotFoundError(f"transcript not found: {transcript}")
            rows = extract_segments(transcript.read_text(encoding="utf-8"))
            if not rows:
                raise ValueError("no timestamps found in transcript")
            write_timestamp_csv(rows, args.output.expanduser().resolve())
            print(json.dumps({"output": str(args.output), "timestampCount": len(rows)}))
            return 0
        return build_packet(args)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
