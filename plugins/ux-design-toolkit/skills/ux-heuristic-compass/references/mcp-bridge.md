# UXHC MCP Bridge

This reference helps the skill route work to the UX Heuristics Compass MCP when the MCP is available. The skill remains useful without the MCP, but the MCP is preferred for structured scoring, validation, state, reports, and local artifacts.

## Core Rule

Use the MCP when the task needs structured source prep, checklist completeness, preferences, human-loop contracts, report validation, generated Markdown/HTML/PDF artifacts, calibration, comparison, or agent-run aggregation.

Use standalone skill mode when the user only needs a lightweight review or the MCP is unavailable.

## Tool Routing

| User need | Preferred tool | Notes |
| --- | --- | --- |
| First use, overview, current runtime contract | `get_started` | Call `get_started(topic="brief")` for ordinary startup. Default `get_started()` retains the deeper startup contract, and `get_started(topic="tools")` returns all 18 tool contracts when needed. Re-call after MCP updates to get a fresh runtime contract. |
| Explain what UXHC can do | `ux_heuristic_overview` | Use for capability summaries and boundaries. |
| Discover the rubric | `list_heuristics` | Start with `detail_level: "brief"` for H01-H14 names, optional profile IDs and item counts. Use `summary` for descriptions or `full` for exact checklist item IDs and text; full detail can exceed 100KB. Request support lenses only when they help explain evidence-backed findings. |
| Prepare screenshot, URL, or source evidence | `prepare_ux_source` | Use for bounded page capture and source manifests. Do not request crawling or authenticated flows. |
| Quick triage | `quick_scan_ux` | Best for compact findings when enough context exists. If context is missing, respect the HIL pause. Response includes `audit_scope_lock` listing any omitted optional profiles with rerun instructions — surface these to the user before summarizing coverage. |
| Full checklist audit | `audit_ux_surface` | Use when the user asks for a full audit, expanded profiles, checklist-level evidence, or report-ready output. Output can exceed 400KB on full-profile desktop audits — pass `output_detail: "compact"` when you only need scores and top findings, or query the saved file with jq (see Output Size section below). |
| Dry-run report readiness | `validate_ux_report_payload` | Always use before generating reports when the payload was assembled by the host. Each rated row needs `checklist_item_id`, `heuristic_id`, `platform`, numeric `rating`, `rationale`, `evidence_refs` or `evidence_limits`, and `confidence`. A verified N/A row instead needs `rating_status: not_applicable`, no numeric rating, and a documented `applicability_reason`; unobserved remains unrated and blocks a complete grade. Use the payload field guide and default `get_started()` rating contract when needed. |
| Generate report artifacts | `generate_ux_audit_report` | Writes Markdown, static one-page HTML, and optional PDF. Do not call with invalid payloads. Do not use `canonical_payload_template` from `audit_ux_surface` output directly because it may contain circular references. Prefer `report_ready_payload`, `report_payload_ref.path`, or returned scored audit fields instead of manual reconstruction. If validation blocks, repair the payload and retry; do not handmake HTML. |
| Severity calibration | `calibrate_ux_sensitivity` | Canonical calibration tool. `calibrate_ux_severity` is a compatibility alias. |
| Compare two audits | `compare_ux_audits` | Use for before/after, desktop/mobile, or regression review. |
| Draft project-specific add-ons | `draft_project_addon_profile` | Keeps add-on criteria separate from core score. |
| Save or update preferences | `save_preferences`, `update_preferences` | Use only for explicit preference workflows. Partial onboarding should not create a preference record. |
| Multi-persona scorecard aggregation | `run_agent_audit` | Host submits researcher-persona scorecards; MCP aggregates and flags disagreement. Personas must be dict objects — `{"id": "...", "label": "...", "description": "..."}` — not plain strings. Passing strings causes a validation error. See `agents/researcher-panel.md` for the correct persona format. |
| Retrieve agent result | `get_agent_run` | Use when an agent run ID is available. |
| Bounded usability-test prep or synthetic walkthrough | `run_usability_test` | Not real user evidence unless real participant data is supplied. When the user wants a real study after the audit, hand the observed questions to the current UX research specialist for study planning, task scenarios, and participant criteria. |
| Challenge one finding | `stress_test_heuristic_finding` | Use for false-positive checks and fix-quality review. Particularly useful for severity 3–4 findings where audience context changed the score. |

## Human-Loop Handling

When a UXHC tool returns `PAUSE_REQUIRED=true`, stop the audit flow and render the questions through native question UI where available.

Expected contract fields may include:

- `human_loop_host_action`
- `required_surface: native_question_ui`
- `ask_user_question_call` — pre-built parameter block for `AskUserQuestion`
- `tool_name: AskUserQuestion`
- `HIL_BLOCKED_UNTIL_NATIVE_UI` — when `true`, do not flatten questions into markdown prose; use the native widget
- `resolved_gates`
- `unresolved_gates`
- `hil_compliance`
- `host_instruction` — plain-language direction for how to render the gate

