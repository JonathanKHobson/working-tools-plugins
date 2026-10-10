# Human-systems method: adopted conditional research card

Integrated 2026-09-30. Read this complete card only for its trigger. The original evidence, examples, counterexamples, tradeoffs and proposed tests are retained below; historical pre-integration coverage statements remain provenance. Participant outcomes are not measured. Normative criteria apply at their stated level and with their exceptions, not as universal design formulas. Source IDs resolve in the linked ledger; user/course proposals remain attributed and unvalidated. Locators such as L27 and U09 identify audited sources, not mandatory private-file dependencies.

## HS-05 — Consequential error: prevent, confirm or undo

- **Owner:** `interaction-resilience`. Existing owner rule: L27 `frontend-design-premium/references/decision-matrix.md` lines 37–46. Overlaps: harden.md, UXHC H3/H5/H9, critique H3 scoring.
- **Trigger:** an action that deletes, overwrites, publishes, pays, submits a commitment, sends to others, or overwrites source data with scenario data.
- **User task:** act efficiently without suffering unrecoverable mistakes.
- **Evidence:** X03 3.3.4 (AA, normative): for legal, financial, data-modification and test-response submissions, at least one of Reversible, Checked or Confirmed; 3.3.6 (AAA) extends this to all submissions. X12 #3 (emergency exit), #5 (prevention), #9 (diagnose and recover). Kyle's source: U14 [0016] (Oak "User control and freedom"). The claim that confirmation dialogs are habitually dismissed is widely reported but uninspected, so it is a hypothesis.
- **Mechanism:** L27 already selects treatment by risk and recoverability. Prevention removes predictable errors; confirmation adds a checkpoint before commitment; undo removes an error's permanence when reliable.
- **Decision rule:** apply the existing L27 confirmation-strength matrix. For reversible low-impact changes, give immediate feedback and optional Undo without confirmation. For destructive but recoverable changes, choose confirmation or Undo based on recovery reliability and the project pattern. For irreversible, external, financial or security effects, use app-owned confirmation naming object, scope and consequence; rare catastrophic operations may need stronger friction. Independently prevent predictable input errors with constraints, defaults and inline validation that preserves input. Check whether WCAG 3.3.4 applies to the submission. This card supplies task examples and checks; L27 remains the single risk matrix.

  Never rely on a generic "Are you sure?" as the only safeguard for a frequent action. Never offer undo that fails silently.
- **When not to use:** don't add confirmation to low-stakes reversible actions. Don't give fake undo where the server has already committed an irreversible external effect such as a sent email; say so plainly instead.
- **Competing considerations:** undo requires system support (soft delete, versioning); confirmation adds time; prevention through constraints can block legitimate edge inputs, which harden.md warns about.
- **Example:** "Apply scenario to source data" is irreversible for downstream reports. The review step shows "This will change capacity for 3 sessions (S04 30→40, S07 25→30, S09 30→35) in the shared dataset. Exports made after this will use the new values." The action is labelled "Apply 3 changes". A 10-second undo is offered only if the backend supports it.
- **Counterexample:** a confirmation modal on every filter change "for safety". People learn to click through it, so the one consequential confirm gets ignored too (hypothesis; see above).
- **Accessibility and ethics:** timed undo windows must respect 2.2.1 where applicable; focus must go to and be announced for confirmation dialogs; confirm-shaming copy ("No, I don't care about my data") is a dark pattern.
- **Evaluation (not run):** error-seeding in a scripted walkthrough: can the reviewer or participant recover from each seeded mistake, how long does it take, and is anything lost? Inspection check: every consequential action is mapped to a row of L27's matrix. Failure condition: a consequential action has no row, or has undo that isn't really implemented.
- **Effort:** small (rule); medium (backend undo).

## Installed support

[Source ledger](../../assets/human-systems/sources.json), [complete evaluation tasks](../../assets/human-systems/evaluation.md), [limits and unresolved terminology](../../assets/human-systems/unresolved.md). [Comparison case](../../assets/human-systems/examples/case-1-dashboard-comparison.md), [interrupted-work case](../../assets/human-systems/examples/case-2-interrupted-work-recovery.md), [neutral-research case](../../assets/human-systems/examples/case-3-neutral-survey-vs-persuasion.md), [optional PCEA worksheet](../../assets/human-systems/examples/pcea-task-worksheet.md).

The existing [consequence-copy method](../ux-writing.md), [risk/recovery matrix](../../../../libraries/frontend-design-premium/skills/frontend-design-premium/references/decision-matrix.md), and [current accessibility checks](../verification.md) remain their respective authorities. Resolve former audit paths through this plugin and its preserved libraries; do not infer participant results from these examples.
