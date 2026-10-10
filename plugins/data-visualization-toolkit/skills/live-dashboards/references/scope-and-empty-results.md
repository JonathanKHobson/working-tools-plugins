# Adopted dashboard decision method

Integrated 2026-09-30. The complete research card below retains its mechanism, limits, examples, counterexamples and tests. Its observations describe the pre-integration audit; they are not continuing claims that the capability is absent. This is contextual design synthesis, not a participant-validated law. Follow the actual brief and existing owner procedures.

The 60% threshold, record IDs, six-chip threshold, 50-entry history and two-slot comparison are synthetic benchmark/prototype choices. Select limits for actual task, space and recovery requirements. A requested format takes precedence. A monitoring surface may use scoped explanatory prose when useful; the computed-prose exclusion concerns needless narrative or unsupported inference, not a blanket ban on sentences. The two-structural-differences check is this benchmark's rubric, not a universal aesthetic law.

Complete method sources and publication limits remain in the source ledger. Use the resolved support and owner links below for the procedures and synthetic fixtures. No arbitrary response-count threshold proves reliability. Do not reuse the baseline's documented cutoff defect as guidance.

## P2 — Scope provenance: every active constraint is visible, removable and attributable; empty results name their cause

**Decision it governs:** how filter scope is shown, and what an empty result says.

**Current coverage (inspected):**
- `interaction-models-and-progressive-disclosure.md`: "Keep active state summaries visible outside the collapsed panel."
- `dashboard-design/SKILL.md`: "Provide visible active filters, reset."
- `ux-design-toolkit/skills/design-studio/references/interaction-resilience.md`: "empty states offer a real next action rather than a blank void."
- `delivery-and-qa.md`: totals, titles, table and export must describe the same state.

**Gap (observed):** the guidance says *show* filters. It does not say *attribute* results to them. The installed guidance gives no rule that each constraint is its own removable token, and none that an empty state identifies which constraint emptied the view. The baseline's cause-specific empty message was improvised.

**Source evidence:**
- The installed dashboard-design skill already requires one transformed state source and visible active filters; interaction-resilience requires a useful action from empty states. The added attribution rule is a design inference from those verified owner paths, not a result tested with users.
- Community lead (unvalidated): a Zoho Analytics community post reports dashboard filters that "work for charts but don't apply to KPI widgets". That is a real case of scope that is invisible or inconsistent. One post shows a problem exists. It does not establish how common it is.
- W3C WCAG 2.2 SC 4.1.3 Status Messages: a result-count message such as "5 results returned" must be programmatically determinable without receiving focus.

**Mechanism:**
1. **Scope record:** keep one filter object (`{from, to, belowOnly}` in `examples/shared/session-model.js`). Every view, total, sentence and export reads from it. This restates the existing "one transformed state source" rule; the next steps are new.
2. **Constraint chips:** render one token per non-default constraint, each with its own remove control labeled with its effect ("Remove week range, show all weeks"). When nothing is constrained, show a dotted "default" chip, so "no filter" is an explicit state rather than an absence.
3. **Count + denominator:** "8 of 12 sessions · pooled 66.0% (70/106 seats)". The pooled figure states its formula in the footer. Recompute on every change.
4. **Status message:** after a scope change, announce the new count through a polite live region (SC 4.1.3). Do not move focus.
5. **Attributed empty state:** when the result is empty, test each constraint by removing it (`explainEmpty()`). Name the cause in words, with a count ("Weeks 1–2 contain 3 sessions, but none is below 60% occupied"). Offer one button per recovery path, each with the size of its result ("Widen to all weeks (5 below 60%)"). Offer Undo when the history includes the change.
6. **Out-of-scope context (optional):** in a workbench, draw out-of-scope marks faded and non-interactive rather than deleting them. This keeps positions stable in this prototype; user comprehension is untested.

**Don't use when:** the view has no user-controlled filters. For >6 simultaneous constraints, collapse the chips to a count with a disclosure, and keep the count visible.

**Examples:** `examples/workbench/workbench.js` → `renderCommand`, `emptyHtml`. `examples/editorial/editorial.js` → `renderRibbon`, `emptyHtml`. The editorial ribbon states the scope that every sentence describes.
**Counterexample:** a "Filters (2)" badge in a closed panel, or "No results" with a single generic Reset that discards everything.

**Owner / overlap:** the **UX toolkit** owns the state/feedback rule. The **DV toolkit** owns the rule that totals and denominators follow scope. This extends the existing lines above; don't restate them.
**Effort:** S.
**Test:** apply weeks 1–2 + "below 60% only". The page must name "below 60%" as the cause, offer both targeted recoveries with counts, and announce the count. A single removal must restore rows without clearing the week range.

## Installed support

- [Source ledger](../assets/dashboard-repertoire/sources.json).
- [Workbench example](../assets/dashboard-repertoire/examples/workbench/index.html), [editorial alternative](../assets/dashboard-repertoire/examples/editorial/index.html), [shared data/model](../assets/dashboard-repertoire/examples/shared/session-model.js).
- Architecture selection: `ux-design-toolkit` → `skills/dashboard-design/references/experience-architecture-selection.md` (resolve in the current installed owner; do not infer its cache path), [scope/recovery](scope-and-empty-results.md), [scenario truth](scenario-overlays.md), [comparison](two-item-comparison.md), committed recovery: `ux-design-toolkit` → `skills/design-studio/references/exploration-recovery.md` (resolve in the current installed owner; do not infer its cache path), [computed prose](computed-prose.md).

These synthetic examples are method fixtures. Public release checks are recorded separately; participant outcomes, complete accessibility, physical touch and native host behavior remain unmeasured. The baseline is a negative fixture with a documented unsupported cutoff, not recommended guidance. UX owns interaction semantics; these cards preserve coordinated-state and numerical methods.

## Domain and constraint checks

Specify inclusion boundaries, time zone and source dates for temporal filters; monetary sums need compatible currency and valuation basis. For a new dataset, derive exact expected totals, missing cases, boundary cases and empty-result explanations before UI work. A set of constraints may have interacting causes: if no single removal restores rows, say so and offer a checked combination or full reset with its actual count. Do not invent a single guilty filter. A dotted default chip and a fixed chip-count collapse threshold are prototype treatments; choose an understandable scope display for the product.
