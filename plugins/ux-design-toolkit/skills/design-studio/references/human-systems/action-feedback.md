# Human-systems method: adopted conditional research card

Integrated 2026-09-30. Read this complete card only for its trigger. The original evidence, examples, counterexamples, tradeoffs and proposed tests are retained below; historical pre-integration coverage statements remain provenance. Participant outcomes are not measured. Normative criteria apply at their stated level and with their exceptions, not as universal design formulas. Source IDs resolve in the linked ledger; user/course proposals remain attributed and unvalidated. Locators such as L27 and U09 identify audited sources, not mandatory private-file dependencies.

## HS-03 — Feedforward, feedback and control–display mapping

- **Owner:** `design-review`, `interaction-resilience`, `ux-writer` for consequence labels. Existing coverage: L26 requires consequence copy before confirmation; UXHC H1 covers feedback and H2 covers real-world match. This card checks non-obvious task controls and whether feedback appears in the affected context.
- **Trigger:** an action whose result isn't visible before or after it happens. Typical cases: a scenario control that changes numbers elsewhere; a "Continue" whose effect is unclear (L08's benefits-form example); a toggle whose direction is ambiguous; a background operation with no completion signal (Kyle's "open-loop" concern, U09 [0016]–[0018]); a slider that moves a chart in an unexpected direction.
- **User task:** choose an action with a correct expectation, then confirm that it did what was intended.
- **Evidence:** L26 already calls for consequences before confirmation. X10 (conceptual framework): feedforward shows the result before action (Gulf of Execution); feedback shows what happened (Gulf of Evaluation); perceived affordances invite an action but don't say its purpose. X12 #1: timely feedback. X03 4.1.3: status messages must be available to assistive technology without moving focus. Mapping (stimulus–response compatibility) is included as standard human-factors guidance, but no primary source was inspected; it is treated as a hypothesis to test.
- **Mechanism:** if people can predict the outcome, they make fewer wrong choices. If they can see the outcome, errors are caught early and the loop closes.
- **Decision rule:**
  1. For every consequential or non-obvious action, write the **feedforward**: label, preview or ghost state saying what will change, where, and by how much. Examples: "Set capacity to 40 (scenario only, source unchanged)"; a preview line on the chart.
  2. Provide **feedback** in the same place the person is looking, and announce it (4.1.3). Distinguish pending, success and failure (already in L01).
  3. Check **mapping**: the control's direction, position and grouping should match the displayed effect. Examples: slider right = more; a filter control next to the chart it filters; the scope indicator next to the results.
  4. Never create *false* feedforward, where a preview differs from the outcome. That is worse than none.
- **When not to use:** trivial, instantly reversible actions where the result *is* the preview (a hover highlight). Don't add confirmation text to every button.
- **Competing considerations:** preview latency and computational cost; verbosity; previews on mobile competing for space.
- **Example:** a capacity scenario slider. Before: moving it silently changes occupancy percentages in four panels. After: while dragging (or on keyboard arrow press), a "Scenario: capacity 30 → 40, occupancy 47% → 35%" chip appears next to the slider. The affected panels show a dashed "scenario" outline, and "Restore original" is visible.
- **Counterexample:** a toast reading "Updated!" on a different part of the screen. It's feedback without specificity, outside the person's attention, and not announced.
- **Accessibility and ethics:** feedforward must not be persuasive framing. For example, "Save 20%!" as a preview of a subscription upgrade is marketing, not consequence disclosure. Previews must be available to keyboard and screen-reader users.
- **Evaluation (not run):** a prediction probe with participants: "What will happen if you press this?" before the action, plus a count of immediate reversals after it. Inspection evidence: check that each consequential action lists its feedforward and feedback. Failure condition: predictions don't improve, or the preview is misread as the committed state.
- **Effort:** small.

## Installed support

[Source ledger](../../assets/human-systems/sources.json), [complete evaluation tasks](../../assets/human-systems/evaluation.md), [limits and unresolved terminology](../../assets/human-systems/unresolved.md). [Comparison case](../../assets/human-systems/examples/case-1-dashboard-comparison.md), [interrupted-work case](../../assets/human-systems/examples/case-2-interrupted-work-recovery.md), [neutral-research case](../../assets/human-systems/examples/case-3-neutral-survey-vs-persuasion.md), [optional PCEA worksheet](../../assets/human-systems/examples/pcea-task-worksheet.md).

The existing [consequence-copy method](../ux-writing.md), [risk/recovery matrix](../../../../libraries/frontend-design-premium/skills/frontend-design-premium/references/decision-matrix.md), and [current accessibility checks](../verification.md) remain their respective authorities. Resolve former audit paths through this plugin and its preserved libraries; do not infer participant results from these examples.
