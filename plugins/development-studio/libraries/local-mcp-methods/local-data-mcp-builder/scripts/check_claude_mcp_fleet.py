#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from claude_fleet_common import (
    ACTIVE_CONFIG_PATH,
    DAILY_PROFILE,
    MCP_LOG_PATH,
    QUARANTINED_SERVERS,
    canonical_name,
    classify_risk,
    command_type,
    compare_codex_launcher,
    infer_profile_name,
    load_claude_config,
    load_log_evidence,
    load_profile_memberships,
    render_command,
    resolve_command,
    runtime_location,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the active Claude Desktop MCP fleet for launch-risk issues.")
    parser.add_argument(
        "--config",
        default=str(ACTIVE_CONFIG_PATH),
        help="Claude Desktop config JSON to validate.",
    )
    parser.add_argument(
        "--mcp-log",
        default=str(MCP_LOG_PATH),
        help="Claude Desktop mcp.log path for recent timeout/parse evidence.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = Path(args.config).expanduser()
    log_path = Path(args.mcp_log).expanduser()
    payload = load_claude_config(config_path)
    active_servers = payload.get("mcpServers", {})
    profile_name = infer_profile_name({canonical_name(name) for name in active_servers})
    memberships = load_profile_memberships()
    evidence = load_log_evidence(log_path)

    errors: list[str] = []
    warnings: list[str] = []

    if config_path == ACTIVE_CONFIG_PATH and profile_name != DAILY_PROFILE:
        warnings.append(
            f"Active Claude config is '{profile_name}', not the default '{DAILY_PROFILE}'. "
            "This is valid for focused work, but it is not the standard daily testing profile."
        )

    if len(active_servers) > 10:
        warnings.append(
            f"Active config contains {len(active_servers)} servers. Fleet-wide boot is an anti-pattern on some macOS hosts."
        )

    print(f"[INFO] Config: {config_path}")
    print(f"[INFO] Active profile: {profile_name}")
    print(f"[INFO] Server count: {len(active_servers)}")

    for server_name in sorted(active_servers):
        config = active_servers[server_name]
        canonical = canonical_name(server_name)
        command = config.get("command")
        command_path = resolve_command(command)
        args_list = config.get("args", [])
        risk_class = classify_risk(canonical, memberships.get(canonical, []))

        print()
        print(f"[SERVER] {server_name}")
        print(f"  launcher: {render_command(command, args_list)}")
        print(f"  risk: {risk_class}")
        print(f"  runtime: {runtime_location(command_path)}")

        if command_path is None:
            errors.append(f"{server_name}: command not found: {command}")

        if command_type(command or "") == "shell" and any(arg.startswith("/Volumes/") for arg in args_list):
            errors.append(
                f"{server_name}: shell wrapper points at an external-drive script. Claude Desktop rejects this pattern."
            )

        if command_path and command_type(command or "") == "python" and command_path.startswith("/Volumes/"):
            warnings.append(
                f"{server_name}: Python interpreter lives on an external drive. Prefer a home-directory runtime."
            )

        if canonical in QUARANTINED_SERVERS and config_path == ACTIVE_CONFIG_PATH:
            errors.append(f"{server_name}: quarantined server is still present in the active Claude profile.")

        drift_note = compare_codex_launcher(canonical, config)
        if drift_note:
            warnings.append(f"{server_name}: {drift_note}")

        server_evidence = evidence.get(canonical, {})
        if "invalid_json" in server_evidence:
            errors.append(f"{server_name}: recent invalid JSON evidence in mcp.log")
        if "parse_error" in server_evidence:
            errors.append(f"{server_name}: recent parse error evidence in mcp.log")
        if "timeout" in server_evidence:
            warnings.append(f"{server_name}: recent initialize timeout evidence in mcp.log")
        if "operation_not_permitted" in server_evidence:
            errors.append(f"{server_name}: recent permission failure evidence in mcp.log")

    print()
    if warnings:
        print("[WARN] Findings")
        for item in warnings:
            print(f"  - {item}")

    if errors:
        print("[ERROR] Blocking findings")
        for item in errors:
            print(f"  - {item}")
        return 1

    print("[OK] Claude Desktop MCP fleet passed the current hardening checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
