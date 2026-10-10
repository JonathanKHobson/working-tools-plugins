# Adopted dashboard decision method

Integrated 2026-09-30. The complete research card below retains its mechanism, limits, examples, counterexamples and tests. Its observations describe the pre-integration audit; they are not continuing claims that the capability is absent. This is contextual design synthesis, not a participant-validated law. Follow the actual brief and existing owner procedures.

The 60% threshold, record IDs, six-chip threshold, 50-entry history and two-slot comparison are synthetic benchmark/prototype choices. Select limits for actual task, space and recovery requirements. A requested format takes precedence. A monitoring surface may use scoped explanatory prose when useful; the computed-prose exclusion concerns needless narrative or unsupported inference, not a blanket ban on sentences. The two-structural-differences check is this benchmark's rubric, not a universal aesthetic law.

Source libraries, historic audit locators and packet-relative paths in the retained card are provenance. Use the resolved support and owner links below for the installed procedures and fixtures. Original source access limits remain in the ledger. No arbitrary response-count threshold proves reliability. Do not reuse the baseline's documented cutoff defect as guidance.

## P1 — Choose the experience architecture from the task sequence, before choosing charts

**Decision it governs:** what kind of information experience to build. Chart choice comes later.

**Current coverage (inspected):**
- `ux-design-toolkit/skills/dashboard-design/SKILL.md`. Its §"Resolve the decision before the layout" separates monitoring, exploration and one-time explanation.
- `ux-design-toolkit/skills/dashboard-design/references/dashboard-patterns.md`. It maps a question to a composition *per panel*, e.g. "Which items lead or lag?" → horizontal ranking.
- `build-web-data-visualization/references/foundations/operational-visualization-workspaces.md` (tri-pane shell).
- `build-web-data-visualization/skills/visualization-strategy-and-critique/SKILL.md`. It covers editorial mode and the stepper-vs-scrollytelling choice.

**Gap (observed):** each archetype is described somewhere. Nothing tells the agent to decide *which archetype fits the whole task sequence* or to test that alternatives differ structurally. In this lane's baseline (`examples/baseline/BASELINE-RECORD.md`), following the installed guidance produced a chart + right rail + table layout by default. The prompt's mission states the **user-reported problem**: "My dashboards currently feel one-dimensional" (`design-upgrade-prompt-kit/prompts/01_RESEARCH_PROMPT.md`, Mission).

**Source evidence:**
- Segel & Heer 2010 section4.4 (source S03, PDF p8 directly read and rendered by Codex) distinguishes author/reader control and three hybrid structures. It supplies a design vocabulary, not a performance advantage for this prototype.
- Heer & Shneiderman 2012 (S02, PDF p2 taxonomy rendered/read and p7 history text read) supports selecting linked views and reversible actions by analysis task. Sarikaya et al.2019 (S04) remains an unread full-text lead. This card adds task-specific synthesis to current owner guidance.

**Mechanism:**
1. Write the task sequence as verbs, in order. Benchmark example: *locate (T1) → scope (T3) → pick two (T2) → compare → try a hypothetical (T4) → recover/reset (T5)*.
2. Classify each step as **author-led** (the reader should see it without acting) or **reader-led** (the reader chooses).
3. Choose the architecture from the ratio and the audience:

| Architecture | Choose when | Default layout | Sequence the reader follows |
| --- | --- | --- | --- |
| **Comparison workbench** | Repeat use; the reader chooses what to inspect; most steps are reader-led | Command/scope bar, main evidence viewport, synchronized ledger, inspector rail (A/B slots + scenario) | scope → locate → pin → compare → test → undo |
| **Guided editorial (martini glass)** | Occasional readers; a few findings deserve an author-chosen starting point; explanation matters as much as lookup | Typographic lead with computed standfirst, then chapters (one encoding each), then an open explorer | read the claim → see the evidence → a starting pair chosen by a transparent rule → one what-if → free exploration |
| **Compact monitor** | Status and exceptions on a cadence; small screens; little manipulation | Exceptions first, stable positions, freshness/stale states (existing `live-dashboards`) | scan → notice → drill once |
| **Single view + table** | One question, one comparison | One chart with direct labels, plus a table | read → look up |

4. **Variety test:** two alternatives count as different only if **at least two** of these differ: task sequence; primary encoding; what is visible without interaction; where and how selection is made; how state is shown. A palette, theme or card-radius change never counts. NS03/NS04/NS05 in `shared/north-star-observations.md` show the same matrix recolored.
5. **Within-product coherence:** each alternative keeps one type system, one semantic-color ledger and one state vocabulary.

