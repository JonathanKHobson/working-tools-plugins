---
name: survey-flow-and-logic
description: "Design or debug survey blocks, skip/display logic, validation and collection paths."
---

# Survey flow and logic

For a supplied form, an optional Form Field Extractor can identify fields and normalize their names while preserving values. Treat its output as transcription to check against the source. It does not judge readiness, completeness, validation, approval or submission and must not replace the survey pilot/quality method. When absent, extract the stated fields directly and keep ambiguous or empty values visible. Never send live respondent records merely to inventory a blank instrument.

Design or debug survey blocks, skip/display logic, validation and collection paths.

## Complete procedures to load

Read the task-matching files below in full before applying that procedure. Load only the relevant variant and its required support. These contain the operative methods, examples and templates; this entrypoint does not replace them. A plugin is a package, not a requirement to read every skill.

- [Complete ordering-flow-and-logic procedure](../survey-strategist/references/ordering-flow-and-logic.md) — read for block order, skip/display rules and answer validation.
- [Complete survey-implementation procedure](../survey-strategist/references/survey-implementation.md) — read for platform behavior, collection paths and tested branches.
- [Canonical instrument contract](../../references/instrument-contract/instrument-contract.md) — read when reviewing or changing stable question IDs, codes and analysis lineage.

## Workflow

1. Map the respondent journey, eligibility and sensitive branches against the canonical instrument.
2. Apply the complete flow/programming procedures; preserve stable IDs and document platform-specific behavior.
3. Exercise reachable paths, skips, backtracking, errors and test-response columns before claiming field readiness.

## Deliver and verify

Return logic/programming notes and observed path/data checks with unsupported mappings explicit.

## Example boundary

Good: test that an ineligible respondent reaches the correct ending. Bad: infer branching works from a diagram alone.

Keep one canonical instrument in its owning project. Preserve decision → construct → question → coded value → analysis use. Never infer anonymity, scale validity, legal compliance or platform compatibility. For rendered deliverables verify the changed visual and respondent path; a schema check alone is insufficient.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Survey Researcher. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
