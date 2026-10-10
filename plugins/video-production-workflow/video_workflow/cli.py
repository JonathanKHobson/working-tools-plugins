from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .audit import audit_project
from .audio import analyze_music, save_music_analysis
from .captions import parse_srt, validate_cues, write_ass
from .caption_exports import CaptionExportError, export_caption_variants
from .delivery import DeliveryError, preflight_delivery
from .interchange import export_cmx3600, export_otio
from .manifest import PRESETS, load_project, project_from_preset, save_project
from .probe import probe_media
from .provenance import inventory_paths
from .reframe import crop_from_anchor
from .qa import save_report, validate_video
from .render import render_project
from .storyboard import write_storyboard
from .timeline import plan_slideshow
from .toolchain import check_toolchain
from .transcript import pack_phrases, snap_ranges
from .visualize import make_contact_sheet, make_timeline_view, make_waveform


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="video-workflow", description="Programmatic video production workflow")
    sub = parser.add_subparsers(dest="command", required=True)

    new = sub.add_parser("new", help="Create a project manifest")
    new.add_argument("output")
    new.add_argument("--id", default="video-project")
    new.add_argument("--preset", choices=sorted(PRESETS), default="landscape-1080")

    check = sub.add_parser("check", help="Inspect local toolchain")
    check.add_argument("--output")

    audit = sub.add_parser("audit-project", help="Audit pacing, source reuse, copy, safe areas, CTA, and music boundaries")
    audit.add_argument("manifest")
    audit.add_argument("--output")

    delivery = sub.add_parser("preflight-delivery", help="Read-only batch check of final media, cover variants and review freshness")
    delivery.add_argument("manifest")

    caption_export = sub.add_parser("export-captions", help="Export hash-bound SRT variants from reviewed cues and ordered constant-speed cuts")
    caption_export.add_argument("manifest")
    caption_export.add_argument("--output", help="Explicit output directory; defaults to a read-only dry run")

    probe = sub.add_parser("probe", help="Probe media with ffprobe")
    probe.add_argument("input")
    probe.add_argument("--output")

    music = sub.add_parser("analyze-music", help="Analyze beats and energy")
    music.add_argument("input")
    music.add_argument("--output", required=True)
    music.add_argument("--no-librosa", action="store_true")

    slideshow = sub.add_parser("plan-slideshow", help="Create timeline JSON from assets")
    slideshow.add_argument("assets", nargs="+")
    slideshow.add_argument("--duration", type=float, required=True)
    slideshow.add_argument("--beats-json")
    slideshow.add_argument("--output", required=True)

    storyboard = sub.add_parser("storyboard", help="Write a markdown storyboard")
    storyboard.add_argument("manifest")
    storyboard.add_argument("--output", required=True)

    captions = sub.add_parser("captions", help="Convert/validate SRT captions")
    captions.add_argument("input")
    captions.add_argument("--ass-output")
    captions.add_argument("--width", type=int, default=1920)
    captions.add_argument("--height", type=int, default=1080)
    captions.add_argument("--font", default="DejaVu Sans")
    captions.add_argument("--font-size", type=int)
    captions.add_argument("--report")

    render = sub.add_parser("render", help="Render a project manifest")
    render.add_argument("manifest")
    render.add_argument("--output", required=True)
    render.add_argument("--work-dir")

    qa = sub.add_parser("qa", help="Validate a rendered video")
    qa.add_argument("input")
    qa.add_argument("--width", type=int)
    qa.add_argument("--height", type=int)
    qa.add_argument("--duration", type=float)
    qa.add_argument("--output")
    qa.add_argument("--deep", action="store_true", help="Run black/freeze/silence/peak detectors")

    interchange = sub.add_parser("export-timeline", help="Export CMX3600 or OTIO")
    interchange.add_argument("manifest")
    interchange.add_argument("--format", choices=["edl", "otio"], required=True)
    interchange.add_argument("--output", required=True)

    inventory = sub.add_parser("inventory", help="Hash and inventory files or directories")
    inventory.add_argument("paths", nargs="+")
    inventory.add_argument("--output", required=True)
    inventory.add_argument("--no-recursive", action="store_true")

    packed = sub.add_parser("pack-transcript", help="Pack word timestamps into readable phrases")
    packed.add_argument("input")
    packed.add_argument("--output", required=True)
    packed.add_argument("--silence", type=float, default=0.65)

    snap = sub.add_parser("snap-ranges", help="Snap rough ranges to complete word boundaries")
    snap.add_argument("ranges")
    snap.add_argument("transcript")
    snap.add_argument("--output", required=True)
    snap.add_argument("--pad-before", type=float, default=0.08)
    snap.add_argument("--pad-after", type=float, default=0.12)

    contact = sub.add_parser("contact-sheet", help="Create timestamped representative frames")
    contact.add_argument("input")
    contact.add_argument("--output", required=True)
    contact.add_argument("--count", type=int, default=12)
    contact.add_argument("--width", type=int, default=320)

    waveform = sub.add_parser("waveform", help="Create a waveform evidence image")
    waveform.add_argument("input")
    waveform.add_argument("--output", required=True)
    waveform.add_argument("--width", type=int, default=1200)
    waveform.add_argument("--height", type=int, default=300)
    waveform.add_argument("--start", type=float)
    waveform.add_argument("--end", type=float)

    timeline_view = sub.add_parser("timeline-view", help="Create frames plus waveform for a time range")
    timeline_view.add_argument("input")
    timeline_view.add_argument("--output", required=True)
    timeline_view.add_argument("--start", type=float, required=True)
    timeline_view.add_argument("--end", type=float, required=True)
    timeline_view.add_argument("--count", type=int, default=6)
    timeline_view.add_argument("--width", type=int, default=240)

    reframe = sub.add_parser("reframe", help="Compute a subject-anchored cover crop")
    reframe.add_argument("--source-width", type=int, required=True)
    reframe.add_argument("--source-height", type=int, required=True)
    reframe.add_argument("--target-width", type=int, required=True)
    reframe.add_argument("--target-height", type=int, required=True)
    reframe.add_argument("--anchor-x", type=float, default=0.5)
    reframe.add_argument("--anchor-y", type=float, default=0.5)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "new":
        save_project(project_from_preset(args.id, args.preset), args.output)
    elif args.command == "check":
        result = check_toolchain()
        text = json.dumps(result, indent=2) + "\n"
        Path(args.output).write_text(text) if args.output else print(text, end="")
    elif args.command == "audit-project":
        result = audit_project(load_project(args.manifest))
        text = json.dumps(result, indent=2) + "\n"
        Path(args.output).write_text(text) if args.output else print(text, end="")
        return 0 if result["passed"] else 2
    elif args.command == "preflight-delivery":
        try:
            result = preflight_delivery(args.manifest)
        except DeliveryError as exc:
            print(f"delivery preflight: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(result, indent=2, allow_nan=False))
        return 0 if result["passed"] else 2
    elif args.command == "probe":
        result = probe_media(args.input)
        text = json.dumps(result, indent=2) + "\n"
        Path(args.output).write_text(text) if args.output else print(text, end="")
    elif args.command == "export-captions":
        try:
            result = export_caption_variants(args.manifest, args.output)
        except CaptionExportError as exc:
            print(f"caption export: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(result, indent=2, allow_nan=False))
    elif args.command == "analyze-music":
        save_music_analysis(analyze_music(args.input, use_librosa=not args.no_librosa), args.output)
    elif args.command == "plan-slideshow":
        beats = None
        if args.beats_json:
            data = json.loads(Path(args.beats_json).read_text())
            beats = data.get("beats_s", data) if isinstance(data, dict) else data
        plan = plan_slideshow(args.assets, target_duration=args.duration, beats=beats)
        Path(args.output).write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    elif args.command == "storyboard":
        write_storyboard(args.manifest, args.output)
    elif args.command == "captions":
        cues = parse_srt(args.input)
        if args.ass_output:
            style = {"font": args.font}
            if args.font_size:
                style["font_size"] = args.font_size
            write_ass(cues, args.ass_output, width=args.width, height=args.height, style=style)
        report = {"cues": len(cues), "issues": validate_cues(cues)}
        if args.report:
            Path(args.report).write_text(json.dumps(report, indent=2) + "\n")
        else:
            print(json.dumps(report, indent=2))
    elif args.command == "render":
        render_project(args.manifest, args.output, work_dir=args.work_dir)
    elif args.command == "qa":
        report = validate_video(args.input, expected_width=args.width, expected_height=args.height, expected_duration=args.duration, deep=args.deep)
        if args.output:
            save_report(report, args.output)
        else:
            print(json.dumps(report, indent=2))
        return 0 if report["passed"] else 2
    elif args.command == "export-timeline":
        (export_cmx3600 if args.format == "edl" else export_otio)(args.manifest, args.output)
    elif args.command == "inventory":
        Path(args.output).write_text(json.dumps({"assets": inventory_paths(args.paths, recursive=not args.no_recursive)}, indent=2) + "\n")
    elif args.command == "pack-transcript":
        data = json.loads(Path(args.input).read_text())
        Path(args.output).write_text(json.dumps({"phrases": pack_phrases(data, silence_threshold=args.silence)}, indent=2) + "\n")
    elif args.command == "snap-ranges":
        ranges = json.loads(Path(args.ranges).read_text())
        transcript = json.loads(Path(args.transcript).read_text())
        if isinstance(ranges, dict):
            ranges = ranges.get("ranges", ranges.get("segments", []))
        result = snap_ranges(ranges, transcript, pad_before=args.pad_before, pad_after=args.pad_after)
        Path(args.output).write_text(json.dumps({"ranges": result}, indent=2) + "\n")
    elif args.command == "contact-sheet":
        make_contact_sheet(args.input, args.output, count=args.count, frame_width=args.width)
    elif args.command == "waveform":
        make_waveform(args.input, args.output, width=args.width, height=args.height, start=args.start, end=args.end)
    elif args.command == "timeline-view":
        make_timeline_view(args.input, args.output, start=args.start, end=args.end, count=args.count, frame_width=args.width)
    elif args.command == "reframe":
        crop = crop_from_anchor(args.source_width, args.source_height, args.target_width, args.target_height, anchor_x=args.anchor_x, anchor_y=args.anchor_y)
        print(json.dumps({"crop": {"x": crop[0], "y": crop[1], "width": crop[2], "height": crop[3]}}, indent=2))
    return 0


def entrypoint() -> None:
    raise SystemExit(main())


if __name__ == "__main__":
    entrypoint()
