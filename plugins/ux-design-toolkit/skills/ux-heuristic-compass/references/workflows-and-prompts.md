# UXHC Workflows And Prompts

Use these prompts as starting points. Adapt them to the user's interface and evidence, but preserve the evidence limits and human-loop behavior.

## Skill-Only Quick Audit

```text
Use UX Heuristics Compass in standalone mode. Review the provided interface evidence as a quick heuristic audit. Identify the user goal, platform, strongest usability risks, and evidence limits. Use the 0-4 severity scale. Return a UX Health Snapshot, top 3 issues, what holds up, and what to validate next. Do not claim real user behavior unless participant data is supplied.
```

## Skill-Only Full Audit

```text
Use UX Heuristics Compass in standalone mode for a fuller heuristic audit. Apply H1-H10 by default, and include H11-H14 only if the evidence or user request makes them relevant. For each material issue, name the heuristic, severity from 0-4, evidence, confidence, and a concrete fix. Separate observed evidence from inference. End with evidence limits and next validation steps.
```

## MCP First-Use Prompt

```text
Use the UX Heuristics Compass MCP. Start with get_started so we know the runtime contract, preferences, available profiles, human-loop behavior, and report path. Then choose the smallest audit path that fits the user's request.
```

## MCP Quick Audit Prompt

```text
Use UX Heuristics Compass for a quick audit. If source evidence is not already prepared, call prepare_ux_source first. Then call quick_scan_ux with the platform, active profiles, user goal, and any host-supplied checklist ratings or observations. If the MCP returns PAUSE_REQUIRED, use native question UI before continuing. Return only the compact UX Health Snapshot, top issues, evidence limits, and next action unless the user asks for a full report.
```

## MCP Full Audit Prompt

```text
Use UX Heuristics Compass for a full checklist-level audit. Prepare the source, confirm platform and optional profile scope, then call audit_ux_surface with output_detail: "compact" unless the full payload is needed for report generation. Make sure every active checklist item has a rating or explicit evidence-limit contract before scoring. If report generation is requested, call validate_ux_report_payload using the checklist_ratings from the audit scorecard — do not build ratings from scratch. Do not call generate_ux_audit_report with an invalid or manually assembled payload.
```

## Advanced Multi-Agent Audit Prompt

```text
Use UX Heuristics Compass advanced audit support. Confirm platform, user task, optional profile scope, and whether Agent Mode 1 is desired. The host AI should embody the researcher personas and submit independent scorecards to run_agent_audit. Personas must be dict objects with id, label, and description fields — not plain strings. Use the aggregation output to identify consensus, disagreement flags, top findings, and calibration risks. Do not describe this as real user testing.
```

## UX Coaching Prompt

```text
Use UX Heuristics Compass as a coaching layer. Review the interface evidence, name the one most important UX issue, explain the relevant heuristic in plain language, suggest a small fix, and give the user one validation exercise they can perform without a full research study. Keep the tone practical and nonjudgmental.
```

## Code-Aware UX Review Prompt

```text
Use UX Heuristics Compass for implementation-aware review. Inspect rendered behavior, screenshots, or frontend code only within the user's provided scope. Map code or Playwright observations to likely affected heuristics, but do not change checklist ratings without visible evidence or explicit evidence limits. Return implementation observations as audit support, not as a replacement for the UX scorecard.
```

## Human-Loop Question Set

Use native question UI (`AskUserQuestion`) when available. One question per call. For single-select questions, provide `options` with `label` and `description`. For open-ended context questions, omit `options` and use free text.

Ask these at the beginning when scope is unclear:

1. What task should this interface help the user complete? *(free text)*
2. Should I audit this as desktop, mobile, or both? *(single select)*
3. Should this use core usability only, or include accessibility, inclusion, journey, and UX writing profiles? *(single select)*
4. Who are the primary users of this interface, and are there constraints or contexts the evidence may not show? *(free text — captures mission context, low-bandwidth users, underserved audiences, literacy levels, and other calibration factors that should affect severity scores)*

Ask these during a deeper audit when judgment matters:

1. Which finding feels most important to validate before shipping? *(single select from top findings)*
2. Should any finding be rescored based on audience context you know that the evidence does not show? *(free text — surfaces hidden severity factors)*
3. Should the recommendation optimize for speed, clarity, accessibility, conversion, learning, or trust? *(single select)*

Ask these before report generation:

1. Is the scorecard ready to generate a report? *(single select: yes / not yet)*
2. Should the report include a mission context section explaining who the users are and why this interface matters? *(single select: yes — recommended / no)*
3. Which finding should lead the executive summary? *(single select from top findings)*

## Plain-Language Heuristic Explainers

Use these when the user is not a UX specialist:

- Heuristic evaluation: a structured review that checks an interface against common usability principles.
- Visibility of system status: users should know what is happening and what changed.
- Recognition rather than recall: users should not have to remember hidden choices when the screen could show them.
- Error prevention: the design should help people avoid mistakes before they happen.
- UX writing: the labels, buttons, instructions, and messages that help people understand what to do.
- Evidence limit: something the audit cannot know from the provided screenshot, URL, notes, or code.

## Mission-Critical Audience Audit Prompt

Use when the product serves users with high stakes, limited resources, intermittent connectivity, low digital literacy, or underserved contexts — and those constraints are not visible in the interface evidence itself.

```text
Use UX Heuristics Compass for a full audit. Before scoring, ask the user one open-ended question about who the primary audience is and whether there are constraints — such as low bandwidth, limited devices, low literacy, high-stakes tasks, or economic barriers — that are not visible in the interface screenshots. Use the answer to calibrate severity. An issue that would be minor for a well-resourced user may be catastrophic for an under-resourced one. Include a Mission Context section at the top of the report that explains the audience and why the interface matters to them.
```

## Post-Fix Verification Audit Prompt

Use after UXHC MCP updates or interface changes to confirm the audit flow still works cleanly without running a full checklist audit.

```text
Use UX Heuristics Compass for a lightweight verification pass. Call get_started, ux_heuristic_overview, and list_heuristics with detail_level: "summary" to confirm the current rubric, optional profiles, and runtime contracts. Then call quick_scan_ux with hil_enabled: true to confirm the HIL gate behavior and audit_scope_lock output. Finally call validate_ux_report_payload with a minimal well-formed payload to confirm the validator accepts correctly structured payloads without blocking. Do not run a full audit unless a specific finding needs verification.
```

## Short Output Template

```markdown
## UX Health Snapshot
The interface is [brief read]. The top priority is [one fix area]. Evidence is limited by [limits].

## Top Issues
1. [Finding] - [H# heuristic], severity [0-4].
   Evidence: [observed evidence].
   Fix: [concrete action].

## What Holds Up
- [Strength or low-risk area.]

## Validate Next
- [Small next test, inspection, or user check.]
```
