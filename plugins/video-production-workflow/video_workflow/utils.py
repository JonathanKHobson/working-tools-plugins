from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, Iterable

from .errors import ToolMissingError, VideoWorkflowError

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
RESOLVABLE_MEDIA_TOOLS = {"ffmpeg", "ffprobe"}


def resolve_tool(name: str, *, required: bool = True) -> str | None:
    """Resolve an executable from explicit overrides, plugin runtime, or PATH."""
    normalized = name.upper().replace("-", "_")
    override_keys = (f"VIDEO_WORKFLOW_{normalized}", normalized)
    for key in override_keys:
        value = os.environ.get(key)
        if not value:
            continue
        candidate = Path(value).expanduser()
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate.resolve())
        if required:
            raise ToolMissingError(f"{key} points to a missing or non-executable file: {candidate}")
        return None

    home = Path(os.environ.get("VIDEO_WORKFLOW_HOME", PLUGIN_ROOT)).expanduser()
    runtime_candidate = home / ".runtime" / "bin" / name
    if runtime_candidate.is_file() and os.access(runtime_candidate, os.X_OK):
        return str(runtime_candidate.resolve())

    if path := shutil.which(name):
        return str(Path(path).resolve())
    if required:
        raise ToolMissingError(
            f"Required executable not found: {name}. Set VIDEO_WORKFLOW_{normalized}, "
            f"place it at {home / '.runtime' / 'bin' / name}, or add it to PATH."
        )
    return None


def require_tool(name: str) -> str:
    path = resolve_tool(name, required=True)
    assert path is not None
    return path


def run(cmd: Iterable[str], *, capture: bool = False, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    command = [str(x) for x in cmd]
    if command and command[0] in RESOLVABLE_MEDIA_TOOLS:
        command[0] = require_tool(command[0])
    try:
        return subprocess.run(
            command,
            check=True,
            text=True,
            capture_output=capture,
            cwd=str(cwd) if cwd else None,
        )
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()
        raise VideoWorkflowError(f"Command failed ({exc.returncode}): {' '.join(command)}\n{detail}") from exc


def sha256_file(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(data: Any, path: str | Path) -> None:
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_fraction(value: str | int | float | None) -> float | None:
    if value in (None, "", "0/0"):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if "/" in value:
        numerator, denominator = value.split("/", 1)
        den = float(denominator)
        return float(numerator) / den if den else None
    return float(value)
