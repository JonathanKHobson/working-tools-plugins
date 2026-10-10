#!/usr/bin/env python3
"""Plan or apply a conservative local video-production toolchain.

Dry-run is the default. This script intentionally avoids downloading models,
source-available renderers, Shaka Packager release binaries, or third-party
assets without an explicit project decision.
"""
from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


PROFILES = ("core", "production", "creator", "qc", "full")


def _mac_commands(profile: str) -> tuple[list[list[str]], list[str]]:
    packages = ["ffmpeg", "python", "git"]
    commands: list[list[str]] = []
    manual: list[str] = []
    if profile in {"production", "full"}:
        packages += ["media-info", "exiftool", "imagemagick", "sox"]
    if profile in {"creator", "full"}:
        packages += ["node"]
    if profile in {"qc", "full"}:
        packages += ["mediaconch", "libvmaf"]
    commands.append(["brew", "install", *dict.fromkeys(packages)])
    if profile in {"qc", "full"}:
        commands.append(["brew", "install", "--cask", "qctools"])
    manual.append("Install Shaka Packager from an official pinned release or controlled container only when DASH/HLS packaging is required.")
    return commands, manual


def _linux_commands(profile: str) -> tuple[list[list[str]], list[str]]:
    packages = ["ffmpeg", "python3", "python3-venv", "python3-pip", "git"]
    manual: list[str] = []
    if profile in {"production", "full"}:
        packages += ["mediainfo", "libimage-exiftool-perl", "imagemagick", "sox"]
    if profile in {"creator", "full"}:
        packages += ["nodejs", "npm"]
    if profile in {"qc", "full"}:
        manual.append("Install a VMAF-enabled FFmpeg build, MediaConch and QCTools from your distribution or MediaArea repository after verifying package provenance.")
    manual.append("Install Shaka Packager from an official pinned release or controlled container only when DASH/HLS packaging is required.")
    return [["sudo", "apt-get", "update"], ["sudo", "apt-get", "install", "-y", *dict.fromkeys(packages)]], manual


def _windows_commands(profile: str) -> tuple[list[list[str]], list[str]]:
    commands = [
        ["winget", "install", "--id", "Gyan.FFmpeg", "-e"],
        ["winget", "install", "--id", "Python.Python.3.12", "-e"],
        ["winget", "install", "--id", "Git.Git", "-e"],
    ]
    manual = [
        "Install MediaInfo and ExifTool from a trusted package manager or official release when metadata inspection is needed.",
        "Install Shaka Packager from an official pinned release or controlled container only when DASH/HLS packaging is required.",
    ]
    if profile in {"creator", "full"}:
        commands.append(["winget", "install", "--id", "OpenJS.NodeJS.LTS", "-e"])
    if profile in {"qc", "full"}:
        manual.append("Install QCTools/MediaConch from MediaArea and confirm the shell-visible executable paths.")
    return commands, manual


def build_plan(profile: str, *, with_audio: bool = False, apply: bool = False) -> dict[str, Any]:
    system = platform.system().lower()
    manager = "manual"
    commands: list[list[str]] = []
    manual: list[str] = []

    if system == "darwin" and shutil.which("brew"):
        manager = "homebrew"
        commands, manual = _mac_commands(profile)
    elif system == "linux" and shutil.which("apt-get"):
        manager = "apt"
        commands, manual = _linux_commands(profile)
    elif system == "windows" and shutil.which("winget"):
        manager = "winget"
        commands, manual = _windows_commands(profile)
    else:
        manual.extend(
            [
                "Install Python 3.10+, FFmpeg/ffprobe and Git from trusted system packages or official releases.",
                "Read docs/OPTIONAL_INTEGRATIONS.md and verify every optional tool before installation.",
            ]
        )

    extras: list[str] = []
    if profile in {"production", "qc", "full"} or with_audio:
        extras.append("audio")
    if profile in {"qc", "full"}:
        extras.append("analysis")
    if profile == "full":
        extras += ["interchange", "python-renderer", "dev"]
    extra_expr = f".[{','.join(dict.fromkeys(extras))}]" if extras else "."
    commands.append([sys.executable, "-m", "pip", "install", "-e", extra_expr])

    manual.extend(
        [
            "Run python scripts/check_environment.py and save the JSON report after installation.",
            "Inspect FFmpeg filters/encoders rather than assuming a package name implies required capabilities.",
            "Install renderer-specific Node/Python dependencies inside the project or animation slot, not globally, unless a team policy says otherwise.",
        ]
    )
    return {
        "reviewed_at": "2026-07-22",
        "platform": platform.platform(),
        "manager": manager,
        "profile": profile,
        "apply": apply,
        "commands": commands,
        "manual_steps": manual,
        "warning": "Dry-run by default. Package availability, licensing and build flags change; review before applying.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Plan or apply a conservative video toolchain install.")
    parser.add_argument("--profile", choices=PROFILES, default="core")
    parser.add_argument("--with-audio", action="store_true", help="Compatibility flag: include Python audio extras")
    parser.add_argument("--apply", action="store_true", help="Execute planned commands after printing the plan")
    parser.add_argument("--json", action="store_true", help="Emit a machine-readable plan")
    args = parser.parse_args(argv)

    plan = build_plan(args.profile, with_audio=args.with_audio, apply=args.apply)
    if args.json:
        print(json.dumps(plan, indent=2))
    else:
        print(plan["warning"])
        for command in plan["commands"]:
            print("+", " ".join(command))
        for step in plan["manual_steps"]:
            print("-", step)

    if args.apply:
        for command in plan["commands"]:
            subprocess.run(command, check=True, cwd=Path(__file__).resolve().parents[1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
