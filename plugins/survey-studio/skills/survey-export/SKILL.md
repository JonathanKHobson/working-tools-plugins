---
name: survey-export
description: "Convert a canonical survey into requested documents or platform imports while preserving IDs, codes, logic and known limitations."
---

# Survey export

Convert a canonical survey into requested documents or platform imports while preserving IDs, codes, logic and known limitations.

## Complete procedures to load

Read the task-matching files below in full before applying that procedure. Load only the relevant variant and its required support. These contain the operative methods, examples and templates; this entrypoint does not replace them. A plugin is a package, not a requirement to read every skill.

- [Complete export-selection procedure](../survey-strategist/references/export-selection.md) when choosing among instrument export formats.
- [Complete limitations-and-platform-caveats procedure](../survey-strategist/references/limitations-and-platform-caveats.md) when stating unsupported mappings or import limits.
- [Complete workflow-qualtrics procedure](../survey-strategist/references/workflow-qualtrics.md) only for a Qualtrics destination.
- [Canonical instrument contract](../../references/instrument-contract/instrument-contract.md) when reading or updating the source instrument.
- [Existing deterministic tools](../../references/instrument-contract/deterministic-tools.md) when running a local exporter or validator.

## Workflow

1. Distinguish instrument export from response-data export and select the required format.
2. Read its complete format-specific guide selected by export-selection, then use the preserved exporter and validation tools.
3. Check warnings, unsupported mappings, encoding and platform import/preview when applicable. Never synthesize unsupported QSF.

## Deliver and verify

Deliver canonical source and requested validated exports plus warning manifest; distinguish generated file from tested platform import.

## Example boundary

Good: inspect a Qualtrics TXT import and test-response columns. Bad: call a descriptive unsupported-type placeholder interactive.

Keep one canonical instrument in its owning project. Preserve decision → construct → question → coded value → analysis use. Never infer anonymity, scale validity, legal compliance or platform compatibility. For rendered deliverables verify the changed visual and respondent path; a schema check alone is insufficient.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Survey Researcher. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
