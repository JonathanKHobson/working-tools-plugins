## Daily Cleanup KSB Guard

Use when auditing or editing Daily Safe Codex Housekeeping, Codex cleanup,
duplicate-process cleanup, or daily maintenance automations.

1. Run `python3 ~/.codex/scripts/codex_ksb_mode.py status` and treat it as the
   source of truth for KSB's Codex config and process state.
2. KSB is the permanent Codex baseline, and Codex should normally preserve the
   broader automation-safe MCP set. If the helper says KSB is missing from Codex
   config, that is an action-required state, not healthy.
3. Cleanup automations may run `codex_ksb_mode.py enable` as a narrow self-heal
   if KSB is missing from config, then report that Codex must be restarted
   before exposure can be claimed. For pressure-prevention maintenance, they may
   also run `codex_mcp_manage.py baseline` after a timestamped config backup to
   remove nonbaseline MCP drift while preserving the automation-safe baseline.
   They must not run `codex_ksb_mode.py disable`, broad direct config edits, or
   MCP profile rewrites.
4. Cleanup automations must never terminate a process whose command includes
   `/kyle-second-brain/mcp_server.py`, `Kyle Second Brain/app/mcp_server.py`,
   `kyle_second_brain`, or `KSB_`, and must never terminate Claude-owned KSB.
5. If a stale Codex-owned KSB child appears, report it as a KSB-specific
   follow-up instead of handling it through generic duplicate-process cleanup.
