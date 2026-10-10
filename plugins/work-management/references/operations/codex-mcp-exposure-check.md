## Codex MCP Exposure Check

Use when a configured Codex MCP launches locally but its tools do not appear in
the current Codex session.

1. Separate the layers: direct MCP health, Codex process lifecycle, and
   deferred-tool visibility.
2. For Kyle Second Brain specifically, first run
   `python3 ~/.codex/scripts/codex_ksb_mode.py status`. If KSB is disabled in
   Codex config, repair config with `python3 ~/.codex/scripts/codex_ksb_mode.py
   enable`, fully restart Codex, then verify `tool_search`.
3. Run `python3 ~/.codex/scripts/codex_ksb_mode.py expose-all-chats` to enforce
   nonfatal permanent KSB enablement, the codex-core allowlist, the
   project-config shadow check, the direct smoke, and any available app-server
   MCP reload. This produces
   `~/.codex/state/ksb-exposure.json`.
   From a `SessionStart` hook, use the lightweight form instead:
   `expose-all-chats --skip-reload --skip-direct-smoke --quiet`. SessionStart
   must prepare config state only; it cannot prove native tool visibility and
   should not launch a competing KSB stdio smoke during chat birth.
4. Run a direct stdio smoke test first; confirm initialize and `tools/list`
   return the expected compact tool set.
5. For KSB-specific exposure failures, run
   `python3 ~/.codex/scripts/codex_ksb_mode.py lock-diagnostic`. The expected
   fixed state is `codex_global_lock_nonfatal`, where both the exact
   `codex-global` profile and a unique Codex profile list the exact 12
   codex-core tools. If the exact profile fails but the unique profile passes,
   the KSB server-instance runtime lock is blocking duplicate Codex initialize;
   repair advisory/nonfatal Codex runtime locking and preserve writer locks.
6. Check live Codex app-server and MCP child process start times; a child that
   predates the fix is stale evidence.
7. Verify the Codex profile is intentionally compact, allowlisted, and
   nonfatal. For Kyle Second Brain, Codex uses `KSB_TOOL_PROFILE=codex-core`,
   `required = false`, and the exact 12-tool codex-core allowlist. Do not use
   `required = true` for KSB in Codex Desktop because a host-side handshake
   glitch can then brick chat resume.
8. Fully quit and reopen Codex after config, server-code, hook, or tool-profile
   changes.
9. Only call the MCP exposed when `tool_search` finds the expected routine
   tools in the current session. Use the exact query
   `kyle_second_brain memory_context_pack memory_search
   memory_capture_working_note stats` so the deferred-tool search includes the
   MCP namespace and the routine tool names.
10. During the KSB canary period, `kyle_second_brain_canary` may be enabled
   with only `stats`, `memory_context_pack`, and `memory_search`. It is a
   diagnostic comparison MCP, not a replacement for the real
   `kyle_second_brain` namespace. Remove it only after several clean
   restart/new-chat cycles.
11. If Claude can use KSB and direct Codex smoke passes, do not rebuild KSB,
   rebuild indexes, or rewrite the server to fix Codex exposure. Keep KSB
   enabled, fully restart Codex after config/profile/code changes, and continue
   debugging Codex deferred-tool exposure if `tool_search` still cannot see the
   routine tools.
12. Known public host-bug shape: Codex Desktop can show MCP servers in Settings
   or `codex mcp list` while a Desktop chat still cannot use them. This matches
   OpenAI Codex issue #10499. If local config, direct smoke, and CLI inventory
   are healthy, treat the remaining failure as Desktop deferred-tool exposure,
   not KSB server health.
13. If an already-open Codex conversation remains stale but the work needs KSB
   recall or capture immediately, use the direct stdio fallback instead of
   hand-rolling a one-off MCP client:
   `~/.codex/scripts/ksb_direct_tool.py`. This is a fallback for stale session
   exposure only; it does not replace native KSB MCP tools when `tool_search`
   exposes them.
