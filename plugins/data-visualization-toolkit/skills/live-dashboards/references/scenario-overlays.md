# Adopted dashboard decision method

Integrated 2026-09-30. The complete research card below retains its mechanism, limits, examples, counterexamples and tests. Its observations describe the pre-integration audit; they are not continuing claims that the capability is absent. This is contextual design synthesis, not a participant-validated law. Follow the actual brief and existing owner procedures.

The 60% threshold, record IDs, six-chip threshold, 50-entry history and two-slot comparison are synthetic benchmark/prototype choices. Select limits for actual task, space and recovery requirements. A requested format takes precedence. A monitoring surface may use scoped explanatory prose when useful; the computed-prose exclusion concerns needless narrative or unsupported inference, not a blanket ban on sentences. The two-structural-differences check is this benchmark's rubric, not a universal aesthetic law.

Complete method sources and publication limits remain in the source ledger. Use the resolved support and owner links below for the procedures and synthetic fixtures. No arbitrary response-count threshold proves reliability. Do not reuse the baseline's documented cutoff defect as guidance.

## P3 — Scenario overlay: hypotheticals are a separate, labeled, restorable layer, never a forecast

**Decision it governs:** where what-if state lives, how it is drawn, and how it is restored.

**Current coverage (inspected):**
- `dashboard-design/references/visualization-contract.md` (Encoding row: "observed/forecast distinction").
- `chart-meaning-and-color.md`: "Observed and forecast values need a visible boundary."
- `advanced-interactive-visualization-contract.md`: "Measured, inferred, simulated, schematic, and decorative layers."

**Gap (observed):** the guidance distinguishes forecasts from observations. It has **no contract for user-driven hypotheticals**: no rule on where scenario state lives, how it interacts with filters, sorting and pooled totals, what restore means, or how to offer goal-seeking without a model. The Shareables interaction registry forbids persistent state and allows only filter/toggle/view-toggle/select/search/drilldown/export/patch-preview controls (`shareables_core.py` `INTERACTION_CONTROL_TYPES`, line 4768). It has no scenario control.

**Source evidence:**
- Gathani et al. 2022's abstract/page summary (S05) identifies interactive what-if analysis as a separate mode. Its PDF fetch did not expose the four operations or a baseline/modified display rule. This card's capacity and goal arithmetic come from the benchmark contract, not from a claimed paper prescription.

**Mechanism:**
1. **Storage:** keep a separate map `{id: hypotheticalCapacity}`. Source records stay frozen (`Object.freeze` in `sessions-data.js`). Derived rows carry both values (`occ` and `effOcc`, `capacity` and `effCapacity`).
2. **Scope of change:** change only the declared driver (capacity). Hold the other inputs at recorded values (enrollment), and say so in the UI.
3. **Validation:** allow whole numbers within the declared bounds. Reject values that would imply an unmodeled change: capacity below current enrollment would remove enrolled people. Explain the rejection in words next to the field.
4. **Visible distinction:** use a dedicated hue *plus* a non-hue cue (a dashed outline or hatching) *plus* the word "hypothetical" wherever a scenario value appears. Scenario values never replace source values in a column named for the source. Give them their own column or a "source → hypothetical" pair.
5. **Totals:** a pooled figure either excludes scenarios and says so (editorial: "These are recorded figures; chapter 3's hypothetical capacity is not included"), or shows both ("pooled 68.7% · with scenario 70.0%"). It never mixes them silently.
6. **Sorting/position:** sort and position by source values, so an edit does not rearrange the page. Draw the hypothetical as a ghost mark linked to the source mark.
7. **Goal inversion by arithmetic:** offer "the largest capacity at which occupancy is at least 60%" = ⌊enrollment × 100 / 60⌋, computed with integers (`capacityForThreshold`). Label it as arithmetic, not a recommendation.
8. **Restore:** give each change its own Restore; add Restore-all; and include "source capacities" in the global Reset. Scenario changes enter undo history where one exists (P5).
9. **Vocabulary:** do not label the arithmetic output a forecast, projection or expected outcome. Explicit negation such as "not a forecast" is useful. Use "hypothetical", "if capacity were…", "enrollment held at N".

**Don't use when:** the driver–outcome relationship is not an identity, or needs a model the product doesn't have. Something like "if we add seats, enrollment rises" is a forecast and needs its own evidence and uncertainty (route to `statistical-evidence`). Scenario controls in public-facing reports can look like predictions: prefer a static annotated example there.

**Examples:** workbench → the inspector "Capacity scenario" with stepper, goal button, active-change ledger and the chip "Scenario: 1 capacity change". Editorial → chapter 3 range slider, seat strip with hatched removed seats, sentence "Hypothetically, with 18 seats instead of 24…".
**Counterexample:** a slider that edits the capacity column in place, leaving no mark that values changed and no path back to the recorded figures.

**Owner / overlap:** the **DV toolkit** owns the truth rules (1–7). The **UX toolkit** owns restore and feedback (8) and vocabulary (9, shared with Writing). Shareables would need a new `scenario` control type before it could render this. That is outside this lane (see `merge-brief.md`).
**Effort:** M.
**Test:** set S04 to 18. The results must be: S04 shows 61.1% as hypothetical, its source column still shows 45.8%, pooled (all weeks) shows 68.7% with scenario 70.0% (217/310), Restore returns to 45.8%, and no label or explanatory sentence claims predictive validity; the disclaimer "not a forecast" is appropriate.

## Installed support

- [Source ledger](../assets/dashboard-repertoire/sources.json).
- [Workbench example](../assets/dashboard-repertoire/examples/workbench/index.html), [editorial alternative](../assets/dashboard-repertoire/examples/editorial/index.html), [shared data/model](../assets/dashboard-repertoire/examples/shared/session-model.js).
- Architecture selection: `ux-design-toolkit` → `skills/dashboard-design/references/experience-architecture-selection.md` (resolve in the current installed owner; do not infer its cache path), [scope/recovery](scope-and-empty-results.md), [scenario truth](scenario-overlays.md), [comparison](two-item-comparison.md), committed recovery: `ux-design-toolkit` → `skills/design-studio/references/exploration-recovery.md` (resolve in the current installed owner; do not infer its cache path), [computed prose](computed-prose.md).

These synthetic examples are method fixtures. Public release checks are recorded separately; participant outcomes, complete accessibility, physical touch and native host behavior remain unmeasured. The baseline is a negative fixture with a documented unsupported cutoff, not recommended guidance. UX owns interaction semantics; these cards preserve coordinated-state and numerical methods.

## Transfer rule before any controls

State the new domain’s exact identity linking the editable driver to the displayed result, all held-fixed inputs, valid domain and units. Derive validation from that identity. The enrollment/capacity lower bound and threshold formula belong only to the fictional workshop. Transport capacity below the number of objects may instead imply multiple shipments; feasibility depends on dimensions, constraints and batching assumptions. Without those facts, show unknown or an explicitly limited illustration, not a fabricated shipment plan.

An arithmetic result cannot be described or visually encoded as safety, risk, quality or causal improvement without an appropriate model and evidence. Label assumptions beside outputs and preserve per-value provenance. Do not communicate unsupported risk through colour, rank or a default selection merely because no forecast word appears.
