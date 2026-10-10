#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from claude_fleet_common import (
    ACTIVE_CONFIG_PATH,
    DAILY_PROFILE,
    EXPECTED_TOOLS,
    FLEET_REPORT_PATH,
    PROFILE_FILES,
    QUARANTINED_SERVERS,
    classify_risk,
    command_type,
    infer_profile_name,
    load_claude_config,
    load_log_evidence,
    load_profile_memberships,
    resolve_command,
    runtime_location,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the human-readable Claude Desktop MCP fleet report.")
    parser.add_argument(
        "--active-config",
        default=str(ACTIVE_CONFIG_PATH),
        help="Active Claude Desktop config JSON.",
    )
    parser.add_argument(
        "--output",
        default=str(FLEET_REPORT_PATH),
        help="Markdown path to write.",
    )
    return parser.parse_args()


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def render_log_signal(server: str, evidence: dict[str, dict[str, str]]) -> str:
    server_evidence = evidence.get(server, {})
    if not server_evidence:
        return "none"
    return ", ".join(sorted(server_evidence.keys()))


def main() -> int:
    args = parse_args()
    active_path = Path(args.active_config).expanduser()
    output_path = Path(args.output).expanduser()
    active_payload = load_claude_config(active_path)
    active_profile = infer_profile_name(set(active_payload.get("mcpServers", {})))
    memberships = load_profile_memberships()
    evidence = load_log_evidence()

    profile_rows: list[list[str]] = []
    for profile_name, path in PROFILE_FILES.items():
        if not path.exists():
            continue
        payload = load_claude_config(path)
        server_count = len(payload.get("mcpServers", {}))
        is_default = "yes" if profile_name == DAILY_PROFILE else "no"
        profile_rows.append([profile_name, str(server_count), is_default, str(path)])

    inventory_rows: list[list[str]] = []
    all_servers = sorted(memberships)
    for server in all_servers:
        server_config = None
        for profile_name, path in PROFILE_FILES.items():
            if not path.exists():
                continue
            payload = load_claude_config(path)
            if server in payload.get("mcpServers", {}):
                server_config = payload["mcpServers"][server]
                break
        command = server_config.get("command") if server_config else None
        command_path = resolve_command(command)
        inventory_rows.append(
            [
                server,
                ", ".join(memberships.get(server, [])) or "unassigned",
                classify_risk(server, memberships.get(server, [])),
                runtime_location(command_path),
                command_type(command),
                "yes" if server not in QUARANTINED_SERVERS and DAILY_PROFILE in memberships.get(server, []) else "no",
                EXPECTED_TOOLS.get(server, "n/a"),
                render_log_signal(server, evidence),
            ]
        )

    active_rows: list[list[str]] = []
    for server, config in sorted(active_payload.get("mcpServers", {}).items()):
        command = config.get("command")
        command_path = resolve_command(command)
        active_rows.append(
            [
                server,
                command_type(command),
                runtime_location(command_path),
                EXPECTED_TOOLS.get(server, "n/a"),
                render_log_signal(server, evidence),
            ]
        )

    report = f"""# Claude MCP Fleet Report

Generated: {datetime.now().astimezone().isoformat(timespec="seconds")}

## Active Profile

- Active config: `{active_path}`
- Active profile: `{active_profile}`
- Active server count: `{len(active_payload.get("mcpServers", {}))}`
- Daily default profile: `{DAILY_PROFILE}`

## Available Claude Profiles

{markdown_table(["Profile", "Servers", "Daily default", "Path"], profile_rows)}

## Active Profile Detail

{markdown_table(["Server", "Command type", "Runtime location", "Required tool", "Recent log signal"], active_rows)}

## Quarantined Or Known-Risk Servers

- Quarantined by policy: {", ".join(sorted(QUARANTINED_SERVERS)) or "none"}
- Risk evidence comes from `~/Library/Logs/Claude/mcp.log`.
- Any `invalid_json` or `parse_error` signal should block a server from the default daily profile.

## Fleet Inventory

{markdown_table(["Server", "Profile membership", "Risk class", "Runtime location", "Command type", "Safe for daily", "Required tool", "Recent log signal"], inventory_rows)}
"""

    output_path.write_text(report)
    print(f"[OK] Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
