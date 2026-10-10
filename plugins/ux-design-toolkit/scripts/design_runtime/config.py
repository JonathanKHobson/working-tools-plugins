"""Idempotent project-local hook configuration for Codex and Claude."""

from __future__ import annotations

import json
import os
import shlex
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .engine import plugin_root, verified_engine
from .scope import disable, enable

CONFIGS = {"codex": Path(".codex/hooks.json"), "claude": Path(".claude/settings.json")}


def _hosts(host: str) -> tuple[str, ...]:
    if host not in {"codex", "claude", "both"}:
        raise ValueError("Host must be codex, claude, or both")
    return ("codex", "claude") if host == "both" else (host,)


def owned_command(root: Path, kind: str, plugin: Path | None = None) -> str:
    launcher = (plugin or plugin_root()) / "scripts" / "design_runtime.py"
    # Keep the invoking venv's executable path, including its Python symlink.
    interpreter = Path(sys.executable).absolute()
    return " ".join(shlex.quote(str(part)) for part in (interpreter, launcher.resolve(), "hook", kind, "--project", root))


def _entries(root: Path, host: str, plugin: Path | None = None) -> dict[str, dict]:
    post = {"type": "command", "command": owned_command(root, "post", plugin), "timeout": 5}
    stop = {"type": "command", "command": owned_command(root, "stop", plugin), "timeout": 30}
    if host == "codex":
        post["statusMessage"] = "Checking edited UI files"
        stop["statusMessage"] = "Checking queued UI files"
    return {"PostToolUse": {"matcher": "Edit|Write|apply_patch", "hooks": [post]},
            "Stop": {"hooks": [stop]}}


def _load(path: Path) -> dict:
    if path.is_symlink():
        raise ValueError(f"Hook config cannot be a symlink: {path}")
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Hook config must be a JSON object: {path}")
    hooks = data.get("hooks", {})
    if not isinstance(hooks, dict):
        raise ValueError(f"Hook config hooks must be an object: {path}")
    for event in ("PostToolUse", "Stop"):
        if event in hooks and not isinstance(hooks[event], list):
            raise ValueError(f"Hook config {event} must be an array: {path}")
    return data


def _is_owned(handler: object, root: Path, plugin: Path | None) -> bool:
    if not isinstance(handler, dict) or handler.get("type") != "command":
        return False
    command = handler.get("command")
    if not isinstance(command, str):
        return False
    try:
        parts = shlex.split(command)
    except ValueError:
        return False
    launcher = ((plugin or plugin_root()) / "scripts" / "design_runtime.py").resolve()
    # The exact launcher, verb, and project identify our entries across a
    # recipient's interpreter change, including migration from Homebrew Python.
    return (len(parts) == 6 and Path(parts[0]).is_absolute()
            and parts[1:] in ([str(launcher), "hook", "post", "--project", str(root)],
                              [str(launcher), "hook", "stop", "--project", str(root)]))


def _remove_owned(data: dict, root: Path, plugin: Path | None = None) -> dict:
    hooks = data.get("hooks")
    if not isinstance(hooks, dict):
        return data
    for event in ("PostToolUse", "Stop"):
        current = hooks.get(event)
        if not isinstance(current, list):
            continue
        updated = []
        for group in current:
            if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
                updated.append(group)
                continue
            remaining = [handler for handler in group["hooks"] if not _is_owned(handler, root, plugin)]
            if remaining:
                updated.append({**group, "hooks": remaining})
        if updated:
            hooks[event] = updated
        else:
            hooks.pop(event, None)
    if not hooks:
        data.pop("hooks", None)
    return data


def _save(path: Path, data: dict) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if path.exists():
        suffix = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        shutil.copy2(path, path.with_name(path.name + ".bak-" + suffix))
    descriptor, name = tempfile.mkstemp(prefix=path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(data, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        Path(name).chmod(0o600)
        Path(name).replace(path)
    finally:
        Path(name).unlink(missing_ok=True)


def install_marker_only(root: Path) -> Path:
    """Opt in to plugin-owned hooks without creating duplicate project hooks."""
    verified_engine()
    for host in _hosts("both"):
        path = root / CONFIGS[host]
        data = _load(path)
        for groups in data.get("hooks", {}).values():
            if not isinstance(groups, list):
                continue
            for group in groups:
                if isinstance(group, dict) and isinstance(group.get("hooks"), list):
                    if any(_is_owned(handler, root, None) for handler in group["hooks"]):
                        raise ValueError(
                            "Owned project-local hooks already exist; remove them with "
                            "remove-hooks --project ROOT --host both before marker-only opt-in"
                        )
    return enable(root)


def install_hooks(root: Path, host: str) -> list[Path]:
    verified_engine()
    planned = []
    for item in _hosts(host):
        path = root / CONFIGS[item]
        data = _load(path)
        before = json.dumps(data, sort_keys=True)
        data = _remove_owned(data, root)
        hooks = data.setdefault("hooks", {})
        for event, group in _entries(root, item).items():
            hooks.setdefault(event, []).append(group)
        planned.append((path, data, before != json.dumps(data, sort_keys=True)))
    for path, data, changed in planned:
        if changed:
            _save(path, data)
    enable(root)
    return [path for path, _, _ in planned]


def remove_hooks(root: Path, host: str) -> list[Path]:
    planned = []
    for item in _hosts(host):
        path = root / CONFIGS[item]
        data = _load(path)
        before = json.dumps(data, sort_keys=True)
        data = _remove_owned(data, root)
        planned.append((path, data, before != json.dumps(data, sort_keys=True)))
    disable(root)
    for path, data, changed in planned:
        if changed:
            _save(path, data)
    return [path for path, _, _ in planned]
