# Case 2 — Interrupted work and recovery (synthetic)

**Labels:** a synthetic scenario with the design described in words. There's no prototype and no participant data. The baseline critique is illustrative, written by this lane. The same scenario facts as case 1 apply.

## Scenario

The coordinator is building a capacity scenario. They have changed three values, none of them applied to source data yet:

- S04 capacity 30 → 20
- S07 capacity 25 → 30
- S09 capacity 30 → 35

They're about to review S07. A phone call interrupts them. They return 25 minutes later, and the authenticated session has expired in the meantime.

## "Before" behavior (described)

1. There is no warning before the session expires.
2. After re-authentication, the app lands on the dashboard home. The scenario is gone.
3. In an alternative version of the same product, the scenario is *silently* restored: the cards show the scenario values with no marker, exactly as in case 1's F4.
4. The one control, labelled "Save", writes the scenario over the source values.

## Baseline-style critique (illustrative)

| # | Finding | Problem |
|---|---|---|
| B1 | "Persist state on interruption (Casey persona: 'Is state preserved?')." | Correct but incomplete. Preservation alone gives variant 3, which risks treating scenario values as real (HS-04 counterexample) |
| B2 | "Add 'Are you sure?' before Save." | Doesn't disclose *what* Save overwrites. A generic confirm on a frequently used button (HS-05) |
| B3 | "Users will be frustrated by losing work." | Plausible, but it's an emotion claim without an evidence type. The finding stands on the data-loss fact (WCAG 2.2.5 / 2.2.6) and doesn't need the emotion claim |

## Upgraded critique

| ID | Observation | Card / standard | Recommendation | Severity (conf.) | Verify |
|---|---|---|---|---|---|
| R1 | Session expires without warning while unsaved scenario changes exist | HS-04; WCAG 2.2.6 (AAA), 2.2.1 (A) where a time limit applies | Warn before expiry and offer an extension. If the person is away, keep the draft scenario (disclosed) through re-authentication | 3 (medium) | Force expiry in a test environment; check the warning, the extension and the retained draft (not run) |
| R2 | Scenario lost after re-authentication | HS-04; WCAG 2.2.5 (AAA) | Return to the same view with the draft intact | 3 (medium) | Same forced-expiry test |
| R3 | Silent restoration (variant 3) | HS-04 counterexample; HS-03 | On return, show a **resumption cue** where the work resumes. For example: "You were building a scenario: 3 changes, not applied. Last: S09 30→35. Next unreviewed: S07." Actions: **Continue reviewing** (focuses S07), **Review all changes**, **Discard scenario**. Scenario cells keep their dashed outline, and source values stay visible | 3 (medium) | Interrupted-task protocol: time to resume, wrong-step resumption, and whether scenario values are misreported as actual (not run) |
| R4 | "Save" overwrites source data | HS-05; X03 3.3.4 concept | Rename it to say what it does ("Apply 3 changes to source data…"). Add a review step listing each change and its downstream effect ("exports made after this use the new values"). Keep "Save scenario as draft" separate and non-destructive. Offer undo only if versioning exists | 3 (high: consequence is clear) | Inspection: every commit path lists the objects it changes. Seeded-error walkthrough |
| R5 | The pending intention ("review S07 next") exists only in the person's head | HS-04 (X07 p. 40: the cue must exist at suspension *and* at resumption) | Record the current focus automatically when it changes (last-edited and next-unreviewed rows), so the cue exists before any interruption. Don't depend on the person saving a note | 2 (low: inference from the model, not tested) | Walkthrough: suspend at each step and check the cue is accurate |
| R6 | Shared-device risk | HS-04 exception | If the product may run on shared machines, show only "You have an unsaved scenario" before authentication; show the details after it | 2 (context-dependent) | Privacy review |
| R7 | Emotion | HS-07 | No emotion finding. Keep B3's point as a question for the next session: "Does losing a scenario change whether coordinators use scenarios at all?" (test: interview or diary) | n/a | T-EMO |

**What changed between critiques (same facts):** preservation became *preservation plus a cue plus a scenario/source distinction*. The generic confirm became a consequence-specific review with a separate non-destructive save. The emotion claim became a research question.
