#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from claude_fleet_common import ACTIVE_CONFIG_PATH, EXPECTED_TOOLS, load_claude_config


PROBE_CODE = r"""
import asyncio
import json
import sys

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

payload = json.loads(sys.argv[1])

async def main():
    server = StdioServerParameters(
        command=payload["command"],
        args=payload.get("args", []),
        env=payload.get("env") or None,
    )
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
    print(json.dumps({"tool_names": [tool.name for tool in tools.tools]}))

asyncio.run(main())
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize every MCP in a Claude Desktop profile and confirm required tools.")
    parser.add_argument(
        "--config",
        default=str(ACTIVE_CONFIG_PATH),
        help="Claude Desktop profile JSON to smoke test.",
    )
    parser.add_argument(
        "--timeout-sec",
        type=float,
        default=25.0,
        help="Per-server initialize/list_tools timeout.",
    )
    parser.add_argument(
        "--server",
        action="append",
        default=[],
        help="Optional server name filter. Repeat as needed.",
    )
    return parser.parse_args()


def inspect_server(name: str, config: dict[str, object], timeout_sec: float) -> tuple[bool, str]:
    payload = {
        "command": str(config.get("command")),
        "args": list(config.get("args", [])),
        "env": dict(config.get("env", {})) or None,
    }
    try:
        result = subprocess.run(
            [sys.executable, "-c", PROBE_CODE, json.dumps(payload)],
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return False, f"timeout after {timeout_sec:.0f}s"

    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip() or f"probe exited {result.returncode}"
        return False, detail

    parsed = json.loads(result.stdout.strip() or "{}")
    tool_names = parsed.get("tool_names", [])
    required_tool = EXPECTED_TOOLS.get(name)
    if not tool_names:
        return False, "returned zero tools"
    if required_tool and required_tool not in tool_names:
        return False, f"missing required tool {required_tool!r}; got {tool_names}"
    preview = ", ".join(tool_names[:6])
    if len(tool_names) > 6:
        preview += ", ..."
    return True, preview


def main() -> int:
    args = parse_args()
    config_path = Path(args.config).expanduser()
    payload = load_claude_config(config_path)
    selected = {name for name in args.server} if args.server else None

    failures = 0
    for name, config in payload.get("mcpServers", {}).items():
        if selected and name not in selected:
            continue
        ok, detail = inspect_server(name, config, args.timeout_sec)
        status = "OK" if ok else "FAIL"
        print(f"[{status}] {name}: {detail}")
        if not ok:
            failures += 1

    if failures:
        print(f"[ERROR] {failures} server(s) failed the profile smoke test.")
        return 1
    print("[OK] Claude Desktop profile smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
