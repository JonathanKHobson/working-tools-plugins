---
name: local-mcp-debugging
description: Diagnose and fix local MCP startup failures in Codex, Claude Desktop, or Claude Code/Cowork plugins, especially when servers live on external drives, launch via shell wrappers, or fail to attach with messages like "Could not attach to MCP server" or "Operation not permitted". Use when debugging plugin `.mcp.json`, mcpServers config, Claude logs, Codex config, Python launcher issues, external-drive sidecar files, local MCP transport startup problems, "tool result could not be submitted", or cases where Claude attaches but chooses the wrong MCP tool/lane, ignores routing rules, asks prose questions instead of using a widget contract, defaults to the wrong source, leaks placeholders/debug strings, or submits oversized/malformed tool results.
---

# Local MCP Debugging

Use this when a local MCP server is configured but the client cannot attach. Also use it when the MCP attaches successfully but Claude repeatedly chooses the wrong tool, ignores the intended lane, submits oversized results, or loses the operational routing rules in a long conversation.

## Quick workflow

1. Read the active config first.
   - Claude Code/Cowork plugin: `<plugin-root>/.mcp.json`
   - Codex: `~/.codex/config.toml`
   - Claude Desktop: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - If you are adding a server, merge into the existing `mcpServers` map instead of replacing the whole file.
   - Treat a wholesale config replacement as exceptional and only do it when the user explicitly asks for it.
   - If many Claude MCPs are failing together, inspect the named Claude profile files before doing single-server surgery:
     - `claude_desktop_config.minimal-profile.json`
     - `claude_desktop_config.task-profile-a.json`
     - `claude_desktop_config.task-profile-b.json`
     - `claude_desktop_config.quarantine-profile.json`
     - `claude_desktop_config.full-fleet.json`
2. Read the server log before guessing.
   - Claude: `~/Library/Logs/Claude/mcp-server-<server-name>.log`
   - Shared-failure lane: `~/Library/Logs/Claude/mcp.log`
3. Reproduce the exact configured command outside the client.
4. Fix the launch path before touching MCP protocol code.
5. If Claude Desktop depends on external-drive MCP runtimes, keep Claude out of
   Login Items and launch it manually after `<external-ssd>` and
   `<external-ssd>` are mounted.

## First Split: Launch Failure Or Agent-Control Failure

Before changing code, classify the failure.

- Launch failure: process exits, client cannot attach, `initialize` never appears, config path is wrong, runtime import fails, sidecars break startup, or logs show transport errors.
- Client/result failure: server initializes and tools list, but a call returns an oversized, malformed, late, or unsubmitted result.
- Agent-control failure: server initializes and calls work, but Claude chooses the wrong tool, ignores a widget/elicitation contract, asks prose questions, leaks placeholders, or uses the wrong source lane.
- Retrieval quality failure: server initializes and returns results, but search/context packs are stale, irrelevant, over-budget, duplicate-heavy, missing expected records, or semantically different from the current SQLite/JSONL source state.

Use launch evidence for launch failures. Use route-level fixtures, schema validators, result-size checks, and tool descriptions for agent-control failures. Use index manifests, retrieval traces, eval fixtures, and SQLite/Chroma count checks for retrieval quality failures. Do not rewrite a working launcher because Claude picked the wrong lane or returned poor search results.

## Coordination and MCP Awareness

- Start with this skill when an MCP is configured but the client cannot attach, initialize, or keep the process alive.
- Use `../local-data-mcp-builder/SKILL.md` when the problem turns out to be server architecture, index design, tool surface, routing contract, or client config shape rather than startup failure.
- Use `../local-data-mcp-builder/references/context-engineering-mcp-reliability.md` when the MCP starts but Claude picks the wrong tool, defaults to the wrong source lane, leaks adapter names, or needs stronger output contracts.
- Use master-security-toolkit:agent-artifact-scanning when the package, plugin, installer, repo, or `.mcp.json` is unfamiliar and needs a safety review before running, granting permissions, or wiring into Claude/Codex.
- Use the owning local-storage MCP project when the failing server is the storage MCP or when a task needs its expected tool surface and evidence model as the baseline.
- Use mac-ops-toolkit:mac-environment-conventions when runtime placement, external-drive execution, or storage location is likely part of the root cause.
- Use mac-ops-toolkit:storage-memory-manager when low disk space, broken caches, or external-drive artifacts are involved.
- Use the Claude logs and Codex config as primary evidence before rewriting server code.
- For plugin MCPs, compare the plugin `.mcp.json` against a known-good Claude Desktop or Codex entry before rewriting server code.
- When making a config fix, back up the live file first, merge the new server into the existing config, and verify no unrelated MCPs disappeared.
- If several Claude MCPs fail together, treat that as a fleet-health problem first.
- Use profile-first remediation for shared startup failures: switch Claude to a smaller named profile before changing server code.
- If the Codex config parser rejects `config.toml`, back up the live file first and validate a scratch copy with `validate a scratch copy with the host-approved Codex config validator` before replacing the live file.

