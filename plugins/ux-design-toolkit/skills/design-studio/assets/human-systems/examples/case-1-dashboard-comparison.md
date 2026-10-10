# Case 1 — Dashboard comparison (synthetic)

**Labels:** a synthetic scenario and a design described in words. No prototype, screenshot or participant data exists. The "baseline critique" below was written by this lane to show what the inherited rules found in inspected files would produce (L16, L17, L19). It is **not** captured output from a real run of the installed skills. That run is test T-VAR in `evaluation.md` and has not been done.

## Shared scenario facts

These are the same facts used in the worksheet and in cases 2 and 3.

- Brief follows `shared/benchmark-brief.md`: a coordinator reviews 12 fictional workshop sessions over weeks 1–8 and picks two for attention.
- **S04** "Data Storytelling Basics": week 3, enrollment 14, capacity 30 (46.7%), rating 4.6 from 5 responses, cost $1,200.
- **S09** "Spreadsheet Modeling": week 6, enrollment 27, capacity 30 (90.0%), rating 3.9 from 22 responses, cost $1,500.
- These values are illustrative. If lane01's embedded dataset differs, substitute its S04/S09 equivalents; the critique logic doesn't depend on the exact numbers.

## "Before" design (described)

1. A grid of 12 equal cards. Each shows the title, an unlabeled occupancy donut and a star rating ("4.6 ★"), with no response count.
2. Clicking a card opens a full-height drawer that covers the grid. Closing it resets the grid's scroll position.
3. A week-range filter sits in a collapsible left panel. When collapsed, nothing shows the active range.
4. The drawer has a capacity slider. Moving it immediately redraws that card's donut. There's no scenario label and no restore control.
5. Per-row edit and delete icons are 16×16 px with 4 px between them. Delete has no confirmation or undo.
6. Pointer only: the slider has no keyboard arrow support, and the drawer can't be closed with Escape.

## Baseline-style critique (illustrative; based on inherited rules)

