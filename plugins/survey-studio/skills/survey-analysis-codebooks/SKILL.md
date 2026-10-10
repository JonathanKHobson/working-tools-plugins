---
name: survey-analysis-codebooks
description: "Plan survey metrics and create codebooks or response-data exports with stable variable definitions and analysis rules."
---

# Survey analysis codebooks

Plan survey metrics and create codebooks or response-data exports with stable variable definitions and analysis rules.

## Complete procedures to load

Read the task-matching files below in full before applying that procedure. Load only the relevant variant and its required support. These contain the operative methods, examples and templates; this entrypoint does not replace them. A plugin is a package, not a requirement to read every skill.

- [Complete analysis-planning-and-codebooks procedure](../survey-strategist/references/analysis-planning-and-codebooks.md) — read for variable definitions, metrics, codebooks and missing-data rules.
- [Complete response-data-exports procedure](../survey-strategist/references/response-data-exports.md) — read for response rows, column mappings or export checks.
- [Canonical instrument contract](../../references/instrument-contract/instrument-contract.md) — read when reviewing or changing stable question IDs, codes and analysis lineage.
- [Existing deterministic tools](../../references/instrument-contract/deterministic-tools.md) — read when a local validator, burden checker or exporter is needed.

## Workflow

1. Define decisions, metrics, segments, missing-data and exclusion rules before interpreting responses.
2. Apply the complete analysis/codebook procedures; use the canonical IDs/codes and preserved generation scripts.
3. Check export columns and categorical mappings against actual responses; separate coding errors from respondent missingness.

## Deliver and verify

Return the analysis plan, codebook and requested response-data format with reproducible mappings and limits.

## Example boundary

Good: preserve a code’s meaning across exports. Bad: recode missing responses as zero without an analysis rule.

Keep one canonical instrument in its owning project. Preserve decision → construct → question → coded value → analysis use. Never infer anonymity, scale validity, legal compliance or platform compatibility. For rendered deliverables verify the changed visual and respondent path; a schema check alone is insufficient.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Data Analyst. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
