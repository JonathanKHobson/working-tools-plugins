#!/usr/bin/env python3

from __future__ import annotations

import ast
import json
import re
import shutil
from pathlib import Path
from typing import Any

HOME = Path.home()
CLAUDE_DIR = HOME / "Library" / "Application Support" / "Claude"
ACTIVE_CONFIG_PATH = CLAUDE_DIR / "claude_desktop_config.json"
MCP_LOG_PATH = HOME / "Library" / "Logs" / "Claude" / "mcp.log"
CODEX_PROFILE_DIR = HOME / ".codex" / "mcp-profiles"
FLEET_REPORT_PATH = Path.cwd() / "claude-mcp-fleet-report.md"

PROFILE_FILES = {
    "minimal-profile": CLAUDE_DIR / "claude_desktop_config.minimal-profile.json",
    "task-profile-a": CLAUDE_DIR / "claude_desktop_config.task-profile-a.json",
    "task-profile-b": CLAUDE_DIR / "claude_desktop_config.task-profile-b.json",
    "quarantine-profile": CLAUDE_DIR / "claude_desktop_config.quarantine-profile.json",
    "full-fleet": CLAUDE_DIR / "claude_desktop_config.full-fleet.json",
}

DAILY_PROFILE = "minimal-profile"
QUARANTINED_SERVERS = set()
EXPECTED_TOOLS = {}  # Fill from the current host's reviewed inventory.

LOG_CATEGORIES = {
    "invalid_json": "Invalid JSON",
    "timeout": "Request timed out",
    "parse_error": "Failed to parse message",
    "operation_not_permitted": "Operation not permitted",
}


def canonical_name(name: str) -> str:
    return name.replace("-", "_")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def load_claude_config(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    payload.setdefault("preferences", {})
    payload.setdefault("mcpServers", {})
    return payload


def server_names(payload: dict[str, Any]) -> set[str]:
    return {canonical_name(name) for name in payload.get("mcpServers", {}).keys()}


def resolve_command(command: str | None) -> str | None:
    if not command:
        return None
    if "/" in command:
        path = Path(command).expanduser()
        return str(path) if path.exists() else None
    return shutil.which(command)


def command_type(command: str | None) -> str:
    if not command:
        return "unknown"
    lower = command.lower()
    if "python" in lower:
        return "python"
    if lower.endswith("npx") or lower == "npx":
        return "npx"
    if lower.endswith("node") or lower == "node":
        return "node"
    if lower.endswith("dotnet") or lower == "dotnet":
        return "dotnet"
    if lower.endswith(("bash", "sh", "zsh")):
        return "shell"
    return "other"


def runtime_location(command_path: str | None) -> str:
    if not command_path:
        return "missing"
    if command_path.startswith("/Volumes/"):
        return "external-drive runtime"
    if command_path.startswith(str(HOME)):
        return "home-directory runtime"
    return "system runtime"


def path_in_args(args: list[str], prefix: str) -> bool:
    return any(arg.startswith(prefix) for arg in args if isinstance(arg, str))


def load_codex_profile(server_name: str) -> dict[str, Any] | None:
    target = canonical_name(server_name)
    if not CODEX_PROFILE_DIR.exists():
        return None
    for path in CODEX_PROFILE_DIR.glob("*.toml"):
        if canonical_name(path.stem) != target:
            continue
        command: str | None = None
        args: list[str] = []
        for raw_line in path.read_text().splitlines():
            line = raw_line.strip()
            if line.startswith("command = "):
                command = ast.literal_eval(line.split("=", 1)[1].strip())
            elif line.startswith("args = "):
                args = ast.literal_eval(line.split("=", 1)[1].strip())
        return {"path": path, "command": command, "args": args}
    return None


def compare_codex_launcher(server_name: str, config: dict[str, Any]) -> str | None:
    codex_profile = load_codex_profile(server_name)
    if not codex_profile:
        return None
    command = config.get("command")
    args = config.get("args", [])
    if command != codex_profile.get("command") or args != codex_profile.get("args", []):
        return (
            f"Codex launcher drift versus {codex_profile['path'].name}: "
            f"Claude uses {render_command(command, args)}"
        )
    return None


def render_command(command: str | None, args: list[str] | None) -> str:
    rendered_args = " ".join(args or [])
    if rendered_args:
        return f"{command} {rendered_args}"
    return command or "(missing command)"


def load_profile_memberships() -> dict[str, list[str]]:
    memberships: dict[str, list[str]] = {}
    for profile_name, path in PROFILE_FILES.items():
        if not path.exists():
            continue
        payload = load_claude_config(path)
        for server in sorted(payload.get("mcpServers", {})):
            memberships.setdefault(canonical_name(server), []).append(profile_name)
    return memberships


def classify_risk(server_name: str, memberships: list[str]) -> str:
    if server_name in QUARANTINED_SERVERS:
        return "quarantine"
    if DAILY_PROFILE in memberships:
        return "daily-default"
    if "quarantine-profile" in memberships:
        return "study"
    if memberships:
        return "pack-only"
    return "unassigned"


def infer_profile_name(active_servers: set[str]) -> str:
    for profile_name, path in PROFILE_FILES.items():
        if not path.exists():
            continue
        if active_servers == server_names(load_claude_config(path)):
            return profile_name
    return "custom"


def load_log_evidence(log_path: Path = MCP_LOG_PATH) -> dict[str, dict[str, str]]:
    evidence: dict[str, dict[str, str]] = {}
    if not log_path.exists():
        return evidence
    pattern = re.compile(r"\[(?:info|warn|error)\] \[(?P<server>[^\]]+)\] (?P<message>.*)$")
    for line in log_path.read_text(errors="ignore").splitlines():
        match = pattern.search(line)
        if not match:
            continue
        server = canonical_name(match.group("server"))
        message = match.group("message")
        for category, needle in LOG_CATEGORIES.items():
            if needle in message:
                evidence.setdefault(server, {})[category] = line.strip()
    return evidence
