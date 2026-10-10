# Adopted dashboard decision method

Integrated 2026-09-30. The complete research card below retains its mechanism, limits, examples, counterexamples and tests. Its observations describe the pre-integration audit; they are not continuing claims that the capability is absent. This is contextual design synthesis, not a participant-validated law. Follow the actual brief and existing owner procedures.

The 60% threshold, record IDs, six-chip threshold, 50-entry history and two-slot comparison are synthetic benchmark/prototype choices. Select limits for actual task, space and recovery requirements. A requested format takes precedence. A monitoring surface may use scoped explanatory prose when useful; the computed-prose exclusion concerns needless narrative or unsupported inference, not a blanket ban on sentences. The two-structural-differences check is this benchmark's rubric, not a universal aesthetic law.

Source libraries, historic audit locators and packet-relative paths in the retained card are provenance. Use the resolved support and owner links below for the installed procedures and fixtures. Original source access limits remain in the ledger. No arbitrary response-count threshold proves reliability. Do not reuse the baseline's documented cutoff defect as guidance.

## P5 — Reversible exploration: committed changes are undoable; transient ones are not recorded

**Decision it governs:** what the history records, and how Reset relates to Undo.

**Current coverage (inspected):**
- `dashboards-and-real-time-visualization/SKILL.md`: "explicit reset and undo paths" (one list item).
- `shareable-state-and-persistence.md`: push history on commit and replace it while dragging. That rule concerns *browser* history.

**Gap (observed):** the guidance names undo but does not define its unit, its relation to Reset, or its exclusions. As a result, Reset becomes a destructive, all-or-nothing action. That is the baseline's behavior.

**Source evidence:** the current dashboard procedure explicitly calls for reset and undo paths. Heer & Shneiderman 2012 (S02, PDF p7/printed51 directly text-read) discusses action history and basic undo/redo. This packet chooses the exact commit unit as a task-specific proposal.

**Mechanism:**
1. **Unit:** one committed state change is one entry. Commits are filter changes, pins/unpins, scenario apply/restore and Reset. Don't record hover, cursor movement, a brush in progress, slider drags before release, or disclosure open/close. In the workbench the brush preview is transient, and the range commits on pointer-up.
2. **Snapshot** the serializable state before the change (`commit()` in `workbench.js`), with a bounded stack (50). Record nothing when the change is a no-op.
3. **Reset is undoable**, and its announcement says so ("Undo is available").
4. **Controls:** an Undo button disabled when the stack is empty, plus ⌘/Ctrl+Z when focus is not in a text field. After undo, announce the resulting scope.
5. **Where not to add it:** a short guided piece whose every change has a visible Restore (the editorial alternative) may omit a global undo. Record that choice as a decision.

**Don't use when:** the state is trivially visible and reversible in place (a single toggle), or the product has no multi-step exploration.

**Example:** workbench `commit`/`undo`. Editorial counter-decision: per-item Restore plus the ribbon Reset, no global undo.
**Counterexample:** Reset as the only recovery. One accidental press discards two pins and a scenario.

**Owner / overlap:** the **UX toolkit**. `interaction-resilience.md` is the natural home.
**Effort:** S.
**Test:** pin S04, set weeks 3–4, press Reset, then Undo. Weeks 3–4 and the S04 pin must return. Press Undo twice more and the state must step back through the week change to the pin.

## Installed support

- Source ledger: `data-visualization-toolkit` → `skills/live-dashboards/assets/dashboard-repertoire/sources.json` (resolve in the current installed owner; do not infer its cache path).
- Evaluation tasks: `data-visualization-toolkit` → `skills/live-dashboards/assets/dashboard-repertoire/evaluation.md` (resolve in the current installed owner; do not infer its cache path); executed desktop/mobile review: `data-visualization-toolkit` → `skills/live-dashboards/assets/dashboard-repertoire/executed-review.md` (resolve in the current installed owner; do not infer its cache path); model checks: `data-visualization-toolkit` → `skills/live-dashboards/assets/dashboard-repertoire/model-results.json` (resolve in the current installed owner; do not infer its cache path).
- Workbench example: `data-visualization-toolkit` → `skills/live-dashboards/assets/dashboard-repertoire/examples/workbench/index.html` (resolve in the current installed owner; do not infer its cache path), editorial alternative: `data-visualization-toolkit` → `skills/live-dashboards/assets/dashboard-repertoire/examples/editorial/index.html` (resolve in the current installed owner; do not infer its cache path), shared data/model: `data-visualization-toolkit` → `skills/live-dashboards/assets/dashboard-repertoire/examples/shared/session-model.js` (resolve in the current installed owner; do not infer its cache path).
- [Architecture selection](../../dashboard-design/references/experience-architecture-selection.md), scope/recovery: `data-visualization-toolkit` → `skills/live-dashboards/references/scope-and-empty-results.md` (resolve in the current installed owner; do not infer its cache path), scenario truth: `data-visualization-toolkit` → `skills/live-dashboards/references/scenario-overlays.md` (resolve in the current installed owner; do not infer its cache path), comparison: `data-visualization-toolkit` → `skills/live-dashboards/references/two-item-comparison.md` (resolve in the current installed owner; do not infer its cache path), [committed recovery](exploration-recovery.md), computed prose: `data-visualization-toolkit` → `skills/live-dashboards/references/computed-prose.md` (resolve in the current installed owner; do not infer its cache path).

Software/model and selected rendered interaction checks passed in the dated review. Participant outcomes, full keyboard/assistive-technology coverage and physical touch remain untested. The old unrun entries in the retained evaluation describe earlier subtask checkpoints. The baseline is a frozen negative/regression fixture, not a recommended template. UX owns interaction semantics; Data maintains the complete coordinated-state cards and their numerical fixtures without duplicating bodies in both plugins.

## Interruption boundary

This card's undo history is session-local. It does not establish persistence or resumption after expiry/reload. For those tasks, read [interaction resilience](interaction-resilience.md): protect draft visibility and permissions, reconcile changed/deleted source records before reusing saved selections or scenarios, and distinguish restored intentions from committed data. The human-systems resumption method adds the person’s next-step cue. Do not claim any backend undo, offline persistence or assistive-technology success from this JavaScript example alone.

For actual interruption or reauthentication, read the complete [task resumption card](human-systems/task-resumption.md) and its worked recovery case. An in-memory Undo stack is not persistence.
