#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print Codex, Claude Desktop, and project MCP config snippets.")
    parser.add_argument("--server-name", required=True, help="Server key/name.")
    parser.add_argument("--command", required=True, help="Absolute command path.")
    parser.add_argument(
        "--arg",
        action="append",
        default=[],
        help="Repeat for each argument. If an argument starts with '-', pass it as --arg=--flag.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("### Codex (`~/.codex/config.toml`)\n")
    print(f"[mcp_servers.{args.server_name}]")
    print(f'command = "{args.command}"')
    if args.arg:
        rendered_args = ", ".join(json.dumps(value) for value in args.arg)
        print(f"args = [{rendered_args}]")
    print()

    payload = {
        "mcpServers": {
            args.server_name: {
                "command": args.command,
                "args": args.arg,
            }
        }
    }

    print("### Claude Desktop (`claude_desktop_config.json`)\n")
    print(json.dumps(payload, indent=2))
    print()
    print("### Claude Code / project (`.mcp.json`)\n")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
