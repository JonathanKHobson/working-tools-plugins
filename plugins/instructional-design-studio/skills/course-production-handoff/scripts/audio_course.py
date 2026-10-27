#!/usr/bin/env python3
"""Run the integrated audio-course helpers in an explicit project workspace."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

RUNTIME = Path(__file__).with_name("audio_lessons")


def within(workspace, path):
    value = Path(path)
    if not value.is_absolute():
        value = workspace / value
    for parent in (value, *value.parents):
        if parent.is_symlink():
            raise ValueError("Symlink inputs are not permitted")
        if parent == workspace:
            break
    value = value.resolve()
    if not value.is_relative_to(workspace):
        raise ValueError("Path escapes the selected workspace")
    return value


def command(args):
    raw = Path(args.workspace).absolute()
    if any(p.is_symlink() for p in (raw, *raw.parents)):
        raise ValueError("Workspace must not use symlinks")
    ws = raw.resolve(strict=True)
    if not ws.is_dir() or ws == Path.home() or ws == Path(ws.anchor):
        raise ValueError("Select a dedicated existing course workspace")
    # Reject links anywhere the helpers traverse, including source and media files.
    for child in ws.rglob("*"):
        if child.is_symlink():
            raise ValueError("Course workspace contains a symlink")
    env = {k: os.environ[k] for k in ("PATH", "LANG", "LC_ALL", "SYSTEMROOT") if k in os.environ}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    scratch = ws / "cache"
    scratch.mkdir(exist_ok=True)
    env["TMPDIR"] = str(scratch)
    cmd = [sys.executable, "-B", str(RUNTIME / (args.action + ".py"))]
    if args.action == "scrape":
        if not args.allow_host:
            raise ValueError("Scraping requires explicit --allow-host entries")
        env["AUDIO_LESSON_ALLOWED_HOSTS"] = ",".join(args.allow_host)
        cmd += [str(ws), args.author or "web"]
    elif args.action == "check_lessons":
        cmd += [str(ws)]
    elif args.action == "package_class":
        if not 1 <= args.max_mb <= 100:
            raise ValueError("Archive cap must be 1 to 100 MiB")
        folders = list((ws / "class").glob("[0-9][0-9]-*"))
        if not folders or any(not (d / "card.md").is_file() or not list(d.glob("*.mp3")) for d in folders):
            raise ValueError("Every lesson needs a card and rendered audio before packaging")
        cmd += [str(ws), "--max-mb", str(args.max_mb)]
    else:
        if not args.script or not args.output:
            raise ValueError("Rendering needs --script and --output")
        script, output = within(ws, args.script), within(ws, args.output)
        if not script.is_file() or output.exists():
            raise ValueError("Script must exist and render destination must be new")
        if args.engine == "elevenlabs":
            if not args.allow_upload:
                raise ValueError("ElevenLabs requires explicit authorized --allow-upload")
            key = os.environ.get("ELEVENLABS_API_KEY")
            if not key:
                raise ValueError("Selected provider key is unavailable")
            env["ELEVENLABS_API_KEY"] = key
            env["AUDIO_LESSON_ALLOW_UPLOAD"] = "1"
        cmd += [str(script), str(output)]
    return cmd, env, ws


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=["scrape", "check_lessons", "render_audio", "package_class"])
    p.add_argument("--workspace", required=True)
    p.add_argument("--allow-host", action="append", default=[])
    p.add_argument("--author")
    p.add_argument("--script")
    p.add_argument("--output")
    p.add_argument("--engine", choices=["local", "elevenlabs"], default="local")
    p.add_argument("--allow-upload", action="store_true")
    p.add_argument("--max-mb", type=int, default=25)
    a = p.parse_args()
    try:
        cmd, env, ws = command(a)
        return subprocess.run(cmd, cwd=ws, env=env, timeout=600, check=False).returncode
    except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
        p.exit(2, str(exc) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