## High-value failure patterns

### "Operation not permitted" when Claude launches `/bin/bash <script>`

- Treat this as a launcher problem, not an MCP protocol problem.
- On some macOS hosts, Claude may refuse to open a shell wrapper stored on `<external-ssd>` even though it can launch a Python interpreter and pass an external script path as an argument.
- Preferred fix:
  - Use `/usr/local/bin/python3.10` as the Claude command
  - Point args at a Python launcher file on the external drive
  - In that launcher, prepend the project root and venv `site-packages` to `sys.path`
  - Do not rely on a bash wrapper as Claude's direct entrypoint

### External-drive Python environments create `._*` sidecar files

- These sidecars can appear inside the venv and may include fake `.pth` files such as `._distutils-precedence.pth`.
- If Python reads those `.pth` sidecars during startup, interpreter startup can fail before the MCP server code runs.
- Preferred fix:
  - Before importing project packages, delete `._*.pth` and `.__*.pth` under the venv `site-packages`
  - Set `PYTHONDONTWRITEBYTECODE=1`
  - Prefer a Python launcher that injects `site-packages` into `sys.path` instead of depending on the external-drive venv as the direct command

### External-drive .NET source sidecars

- If a .NET build starts failing with compiler errors against files like `._Program.cs`, treat it as sidecar contamination.
- AppleDouble files can be globbed as fake source inputs by the C# compiler.
- Delete `._*` and `.__*` files from the checkout before rebuilding.

### Claude and `dotnet run --project`

- If Claude can launch a .NET MCP in Terminal but fails when using `dotnet run --project`, prefer a built DLL launch instead.
- After a successful build, point Claude at `dotnet /absolute/path/to/ToolBox.dll --stdio` rather than the project file.
- This avoids client-side project-file resolution during attach and is often more stable for external-drive checkouts.

### Claude Desktop fleet overload / shared timeout wave

- Treat "MCP server not accessible", "server not found", or "tool result could not be submitted" as possible fleet symptoms, not proof that one server is missing.
- Evidence pattern:
  - multiple Claude servers fail in the same startup window
  - `~/Library/Logs/Claude/mcp.log` shows repeated `notifications/cancelled`
  - the cancellation reason contains `McpError: MCP error -32001: Request timed out`
  - at least one of the same servers can still initialize when isolated
- Preferred fix:
  - switch the active Claude Desktop config to the smallest named profile that fits the task
  - keep `minimal-profile` as the default daily profile
  - quarantine servers with recent `Invalid JSON` or parse-error evidence until they pass a smoke check
  - run the fleet checker before re-expanding the active profile
- Do not keep piling more servers into the active Claude config while this pattern is unresolved.

### Tool result could not be submitted

- Treat this as a client/result-submission problem until isolated, not proof that the server tool failed.
- Common causes:
  - Claude session expired or page/app connection interrupted
  - fleet overload or shared timeout wave
  - oversized or deeply nested tool result payload
  - slow backend call that returns after the client has abandoned the request
  - malformed result envelope that a strict client refuses to submit
- Preferred diagnosis:
  - run the exact tool call through an isolated stdio MCP client
  - inspect `~/Library/Logs/Claude/mcp-server-<server-name>.log` and `~/Library/Logs/Claude/mcp.log`
  - compare a small known-good tool result against the failing result
  - check whether the failing result can be paginated, summarized, or capped by retrieval budget
- Preferred fix:
  - return compact, high-signal payloads with pagination/cursors for large data
  - add retrieval budgets by mode
  - validate the top-level result envelope before returning
  - add degraded partial results instead of waiting indefinitely for every backend
  - add a smaller dry-run or validation tool when the full result is too large for diagnosis

### Codex MCP launches but tools are not exposed

Treat this as three distinct layers: direct stdio initialization and `tools/list`, the live host process and configured profile, and current-session tool discovery. A direct smoke pass cannot prove model-visible tools. Inspect the active config and process start times; verify the compact allowlist and metadata budget, then restart the host only when required. Query current-session discovery for exact routine tool names. If a server-instance lock rejects duplicate Codex clients, make only the server-instance lock advisory while preserving writer locks; validate with an isolated diagnostic first. A tool absent only in the current thread after direct and host checks is a registry exposure issue, not a reason for repeated server surgery. Keep a task-specific direct fallback separate from a verified native connection.