| # | Finding | Rule it follows | Problem with the finding |
|---|---|---|---|
| B1 | "12 cards exceeds working-memory limits (≤4). Show the top 4 and put the rest under 'Show more'." | critique.md lines 372–381 | Visible cards are *recognition*. Hiding 8 of them makes the coordinator remember they exist (X05 conditions; X12 #6). The real memory problem, comparing across the drawer, goes undiagnosed |
| B2 | "Touch targets must be 44×44 px." | adapt.md line 46; critique.md line 797 | Presents AAA as the minimum (X03, X04). Ignores the 2.5.8 spacing exception and the density tradeoff. Doesn't mention the real risk: delete sits next to edit |
| B3 | "Apply Fitts' law: make the primary CTA larger." | heuristics-detail.md lines 77–80 | There is no repeated rapid pointing task at the CTA. Fitts' law is misapplied to salience (X01 fn 11) |
| B4 | "Users will feel overwhelmed by the dense grid." | critique.md line 62 (emotional journey) | An emotion claim with no evidence type (X08, HS-07) |
| B5 | "Add an 'Are you sure?' modal to the capacity slider." | Generic H3/H5 | A modal on a frequent, reversible scenario action. The actual gap — scenario vs. source ambiguity — is still missing |
| B6 | "Cognitive load: 5 of 8 checklist items fail → critical." | critique.md line 366 | A count-based severity that doesn't say *which* effort moved where (X06) |

The baseline does catch real issues: an unlabeled donut, and a destructive action with no protection. But its fixes point the wrong way on B1, B3 and B5.

## Upgraded critique using the lane02 cards

Anchors refer to the described design. Severity uses the UXHC 0–4 scale (L05), calibrated for a coordinator who uses the tool weekly and makes moderately consequential decisions (L08). All findings are **inspection evidence**; none are participant evidence.

| ID | Anchor | Observation | Card | Recommendation | Severity (conf.) | How to verify |
|---|---|---|---|---|---|---|
| F1 | Drawer covers grid (design item 2) | To compare S04 and S09, the coordinator carries four values plus a missing n across two drawer openings and a scroll reset | HS-02 | Add a two-slot comparison tray, pinned beside the grid, with the same units and scales (occupancy %, enrollment/capacity, rating with n). Echo the selected pair and the active week range in the tray header. Keep the full grid visible | 3 (medium) | Carried-item count goes from 4 to 0 (inspection). Participant task T2: comparison accuracy and the number of drawer re-opens (not run) |
| F2 | Rating "4.6 ★" (item 1) | Response count is hidden; 4.6 from n=5 looks stronger than 3.9 from n=22 | HS-02 + lane01 contract | Show "4.6 (5 responses)" everywhere a rating appears, with the same precision for both sessions. Don't add significance language (benchmark brief) | 3 (high: the rule comes from the brief) | Inspection: every rating instance shows n |
| F3 | Collapsed week filter (item 3) | Active scope is invisible once the panel is closed, so an empty or low result can't be distinguished from a narrow filter | HS-02, HS-06 | Show a persistent scope chip ("Weeks 3–6 · 7 of 12 sessions") above the results, with "Reset". Keep it even in "minimal" mode | 3 (medium) | T3/T5 walkthrough: scope is visible in every state, including empty |
| F4 | Capacity slider (item 4) | A scenario change redraws the source card with no marker. The coordinator may report hypothetical occupancy as actual | HS-03, HS-05 | Feedforward chip: "Scenario: capacity 30 → 20, occupancy 46.7% → 70.0%". Mark affected cards with a dashed scenario outline, keep source values visible, add "Restore original". *No* confirmation modal, because the change is scenario-only and reversible | 3 (medium) | T4: restore returns every changed value; scenario state is announced (4.1.3) |
| F5 | Edit/delete icons (item 5) | 16 px targets 4 px apart; delete sits next to the frequent edit action and has no recovery | HS-01, HS-05 | Meet 2.5.8 through size or the spacing exception, and separate delete from edit. Delete gets **undo** if the data store supports soft delete; otherwise a review step naming the session. Full 44 px is optional density-for-safety, not a requirement | 3 (medium) | Hit-area measurement; seeded mis-tap walkthrough; undo check |
| F6 | Pointer-only slider and drawer (item 6) | Keyboard users can't do T4, and Escape doesn't close the drawer | Accessibility (H11, Kyle's proposal); WCAG 2.1.1 Keyboard applies (criterion text not re-fetched this session) | Arrow keys on the slider plus a numeric input alternative (also covers 2.5.7 if dragging is ever required). Escape closes and returns focus to the originating card | 4 for keyboard users (high) | T6 at 390 px width: keyboard-only completion (not run) |
| F7 | Unlabeled donuts (item 1) | Occupancy must be estimated from angle; the 60% threshold is remembered | HS-02, HS-03 | Print the % value on or beside each donut and draw the 60% reference in a consistent place. Lane01 decides the encoding (a bar may beat a donut) | 2 (medium) | T1: first-click and time to find sessions under 60% (not run) |
| F8 | — | No emotion evidence exists | HS-07 | Record in the worksheet "possible uncertainty about S04 quality (alt: prior knowledge; test: ranking + justification task)" as a *question*. No emotion finding | n/a | T-EMO audit |

**What changed between critiques (same facts):**
- B1 → F1: the problem moved from "too many options" to "too much carried across a gap", and the fix changed from *hide* to *co-locate*.
- B2 → F5: the fix changed from a universal 44 px rule to meeting the standard's floor plus separating the destructive action.
- B3 was removed as a misapplication.
- B4 → F8: a claim became a test.
- B5 → F4: the fix changed from a confirmation modal to feedforward plus restore, because the action is reversible.
- B6 was replaced by findings that each name what moves and where.

## Structurally different alternatives this unlocks (for lane01; not built)

The same facts and conditions can support different interaction architectures, chosen by context rather than by recoloring:

1. **Comparison workbench:** grid plus pinned two-slot tray (F1), for weekly desk use with a mouse and keyboard.
2. **Exception-first monitor:** a sentence-style exception list ("2 sessions below 60% in weeks 1–8") with ambient scope and last-checked line (HS-06), for a glance at the start of the day.
3. **Scenario sandbox:** a split view of source vs. scenario columns with per-cell restore (HS-03/05), when the task *is* capacity planning.

Each keeps the same controls and units (per `north-star-observations.md`) and differs in task sequence and interaction. Lane01 owns the choice and the build.