When the MCP returns `HIL_BLOCKED_UNTIL_NATIVE_UI: true`, use the `AskUserQuestion` tool directly. The MCP may pre-build the exact `ask_user_question_call` parameters — use them as-is. Standard format:

```json
{
  "question": "...",
  "multiSelect": false,
  "options": [
    { "label": "Option A", "description": "When to choose this" },
    { "label": "Option B", "description": "When to choose this" }
  ]
}
```

For free-text gates (mission context, user goal), use `AskUserQuestion` without `options`. Do not ask multiple HIL questions in a single widget call — one question per call.

If native UI is unavailable, use the text fallback policy and record that fallback was used. Do not pretend a native UI pause happened.

## Common MCP Flows

### Quick Audit

1. Call `get_started(topic="brief")` if this is first use or the host lacks context.
2. Call `prepare_ux_source` if the evidence is not already structured.
3. Call `quick_scan_ux` with platform, user task, profiles, and observations or checklist ratings.
4. If paused, ask the required questions and resume with answers.
5. Return compact findings and evidence limits.

### Full Report

1. Prepare source evidence.
2. Run `audit_ux_surface` with the chosen platform and all 14 heuristics by default: omit scope parameters or set `optional_profile_mode="all_optionals"`. Use `core_only` or `scoped` only for an explicit user request to narrow the rubric, never for an agent-selected relevance shortcut. Retain every heuristic and explain genuinely inapplicable checkpoints with N/A reasons. Set `hil_enabled=false` when no material user clarification is needed; AI agents evaluate the interface evidence.
3. Follow `completion_contract`: inspect and rate every remaining applicable checklist item, or document genuine out-of-scope N/A with its reason. Continue to the full grade and HTML; a partial artifact is interim output. Only a concrete access blocker justifies stopping incomplete. Resolve human-loop gates only when enabled and relevant.
4. Use `report_ready_payload` or the full scored audit payload.
5. Run `validate_ux_report_payload`.
6. Only if ready, call `generate_ux_audit_report`, keeping the HTML viewer enabled. Resolve report identity before rendering: explicit user choice first, then the evaluated site/client/project identity, then an eligible private host default. Prefer `report_brand_path` for a supplied or source-grounded site/client binding; do not apply an unrelated host brand to a client report. A minimal local binding has the actual logo and optional CSS, with optional font/decorative assets. `auto` loads the configured host default, not an automatic site-brand detector. Use `report_brand="generic"` only when requested or when the correct identity assets cannot be resolved, and disclose that limitation. Identity changes never reduce report depth. For an explicitly requested stakeholder/developer export without the assistant handoff prompt, pass `include_remediation_prompt=false`. This omits the copy prompt and its navigation/control/print content across HTML, Markdown and PDF while retaining the complete assessment and recommendations. Leave it enabled by default.
7. Check `artifact_delivery.primary_artifact.path` (or `viewer_path` on older runtimes), verify that the HTML file exists, and open it in the host's native file panel. Give that clickable absolute HTML path as the primary report link in the final response. Summarize the findings and state full versus partial evidence coverage. A payload JSON reference, local generation, or a Markdown summary does not establish HTML delivery; generated artifacts also do not establish rendered visual QA.

Keep the main supplied findings in `payload.findings` with canonical checklist IDs and evidence refs before validating. The renderer retains that array, including in partial reports; it cannot incorporate a separate prose report automatically. Preserve the detailed issue, impact, recommendation and acceptance checks rather than delivering only the scored checklist. Never fill unknown ratings to earn a full label.

### Advanced Agent Audit

1. Confirm platform, user task, and optional profile mode.
2. Ask beginning human-loop questions if required.
3. Use Work Management's installed `worker-delegation` owner and `references/decision-council.md` for an optional independent reviewer pass. Separate worker execution before claiming independence; if one assistant generates all scorecards, label them single-assistant perspective scorecards.
4. Submit those scorecards with `run_agent_audit` only when aggregation is useful.
5. Treat consensus and disagreement flags as diagnostics. Check findings against observed evidence and preserve consequential dissent; aggregation does not establish truth, representative user outcomes or calibrated confidence.
6. Critique consequential findings with the existing `stress_test_heuristic_finding` route and [evaluator bias guard](evaluator-bias-guard.md), then recheck affected evidence. Do not claim real user testing.

## Browser And Source Boundaries

UXHC source prep can support bounded public URL capture, but it is not a crawler or autonomous browser agent.

Respect these boundaries:

- no full-site crawling
- no authenticated flows
- no competitor scraping by default
- no uncontrolled navigation
- no killing or taking over browser sessions owned by another host
- no treating synthetic walkthroughs as participant evidence

## Report Readiness Guardrails

Before report generation, confirm:

