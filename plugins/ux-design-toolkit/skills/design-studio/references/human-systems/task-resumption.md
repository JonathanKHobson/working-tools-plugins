# Human-systems method: adopted conditional research card

Integrated 2026-09-30. Read this complete card only for its trigger. The original evidence, examples, counterexamples, tradeoffs and proposed tests are retained below; historical pre-integration coverage statements remain provenance. Participant outcomes are not measured. Normative criteria apply at their stated level and with their exceptions, not as universal design formulas. Source IDs resolve in the linked ledger; user/course proposals remain attributed and unvalidated. Locators such as L27 and U09 identify audited sources, not mandatory private-file dependencies.

## HS-04 — Interruption and resumption cues

- **Owner:** `interaction-resilience` (skill and design-studio reference). Overlaps: L09 "Interrupted and stale interactions" (system integrity, preserved), harden.md, critique "Casey".
- **Trigger:** multi-step or long-running work that can be suspended — by a session timeout, a notification, a device switch, the end of a shift, or a phone call — especially where resuming at the wrong step causes duplicate or skipped actions. Examples include partial data entry, a scenario in progress, a multi-row edit, or a review queue.
- **User task:** return later and continue correctly without redoing work or skipping steps.
- **Evidence:** X07 p. 40 (model plus empirical fit): a pending goal is retrieved through an associated cue, which must exist both when the goal is suspended and when it is resumed. X03 2.2.5 and 2.2.6 (AAA): no data loss across re-authentication, and warnings before inactivity timeouts. 3.3.7 (A): no re-entry of information already provided. Kyle's source: U08 [0012] on attention. Atlas persona A01 includes "Pause and resume" as a goal (unsourced persona; not evidence).
- **Mechanism:** preserved *state* keeps the data; a *cue* restores the person's intention and position.
- **Decision rule:**
  1. As meaningful state or focus changes, and at explicit suspension where possible, capture the last completed step, the pending intention if it can be inferred from state (for example, "editing S09 capacity, not yet applied"), and unsaved values.
  2. On return, present a resumption cue *where work resumes*: the last position highlighted, pending changes listed, and the choices "Continue", "Review changes" and "Discard" with their consequences stated (HS-03).
  3. Keep drafts and scenario changes clearly separate from committed data (HS-05).
  4. Before a timeout that loses data, warn and allow extension (2.2.1 / 2.2.6). After re-authentication, return to the same state (2.2.5).
- **When not to use:** single-step or instant tasks. Privacy-sensitive shared devices, where showing pending details to the next person is itself a risk; there, prefer a neutral "You have unsaved changes" behind authentication.
- **Competing considerations:** stale drafts can conflict with newer server data (L09 covers stale overwrite); resumption banners add clutter; storing drafts has privacy and security implications.
- **Example:** see `examples/case-2-interrupted-work-recovery.md`.
- **Counterexample:** auto-restoring a half-finished scenario *silently*, so the coordinator doesn't notice the numbers are hypothetical and reports them as actual.
- **Accessibility and ethics:** interruptions affect everyone, but resumption cost falls harder on people with memory, attention or fatigue-related disabilities and on people in interruption-heavy jobs. Don't store sensitive drafts without disclosure.
- **Evaluation (not run):** an interrupted-task protocol: suspend participants at a fixed step, impose a distractor, then measure resumption time, wrong-step resumption and duplicate actions. Baseline is state preservation alone. Inspection check: each multi-step flow lists its suspension triggers and resumption cue. Failure condition: the cue is ignored or misread, or it exposes data on a shared device.
- **Effort:** medium.

## Installed support

[Source ledger](../../assets/human-systems/sources.json), [complete evaluation tasks](../../assets/human-systems/evaluation.md), [limits and unresolved terminology](../../assets/human-systems/unresolved.md). [Comparison case](../../assets/human-systems/examples/case-1-dashboard-comparison.md), [interrupted-work case](../../assets/human-systems/examples/case-2-interrupted-work-recovery.md), [neutral-research case](../../assets/human-systems/examples/case-3-neutral-survey-vs-persuasion.md), [optional PCEA worksheet](../../assets/human-systems/examples/pcea-task-worksheet.md).

The existing [consequence-copy method](../ux-writing.md), [risk/recovery matrix](../../../../libraries/frontend-design-premium/skills/frontend-design-premium/references/decision-matrix.md), and [current accessibility checks](../verification.md) remain their respective authorities. Resolve former audit paths through this plugin and its preserved libraries; do not infer participant results from these examples.

Do not rely on receiving a final timeout/unload event to save the cue. Reconcile changed or deleted records and current permissions before offering restored selections or drafts. Never imply that a restored pending action was committed.