**Don't use when:** the user has specified the format. Honor it (dashboard-design SKILL says so already). A single question with one comparison doesn't need an architecture decision.

**Example:** `examples/workbench/` and `examples/editorial/` answer the same six tasks with the same data. The workbench's primary encoding is rate: occupancy is a position on a 0–100% axis. The editorial's primary encoding is count: every seat is a square. The workbench shows nothing author-selected. The editorial opens on a computed claim and a starting pair chosen by a rule.
**Counterexample:** the baseline (`examples/baseline/`) is competent but defaulted: the same layout would come out for any brief.

**Owner / overlap:** the **UX toolkit** (`dashboard-design`) owns the selection table. The **DV toolkit** owns the encoding row of each archetype. **Graphic Design Studio** owns direction within an archetype (`composition-and-typography/references/layout-decisions.md` already has "asymmetrical editorial", "field-and-band" and "modular structure"). Proposed file: `proposed/…/experience-architecture-selection.md`.
**Effort:** S (reference file + one router line).
**Test:** give the same brief twice and ask for two alternatives. The pass condition is that the variety test above records ≥2 differing dimensions and the same known answers for T1–T5. A theme-only pair fails.

## Installed support

- Source ledger: `data-visualization-toolkit` → `skills/live-dashboards/assets/dashboard-repertoire/sources.json` (resolve in the current installed owner; do not infer its cache path).
- Evaluation tasks: `data-visualization-toolkit` → `skills/live-dashboards/assets/dashboard-repertoire/evaluation.md` (resolve in the current installed owner; do not infer its cache path); executed desktop/mobile review: `data-visualization-toolkit` → `skills/live-dashboards/assets/dashboard-repertoire/executed-review.md` (resolve in the current installed owner; do not infer its cache path); model checks: `data-visualization-toolkit` → `skills/live-dashboards/assets/dashboard-repertoire/model-results.json` (resolve in the current installed owner; do not infer its cache path).
- Workbench example: `data-visualization-toolkit` → `skills/live-dashboards/assets/dashboard-repertoire/examples/workbench/index.html` (resolve in the current installed owner; do not infer its cache path), editorial alternative: `data-visualization-toolkit` → `skills/live-dashboards/assets/dashboard-repertoire/examples/editorial/index.html` (resolve in the current installed owner; do not infer its cache path), shared data/model: `data-visualization-toolkit` → `skills/live-dashboards/assets/dashboard-repertoire/examples/shared/session-model.js` (resolve in the current installed owner; do not infer its cache path).
- [Architecture selection](experience-architecture-selection.md), scope/recovery: `data-visualization-toolkit` → `skills/live-dashboards/references/scope-and-empty-results.md` (resolve in the current installed owner; do not infer its cache path), scenario truth: `data-visualization-toolkit` → `skills/live-dashboards/references/scenario-overlays.md` (resolve in the current installed owner; do not infer its cache path), comparison: `data-visualization-toolkit` → `skills/live-dashboards/references/two-item-comparison.md` (resolve in the current installed owner; do not infer its cache path), [committed recovery](../../design-studio/references/exploration-recovery.md), computed prose: `data-visualization-toolkit` → `skills/live-dashboards/references/computed-prose.md` (resolve in the current installed owner; do not infer its cache path).

Software/model and selected rendered interaction checks passed in the dated review. Participant outcomes, full keyboard/assistive-technology coverage and physical touch remain untested. The old unrun entries in the retained evaluation describe earlier subtask checkpoints. The baseline is a frozen negative/regression fixture, not a recommended template. UX owns interaction semantics; Data maintains the complete coordinated-state cards and their numerical fixtures without duplicating bodies in both plugins.

## Transfer to a new brief

The table is illustrative, not an exhaustive list or a one-to-one classifier. Two appropriate alternatives may belong to the same architecture: change the primary entity (object versus shipment), comparison workspace, task sequence or selection locus while retaining the audience and truth constraints. Do not force a guided story onto a repeat staff task merely to produce variety. An authored starting pair or encoding cannot imply a causal, risk or quality ranking that the evidence does not support.

Before implementing another domain, write its entity, task verbs, source fields and provenance, units, value types, allowed transforms, unknown relationships and known-answer cases. Replace the synthetic session thresholds and IDs with derived domain fixtures. Carry this contract to Data; neither the museum nor workshop example defines a universal schema.
