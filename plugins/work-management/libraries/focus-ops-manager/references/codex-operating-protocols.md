# Codex Operating Protocols

Use only the section that matches the current situation. These are lightweight
guardrails, not a new planning system.

## Focus Start

Use when the work is vague, scattered, overwhelming, or just beginning.

1. Pick one deliverable that can move today.
2. Write it in one sentence.
3. Name the next visible action, not the whole plan.
4. Ask what this displaces right now.
5. Open only the files, tools, or sources needed for that action.
6. Make the first useful pass before improving the system around it.
7. Capture the result in one line and ship at 80% if it is useful.

## System Pressure Guard

Use when the user reports freezing, Finder/Chrome/Codex slowness, hard resets,
power failure recovery, missing Codex project folders, memory pressure, or when
starting a broad/resource-heavy lane.

1. Run
   `python3 ~/.codex/scripts/codex_pressure_guard.py check --json`.
2. Treat `warn` and `critical` as advisory only. Never refuse, pause, delay, or
   abandon requested work solely because of memory or process pressure. Name
   the source briefly when useful, then continue the requested lane.
3. Prefer the centralized guard for cleanup:
   `python3 ~/.codex/scripts/codex_pressure_guard.py cleanup-stale`.
   It may close confirmed Codex-owned stale duplicates, but the task continues
   even when nothing is eligible. Do not hand-kill generic Node/Python processes
   unless ownership is clear.
4. Check the four recurring overload vectors: Codex duplicate helpers,
   Spotlight/`mds*`, network mounts, and background app clutter.
5. Keep `$PROJECT_VOLUME`, `$RUNTIME_VOLUME`, and
   `$PROJECT_VOLUME III` guarded with `.metadata_never_index` and
   `mdutil -i off`.
6. Keep Codex on the automation-safe MCP baseline unless the user explicitly asks
   to keep a temporary MCP enabled.
7. Do not disable Malwarebytes, GhostPepper, KSB, or Claude-owned KSB
   processes from generic cleanup.
8. Throttle identical prompt-time warnings to at most once per hour unless the
   pressure category changes or new safe cleanup targets appear.

## Codex Desktop Launch and Window Recovery

Use when Codex Desktop has blank conversations, appears to open and immediately
close, stays active without a visible window, or stops restoring its task list.

1. Define success before repair: the app remains running, its main window is
   visible, the task list populates, and one existing conversation renders.
2. Distinguish a real process exit from an invisible window. After one launch,
   check whether the menu bar still says `ChatGPT` and whether the process
   persists for at least ten seconds. If it does, inspect the `Window` menu.
   An enabled generic window menu means a window exists even if none is visible.
3. Recover an off-screen window with `Window -> Zoom`. In the verified July 24,
   2026 incident, `Center` and `Bring All to Front` did not reveal the window,
   while `Zoom` restored it immediately.
4. Do not repeat launches without a new hypothesis. Reproduce once per layer:
   process lifecycle, app-only state, reboot, and window placement.
5. Preserve history before changing state. Do not delete
   `~/.codex/sessions/`, `~/.codex/state_5.sqlite`, or its WAL/SHM files.
   Copy the database with WAL/SHM to a local path and run
   `PRAGMA quick_check`; verify thread counts, titles, and recent rows.
6. Treat `~/.codex/process_manager/chat_processes.json` as resumable process
   state, not conversation history. If it contains dead PIDs or stale commands,
   make a timestamped backup and replace only that registry with `[]`.
7. If the app still exits, back up and reset only app UI/session state:
   `~/Library/Application Support/com.openai.codex`,
   `~/Library/Caches/com.openai.codex`, and
   `~/Library/Preferences/com.openai.codex.plist`. Then perform a normal reboot
   before another launch.
8. Verify the app bundle and host before reinstalling: check code signing,
   macOS build, and executable architecture. A valid current Intel `x86_64`
   build on an Intel Mac is not an architecture mismatch.
9. Interpret the July 24 incident as a compound stale process/UI restore-state
   failure. Evidence: the thread database passed integrity checks with 170
   indexed conversations; stale process records were present; clearing
   process/UI state plus reboot stopped the immediate exit; the surviving
   window then had to be recovered from off-screen with `Window -> Zoom`.
   No macOS ChatGPT crash report existed, so do not claim a more precise
   internal abort mechanism without new logs.
