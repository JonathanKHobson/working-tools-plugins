#!/usr/bin/env python3
"""Bounded launcher for the first-party Data Explorer MCP server.

This script never installs dependencies, repairs configuration, or creates
files/directories at startup. It resolves an interpreter and a data
directory from (in strict precedence order) environment variables, an
optional private binding file, and finally built-in bundled defaults, then
execs the bundled server with the resolved values.

Legacy private installations may still have a ``server`` field recorded in
their binding file; it is read but intentionally never executed. We always
exec the bundled ``runtime/data-explorer/server.py`` that ships alongside
this launcher.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Mapping, MutableMapping, Optional

ROOT = Path(__file__).resolve().parents[1]


class LaunchError(RuntimeError):
    """Raised when a launch configuration cannot be resolved safely."""


def _expand_home(value: str, home: Path) -> str:
    """Expand a leading ``~`` using the *injected* home, never the real HOME."""
    if value == "~":
        return str(home)
    if value.startswith("~/"):
        return str(home / value[2:])
    return value


def _validate_absolute_path(value: object, home: Path, label: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise LaunchError(f"{label} must be a nonempty string path")
    expanded = _expand_home(value, home)
    path = Path(expanded)
    if not path.is_absolute():
        raise LaunchError(
            f"{label} must be an absolute path after expanding '~'; got relative path {value!r}"
        )
    return path


def _verify_interpreter(path: Path, label: str) -> None:
    if not path.is_file():
        raise LaunchError(f"{label} does not exist or is not a regular file: {path}")
    if not os.access(path, os.X_OK):
        raise LaunchError(f"{label} is not executable: {path}")


def _load_config(home: Path, env: Mapping[str, str]) -> Optional[dict]:
    explicit = "DATA_EXPLORER_BINDING" in env
    config_path = (_validate_absolute_path(env["DATA_EXPLORER_BINDING"], home, "DATA_EXPLORER_BINDING")
                   if explicit else home / ".config/studio-tools/data-explorer.json")
    if not config_path.is_file():
        if explicit:
            raise LaunchError("The explicitly selected Data Explorer binding does not exist")
        return None
    try:
        data = json.loads(config_path.read_text())
    except (OSError, ValueError) as exc:
        raise LaunchError("Data Explorer binding must be readable JSON") from exc
    if not isinstance(data, dict):
        raise LaunchError("Data Explorer binding must contain a JSON object")
    return data


def _resolve_interpreter(root: Path, env: Mapping[str, str], home: Path, binding: Optional[dict]) -> Path:
    override = env.get("DATA_EXPLORER_PYTHON")
    if "DATA_EXPLORER_PYTHON" in env:
        path = _validate_absolute_path(override, home, "DATA_EXPLORER_PYTHON")
        _verify_interpreter(path, "DATA_EXPLORER_PYTHON")
        return path

    if binding is not None and "interpreter" in binding:
        path = _validate_absolute_path(binding["interpreter"], home, "binding 'interpreter'")
        _verify_interpreter(path, "binding interpreter")
        return path

    relative = ("Scripts", "python.exe") if os.name == "nt" else ("bin", "python")
    bundled = root / ".runtime" / "venv" / relative[0] / relative[1]
    _verify_interpreter(bundled, "bundled venv interpreter")
    return bundled


def _resolve_data_dir(env: Mapping[str, str], home: Path, binding: Optional[dict]) -> Path:
    override = env.get("DATA_EXPLORER_DATA_DIR")
    if "DATA_EXPLORER_DATA_DIR" in env:
        return _validate_absolute_path(override, home, "DATA_EXPLORER_DATA_DIR")

    if binding is not None and "data_dir" in binding:
        return _validate_absolute_path(binding["data_dir"], home, "binding 'data_dir'")

    xdg_data_home = env.get("XDG_DATA_HOME")
    if xdg_data_home:
        return _validate_absolute_path(xdg_data_home, home, "XDG_DATA_HOME") / "working-tools" / "data-explorer"
    return home / ".local" / "share" / "working-tools" / "data-explorer"


def _resolve_server(root: Path) -> Path:
    server = root / "runtime" / "data-explorer" / "server.py"
    if not server.is_file():
        raise LaunchError(f"bundled server script is missing: {server}")
    return server


def launch_spec(
    root: Path = ROOT,
    env: Optional[Mapping[str, str]] = None,
    home: Optional[Path] = None,
):
    """Resolve the interpreter, argv, and child environment for the server.

    Never mutates the global environment; ``env``/``home`` may be injected
    for testing and otherwise default to ``os.environ``/``Path.home()``.
    """
    source_env: Mapping[str, str] = env if env is not None else os.environ
    resolved_home: Path = Path(home) if home is not None else Path.home()

    # A complete environment override does not depend on the default binding.
    # An explicitly selected binding is still validated to catch setup mistakes.
    needs_binding = not all(key in source_env for key in (
        "DATA_EXPLORER_PYTHON", "DATA_EXPLORER_DATA_DIR"))
    binding = (_load_config(resolved_home, source_env)
               if needs_binding or "DATA_EXPLORER_BINDING" in source_env else None)

    interpreter = _resolve_interpreter(root, source_env, resolved_home, binding)
    data_dir = _resolve_data_dir(source_env, resolved_home, binding)
    server = _resolve_server(root)

    argv = [str(interpreter), str(server), "--data-dir", str(data_dir), "--stdio"]

    child_env: MutableMapping[str, str] = dict(source_env)
    child_env["PYTHONDONTWRITEBYTECODE"] = "1"

    return str(interpreter), argv, child_env


def main() -> None:
    if len(sys.argv) > 1:
        print(
            "data_explorer_mcp.py accepts no command-line arguments; "
            "configure via DATA_EXPLORER_PYTHON, DATA_EXPLORER_DATA_DIR, "
            "DATA_EXPLORER_BINDING, or ~/.config/studio-tools/data-explorer.json instead",
            file=sys.stderr,
        )
        raise SystemExit(1)

    try:
        interpreter, argv, child_env = launch_spec()
        os.execve(interpreter, argv, child_env)
    except (LaunchError, OSError) as exc:
        print(f"data_explorer_mcp.py: cannot start Data Explorer server: {exc}", file=sys.stderr)
        raise SystemExit(1)



if __name__ == "__main__":
    main()
