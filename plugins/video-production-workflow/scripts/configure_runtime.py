#!/usr/bin/env python3
"""Register FFmpeg and ffprobe for the plugin without modifying global PATH."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _verify(path: Path) -> str:
    if not path.is_file() or not os.access(path, os.X_OK):
        raise SystemExit(f"Not an executable file: {path}")
    proc = subprocess.run([str(path), "-version"], capture_output=True, text=True, check=False)
    if proc.returncode:
        raise SystemExit(f"Executable failed its version check: {path}")
    return next((line.strip() for line in proc.stdout.splitlines() if line.strip()), "present")


def _install(source: Path, destination: Path, mode: str, force: bool) -> None:
    if destination.exists() or destination.is_symlink():
        if not force:
            raise SystemExit(f"Runtime target exists; rerun with --force: {destination}")
        destination.unlink()
    destination.parent.mkdir(parents=True, exist_ok=True)
    if mode == "symlink":
        destination.symlink_to(source.resolve())
        return
    with tempfile.NamedTemporaryFile(dir=destination.parent, prefix=f".{destination.name}-", delete=False) as handle:
        temporary = Path(handle.name)
    try:
        shutil.copy2(source, temporary)
        temporary.chmod(0o755)
        temporary.replace(destination)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ffmpeg", required=True)
    parser.add_argument("--ffprobe", required=True)
    parser.add_argument("--mode", choices=("copy", "symlink"), default="symlink")
    parser.add_argument("--runtime-root", default=str(ROOT / ".runtime"))
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    runtime = Path(args.runtime_root).expanduser().resolve()
    sources = {
        "ffmpeg": Path(args.ffmpeg).expanduser().resolve(),
        "ffprobe": Path(args.ffprobe).expanduser().resolve(),
    }
    versions = {name: _verify(path) for name, path in sources.items()}
    destinations = {name: runtime / "bin" / name for name in sources}
    for name in sources:
        _install(sources[name], destinations[name], args.mode, args.force)

    report = {
        "mode": args.mode,
        "runtime_root": str(runtime),
        "tools": {
            name: {
                "source": str(sources[name]),
                "installed": str(destinations[name]),
                "version": versions[name],
                "sha256": _sha256(destinations[name]),
            }
            for name in sources
        },
    }
    runtime.mkdir(parents=True, exist_ok=True)
    (runtime / "runtime-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
