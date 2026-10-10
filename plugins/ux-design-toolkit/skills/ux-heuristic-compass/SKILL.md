---
name: ux-heuristic-compass
description: Run formal UX Heuristics Compass audits with the 14-heuristic rubric, evidence limits, audience-calibrated severity and structured reports. Use when evidence-backed usability triage, graded evaluation, or a release/handoff audit helps the task; ordinary UI fixes belong to design-studio.
---
# UX Heuristics Compass

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


The user need not mention UXHC by name. Select it for a relevant authorized interface evaluation and explain the expected evidence, fixes or report briefly. Use compact startup and a bounded quick scan for triage; propose a full audit only when its depth serves the requested decision. Ask platform for each new audit, retaining a platform already confirmed for that audit. Human checkpoints show their current findings preview before reflection questions and use a supported answer acknowledgment; accepted calls alone do not prove that questions were visible.

Identify the supplied interface evidence, user task, audience, platform and requested audit depth. Infer routine context from the task; ask only for missing facts that materially change the evaluation. Honor existing authorization. Inspect a bounded surface rather than silently expanding to a whole site.

For a task that crosses an entry state, evaluate the whole bounded path from first direct link through the confirmed outcome, including delayed loading, the available primary action, duplicate or competing actions, action feedback and recovery. A screenshot or rubric inventory can suggest risks but cannot establish that journey. Record which states were actually exercised and the evidence for each; mark the others unverified. Distinguish an available or invoked UXHC tool from a completed audit with observed findings and validation.

For a standalone audit read [the checklist](references/heuristics-checklist.md), then the [severity guide](references/severity-calibration-guide.md) as needed. Rate findings 0–4, distinguish observation from inference, and state which states or populations were not observed. Screenshots cannot establish keyboard behavior, real participant outcomes or accessibility conformance. Check [evaluator bias](references/evaluator-bias-guard.md) for severe or uncertain findings. Before finalizing consequential findings, run its bounded critique pass with the existing `stress_test_heuristic_finding` tool when callable, then verify the claim against observed evidence; tool output alone does not settle severity.

When UXHC MCP tools are callable, use the existing `ux-heuristic-compass` server for structured evidence, scoring, report validation and artifacts. Read [the bridge](references/mcp-bridge.md), call `get_started(topic="brief")` once for ordinary startup, and request default `get_started()` or `get_started(topic="tools")` only when their deeper contracts are needed. Use `list_heuristics(detail_level="brief")` to choose profiles, then request `summary` or `full` only for the descriptions or item IDs needed. Formal report work uses [payload fields](references/report-payload-field-guide.md) and [report design](references/report-design-system/design.md); validate before generating. Do not improvise field names or report HTML to bypass a failing validator. Current user authorization and host instructions govern any requested pause; never manufacture a tool the host does not expose.

Report the most consequential findings with location/evidence, relevant heuristic, severity, user impact, concrete fix and validation need. Preserve successful aspects. A quick scan need not assign a score; a complete score requires the rubric's evidence and rating coverage. Synthetic personas or walkthroughs are hypotheses, not participants.

For competing fixes or simulated task contexts, read [decision alternatives](../design-studio/references/decision-alternatives.md). Optional independent review follows Work Management's shared method; single-assistant lenses are labeled, and agreement is not user evidence.

Advanced aggregation roles, source preparation and examples remain in [the reference workflow](REFERENCE-WORKFLOW.md). Read only the section needed for that requested mode. `design-studio` owns routine implementation and visual polish; `ux-writer` owns copy-only changes.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Design Quality Reviewer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
