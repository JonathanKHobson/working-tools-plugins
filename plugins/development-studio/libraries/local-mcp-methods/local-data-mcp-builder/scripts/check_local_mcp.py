#!/usr/bin/env python3

from __future__ import annotations

import argparse
import asyncio
import shutil
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check a local stdio MCP command end to end.")
    parser.add_argument("--command", required=True, help="Absolute command path or executable name.")
    parser.add_argument(
        "--arg",
        action="append",
        default=[],
        help="Repeat for each server argument. If an argument itself starts with '-', pass it as --arg=--flag.",
    )
    parser.add_argument("--cwd", default=None, help="Optional working directory.")
    parser.add_argument("--db-path", default=None, help="Optional DB/file path that should already exist.")
    parser.add_argument("--expect-tool", action="append", default=[], help="Repeat for tool names that must be present.")
    parser.add_argument(
        "--client",
        choices=["generic", "codex", "claude-desktop", "claude-code"],
        default="generic",
        help="Optional client context so the checker can warn about known launch-pattern issues.",
    )
    return parser.parse_args()


def resolve_command(command: str) -> str | None:
    if "/" in command:
        path = Path(command).expanduser()
        if not path.exists():
            return None
        # Preserve virtualenv launcher paths instead of resolving symlinks all the
        # way to the system interpreter, which can escape the venv site-packages.
        return str(path.absolute())
    return shutil.which(command)


def detect_launch_pattern_risks(command_path: str, args: list[str], client: str) -> list[tuple[str, str]]:
    risks: list[tuple[str, str]] = []
    command_name = Path(command_path).name.lower()
    shell_names = {"bash", "sh", "zsh"}
    first_arg = args[0] if args else ""
    first_arg_path = Path(first_arg).expanduser() if first_arg else None
    is_external_path = bool(first_arg_path and str(first_arg_path).startswith("/Volumes/"))
    is_shell_launcher = command_name in shell_names or command_path in {"/bin/bash", "/bin/sh", "/bin/zsh"}

    if is_shell_launcher and is_external_path:
        message = (
            "Shell launcher points at a script on an external drive. "
            "Claude Desktop on some macOS hosts has failed this pattern with "
            "'Operation not permitted' even when the server works from a terminal."
        )
        risks.append(("error" if client == "claude-desktop" else "warn", message))

    if client == "claude-desktop" and is_shell_launcher:
        risks.append(
            (
                "warn",
                "Claude Desktop is more reliable with a direct interpreter command "
                "(for example a home-directory Python venv) than a shell wrapper.",
            )
        )

    if client == "claude-desktop" and "/Volumes/" in command_path and command_name.startswith("python"):
        risks.append(
            (
                "warn",
                "Interpreter itself lives on an external drive. Prefer keeping the runtime in a home-directory path "
                "and only the data/index on the external SSD.",
            )
        )

    return risks


async def run_check(args: argparse.Namespace) -> int:
    command_path = resolve_command(args.command)
    if not command_path:
        print(f"[ERROR] Command not found: {args.command}")
        return 1

    if args.db_path:
        db_path = Path(args.db_path).expanduser()
        if not db_path.exists():
            print(f"[ERROR] Expected path does not exist: {db_path}")
            return 1

    risk_level = 0
    for severity, message in detect_launch_pattern_risks(command_path, args.arg, args.client):
        prefix = "[ERROR]" if severity == "error" else "[WARN]"
        print(f"{prefix} {message}")
        if severity == "error":
            risk_level = 1

    if risk_level:
        print("[ERROR] Refusing to continue until the launch command is made Claude-safe.")
        print(
            "        Prefer a direct interpreter launch such as "
            "`<internal-runtime>/venv/bin/python /path/to/server.py --root /path/to/data`."
        )
        return 1

    try:
        from mcp.client.session import ClientSession
        from mcp.client.stdio import StdioServerParameters, stdio_client
    except ImportError:
        print("[ERROR] Python package 'mcp' is not installed in this interpreter.")
        print("Run this script with the same Python environment that has the MCP client SDK installed.")
        return 1

    server = StdioServerParameters(
        command=command_path,
        args=args.arg,
        cwd=args.cwd,
    )

    try:
        async with stdio_client(server) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                tool_names = [tool.name for tool in tools.tools]
    except Exception as error:
        print(f"[ERROR] MCP client check failed: {error}")
        return 1

    missing = [tool for tool in args.expect_tool if tool not in tool_names]
    print(f"[OK] MCP responded with {len(tool_names)} tools")
    print("Tools:", ", ".join(tool_names))

    if missing:
        print(f"[ERROR] Missing expected tools: {', '.join(missing)}")
        return 1

    return 0


def main() -> None:
    args = parse_args()
    raise SystemExit(asyncio.run(run_check(args)))


if __name__ == "__main__":
    main()