10. Prefer Screen Sharing and small targeted reads over recursive SMB scans.
    SMB can stall on many small files. If Screen Sharing keyboard automation
    maps `_` to `-`, `|` to `\`, or modifiers to literal letters, use simple
    commands, separate typing from Return, and visually verify the command
    before executing it.
11. Before signoff, confirm the changed visual anchors: visible main window,
    populated task list, and rendered prior conversation. Disconnect Screen
    Sharing and leave the repaired Codex window open for the user.

## External Pattern Harvest

Use when a public repo, GitHub topic, skill marketplace, MCP example, agent
rulebook, or external workflow looks useful for Jonathan's local skills or
MCPs.

1. Default harvest is inspect-only. Do not install, run scripts, enable MCPs,
   wire configs, or copy executable code during the first pattern pass.
   Downloading/extracting source archives into a workspace cache for read-only
   review is allowed when the user explicitly asks for a thorough pass; executing
   anything from those archives is not.
2. Inventory the local target first: existing skill, MCP, protocol, or backlog
   file. Prefer improving an existing surface over creating a new one.
3. For a shallow pass, extract 5-8 reusable patterns as pattern cards with
   source, reusable pattern, local target, effort, impact, risk, first-pass
   action, and validation.
4. For a deep pass, inspect actual repo manifests, `SKILL.md` files, READMEs,
   command/mode docs, workflows, scripts, package manifests, MCP configs,
   examples, and tests. Compare them against all first-party local skills plus
   the relevant MCP workflow docs, not only the obvious target.
5. Prioritize low-effort, high-impact language and workflow tightening before
   new eval harnesses, validators, or MCP code.
   If the target is skill quality, trigger quality, or safety boundaries, use
   `skill-review-mini-rubric.md` before editing.
6. Patch at most one local artifact in a first pass unless the user asks for
   broader implementation. When Kyle explicitly asks for implementation, patch
   every owning surface needed to close the gap, including MCP workflow docs.
7. Create a new local skill only when the gap has no clear owner after checking
   existing skills, MCP docs, and backlog entries. Prefer a local wrapper skill
   over installing an external runtime when the external repo needs browser
   sessions, API keys, scrapers, or command execution.
8. Route any future copying, installing, executing, or MCP wiring through
   `personal-security-check` before touching the external artifact.
9. Verify with local discovery commands and record the result in
   `skill-mcp-improvement-backlog.md`. Capture durable memory only if the
   decision changes future work.

## Phase Handoff

Use when a workflow spans rounds, stages, or several skills and the next phase
must inherit context without restarting the whole system.

- Phase:
- Decision:
- Artifact(s):
- Verification:
- Next phase:
- Stop condition:
- What not to touch:

Keep handoffs short enough to fit in a status update. They should preserve the
decision, the proof, and the next lane without turning the handoff into a new
planning artifact.

## MCP Use Check

Use when enabling or relying on a Codex MCP for a task.

1. Confirm the MCP is needed for this task. The automation-safe baseline is
   exempt from temporary-use cleanup: `arxiv-scout`, `critical-compass`,
   `discord_digest`, `knowledge_atlas`, `shareables`, and
   `kyle_second_brain`.
2. Enable only the MCPs required for the current work.
3. Use the narrowest tool that answers the question.
4. Keep MCP output tied to the deliverable, not exploratory sprawl.
5. Before signoff, disable MCPs enabled for the task unless the user explicitly asks
   to leave them on. Never disable the automation-safe baseline as routine
   cleanup.
6. Report what was enabled, what evidence it provided, and whether it was
   disabled again.

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

## Browser Handoff

Use when browser automation, Playwright, Chrome control, or browser MCPs were
used.

1. Close automation-owned browser windows, tabs, sessions, and parent daemons.
2. Check for automation-only args such as `--headless`, temp `--user-data-dir`,
   remote debugging ports, or `ms-playwright` profile paths.
3. Verify either no automation Chrome session remains or normal Chrome is
   relaunched as the real app with a visible window.
4. Treat browser handoff as part of the task, not a courtesy after the task.

## Ship Log

Use when closing a deliverable, decision, cleanup, or meaningful work loop.

- Outcome:
- Evidence:
- Next action:
- What not to touch yet:

Keep it short. Record the result, the proof, the next concrete step, and the
lane to leave alone for now.
