#!/usr/bin/env python3
"""Launch the separately installed Discord Digest MCP from local configuration."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


CONFIG_ENV = "DISCORD_CONNECTOR_CONFIG"
DEFAULT_CONFIG = "~/.config/discord-connector/config.json"
OVERRIDES = {
    "python": "DISCORD_CONNECTOR_PYTHON",
    "server_path": "DISCORD_CONNECTOR_SERVER",
    "db_path": "DISCORD_CONNECTOR_DB",
}


def resolve_path(value: str, base: Path) -> Path:
    expanded = Path(os.path.expandvars(os.path.expanduser(value)))
    return (expanded if expanded.is_absolute() else base / expanded).resolve()


def load_settings() -> tuple[Path, Path, Path]:
    config_path = Path(os.path.expandvars(os.path.expanduser(
        os.environ.get(CONFIG_ENV, DEFAULT_CONFIG)
    ))).resolve()
    config: dict[str, str] = {}
    if config_path.is_file():
        try:
            raw = json.loads(config_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ValueError(f"Cannot read Discord connector config: {exc}") from exc
        if not isinstance(raw, dict):
            raise ValueError("Discord connector config must be a JSON object")
        config = raw

    values = {key: os.environ.get(env_name) or config.get(key) for key, env_name in OVERRIDES.items()}
    missing = [key for key, value in values.items() if not isinstance(value, str) or not value.strip()]
    if missing:
        raise ValueError(
            "Missing Discord connector settings: " + ", ".join(missing)
            + f". Set them in {config_path} or the DISCORD_CONNECTOR_* environment variables."
        )
    base = config_path.parent
    return (
        resolve_path(values["python"], base),
        resolve_path(values["server_path"], base),
        resolve_path(values["db_path"], base),
    )


def main() -> int:
    try:
        python, server, database = load_settings()
        if not python.is_file():
            raise ValueError("Configured Discord connector Python executable does not exist")
        if not os.access(python, os.X_OK):
            raise ValueError("Configured Discord connector Python is not executable")
        if not server.is_file():
            raise ValueError("Configured Discord MCP server does not exist")
        if not database.is_file():
            raise ValueError("Configured Discord database does not exist")
    except ValueError as exc:
        print(f"discord plugin: {exc}", file=sys.stderr)
        return 2
    os.execv(str(python), [str(python), str(server), "--db-path", str(database)])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
