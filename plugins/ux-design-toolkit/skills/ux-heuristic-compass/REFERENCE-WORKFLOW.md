---
name: ux-heuristic-compass
description: Use UX Heuristics Compass to review interfaces, screenshots, app screens, websites, prototypes, or UI code for visible usability issues. Use it for heuristic UX audits, usability reviews, UX writing checks, accessibility-and-inclusion passes, evidence-bound interface critique, launch-readiness review, or coaching a builder on what to fix next.
compatibility: Claude Desktop, Claude Code, Codex, ChatGPT, and other hosts that can use Markdown skills or local MCP tools
---

# UX Heuristics Compass

UX Heuristics Compass helps a host AI audit a visible interface before it ships. It turns bounded evidence into plain-language UX risks, severity-calibrated findings, and concrete next actions.

Aliases: UXHC, UXH Compass.

Use this skill when the user asks for:

- a UX audit, heuristic evaluation, usability review, or interface critique
- feedback on a screenshot, website, app screen, prototype, landing page, form, dashboard, flow, or UI copy
- help finding confusing, hidden, inconsistent, inaccessible, or hard-to-recover interface issues
- a code-aware UX review where rendered behavior, frontend code, or Playwright observations can support the audit
- deck-like Shareables, browser presentations, visual explainers, learning
  artifacts, and public proof pages where viewport fit, progressive disclosure,
  image/source status, or channel readiness affect usability
- coaching on what to fix first before shipping or showing an interface

Do not treat UXHC as a full UX research platform. It does not replace usability testing with real users, WCAG certification, analytics review, market research, authenticated-flow automation, or full-site crawling.

## Start Here

Before auditing, identify the smallest useful scope:

1. Interface evidence: screenshot, URL, prototype notes, rendered preview, source manifest, or code observations.
2. Platform: desktop, mobile, or both.
3. User goal: what the user is trying to do on this interface.
4. Audit depth: quick scan, full checklist audit, advanced multi-agent audit, or coaching.
5. Optional profiles: core only, accessibility, inclusion, journey, UX writing, or all optionals.

If any of those answers are missing and they materially affect the audit, ask bounded questions. When the host has native question UI, use it instead of ordinary prose questions. If native question UI is unavailable, ask the same questions clearly and wait for answers before continuing.

## Two Modes

### Standalone Mode

Use standalone mode when the UXHC MCP is not available or the user only needs a lightweight review.

In standalone mode:

- apply the 14-heuristic system from `references/heuristics-checklist.md`
- rate issues with the 0-4 severity scale
- calibrate severity against audience context with `references/severity-calibration-guide.md`
- separate observed evidence from inference
- name evidence limits with `references/evidence-collection-guide.md` instead of pretending to see unavailable states
- check evaluator bias before accepting severe or uncertain findings
- return a compact score-style summary only when there is enough evidence
- give concrete next fixes and validation suggestions

Standalone mode can produce a useful Markdown audit, but it cannot persist preferences, prepare source manifests, validate report payloads, generate local files, run MCP aggregation, or create PDF/HTML artifacts.

### MCP-Enhanced Mode

Use MCP-enhanced mode when UXHC tools are available. The MCP owns structured source prep, checklist contracts, scoring validation, report readiness, artifact generation, preferences, and agent-run aggregation.

Recommended routes:

- `get_started`: orientation, runtime contract, preferences, host guidance, `profile_aliases`, and `checklist_rating_contract` — call this before any audit to get current field requirements
- `ux_heuristic_overview`: compact explanation of UXHC capabilities and boundaries
- `list_heuristics`: discover the 14-heuristic rubric; always use `detail_level: "summary"` unless full item IDs are needed — full detail output can overflow context
- `prepare_ux_source`: prepare screenshots, bounded URLs, or source manifests
- `quick_scan_ux`: choose an explicit mode; `output_detail: "guidance_only"` is ultra-quick non-scoring support for direct edits/fix prompts/micro-plans, `status_only` is small scored-audit orchestration, and omitted output detail returns a mode gate so options are not hidden
- `audit_ux_surface`: full checklist-level audit path; use `output_detail: "compact"` to avoid context overflow on large audits
- `validate_ux_report_payload`: dry-run report readiness before generating artifacts; use the `checklist_ratings` from the audit scorecard, not manually assembled ratings
- `generate_ux_audit_report`: write Markdown, static one-page HTML, and optional PDF when validation passes; use the UXHC report design harness, never `canonical_payload_template`, and repair blocked payloads instead of handmaking HTML
- `run_agent_audit`: aggregate host-supplied researcher persona scorecards; personas must be dict objects `{id, label, description}` — not strings
- `get_agent_run`: retrieve a stored agent audit run
- `run_usability_test`: bounded usability-test prep or synthetic walkthrough support, not real user evidence unless participant data is supplied
- `stress_test_heuristic_finding`: check one finding for false-positive risk, evidence limits, and practical fix quality
- `compare_ux_audits`: compare before/after or desktop/mobile audits
- `calibrate_ux_sensitivity`: review deterministic severity calibration fixtures
- `draft_project_addon_profile`: draft opt-in project-specific add-on criteria without changing the core score

