# Human-systems method: adopted conditional research card

Integrated 2026-09-30. Read this complete card only for its trigger. The original evidence, examples, counterexamples, tradeoffs and proposed tests are retained below; historical pre-integration coverage statements remain provenance. Participant outcomes are not measured. Normative criteria apply at their stated level and with their exceptions, not as universal design formulas. Source IDs resolve in the linked ledger; user/course proposals remain attributed and unvalidated. Locators such as L27 and U09 identify audited sources, not mandatory private-file dependencies.

## HS-01 — Target acquisition cost (Fitts' law, correctly scoped)

- **Owner:** ux-design-toolkit `design-review`, `responsive-design`. Overlaps: `design-studio/references/verification.md` (target size), Impeccable `adapt.md`.
- **Trigger (observable):** people repeatedly point at the *same known* targets under time pressure, and those targets are small, far from the preceding action, or crowded by neighbors. Typical cases: row actions in a dense table, a frequent toolbar button at the far edge of a wide display, a small slider thumb, adjacent destructive and benign icons.
- **User task:** rapidly select a known target that they already intend to use.
- **Evidence:** X01 pp. 751–756 (empirical review). Movement time grows with distance and shrinks with width, but only for rapid aimed movements. It excludes reaction, homing and dwell time. People trade speed for accuracy, so report both. X03 is normative for the WCAG 2.2 floor: 24×24 CSS px AA with exceptions and 44×44 AAA; X04 is informative guidance. A 44px design convention may still help the audience. Kyle's source is U09 [0010]–[0012]. X02, the original, was not read.
- **Mechanism:** a larger effective width or a shorter distance reduces the precision needed per movement. Mis-hits on crowded targets are a speed–accuracy failure, not carelessness.
- **Decision rule:**
  1. Confirm that the problem really is *acquisition*. If people hesitate before moving, the problem is finding the target or deciding what to do; route that to HS-02 or HS-03 instead.
  2. Prefer enlarging the *hit area*, which can extend beyond the visible glyph. Move frequent targets toward the preceding focus or action. Separate destructive targets from frequent benign ones.
  3. Keep the WCAG 2.5.8 floor (or its spacing exception). For motor-constrained or touch-primary audiences, move toward 2.5.5 and state the audience reason.
  4. Where dragging is involved, provide a single-pointer non-drag alternative (2.5.7). Offer a keyboard path for expert repetition so pointing isn't the only route.
- **When not to use:** exploration, reading, search or first-time decisions. Keyboard-only or voice-driven tasks. Don't cite Fitts to justify a bigger primary CTA on a marketing page; that is a visual-hierarchy or persuasion choice.
- **Competing considerations:** density versus larger targets in expert data tools; screen real estate; accidental activation when targets grow into each other; enlarging one target can push others away.
- **Example:** a coordinator adjusts capacity for 12 sessions using 16px "+/−" icons sitting 4px apart at the far right of each row. The proposed change is a 24×24 minimum hit area with 8px separation, the step control placed next to the value it changes, and a typed-entry alternative. Evaluate with time per adjustment *and* wrong-row or wrong-sign errors.
- **Counterexample:** "Fitts' law says make every button 44px" applied to a dense analytics table. It halves visible rows and forces more scrolling, and scrolling is also movement cost. It also presents an AAA option as a universal law, although 44px can be a useful design convention in context.
- **Accessibility and ethics:** size is only one factor for motor access. Also check tremor-tolerant activation (activate on up-event, allow cancel by moving off the target) and keyboard paths.
- **Evaluation (not run):** a task-based comparison on the same data: time to complete N adjustments plus wrong-target and wrong-direction error counts, with speed and accuracy reported separately. Baseline is the current layout. Failure condition: errors fall but time or scroll volume rises enough to offset the benefit for the target audience. An AI review can only flag the hypothesis.
- **Effort:** small.

## Installed support

[Source ledger](../../assets/human-systems/sources.json), [complete evaluation tasks](../../assets/human-systems/evaluation.md), [limits and unresolved terminology](../../assets/human-systems/unresolved.md). [Comparison case](../../assets/human-systems/examples/case-1-dashboard-comparison.md), [interrupted-work case](../../assets/human-systems/examples/case-2-interrupted-work-recovery.md), [neutral-research case](../../assets/human-systems/examples/case-3-neutral-survey-vs-persuasion.md), [optional PCEA worksheet](../../assets/human-systems/examples/pcea-task-worksheet.md).

The existing [consequence-copy method](../ux-writing.md), [risk/recovery matrix](../../../../libraries/frontend-design-premium/skills/frontend-design-premium/references/decision-matrix.md), and [current accessibility checks](../verification.md) remain their respective authorities. Resolve former audit paths through this plugin and its preserved libraries; do not infer participant results from these examples.

Conformance target matters: when a project claims WCAG AAA, the enhanced target criterion and its exceptions are part of that target, not merely optional advice. In an AA-targeted review, distinguish the applicable minimum, a stronger chosen convention, and actual input/task needs. Verify CSS hit area rather than inferring it from an icon screenshot. Official WCAG 2.2 and its target-size Understanding page were rechecked on 2026-09-30: https://www.w3.org/TR/WCAG22/#target-size-minimum and https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html .
