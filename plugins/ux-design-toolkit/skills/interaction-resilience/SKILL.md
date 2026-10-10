---
name: interaction-resilience
description: "Design first-use flows and robust interface states for empty data, errors, recovery, retries and interrupted actions."
---

# Interaction resilience

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


Design first-use flows and robust interface states for empty data, errors, recovery, retries and interrupted actions.

## Complete procedures to load

Select by the triggers below. Read the complete chosen procedure and its required support; skip unrelated variants. These links preserve the full methods.

- [Complete onboard playbook](../../runtime/impeccable/skill/reference/onboard.md) — For first-use or first-value flows; introduction and useful initial action.
- [Complete harden playbook](../../runtime/impeccable/skill/reference/harden.md) — For malformed input, async errors, retries or recovery; resilient states.
- [Complete operate playbook](../../runtime/impeccable/skill/reference/operate.md) — For operational interface states and workflows; task continuity.
- [Edit-time craft floor](../../runtime/impeccable/skill/reference/craft-floor.md) — When editing UI; minimum craft and verification checks.
- [Owned runtime and hooks](../../docs/design-runtime.md) — Only when invoking or maintaining the detector, live variants or hooks; supported adapter commands.

## Workflow

1. Identify the user’s task and failure/recovery states from current behavior and data constraints.
2. Apply onboarding for first-value work or hardening for error/async/i18n edges; read the complete matching playbook.
3. Test the main action and changed non-happy paths, including empty and repeated clicks. Inspect feedback on the invoking control as well as any adjacent status, preserving work and distinguishing pending, confirmed success, unchanged/no-op and failure.

## Deliver and verify

Deliver the implemented or specified state transitions, recovery copy and observed checks.

## Feedback lifetime during visual cleanup

Before removing apparently duplicated or overlapping feedback, identify its trigger, placement, duration and clearing condition from the user's intent or existing behavior. A static frame may show a brief overlay and a persistent field warning simultaneously. Similar wording does not make their roles interchangeable. Preserve a specified overlay without introducing page reflow; if timing is unknown, flag the uncertainty instead of deleting the layer as a cosmetic fix.

Choose severity styling from the consequence and recovery path, using the incumbent palette. A recoverable eligibility limitation may merit amber; this is a contextual decision, not a rule that every validation error must be amber. Matching severity colors can coexist with different lifetimes. Keep explicit wording and an icon where appropriate; color alone cannot explain status.

Example: a top notice disappears after a few seconds, while the related inline warning remains until the problem is resolved. A recolor changes neither lifetime. Verify appearance in the design and timing/clearing in an interactive implementation separately; a static mockup proves only the former.

## Example boundary

Good: retain an unsent form after a retryable failure. Bad: show success before the server accepts the operation.

Use the owned native adapter in the runtime guide for detector/live/hook commands; do not execute an upstream downloader or silently register a second hook. The brief and verified incumbent design govern style. For edits, load the complete craft-floor playbook. Preserve function/content and perform bounded rendered checks of changed anchors.

For methods inherited from Product Design, Frontend Design Premium, Design Partner, UXCritique or UI UX Designer, select and **read the complete matching procedure** from [this workflow’s source map](../../docs/procedures/interaction-resilience.md), applying its [host adapter](../../docs/full-design-host-adapter.md). Load only the relevant method and required support.

For an exploration sequence with committed filters, pins or scenarios, read the full [exploration recovery method](../design-studio/references/exploration-recovery.md). Include the actual task’s resumption and recovery requirements; a single reversible toggle does not require a history system.

For pointing, carried memory, feedback, interrupted work, consequential error, workload or emotion claims, select and read the complete task-matching card through [human-systems decisions](../design-studio/references/human-systems-decisions.md). This maintained guidance supersedes inherited fixed visible-option caps and checklist-count workload scores; it preserves useful effort and applies accessibility criteria at their stated conformance level.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports UX Designer, Web Designer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
