---
name: design-review
description: "Critique, audit or polish a visible interface using observed design, accessibility and performance evidence."
---

# Design review

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


Critique, audit or polish a visible interface using observed design, accessibility and performance evidence.

## Complete procedures to load

Select by the triggers below. Read the complete chosen procedure and its required support; skip unrelated variants. These links preserve the full methods.

- [Complete critique playbook](../../runtime/impeccable/skill/reference/critique.md) — For an evidence-backed design critique; structure and prioritization of findings.
- [Complete audit playbook](../../runtime/impeccable/skill/reference/audit.md) — For a web interface audit; technical and usability inspection.
- [Complete audit.native playbook](../../runtime/impeccable/skill/reference/audit.native.md) — For a native application audit; platform-specific checks instead of the web variant.
- [Complete polish playbook](../../runtime/impeccable/skill/reference/polish.md) — For authorized visual polish; bounded refinements and verification.
- [Complete component-review playbook](../../runtime/impeccable/skill/reference/component-review.md) — For one component; examine its states, reuse and implementation.
- [Edit-time craft floor](../../runtime/impeccable/skill/reference/craft-floor.md) — When editing UI; minimum craft and verification checks.
- [Owned runtime and hooks](../../docs/design-runtime.md) — Only when invoking or maintaining the detector, live variants or hooks; supported adapter commands.

For an accessibility finding or requested accessibility verification, read [flow-bound accessibility evidence](references/accessibility-evidence.md). It binds the existing full methods to observed keyboard/manual checks and the same path after fixes; it does not add a whole-product conformance claim.

## Workflow

1. Choose critique, technical audit or authorized polish from the requested result. Read the complete selected procedure.
2. Capture source/viewport/region anchors. For a sibling surface, compare its rendered state with the related prior design at the same viewport and theme where available; flag unintended system drift and label any unavailable baseline. Tie each finding to an observed behavior or rendered defect and concrete user impact. Separate observation, participant self-report and reviewer inference; an emotion inference needs an alternative explanation and a test.
3. For fixes, batch material corrections and confirm changed anchors. For review-only tasks, deliver findings without editing.

When the same control or card appears on sibling surfaces, compare its visible
label/icon, accessible name, placement and relevant interaction at the same
viewport/theme. Shared CSS does not establish matching markup or behavior.
Before implementing a new sibling page or repeated visitor action, note the
incumbent screen/viewport, action name, destination or panel behavior, proposed
counterpart and any task-based reason to differ in the existing anchor record.
Recheck both rendered paths after the change. Translate production prompts and
review records into visitor-facing purpose and status unless the page explicitly
serves a technical source-reading task.
Reuse a common implementation when practical, or check the duplicate instances
explicitly; keep intentional differences tied to a user task. Preserve useful
downloads and facts in the accepted layout rather than hiding them merely to
reduce the amount visible. An accordion or tab needs a task-based reason and a
verified keyboard/focus path.

For a reusable template, content projection or component-contract review, apply
the [contract review cases](../design-systems/references/template-design-contract.md#review-preconditions-and-deliberately-failing-cases). Confirm required assets and the expected state are loaded before interpreting fit; inspect relevant expanded content, long labels and keyboard focus. Retain claims, essential qualifications and evidence relationships through trimming. Reuse the owning project's checks; the matrix is not itself an executed test.

## Deliver and verify

Return prioritized evidence, correction and verification state. Use UX Heuristics Compass for its formal score/report contract.

For an in-chat MCP app widget, apply [compact widget acceptance](../design-studio/references/mcp-app-widgets.md#review): inspect the actual inline footprint, arrow navigation, progressive disclosure, keyboard/touch access and details, and distinguish backend-only retrieval from a deliberately opened human-facing app. Do not apply this layout wholesale to ordinary websites or full editors.

For charts, scales or trait scores, run the [reader-comprehension acceptance cases](../dashboard-design/references/delivery-and-qa.md#reader-comprehension-acceptance) on the actual rendered default and details views. Lay readers should understand the question, scale ends and middle, values/ranges and span meaning at a glance. Flag jargon, duplicate dimensions, high-is-good assumptions, blanket accordions, ordinary web reading text below 16px and targets mislabeled as observations. Preserve numerical and epistemic honesty; reviewer/model consensus is not empirical validity evidence.

## Example boundary

Good: show the clipped error label and its viewport. Bad: declare the interface inaccessible from a source inventory alone.

Use the owned native adapter in the runtime guide for detector/live/hook commands; do not execute an upstream downloader or silently register a second hook. The brief and verified incumbent design govern style. For edits, load the complete craft-floor playbook. Preserve function/content and perform bounded rendered checks of changed anchors.

For deeper internal workflows and retained licensed methods, select and **read the complete matching procedure** from [this workflow’s source map](../../docs/procedures/design-review.md), applying its [host adapter](../../docs/full-design-host-adapter.md). Load only the relevant method and required support.

For pointing, carried memory, feedback, interrupted work, consequential error, workload or emotion claims, select and read the complete task-matching card through [human-systems decisions](../design-studio/references/human-systems-decisions.md). This maintained guidance supersedes inherited fixed visible-option caps and checklist-count workload scores; it preserves useful effort and applies accessibility criteria at their stated conformance level.

For a bounded component/detail polish request involving nested corners, optical alignment, icon weight/render size, image edges, text wrapping or transition timing, read the [interface craft adapter](../design-studio/references/interface-craft.md) and its complete task-matching source method. It preserves the existing system and treats upstream values as testable examples, with no automatic runtime or global aesthetic mandate.

For generic-output, anti-slop, unsupported product imagery or content-to-layout concerns, read [context-sensitive design review](references/intentional-design.md) before applying inherited aesthetic flags. It requires a concrete consequence, protects legitimate conventions and allows retain/investigate outcomes; detector matches never establish authorship. Load matching patterns only. Narrow fixes remain narrow.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Design Quality Reviewer, Web Designer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
