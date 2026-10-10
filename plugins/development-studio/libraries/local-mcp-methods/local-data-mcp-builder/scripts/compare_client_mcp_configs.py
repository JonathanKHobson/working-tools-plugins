#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare MCP server names across Codex, Claude Desktop, and optional project configs."
    )
    parser.add_argument(
        "--codex-config",
        default="~/.codex/config.toml",
        help="Path to Codex config.toml",
    )
    parser.add_argument(
        "--claude-config",
        default="~/Library/Application Support/Claude/claude_desktop_config.json",
        help="Path to Claude Desktop config JSON",
    )
    parser.add_argument(
        "--project-config",
        action="append",
        default=[],
        help="Repeat for project .mcp.json files to compare.",
    )
    parser.add_argument(
        "--expect-server",
        action="append",
        default=[],
        help="Optional logical server name to focus on. Hyphens and underscores are treated as equivalent.",
    )
    return parser.parse_args()


def canonical_name(name: str) -> str:
    return name.replace("-", "_")


def load_codex_servers(path: Path) -> set[str]:
    if not path.exists():
        return set()
    servers: set[str] = set()
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith("[mcp_servers.") and line.endswith("]"):
            servers.add(canonical_name(line[len("[mcp_servers.") : -1].strip('"')))
    return servers


def load_json_servers(path: Path) -> set[str]:
    if not path.exists():
        return set()
    payload = json.loads(path.read_text())
    return {canonical_name(name) for name in payload.get("mcpServers", {}).keys()}


def print_group(name: str, servers: set[str]) -> None:
    rendered = ", ".join(sorted(servers)) if servers else "(none)"
    print(f"{name}: {rendered}")


def main() -> int:
    args = parse_args()

    codex_path = Path(args.codex_config).expanduser()
    claude_path = Path(args.claude_config).expanduser()
    project_paths = [Path(value).expanduser() for value in args.project_config]

    groups: list[tuple[str, set[str]]] = [
        ("Codex", load_codex_servers(codex_path)),
        ("Claude Desktop", load_json_servers(claude_path)),
    ]
    groups.extend((str(path), load_json_servers(path)) for path in project_paths)
    expected = {canonical_name(name) for name in args.expect_server}

    for name, servers in groups:
        print_group(name, servers)

    union = set().union(*(servers for _, servers in groups))
    if expected:
        union &= expected
    if not union:
        print("[WARN] No MCP servers found in the supplied configs.")
        return 1

    drift = False
    for server in sorted(union):
        missing = [name for name, servers in groups if server not in servers]
        if missing:
            drift = True
            print(f"[DRIFT] {server} missing from: {', '.join(missing)}")

    if drift:
        return 1

    print("[OK] All compared config files contain the same MCP server names.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
