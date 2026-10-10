> Historical source evidence with receiving-host-neutral locators. Listed configuration, availability, old observations and changes are not current facts or instructions for the recipient. Inspect actual callable capabilities and preserve active jobs before acting. No private config or corpus is supplied.

# Codex MCP Idle Memory Investigation Report

## Summary

Codex was intermittently consuming extreme amounts of memory while apparently idle, with spikes reported around 40 GB to 48 GB. The pattern was not normal user activity. It looked like a Codex startup and lifecycle cleanup problem, likely amplified by a large MCP stack and by the app keeping helper processes alive longer than it should.

## What We Observed

- Live Codex process tree included:
  - main Codex app process
  - renderer
  - GPU helper
  - app-server
  - multiple MCP child processes
- The active Codex config originally loaded a large MCP set at startup.
- Local Codex state was non-trivial:
  - `~/.codex/state_5.sqlite` was large
  - `~/.codex/logs_1.sqlite` was large
  - the state database contained many threads and log rows
- Memory spikes happened even when the app appeared idle.

## Likely Bug Class

- Startup hydration too heavy for the installed MCP stack
- Process cleanup / orphaned helper leak
- App-server or renderer retaining MCP-related state longer than expected

## What We Changed

- Restored the active Codex config to an MCP-free baseline by default.
- Kept `multi_agent = true` in the active config.
- Preserved the original MCP-heavy config in a backup file.
- Added verbatim per-server MCP snippets in `~/.codex/mcp-profiles/`.
- Added a canonical MCP registry and a Codex-only enable/disable test plan.
- Added a Codex-side helper script:
  - `~/.codex/scripts/codex_mcp_manage.py`
- Added a log template:
  - `~/.codex/mcp-test-log.md`
- Added an explicit rule that Codex MCPs should be disabled again after use unless the user explicitly asks to leave one on.
- Did not edit Claude Desktop config.

## Current Operating Model

1. Start from the MCP-free Codex baseline.
2. Enable exactly one MCP at a time.
3. Restart Codex.
4. Run one smoke action.
5. Disable the MCP again.
6. Restart Codex.
7. Confirm the process tree returns to baseline and idle memory stays flat.

## Key Files

- [MCP registry](mcp-registry.md)
- [Codex-only test plan](mcp-test-plan.md)
- MCP helper script (historical receiving-host locator `~/.codex/scripts/codex_mcp_manage.py`; external input, not bundled)
- Active Codex config (historical receiving-host locator `~/.codex/config.toml`; external input, not bundled)
- Preserved MCP backup (historical receiving-host locator `~/.codex/config.mcp-disabled.backup.toml`; external input, not bundled)

## Verification

- Enabled `playwright` via the helper script.
- Confirmed it was the only active MCP.
- Restored the MCP-free baseline.
- Validated the active config back to `0 MCP server blocks`.

## Why This Matters

- This gives future MCP work a safer default.
- It keeps Codex from paying the startup cost of every server all the time.
- It creates a repeatable way to isolate a single problematic MCP if memory or cleanup regressions return.

