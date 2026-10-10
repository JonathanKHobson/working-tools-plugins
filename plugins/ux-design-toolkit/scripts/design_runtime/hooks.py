"""Bounded, advisory PostToolUse and Stop scanning."""

from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

from .engine import RuntimeErrorWithMessage, invoke
from .scope import allowed_file, enabled, project_root

MAX_INPUT = 256_000
MAX_FILES = 12
MAX_FINDINGS = 8
DEBOUNCE_SECONDS = 2.0
PATCH_PATH = re.compile(r"^\*\*\* (?:Add|Update|Delete|Move to) File: (.+)$", re.M)
FRONTEND_TOOLS = {"edit", "write", "apply_patch", "multiedit", "str_replace_editor", "functions.apply_patch"}


def event_paths(event: dict) -> list[str]:
    name = event.get("tool_name") or event.get("toolName") or event.get("tool")
    if isinstance(name, dict):
        name = name.get("name")
    if not isinstance(name, str) or name.lower() not in FRONTEND_TOOLS:
        return []
    payload = event.get("tool_input") or event.get("toolInput") or event.get("input") or {}
    if isinstance(payload, str) and "apply_patch" in name.lower():
        return PATCH_PATH.findall(payload)
    if not isinstance(payload, dict):
        return []
    values: list[str] = []
    for key in ("file_path", "path", "filename"):
        value = payload.get(key)
        if isinstance(value, str):
            values.append(value)
    for key in ("patch", "content", "command", "input"):
        value = payload.get(key)
        if isinstance(value, str) and ("apply_patch" in name.lower() or key == "patch"):
            values.extend(PATCH_PATH.findall(value))
    edits = payload.get("edits")
    if isinstance(edits, list):
        values.extend(edit.get("file_path") for edit in edits if isinstance(edit, dict) and isinstance(edit.get("file_path"), str))
    return values


def _session_key(root: Path, event: dict) -> str | None:
    session = event.get("session_id") or event.get("sessionId")
    if not isinstance(session, str) or not session or len(session) > 256:
        return None
    return hashlib.sha256((str(root) + "\x00" + session).encode()).hexdigest()


def _cache_path(key: str) -> Path:
    if sys.platform == "darwin":
        cache_home = Path.home() / "Library" / "Caches"
    else:
        configured = Path(os.environ.get("XDG_CACHE_HOME") or "").expanduser()
        cache_home = configured if configured.is_absolute() else Path.home() / ".cache"
    base = cache_home / "ux-design-toolkit" / "design-runtime"
    base.mkdir(parents=True, mode=0o700, exist_ok=True)
    base.chmod(0o700)
    return base / f"{key}.json"


def _read_state(path: Path) -> dict:
    try:
        if path.is_symlink():
            return {}
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {}
        pending = data.get("pending")
        last = data.get("lastScan")
        return {"pending": pending if isinstance(pending, list) else [],
                "lastScan": last if isinstance(last, (int, float)) and last >= 0 else 0}
    except (OSError, ValueError):
        return {}


def _write_state(path: Path, state: dict) -> None:
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(state, separators=(",", ":")), encoding="utf-8")
    temp.chmod(0o600)
    temp.replace(path)


def _scan(root: Path, files: list[str], *, timeout: int) -> str:
    # One bounded detector invocation; no source text enters adapter state or logs.
    result = invoke(["detect", "--json", *files], cwd=root, timeout=timeout)
    if result.returncode not in {0, 2}:
        return "Design detector could not complete this scoped scan. Run an explicit manual scan if needed."
    try:
        findings = json.loads(result.stdout)
    except ValueError:
        return "Design detector returned invalid JSON for this scoped scan."
    if not isinstance(findings, list) or not findings:
        return ""
    lines = ["Impeccable advisory findings for edited frontend files (review against the rendered UI):"]
    for finding in findings[:MAX_FINDINGS]:
        if not isinstance(finding, dict):
            continue
        location = finding.get("file") or finding.get("path") or "edited file"
        line = finding.get("line") or finding.get("start_line")
        rule = finding.get("antipattern") or finding.get("rule") or finding.get("rule_id") or finding.get("id") or "design rule"
        message = finding.get("message") or finding.get("description") or "Review this finding."
        location = str(location)[:180]
        message = " ".join(str(message).split())[:240]
        lines.append(f"- {location}{':' + str(line) if line else ''}: {rule}: {message}")
    if len(findings) > MAX_FINDINGS:
        lines.append(f"- {len(findings) - MAX_FINDINGS} more findings omitted; run a manual scan for full JSON.")
    return "\n".join(lines)


def handle(kind: str, event: dict, root_arg: str) -> str:
    if os.environ.get("IMPECCABLE_HOOK_DISABLED") or os.environ.get("IMPECCABLE_HOOK_DEPTH") not in (None, "", "0") or os.environ.get("CLAUDE_HOOK_DEPTH") not in (None, "", "0"):
        return ""
    if not isinstance(event, dict) or kind not in {"post", "stop"} or event.get("stop_hook_active") or event.get("stopHookActive"):
        return ""
    try:
        root = project_root(root_arg)
        declared_cwd = event.get("cwd") or event.get("working_directory")
        cwd = Path(declared_cwd).resolve(strict=True) if isinstance(declared_cwd, str) else None
        if cwd is None or not cwd.is_relative_to(root) or not enabled(root):
            return ""
    except (OSError, ValueError, RuntimeError):
        return ""
    key = _session_key(root, event)
    if key is None:
        return ""
    path = _cache_path(key)
    lock = path.with_suffix(".lock")
    with lock.open("a+") as handle_lock:
        lock.chmod(0o600)
        fcntl.flock(handle_lock.fileno(), fcntl.LOCK_EX)
        state = _read_state(path)
        pending = [str(p) for raw in state.get("pending", []) if isinstance(raw, str) if (p := allowed_file(root, raw))]
        if kind == "post":
            for raw in event_paths(event):
                file = allowed_file(root, raw)
                if file and str(file) not in pending:
                    pending.append(str(file))
            pending = pending[:MAX_FILES]
            now = time.monotonic()
            if not pending or (state.get("lastScan", 0) and now - float(state["lastScan"]) < DEBOUNCE_SECONDS):
                _write_state(path, {"pending": pending, "lastScan": state.get("lastScan", 0)})
                return ""
            _write_state(path, {"pending": [], "lastScan": now})
        else:
            if not pending:
                return ""
            pending = pending[:MAX_FILES]
            _write_state(path, {"pending": [], "lastScan": state.get("lastScan", 0)})
    try:
        return _scan(root, pending, timeout=3 if kind == "post" else 20)
    except RuntimeErrorWithMessage:
        return "Design detector runtime unavailable for this scoped scan."
