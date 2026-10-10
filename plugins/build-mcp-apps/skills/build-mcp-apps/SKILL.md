---
name: build-mcp-apps
description: "Explain Build MCP Apps capabilities and getting started, or create an MCP widget or build/update MCP servers and MCP Apps with an end-to-end, capability-aware workflow. Use for MCP protocol, view resources, host bridges, state, retries and app verification; route Skybridge-specific work to the preserved Alpic procedures."
---

# Build MCP apps

For “what can Build MCP Apps do?”, setup or getting-started help, read the capability, first-task and setup sections of the [plugin introduction](../../README.md) and recommend one relevant first task; skip maintainer notes unless updating the package. Help alone does not start a diagnosis, scan, audit or external action. For a concrete request, use the matching procedure below without loading the whole plugin.


Use this maintained entrypoint for MCP-specific implementation decisions. It is
portable across MCP Apps hosts and does not require migrating an existing app to
Skybridge. For an existing small app, inspect its current runtime and make the
smallest compatible change; do not create SPEC scaffolding or a framework
migration solely because this skill has a specification workflow.

For Skybridge or Alpic projects, read the complete preserved procedure at
[`libraries/alpic-1.0.1/skills/build-mcp-apps/SKILL.md`](../../libraries/alpic-1.0.1/skills/build-mcp-apps/SKILL.md)
and the relevant original references. Use the same route for Alpic deployment,
debugging, auth, environments and publishing through
[`use-alpic`](../use-alpic/SKILL.md). The preserved source is a read-only
reference snapshot; maintained routing and MCP-neutral guidance live here.

For MCP Apps in any framework, read the applicable sections of
[`mcp-widget-technical-contract.md`](references/mcp-widget-technical-contract.md)
and the matching test cases in
[`mcp-widget-test-plan.md`](references/mcp-widget-test-plan.md).
Do not import Skybridge hooks, Alpic commands or generated project structure
into another runtime.

## Create or improve an MCP widget

Use this entrypoint to orchestrate a widget from task to verified delivery; do not create a second overlapping “create MCP widget” skill.

1. **Find the job and owner.** Consult the owning project map and current implementation. Name what the human will select, compare, adjust or approve and why a widget helps. Use a text/tool result when interaction adds no value. For an existing widget, audit concrete gaps first and preserve the accepted visual direction.
2. **Set the interaction contract.** Use UX Design Studio's `skills/design-studio/SKILL.md` and generic `skills/design-studio/references/conversational-widgets.md`; load its `mcp-app-widgets.md` only for compact library choosers. Resolve these from the installed UX plugin root rather than assuming a fixed cache version. Map 3–8 reference anchors, required states and intentional content differences. Share components/bridge across siblings; adapters own domain fields. For analytical widgets, include Data Visualization Toolkit's correctness checks.
3. **Bind to actual capabilities.** Record the host/surface/build and installed SDK. Apply the technical contract and test plan linked above. Distinguish inline, expanded, standalone and simulated-host behavior; use acknowledged host modes rather than drawing a pretend host panel. Decide storage, context, message and write ownership before implementing.
4. **Build one complete task path.** Include real data, honest pending/error/unknown states and a useful unavailable-host fallback. Named create actions must prepare a self-contained request with destination, authoring requirements, supplied brief, registration steps and success checks. Prepared/sent prompts are not saved items. Admit external examples through the security owner before reuse; do not import them merely for their UI appearance.
5. **Verify the changed behavior.** Run proportionate protocol/state tests, then UX `design-review` on actual rendered anchors and relevant states. Test rejection, stale results, keyboard return, narrow/enlarged text and theme changes where affected. Separate local harness evidence from real-host expansion and delivered-message evidence. User approval of a screenshot is visual approval only.
6. **Ship and learn.** Project shared changes to adapters, validate source/installed parity through the owning native installer, then apply the live-release checks in the test plan. Installed bytes and a fresh subprocess do not establish what an already-running MCP connection serves. Record exact remaining host limits. Keep project-specific findings in its evidence record. Promote repeated failure → correction → verified example → applicability into the existing owning reference; review user/Claude suggestions against current requirements rather than importing a review wholesale. Stop after the bounded outcome; no automatic extra widget/catalog work.

If the actual host cannot be inspected, finish useful local checks and report a locally verified candidate with the specific missing interaction evidence. Do not request remote physical testing repeatedly, equate a mock with acceptance, or mark the full host-dependent outcome complete.

## Technical gates

- Treat initialization, negotiated capabilities, display modes, tool calls,
  context updates, message requests and teardown as separate protocol
  boundaries. Feature-detect optional capabilities and provide an honest
  fallback for each unavailable one.
- Keep read/search tools, render-linked tools and external write tools distinct
  in descriptions and metadata. AI-only retrieval must return structured data
  without UI-opening metadata; attach a view only when the human is intentionally
  choosing, browsing or inspecting.
- A human-facing view does not imply human-only authorship. For shared artifacts
  such as drawing canvases, give the assistant structured create/read/edit tools
  over the same saved object that the human edits. Present the view for visual
  communication and collaboration; do not require UI clicking for AI authoring.
  Library choosers still use background retrieval. Shared editing needs revision
  checks, draft protection and an honest refresh/handoff contract.
- Keep local selection/draft state separate from authoritative server state and
  model-context snapshots. Persist only an explicitly declared, non-sensitive
  state subset; never persist credentials or private briefs/source content by accident.
- Treat accepted, pending, completed, failed and outcome-unknown as different
  states. Use operation IDs and server-side idempotency for retryable writes;
  reconcile an ambiguous result before inviting a retry.
- A host acknowledgment proves transport handling, not semantic assistant use or
  external persistence. Record real-host evidence separately from local export,
  VM protocol tests and browser checks.

Run the relevant protocol, state, accessibility and real-host checks before
claiming compatibility. Use current matching Skybridge/Alpic documentation for exact APIs; the preserved
procedures are a versioned workflow baseline, not a guarantee of current host
persistence or model visibility. UX Design Studio owns generic widget interaction
design; Data Visualization Toolkit owns chart meaning and analytical correctness.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports MCP Application Engineer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
