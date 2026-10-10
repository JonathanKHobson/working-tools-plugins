"""Verify and invoke only the packaged native engine."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import struct
import subprocess
from pathlib import Path


class RuntimeErrorWithMessage(Exception):
    pass


def plugin_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _binary_arch_ok(binary: Path, arch: str) -> bool:
    """Check the Mach-O header independently of manifest metadata."""
    if platform.system() != "Darwin":
        return True
    wanted = {"arm64": 0x0100000C, "x86_64": 0x01000007}.get(arch)
    if wanted is None:
        return False
    with binary.open("rb") as stream:
        header = stream.read(4096)
    if len(header) < 8:
        return False
    magic = header[:4]
    if magic == b"\xcf\xfa\xed\xfe":
        return struct.unpack_from("<I", header, 4)[0] == wanted
    if magic == b"\xfe\xed\xfa\xcf":
        return struct.unpack_from(">I", header, 4)[0] == wanted
    if magic in {b"\xca\xfe\xba\xbe", b"\xca\xfe\xba\xbf"}:
        count = struct.unpack_from(">I", header, 4)[0]
        entry_size = 20 if magic == b"\xca\xfe\xba\xbe" else 32
        if count > 100 or len(header) < 8 + count * entry_size:
            return False
        return any(struct.unpack_from(">I", header, 8 + i * entry_size)[0] == wanted for i in range(count))
    return False


def _asset_digest(runtime: Path, assets: Path) -> str:
    lines = []
    for item in sorted(assets.rglob("*"), key=lambda path: path.relative_to(runtime).as_posix()):
        if item.is_symlink():
            raise RuntimeErrorWithMessage("Pinned runtime assets contain a symlink")
        if item.is_file():
            relative = item.relative_to(runtime).as_posix()
            lines.append(f"{relative} {hashlib.sha256(item.read_bytes()).hexdigest()}\n")
    return hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()


def verified_engine(root: Path | None = None) -> tuple[Path, Path]:
    root = (root or plugin_root()).resolve()
    runtime = root / "runtime" / "impeccable"
    manifest_path = runtime / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        info = manifest["engine"]
        relative = Path(info["path"])
        expected_hash = info["sha256"]
        asset_relative = Path(manifest["skillDir"])
    except (OSError, KeyError, ValueError, TypeError) as exc:
        raise RuntimeErrorWithMessage(f"Pinned runtime manifest missing or invalid: {manifest_path}") from exc
    if manifest.get("schemaVersion") != 1 or not isinstance(expected_hash, str) or len(expected_hash) != 64:
        raise RuntimeErrorWithMessage("Pinned runtime manifest has an unsupported schema or SHA-256")
    if info.get("platform") != platform.system().lower() or info.get("arch") != platform.machine():
        raise RuntimeErrorWithMessage("Pinned runtime architecture/platform does not match this host")
    if relative.is_absolute() or ".." in relative.parts or asset_relative.is_absolute() or ".." in asset_relative.parts:
        raise RuntimeErrorWithMessage("Pinned runtime manifest path escapes its package")
    binary = (runtime / relative).resolve()
    assets = (runtime / asset_relative).resolve()
    if not binary.is_relative_to(runtime.resolve()) or not assets.is_relative_to(runtime.resolve()):
        raise RuntimeErrorWithMessage("Pinned runtime package contains an escaping path")
    if not binary.is_file() or not os.access(binary, os.X_OK):
        raise RuntimeErrorWithMessage(f"Pinned runtime executable is missing or not executable: {binary}")
    if not assets.is_dir():
        raise RuntimeErrorWithMessage(f"Pinned runtime assets are missing: {assets}")
    asset_hash = manifest.get("skillAssetsSha256")
    if not isinstance(asset_hash, str) or len(asset_hash) != 64 or _asset_digest(runtime, assets) != asset_hash.lower():
        raise RuntimeErrorWithMessage("Pinned runtime asset SHA-256 mismatch; refusing to execute")
    digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    if digest != expected_hash.lower():
        raise RuntimeErrorWithMessage("Pinned runtime SHA-256 mismatch; refusing to execute")
    if not _binary_arch_ok(binary, info["arch"]):
        raise RuntimeErrorWithMessage("Pinned runtime binary architecture does not match its manifest")
    return binary, assets


def private_env(assets: Path, self_path: Path) -> dict[str, str]:
    # No inherited API/cloud credentials, browser override, update URL, or downloader controls.
    names = ("HOME", "PATH", "TMPDIR", "LANG", "LC_ALL", "USER", "SHELL", "NODE_ENV")
    env = {key: os.environ[key] for key in names if key in os.environ}
    env.update({
        "IMPECCABLE_SKILL_DIR": str(assets),
        "IMPECCABLE_SELF": str(self_path.resolve()),
        "IMPECCABLE_NO_UPDATE_CHECK": "1",
        "IMPECCABLE_HOOK_DEPTH": "1",
    })
    return env


def invoke(args: list[str], *, root: Path | None = None, timeout: int = 30,
           input_text: str | None = None, cwd: Path | None = None,
           extra_env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    binary, assets = verified_engine(root)
    launcher = (root or plugin_root()) / "scripts" / "design_runtime.py"
    try:
        env = private_env(assets, launcher)
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            [str(binary), *args], cwd=str(cwd) if cwd else None,
            env=env, input=input_text, text=True,
            capture_output=True, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeErrorWithMessage(f"Pinned runtime timed out after {timeout}s") from exc
    except OSError as exc:
        raise RuntimeErrorWithMessage(f"Pinned runtime could not start: {exc.strerror}") from exc