- source manifest is ready
- platform is present
- active heuristics are named
- checklist ratings include stable IDs or evidence limits
- ratings use 0-4 severity
- rationales, evidence refs, confidence, and evidence limits are present
- grade fields match UXHC scoring rules
- optional profiles have ratings or explicit non-evaluability records

Each `checklist_ratings` entry requires these fields or validation will block:

| Field | Required | Notes |
| --- | --- | --- |
| `checklist_item_id` | Yes | e.g. `h01_d_01` |
| `heuristic_id` | Yes | e.g. `h01` |
| `platform` | Yes | `desktop` or `mobile` |
| `rating` | For rated rows | Integer 0-4. Omit for verified N/A; never use 0 for unobserved evidence. |
| `rationale` | Yes | Plain-language reason for the score |
| `evidence_refs` | Yes unless `evidence_limits` explains the gap | List of evidence strings |
| `confidence` | Yes | `high`, `medium`, or `low` |
| `evidence_limits` | Optional but required when evidence refs are unavailable | Describe what could not be observed |
| `rating_status` | For N/A rows | `not_applicable`; use only when the checklist item genuinely cannot apply to the declared surface. |
| `applicability_reason` | For N/A rows | Document the concrete surface/flow basis. The scorer requires a reason but cannot verify its truth; the host must check it against evidence. |

Use the `checklist_rating_contract` from default `get_started()` as the rated-field reference. Do not assemble ratings manually from scratch. Prefer the `checklist_ratings` array returned in the `scorecard` from `audit_ux_surface`, which already includes all required fields.

If validation blocks the report, return the blockers and the smallest resubmission path. Do not generate polished artifacts from a blocked payload.

For a full field guide, use `references/report-payload-field-guide.md`.

## Output Size and Token Management

Two UXHC tools produce large output that can overflow context:

**`list_heuristics`**
- Brief output: ~8KB over the MCP wire; use `detail_level: "brief"` for profile/rubric routing
- Summary output: ~47KB over the MCP wire; use when heuristic descriptions and support-lens overview are needed
- Full detail output: can exceed 100KB
- Use full detail only when you need every checklist item's text and ID for a manual audit submission
- If output is auto-saved to a file, use `jq` to extract targeted sections:
  ```bash
  jq '.heuristics[] | {id, name, item_count}' output.txt
  jq '[.heuristics[] | select(.id == "h11")]' output.txt
  ```

**`audit_ux_surface`**
- Full output on all-profile desktop audit: ~400–500KB
- Use `output_detail: "compact"` when only scores and top findings are needed
- The full file is saved locally — use `jq` to extract what you need:
  ```bash
  jq '{overall_grade, overall_percentage, hil_state}' output.txt
  jq '[.heuristic_scores[] | {id, grade, percentage, top_finding}]' output.txt
  jq '[.top_findings[] | {severity, title, heuristic_id, fix}]' output.txt
  jq '.scorecard.checklist_ratings' output.txt
  ```

## Profile Aliases

Default `get_started()` returns a `profile_aliases` map. These aliases are accepted in profile activation params:

| Alias | Resolves to |
| --- | --- |
| `empathy` | `inclusion` (H12) |
| `content_strategy` | `ux_writing` (H14) |
| `a11y` | `accessibility` (H11) |
| `cx` | `journey` (H13) |

Use canonical profile IDs in final audit calls. Aliases are for convenience in conversation and quick prompts.

## After The Audit: Real Research Handoffs

UXHC can prepare a user for real research, but it should not pretend synthetic walkthroughs are participant evidence.

When the audit reveals issues that need real users, hand the observed questions to the current UX research specialist for a study plan, task scenarios, and participant criteria. Use the authorized project-specific specialist only when the current task supplies that context. Do not treat the historical `task-templates:*` labels as installed skills.

When H11 surfaces severity 3-4 accessibility issues, recommend a formal accessibility/WCAG pass. Keep the boundary clear: UXHC flags likely risks; it does not certify compliance.

## Optional Atlas Pattern Handoffs

The IDs below are historical knowledge-atlas references, not guaranteed callable skill names. Resolve them only when the current Atlas tool is exposed and the lookup helps this audit. Otherwise use the plain-language method in the right column without claiming a lookup.

| UXHC need | Atlas ID | How to use it |
| --- | --- | --- |
| Inclusion and Persona Spectrum calibration | `patterns:inclusive-design-framework` | Use with H12 and the Inclusion reviewer to compare permanent, temporary, and situational constraints. |
| Accessibility escalation | `patterns:accessibility-reality-check` | Use after H11 severity 3-4 findings to produce a deeper fix list or engineering handoff. |
| Ability-cost severity calibration | `patterns:fogg-behavior-model-fbm` | Use with H7 and H13 when low ability, low bandwidth, or high cognitive load changes severity. |
| Evaluator bias preflight | `patterns:heuristics-biases-preflight` | Use before accepting severe or surprising findings. |
| Cognitive debiasing | `patterns:cognitive-debiasing` | Use to seek disconfirming evidence and reduce confirmation bias before report generation. |
