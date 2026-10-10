# Adopted dashboard decision method

Integrated 2026-09-30. The complete research card below retains its mechanism, limits, examples, counterexamples and tests. Its observations describe the pre-integration audit; they are not continuing claims that the capability is absent. This is contextual design synthesis, not a participant-validated law. Follow the actual brief and existing owner procedures.

The 60% threshold, record IDs, six-chip threshold, 50-entry history and two-slot comparison are synthetic benchmark/prototype choices. Select limits for actual task, space and recovery requirements. A requested format takes precedence. A monitoring surface may use scoped explanatory prose when useful; the computed-prose exclusion concerns needless narrative or unsupported inference, not a blanket ban on sentences. The two-structural-differences check is this benchmark's rubric, not a universal aesthetic law.

Complete method sources and publication limits remain in the source ledger. Use the resolved support and owner links below for the procedures and synthetic fixtures. No arbitrary response-count threshold proves reliability. Do not reuse the baseline's documented cutoff defect as guidance.

## P6 — Scope-bound computed prose: generated sentences are recomputed, name their scope, and withdraw when invalid

**Decision it governs:** when interactive pages may carry claims in words.

**Current coverage (inspected):**
- `dashboard-design/SKILL.md`: "If a supported claim is requested, recompute it for the current population and period or remove it when invalid. Keep authored notes distinct from computed findings."
- `visualization-strategy-and-critique/SKILL.md` editorial mode: claim titles.

**Gap (observed):** the principle exists, but no *generation procedure* does. There is nothing on which templates to use, how ties and empty scopes are handled, or how the scope is named in the sentence. Editorial claim titles plus interactive filters can produce stale claims.

**Source evidence:**
- Segel & Heer 2010 section4.4 (S03, PDF p8 directly read and rendered) discusses messaging and the balance of author/reader control. The installed dashboard-design skill directly requires a claim to be recomputed for the current scope or removed. The specific sentence procedure below is this packet's proposal, not a paper result.

**Mechanism:**
1. Build each sentence from a template with typed slots filled by the model (`renderStandfirst`, `renderNotes`, `renderPair` in `editorial.js`). Recompute on every state change.
2. **Scope phrase first:** "Across all eight weeks" or "In weeks 3–4". A sentence without its scope does not ship.
3. **Ties:** list all tied items ("S06 and S12"). Never pick one silently.
4. **Boundaries:** add a note for items exactly at a threshold ("S08 filled exactly 60% and is not counted as below").
5. **Empty scope:** replace the claim with a pointer to recovery. Never render "0 of 0".
6. **Default selection by stated rule:** "Starting pair: the two sessions in this scope with the most unfilled seats." The rule is written on the page, and the reader can override it. When they do, offer "Return to the starting pair".
7. **Caveats travel with claims:** response counts, missing ratings, unknown sampling/comparability and excluded scenarios appear near the affected sentence. Do not infer reliability from an arbitrary n cutoff.

**Don't use when:** the page is a monitoring surface, where status words replace sentences. Also don't use it when the claim requires inference beyond arithmetic on the displayed data, such as causes or recommendations.

**Examples:** editorial standfirst, margin notes, pair sentence.
**Counterexample:** a static headline "Five sessions are under-filled" that still reads the same after the reader filters to weeks 1–2.

**Owner / overlap:** the **DV toolkit** owns computation. **Writing Quality Studio** owns sentence voice; this lane defines slots, not tone.
**Effort:** S–M.
**Test:** filter to weeks 1–2. The standfirst must read "In weeks 1–2, 69 of 85 seats were filled (81.2%). 0 of 3 sessions filled fewer than 60% of their seats." The notes must change their "lowest occupancy" entry to S02, 63.3%.

## Installed support

- [Source ledger](../assets/dashboard-repertoire/sources.json).
- [Workbench example](../assets/dashboard-repertoire/examples/workbench/index.html), [editorial alternative](../assets/dashboard-repertoire/examples/editorial/index.html), [shared data/model](../assets/dashboard-repertoire/examples/shared/session-model.js).
- Architecture selection: `ux-design-toolkit` → `skills/dashboard-design/references/experience-architecture-selection.md` (resolve in the current installed owner; do not infer its cache path), [scope/recovery](scope-and-empty-results.md), [scenario truth](scenario-overlays.md), [comparison](two-item-comparison.md), committed recovery: `ux-design-toolkit` → `skills/design-studio/references/exploration-recovery.md` (resolve in the current installed owner; do not infer its cache path), [computed prose](computed-prose.md).

These synthetic examples are method fixtures. Public release checks are recorded separately; participant outcomes, complete accessibility, physical touch and native host behavior remain unmeasured. The baseline is a negative fixture with a documented unsupported cutoff, not recommended guidance. UX owns interaction semantics; these cards preserve coordinated-state and numerical methods.

An explicit starting-pair rule can still imply unsupported judgment. Use a task-relevant neutral rule, state its meaning and avoid risk/quality/causal rankings without evidence. Apply the same truth boundary to ordering, highlights and imagery as to literal prose.