### Claude uses the wrong MCP tool or wrong lane

- Treat this as an agent-control/routing-contract bug, not just a better-prompt problem.
- Evidence pattern:
  - the MCP attaches and tools list correctly
  - Claude can use the right tool only when the user names it exactly
  - broad requests default to web, papers, or the first visible source lane
  - private corpus, notes, reality-check, or library queries are misrouted
  - long conversations make tool-choice behavior drift
- Inspect:
  - tool names and descriptions for vague or overlapping language
  - whether the tool list is too flat, too large, or missing a "start here" orchestrator
  - whether important descriptions include use-when and do-not-use-when guidance
  - whether wrong-lane calls return redirects or accidentally perform the wrong lookup
  - whether public payloads expose adapter names instead of user-facing lane labels
  - whether routing smoke tests cover expected routes and expected non-routes
- Preferred fix:
  - add or harden a shared intent classifier inside the MCP
  - make the orchestrator the true default route
  - add wrong-lane redirect contracts with `recommended_tool`, `recommended_arguments`, `reason`, and `no_lookup_performed`
  - change ambiguous defaults from "lookup first" to "frame first, then route"
  - rewrite high-impact tool descriptions as decision tables
  - add a compact runtime policy or routing contract to overview/get-started outputs
  - add eval fixtures for route accuracy, wrong-lane redirect pass rate, private-leak checks, schema pass rate, and budget pass rate
- In Claude Desktop and Claude.ai, do not assume API-only `tool_choice` enforcement is available. Enforce the practical contract inside the MCP server.
- If the only fix proposed is "make the system prompt stronger," route back to `local-data-mcp-builder` and design a runtime contract instead.

### Retrieval returns stale, noisy, or wrong results

- Treat this as an index/retrieval contract problem, not a startup problem.
- Evidence pattern:
  - the MCP initializes and tool calls return normally
  - expected records are missing from search or context packs
  - Chroma returns old or semantically nearby but operationally wrong results
  - SQLite/FTS and Chroma disagree on counts or behavior
  - results exceed the selected budget or flood the host context
  - lens cards, graph edges, source paths, or build metadata are missing
  - broad queries work only when the exact title or slug is named
- Inspect:
  - `get_index_manifest` or equivalent build metadata
  - record/chunk/lens-card counts in SQLite
  - FTS row counts versus source table counts
  - Chroma cached health and live collection count, if Chroma is enabled
  - retrieval trace fields: selected budget, result counts, truncation, skipped lanes
  - eval fixtures with expected IDs and `must_not_include` IDs
  - graph-edge target integrity and allowed relation types
  - source-path/provenance fields and source-vs-presentation metadata
- Preferred fix:
  - rebuild SQLite/JSONL first and verify counts before rebuilding Chroma
  - keep Chroma optional; if stale or unavailable, fall back to SQLite/FTS with a clear degraded notice
  - add or tune lens-card retrieval instead of dumping raw chunks
  - add lightweight graph edges only from explicit links, source relationships, shared slugs, curated topics, or workflow metadata
  - enforce retrieval budgets for results, chunks, related entries, graph edges, and approximate context characters
  - add eval fixtures for expected hits, expected non-hits, must-not-include violations, and budget compliance
  - clean `.DS_Store`, `._*`, `__pycache__`, and `.pyc` artifacts after external-drive builds
- Do not solve retrieval quality by adding more prompt text. Route back to `local-data-mcp-builder` and harden the index, schema, budgets, validators, and evals.

### Claude asks prose questions instead of using the widget contract

- Treat this as a missing or buried interaction contract, not a personality problem.
- Evidence pattern:
  - the MCP returns `PAUSE_REQUIRED`, `questions_for_user`, or a human-loop gate
  - Claude asks "Which would you prefer?" in normal chat instead of rendering the declared widget
  - behavior works early in a thread and drifts later
- Inspect:
  - whether pause responses put `PAUSE_REQUIRED` and `human_loop_host_action` near the top
  - whether the payload names the required surface, widget tool name, question types, fallback rule, and repair instruction
  - whether a `tool_compliance_signal` or smoke-test field makes expected widget use machine-checkable
- Preferred fix:
  - add a compact runtime policy card to the pause response
  - set `plain_text_questions_valid=false` when native widget UI is available
  - include a repair instruction such as "Convert the prose question into Ask_User_Input_V0 and do not continue until the user responds"
  - add fixtures for onboarding, consent, judgment, reflection, and approval gates
  - if widget UI is unavailable in the host, include an explicit inline fallback so the host is not guessing

### Schema drops, placeholders, or debug strings reach the user

