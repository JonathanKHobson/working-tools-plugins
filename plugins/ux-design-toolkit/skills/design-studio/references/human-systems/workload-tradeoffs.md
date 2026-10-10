# Human-systems method: adopted conditional research card

Integrated 2026-09-30. Read this complete card only for its trigger. The original evidence, examples, counterexamples, tradeoffs and proposed tests are retained below; historical pre-integration coverage statements remain provenance. Participant outcomes are not measured. Normative criteria apply at their stated level and with their exceptions, not as universal design formulas. Source IDs resolve in the linked ledger; user/course proposals remain attributed and unvalidated. Locators such as L27 and U09 identify audited sources, not mandatory private-file dependencies.

## HS-06 — Workload tradeoffs (not always "less")

- **Owner:** `design-review`, `dashboard-design` via the contract, `spreadsheet-usability`. Existing coverage: critique.md explicitly supports germane learning effort (lines 342–349), and UXHC H7 includes time pressure. Preserve both; replace the unsupported failed-item count as a workload severity measure with task-specific evaluation.
- **Trigger:** a recommendation to "simplify", "reduce clutter" or "minimize steps" on a surface used under time pressure, for monitoring, for learning, or for high-stakes decisions. Or a design that front-loads effort, for example a setup wizard for an expert tool.
- **User task:** sustain adequate performance at an acceptable human cost over the realistic duration of use.
- **Evidence:** X06 pp. 1–3 (method review): workload is multidimensional (mental, physical and temporal demand, frustration, effort, performance); workload and performance can dissociate; boredom can raise workload on undemanding vigilance tasks; modified subscales need re-validation. U07 [0014] (Kyle): keep useful engagement; L16 lines 342–349 already support germane learning effort. U10 [0011]–[0018]: physical-workspace findings transfer to screens only if tested.
- **Mechanism:** removing information can move work from the eye to the memory or to extra navigation (HS-02). Too little demand can reduce vigilance. Time pressure and frustration add workload even when the steps are few.
- **Decision rule:**
  1. Name the dominant dimension at risk (mental, physical, temporal, frustration, effort) and the use duration (glance, session, shift).
  2. For monitoring and glance use, keep ambient context visible (status, scope, last update) rather than hiding it for minimalism.
  3. For learning or reflective tasks, keep *germane* effort (work that builds understanding) and remove *extraneous* effort.
  4. For time-pressured tasks, move effort out of the critical moment through defaults, preparation and pre-filled context.
  5. State any workload claim as a hypothesis. Only participant ratings or measures during or after real tasks count as workload evidence.
- **When not to use:** don't cite workload to justify dense UIs for novices. Don't treat an AI "TLX estimate" as a measurement.
- **Competing considerations:** HS-02 co-location adds density; aesthetic minimalism (UXHC H8); expert versus novice modes.
- **Example:** a weekly occupancy monitor. The "minimal" version shows only exceptions below 60%. The recommended version adds a quiet "12 sessions checked, updated 09:12, weeks 1–8" line so the coordinator can trust that an empty exception list is a real result and not a failure (links to the lane01 empty-state contract).
- **Counterexample:** removing the scope and last-updated text because it "adds cognitive load". The person now has to open settings to confirm what they're looking at.
- **Accessibility and ethics:** workload interacts with disability, fatigue and language proficiency; calibrate with `severity-calibration-guide.md`. Engagement design must not raise effort to increase time-on-site.
- **Evaluation (not run):** if a study is run, ask participants for raw TLX-style self-ratings after each task alongside performance, and report the dissociation if it appears. Inspection check: each "simplify" recommendation names what moved where. Failure condition: a simplification that raises carried items (HS-02) or navigation.
- **Effort:** medium.

## Installed support

[Source ledger](../../assets/human-systems/sources.json), [complete evaluation tasks](../../assets/human-systems/evaluation.md), [limits and unresolved terminology](../../assets/human-systems/unresolved.md). [Comparison case](../../assets/human-systems/examples/case-1-dashboard-comparison.md), [interrupted-work case](../../assets/human-systems/examples/case-2-interrupted-work-recovery.md), [neutral-research case](../../assets/human-systems/examples/case-3-neutral-survey-vs-persuasion.md), [optional PCEA worksheet](../../assets/human-systems/examples/pcea-task-worksheet.md).

The existing [consequence-copy method](../ux-writing.md), [risk/recovery matrix](../../../../libraries/frontend-design-premium/skills/frontend-design-premium/references/decision-matrix.md), and [current accessibility checks](../verification.md) remain their respective authorities. Resolve former audit paths through this plugin and its preserved libraries; do not infer participant results from these examples.