See `references/mcp-bridge.md` for routing details, output size guidance, and profile alias mapping.

For reports, use `references/report-payload-field-guide.md` before assembling or repairing payloads. The current validator uses `checklist_item_id` and `rating`; do not rename those fields to `item_id` or `severity`.

## Default Audit Shape

Use this shape unless the user asks for something narrower:

```markdown
## UX Health Snapshot
- Scope:
- Platform:
- User goal:
- Overall read:
- Top priority:
- Evidence limits:

## Top Issues
1. Finding:
   - Heuristic:
   - Severity:
   - Evidence:
   - Why it matters:
   - Fix:

## What Holds Up
- 

## What To Validate Next
- 
```

For a fuller report, include per-heuristic grades, checklist-level issue rows, optional-profile sections, and a clear next-validation plan.

## Human-In-The-Loop Contract

UXHC uses human-loop questions to keep audits calibrated instead of letting the host guess about context, user goals, optional profiles, severity judgment, or report readiness.

When a UXHC response says `PAUSE_REQUIRED=true`, the host must pause and ask the user through native question UI when available. For the local MCP, that contract may appear as `ask_user_question_call` with `tool_name: AskUserQuestion`.

When `HIL_BLOCKED_UNTIL_NATIVE_UI: true` appears in the response, the host must use the `AskUserQuestion` tool — not prose paragraphs. The MCP often provides a pre-built `ask_user_question_call` block with exact parameters. Use it directly. If no pre-built block is provided, use this format:

```json
{
  "question": "...",
  "multiSelect": false,
  "options": [
    { "label": "Option text", "description": "Context for choosing this option" }
  ]
}
```

Ask one question per native widget call. For open-ended context questions (audience, mission, constraints), omit `options` and accept free text.

Use human-loop questions for:

- missing platform, user task, audience, or interface goal
- audience context that could change severity calibration (low-bandwidth users, high-stakes tasks, underserved populations)
- deciding whether optional H11-H14 profiles are in scope
- clarifying low-confidence or high-severity findings
- confirming report readiness before artifact generation
- coaching moments where the user wants to learn, not just receive a report

Do not flatten required native UI questions into a normal Markdown paragraph when a native question surface is available. If no native question UI exists, ask the same questions as a fallback and explicitly say you are using text fallback.

## Evidence Rules

- Only score what the provided evidence can support.
- If a screenshot does not show hover, focus, error, loading, back-navigation, or visited states, mark that as an evidence limit.
- Do not claim real users struggled unless the user provides real participant data.
- Do not claim accessibility compliance or legal conformance from heuristic evidence alone.
- Do not browse, crawl, authenticate, or operate the user's interface unless the host/tooling explicitly supports that action and the user has provided the scope.
- Do not let code observations override visual evidence; code can suggest likely issues, but checklist ratings still need evidence or stated limits.
- For decks and slide-like artifacts, visible overflow, clipped controls,
  unreadable charts, or text that only fits by shrinking below readable size are
  usability findings, not just visual polish.
- For social/profile/launch artifacts, distinguish public-readiness issues
  from platform automation. UXHC can audit the artifact, but posting,
  scheduling, scraping, or account mutation belongs behind explicit approval.

## Output Discipline

Lead with the audit, not the method. The product center is the UX Health Snapshot, checklist-style findings, top priority, plain-language read, and concrete next action.

For each finding, include:

- what the user may experience
- the relevant heuristic
- severity from 0-4
- evidence or evidence limit
- the smallest useful fix
- what should be validated next

Use plain language. Avoid jargon unless the user is clearly a UX practitioner. Explain terms such as "heuristic evaluation" or "recognition rather than recall" in everyday language when needed.

## Reference Navigation

| Need | Read |
| --- | --- |
| Heuristic names, item counts, and severity scale | `references/heuristics-checklist.md` |
| Audience-aware severity calibration | `references/severity-calibration-guide.md` |
| Evidence collection, screenshots, SPA states, and Playwright observations | `references/evidence-collection-guide.md` |
| Report payload fields and validation blockers | `references/report-payload-field-guide.md` |
| Report design system, section order, tokens, and validation rules | `references/report-design-system/design.md` |
| Evaluator bias checks for severe or uncertain findings | `references/evaluator-bias-guard.md` |
| Ready-to-use prompts for skill and MCP use | `references/workflows-and-prompts.md` |
| Which UXHC MCP tool to call and when | `references/mcp-bridge.md` |
| Advanced researcher persona guidance | `agents/researcher-panel.md` |
| Report payload repair, layout review, and QA roles | `agents/report-content-editor.md`, `agents/report-layout-reviewer.md`, `agents/report-qa-reviewer.md` |
| Compact example output shape | `examples/sample-audit-output.md` |

## Quick First Prompt

If the user says "audit this interface" and provides evidence, start with:

```text
I can do this as a bounded UX heuristic audit. I need three pieces of context before I score it: what user task this screen supports, whether to treat it as desktop or mobile, and whether you want core usability only or the expanded accessibility, inclusion, journey, and UX writing profiles too.
```

If those answers are already clear, proceed without slowing the user down.
