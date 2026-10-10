# Adopted dashboard decision method

Integrated 2026-09-30. The complete research card below retains its mechanism, limits, examples, counterexamples and tests. Its observations describe the pre-integration audit; they are not continuing claims that the capability is absent. This is contextual design synthesis, not a participant-validated law. Follow the actual brief and existing owner procedures.

The 60% threshold, record IDs, six-chip threshold, 50-entry history and two-slot comparison are synthetic benchmark/prototype choices. Select limits for actual task, space and recovery requirements. A requested format takes precedence. A monitoring surface may use scoped explanatory prose when useful; the computed-prose exclusion concerns needless narrative or unsupported inference, not a blanket ban on sentences. The two-structural-differences check is this benchmark's rubric, not a universal aesthetic law.

Complete method sources and publication limits remain in the source ledger. Use the resolved support and owner links below for the procedures and synthetic fixtures. No arbitrary response-count threshold proves reliability. Do not reuse the baseline's documented cutoff defect as guidance.

## P4 — Two-item comparison: explicit slots, a shared scale, a computed difference, and an evidence gate

**Decision it governs:** how a "compare two" task is built.

**Current coverage (inspected):**
- `dashboard-patterns.md` row "equal-priority teams" (shared scale, comparable weight).
- `chart-meaning-and-color.md`: "Many comparable groups → small multiples".
- Shareables `comparison-matrix` / `pros-cons-panel` (options compared as static text cells, `widgets.json` record `widget.decision-support`).

**Gap (observed):** nothing prescribes (a) how to choose between side-by-side, overlay and explicit difference; (b) what happens when a third item is selected; (c) how to retain response-count and missingness context beside a descriptive rating difference. The baseline replaced the oldest selection silently (announced only) and showed no difference column.

**Source evidence:**
- Gleicher et al.2011 (S01, preprint PDF p4 section2/Figure1 directly read and rendered by Codex) distinguishes separate views, overlays and explicit relational encodings. For two scalar records this is a design vocabulary, not a performance finding.
- Benchmark brief: rating "must visibly retain response count; do not imply statistical significance."

**Mechanism:**
1. **Slots, not a set:** name the slots A and B. Pinning fills an empty slot. When both are full, **ask**: "Replace A / Replace B / Cancel". Move focus to that prompt and announce it. Where a quiet default is appropriate (editorial), use one stated rule instead ("the newest choice replaces the second session"), and show the result in visible pickers.
2. **Pick the comparison build:**
   - *Superposition* on one shared track when there are 2 items and one scaled measure (workbench occupancy bar, `superposeSvg`).
   - *Aligned juxtaposition* when items have a physical or count form readers must see (editorial seat strips: same square size, left-aligned).
   - *Explicit difference* (a B − A column with signed values and units) whenever the reader must state "how much". Compute it from unrounded values and round at display.
3. **Evidence and comparability gate:** show each mean rating with its exact response count. If either mean is missing, show no difference and state why. Otherwise a B − A difference may be shown as *descriptive arithmetic only*, with the counts beside the source values and a nearby caveat: sampling and comparability are unknown; no inferential claim is made. No universal response-count cutoff makes a mean valid or comparable. If populations, instruments, or periods are known to differ, describe those differences or withhold a comparison that would mislead.
4. **Persistence:** pins survive filters. A pinned item outside scope is marked "outside current scope — kept pinned" rather than dropped.
5. **Narrow screens:** keep the comparison result near where it was triggered. The workbench uses a fixed mini-tray ("A S09 45.0% · B S06 50.0% · Δ +5.0 pts") with "Open comparison".

**Don't use when:** comparing ≥4 items. Use small multiples or a ranked table with in-cell marks (existing guidance). Don't use it when items have different units or populations and no common denominator.

**Examples:** workbench `renderTray` (slots, replace prompt, superposition, difference table, rating gate). Editorial `renderPair` (aligned seat strips, generated sentence, label stanza, rating caveat).
**Counterexample:** two KPI cards side by side, each with its own auto-scaled mini chart. A 45% bar and a 50% bar then look the same length because each is scaled to itself.

**Owner / overlap:** the **DV toolkit** owns 2–3. The **UX toolkit** owns 1, 4 and 5. It complements the Shareables `comparison-matrix`, which compares *options* by text and is out of scope for quantitative records.
**Effort:** M.
**Test:** pin S09 then S06. Expect Δ occupancy +5.0 pts, Δ cost per enrolled −$74.31, and rating means shown with n=6 and n=4. A descriptive B − A rating difference may appear with an explicit sampling/comparability caveat; it must not imply significance or reliability. Pair either with S12 and the rating difference must be absent because its mean is missing. Pin a third session and a prompt must appear. Neither pin changes until you choose.

## Installed support

- [Source ledger](../assets/dashboard-repertoire/sources.json).
- [Workbench example](../assets/dashboard-repertoire/examples/workbench/index.html), [editorial alternative](../assets/dashboard-repertoire/examples/editorial/index.html), [shared data/model](../assets/dashboard-repertoire/examples/shared/session-model.js).
- Architecture selection: `ux-design-toolkit` → `skills/dashboard-design/references/experience-architecture-selection.md` (resolve in the current installed owner; do not infer its cache path), [scope/recovery](scope-and-empty-results.md), [scenario truth](scenario-overlays.md), [comparison](two-item-comparison.md), committed recovery: `ux-design-toolkit` → `skills/design-studio/references/exploration-recovery.md` (resolve in the current installed owner; do not infer its cache path), [computed prose](computed-prose.md).

These synthetic examples are method fixtures. Public release checks are recorded separately; participant outcomes, complete accessibility, physical touch and native host behavior remain unmeasured. The baseline is a negative fixture with a documented unsupported cutoff, not recommended guidance. UX owns interaction semantics; these cards preserve coordinated-state and numerical methods.

## Match the evidence type

Response count applies to a mean over responses, not every numerical score. For a single assessor judgment, carry assessor, instrument/scale, date and context instead. If scales, currencies, valuation dates, populations or assessors differ and comparability is unestablished, retain source values separately and withhold a numerical difference that would imply equivalence. Explain the missing basis and what would establish it. Show descriptive differences only when their meaning and comparability can be stated honestly; never turn arithmetic into significance.
