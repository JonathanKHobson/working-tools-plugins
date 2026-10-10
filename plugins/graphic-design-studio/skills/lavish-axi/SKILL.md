---
name: lavish-axi
description: "Use when evaluating, piloting, or adapting the Lavish AXI local HTML review loop: annotation feedback, poll-based agent handoff, render-time layout warnings, or Shareables/Cuts artifact review surfaces. Prefer local Shareables and existing visual-QA workflows first; use Lavish itself only as a sandboxed side tool after safety review."
---

# Lavish AXI

Use this skill when the task mentions Lavish, AXI, click-to-annotate review,
`lavish-axi poll`, layout warnings, artifact review loops, or a Shareables/Cuts
pilot that needs feedback to ride from a rendered HTML artifact back to the
agent.

This is a local wrapper around the useful pattern, not a standing instruction
to run the external tool as part of a shipped artifact. The reviewed package is
`lavish-axi@0.1.31` (MIT). For inspection, select your own separately installed reviewed executable:

```bash
"${LAVISH_AXI_BIN:?Set LAVISH_AXI_BIN to your reviewed installed executable}"
```

The historical source inspection used `npm install --ignore-scripts`; no hook setup, global install,
server start, browser open, or artifact session was run during review.

## Safety Boundary

- Do not run `npx`, fresh `npm install`, global hooks, or `lavish-axi setup
  hooks` unless the user explicitly approves after a focused safety review.
- Safe without extra approval after the 2026-06-19 review: read local docs,
  inspect the isolated install, and run non-server commands such as `--help` or
  `playbook` with `LAVISH_AXI_TELEMETRY=off`.
- Requires exact-step approval: `lavish-axi <html-file>`, `poll`, `server`,
  `setup hooks`, or any command that opens a browser, starts the Express server,
  watches files, long-polls, or writes hook/config state.
- Keep all Lavish runtime trials in a sandbox such as
  `_Sandbox/lavish-axi-pilot/`; do not write into canonical artifact folders
  during the pilot.
- Bind only to loopback/default local mode. Do not set `LAVISH_AXI_HOST` to a
  non-loopback address unless the user explicitly approves the exposure risk.
- Set `LAVISH_AXI_TELEMETRY=off` for all review/pilot commands unless the user
  explicitly asks to allow telemetry. Static review found telemetry is no-op
  unless a website ID is configured, but opt-out is still the local default.
- Never ship a click-to-annotate layer, localhost endpoint, Lavish SDK,
  unreviewed CDN snippet, or runtime-only browser dependency inside the final
  artifact.
- If the output is a Shareable or single-file handoff, it must pass the
  Shareables quality gates for external URLs, private paths, route assets,
  mobile overflow, and visual QA.

## What To Borrow

- Open-time or build-time layout gates that catch horizontal overflow, clipped
  text, and overlapping text before human review.
- A dev-only annotation loop where the reviewer clicks an element or selected
  text, leaves a note, the agent polls the queue, fixes the file, and reloads
  the artifact.
- A design-source resolver that prefers the user's/project's tokens first,
  detected project config second, and bundled defaults last.
- A strict portability contract: exported HTML should open cold without a
  local server, package install, private path, or network dependency unless the
  artifact explicitly declares that dependency.
- Agent-ergonomic CLI/MCP design: commands should return small structured
  feedback, preserve context, and separate machine faults from human judgment.
- Playbooks for plan, comparison, diagram, table, code, input, and slides as
  compact prompts for visual artifacts. Use the installed CLI's `playbook`
  command with telemetry off to inspect them.

## Workflow

1. Classify the ask as one of four lanes: pattern adoption, Shareables review
   loop, sandbox pilot, or native rebuild.
2. If the user wants to run Lavish, first use the security review lane from
   `personal-security-check`; inspect `package.json`, scripts, dependencies,
   bind addresses, hook behavior, telemetry, filesystem access, server state,
   and generated artifacts.
3. For a sandbox pilot, copy exactly one representative HTML artifact into the
   sandbox, bring the local design tokens, and define exit criteria before any
   command runs.
4. For Shareables or durable workflows, update the local workflow docs or build
   tools first. Treat Lavish as a source of review-loop patterns, not as a
   default runtime dependency.
5. Before signoff, prove that the final artifact has no unapproved external
   scripts/styles, no `localhost` links, no private paths, and no shipped
   annotation overlay.

## Load When Needed

Read [pilot-and-shareables.md](references/pilot-and-shareables.md) when the
task involves Shareables/Cuts integration, a Lavish pilot, or deciding whether
to keep Lavish as a side tool versus rebuilding the loop locally.

Use [the receiving-host contract](../../docs/standalone-visual-workflows.md) for configured binary/source boundaries. Existing user authorization applies to the exact current task; old review permission is not automatically current execution evidence.
