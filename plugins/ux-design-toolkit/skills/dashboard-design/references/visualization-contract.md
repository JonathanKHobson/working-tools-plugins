# Visualization contract

Map these fields onto the owning project's brief and specification. Keep it compact; omit irrelevant fields and preserve established schema names.

| Concern | Record before it can change meaning |
| --- | --- |
| Reader and purpose | Question, intended decision, monitoring/exploration/explanation mode; priority of each view |
| Evidence | Source/version, freshness, period/timezone, population, exclusions, grain, missing/suppressed/estimated status; sensitivity and permitted sharing |
| Metric | Formula, numerator, denominator, aggregation, weighting, deduplication, unit, comparison window, direction of favorable change |
| Comparison | Entity identities, natural or ranked order, peer versus focal emphasis, panel relationships |
| Encoding | Chart and field mapping, baseline/domain, transformation, intervals, missingness and observed/forecast distinction |
| Color | Surface/text tokens, unordered identities, ordered magnitude or defensible diverging reference, selection/status; redundant cues |
| Annotation | Source evidence or calculation, dependencies on filters/period/units, behavior when evidence becomes invalid |
| Customization | Allowed presentation changes, exploration controls, explicit semantic changes, validation/reset and persistence version |
| Delivery | Mobile reading order, text/table alternative, promised file/site mode, export scope, locally bundled assets |
| Acceptance | Known answers, interaction outcomes, visual anchors, accessibility checks, external-request expectations and evidence limits |

Never infer exact source data from a screenshot when authoritative data is available. Image recovery is approximate and must be labeled. Synthetic fixtures must remain visibly synthetic and never become product evidence.

## Arithmetic fixture for weighted rates

Two disjoint groups: A has 40 completions / 50 participants; B has 9 / 10. The pooled participant rate is 49 / 60 = 81.666…%, normally displayed as 81.7%. An equal-weight mean of the group rates is 85%; that is a different metric and needs that explicit definition. Filtering to B yields 90% and n=10. Hide A without filtering the population and the pooled denominator remains 60. If a denominator is zero, represent the rate as undefined, not 0%.

From 80% to 90% is +10 percentage points, or +12.5% relative change. Compute before rounding. Compare equivalent periods; a partial current month is not directly equivalent to a complete previous month without qualification.

## State acceptance example

Changing region must update every dependent mark, total, denominator, accessible table, computed claim and export. Changing theme must preserve the same metric values and category identities. Saving and restoring configuration must restore only its declared settings, reject unsupported versions safely, and not execute imported content. A persisted setting is not proof that the rendered chart applied it.

## Human-systems requirements mapped to this contract

For an interactive dashboard or widget, map the relevant requirement below into the project's existing fields; do not add an always-required parallel schema. The [original ten-requirement research handoff](../../design-studio/assets/human-systems/dashboard-handoff-proposal.md) is retained as dated proposal evidence. This table resolves its previously unknown mapping and scopes prototype assumptions. Read the linked complete human-systems cards when the decision needs their rationale, examples or exceptions.

| Handoff requirement | Existing field / decision | Observable acceptance |
| --- | --- | --- |
| 1. Carried-item count | Comparison + Acceptance: [carried memory](../../design-studio/references/human-systems/carried-memory.md). List what a person must retain across view changes before and after the design; reduce unnecessary retention, without claiming every task must reach zero. | Task walkthrough shows comparable identities, units/scales and co-visible values or a reliable external comparison aid. Visible information still requires reading and integration. |
| 2. Scope and freshness | Evidence + Annotation: show active filters/range, selected versus eligible population and meaningful freshness beside results, including empty/error states. A static source uses its actual version/date; do not invent live updates. | Default, filtered, empty and error paths retain scope; reachable Reset restores its declared scope. |
| 3. Rating with its base | Metric + Evidence: survey means travel with exact response count, scale, period and comparability caveat; missing stays missing. No universal n cutoff or significance claim. Other assessment types use their actual provenance, not a fabricated respondent count. | Inspect every displayed instance, computed comparison and export; no unsupported reliability claim. |
| 4. Consequence before commit | Customization + Annotation: [action feedback](../../design-studio/references/human-systems/action-feedback.md). State what a scenario/analytic action will change, where, and by how much when calculable; distinguish source from hypothetical values. | Preview agrees with result; status is clear; restoring source actually restores it. Do not invent a numeric prediction for an unquantified action. |
| 5. Consequential-action mechanism | Customization + Acceptance: use [the existing risk matrix through this card](../../design-studio/references/human-systems/consequential-error.md). Map each consequential action to prevention, review/confirmation or reliable undo; temporary scenarios remain reversible. | Action inventory and actual recovery check; a source-data commit has an explicit consequence/scope review. No generic modal on each frequent reversible edit. |
| 6. Resumption | Customization + Acceptance: [task resumption](../../design-studio/references/human-systems/task-resumption.md). Declare the draft/scenario persistence boundary and retention/privacy rules; capture progressively, reconcile stale records and permissions, and restore a cue as well as values. | Force relevant navigation, timeout and re-authentication paths. If persistence is promised, verify it; an in-memory undo stack does not prove survival. On shared devices authenticate before revealing private drafts. |
| 7. Pointer, keyboard and dragging | Delivery + Acceptance: [target acquisition](../../design-studio/references/human-systems/target-acquisition.md) and existing accessibility verification. Apply the actual WCAG criterion/exceptions, a single-pointer alternative to dragging, keyboard access, and separation of destructive targets. | Measure hit areas and run core tasks by keyboard and non-drag pointer at target viewports. The research fixture's 390px check is one test viewport, not the complete reflow standard. |
| 8. Announced status | Annotation + Acceptance: expose applicable result counts, scenario changes, errors and completion as perceivable status without stealing focus. | Inspect accessible semantics and use a screen reader where available. Distinguish an accessibility-tree inspection from an executed assistive-technology test; mark unrun checks explicitly. |
| 9. Workload rationale | Reader and purpose + Delivery: [workload tradeoffs](../../design-studio/references/human-systems/workload-tradeoffs.md). Name mental, physical, temporal or other relevant demand and the duration/context when changing density or depth. | Every simplification states what moved where; participant workload and task performance are separate outcomes, unmeasured until actually tested. |
| 10. Emotion evidence | Evidence + Acceptance: [emotion evidence](../../design-studio/references/human-systems/emotion-evidence.md). Separate observed behavior, self-report and reviewer inference. | Audit emotional claims; screenshots do not establish feelings. Record alternative explanations and a research question for inferences. |

Correctness, source/scenario integrity, safety and applicable accessibility are gates; aesthetic preferences do not override them. Other conflicts are explicit task tradeoffs. UX owns task and human-interaction judgments; Data Visualization owns encoding, formulas and chart implementation; Graphic Design owns composition craft. A human-performance claim requires actual evidence, not merely citing a card ID. Rhetorical emotion in Writing or Marketing is not participant-emotion evidence. Collaborative, shared-device and environmental performance claims remain hypotheses unless task-specific evidence supports them.