- Treat this as a validator/template failure, not a cosmetic copy issue.
- Evidence pattern:
  - a natural key such as `bias` silently drops a populated section
  - text like "No rows were supplied", "Name the evidence", `unknown`, raw enum values, beta notes, DB paths, or KB internals appears in public output
  - rendered output is the first place the problem becomes visible
- Inspect:
  - alias normalization before render
  - unknown sibling-key diagnostics and "did you mean" hints
  - schema-only or validation-only responses for canonical field shape
  - post-render/text-QA blocklists
- Preferred fix:
  - warn or block before render for unknown fields and over-limit text
  - expose canonical schema, aliases, constraints, example shape, schema hash, and `writes_files=false` through validation
  - add explicit valid null states for real analytical outcomes such as consensus
  - suppress empty sections instead of rendering raw system messages
  - fail polished output when debug strings or placeholders leak

### Private data or memory-like writes behave unpredictably

- Treat private notes, personal corpora, feedback stores, and living docs as governed write surfaces.
- Direct user write actions may write, but inferred "save this insight" behavior should become a patch proposal or explicit confirmation path.
- Validate that private results carry provenance labels and that release artifacts exclude private data, state, logs, and local config.

### Claude plugin validation failed during upload

- Treat this as package-shape validation before debugging MCP runtime code.
- Compare against a known-working plugin zip and inspect `~/Library/Logs/Claude/main.log` plus `~/Library/Logs/Claude/claude.ai-web.log`.
- For top-level `agents/*.md`, keep strict YAML frontmatter: `name`, folded `description: >`, `model`, `color`, and optional block-list `tools`; do not put loose XML/example blocks inside frontmatter.
- Zip the plugin with a single top-level folder, for example `critical-compass-plugin/.claude-plugin/plugin.json`, not loose root-level files.
- Avoid custom manifest path keys such as `agents`, `skills`, or `mcpServers` unless a working plugin proves they are required; Claude can discover conventional folders.
- Remove AppleDouble sidecars and xattrs before sharing: delete `._*`, `.__*`, `.DS_Store`, `__pycache__`, and `.pyc`, then run `xattr -c` on final zips when on macOS.
- Bump the plugin version after package changes so Claude does not appear to reuse stale validation state.
- Watch for standalone skill-name collisions such as an existing uploaded `critical-compass` skill when the plugin also bundles `skills/critical-compass/`.
- Treat Claude's installed plugin folder as generated cache. Inspect it for diagnosis, but update the source package and reinstall/upload instead of hand-editing the cache.

## Claude-specific rule

- If another Claude MCP server already works with:
  - a Python interpreter in home/internal storage
  - an external script path in `args`
- then prefer that pattern over a bash wrapper for new servers.

Current preferred storage-MCP pattern on some macOS hosts:

- command:
  `<home>/.local/share/local-storage-mcp/venv/bin/python`
- args:
  `<external-ssd>/ExternalApplications/local-storage-mcp/mcp_server.py`
  plus `--db-path` pointing at the external-drive SQLite index

## Validation

- Confirm the launcher stays alive when run directly from Terminal.
- After restarting Claude or Codex, confirm the server reaches `initialize` and `tools/list` in the client log.
- If logs never reach `initialize`, the problem is still process launch, permissions, or environment setup.
- For Codex tool exposure, direct `tools/list` is necessary but not sufficient: also confirm the live MCP child process started after the relevant change and that `tool_search` finds the expected routine tools in the current Codex session.
- If logs reach `tools/list` but Claude misuses the MCP, run route-level smoke tests: correct lane, wrong-lane redirect, degraded backend, private-data boundary, and compact result payload.
- If logs reach `tools/list` and retrieval quality is the problem, run index and retrieval checks: SQLite integrity, collection counts, FTS row parity, lens-card count, graph-edge target validity, cached/live Chroma count parity, budget smoke tests, and retrieval eval fixtures with expected IDs plus `must_not_include` IDs.
- For shareable or agent-control MCPs, verify tool descriptions include explicit use/do-not-use guidance and that evals include expected non-routes, expected non-findings, widget-contract fixtures, schema-drop fixtures, budget fixtures, and public-output leak checks.
- A successful fix should identify which layer changed: launcher/config, result envelope, routing contract, schema validator, tool description, retrieval budget, or package shape.
- For Claude Desktop profile health, run:
  - `python3 <development-studio-plugin>/libraries/local-mcp-methods/local-data-mcp-builder/scripts/check_claude_mcp_fleet.py`
  - `<mcp-enabled-python> <development-studio-plugin>/libraries/local-mcp-methods/local-data-mcp-builder/scripts/smoke_claude_profile.py`

