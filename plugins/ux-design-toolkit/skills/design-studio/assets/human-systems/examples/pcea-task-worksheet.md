# PCEA task worksheet

**Attribution:** PCEA (Perception, Cognition, Emotion, Action) is Kyle Hobson's proposed extension of the PCA task-analysis framing (U15 [0008]–[0012]). It's used here as a candidate lens, not a validated method. The supporting columns (Feedback/Feedforward, Error/Recovery, Workload, Context) are this packet's additions, drawn from X10, X03, X06 and X07. They don't rename Kyle's model.

**Status:** template plus a reviewer-only filled example. No participant sessions were run, so every Observed and Self-reported cell below is empty or a placeholder.

## Rules for filling it in

1. **One row per task step** at the grain of one decision or action. Name the step with a verb ("Compare S04 with S09").
2. **Perception:** what the person must notice, and whether it's present and salient *at that moment*. Record the source: design artifact, rendered screen, or observation.
3. **Cognition:** what must be known, decided or remembered. Mark **carried items** — things that must be held across a gap (HS-02) — and mark recognition vs. recall.
4. **Emotion** is split into three columns, and must never be merged:
   - **E-observed:** behavior seen in a real session, with the interpretation in brackets and the behavior itself kept separate. Facial expression alone doesn't qualify (X08).
   - **E-self-reported:** the participant's own words or ratings, verbatim.
   - **E-inferred:** the reviewer's hypothesis, which must include *(alt: …)* for an alternative explanation and *(test: …)* for how it would be checked.
5. **Action:** the control, input mode and motor demand. Note repeated rapid pointing (HS-01), dragging (WCAG 2.5.7) and keyboard path.
6. **Feedback/Feedforward:** what tells the person the consequence before acting, and the outcome after (HS-03).
7. **Error/Recovery:** plausible slip or mistake, and the mechanism — prevent, confirm or undo (HS-05).
8. **Workload / Context:** dominant workload dimension (mental, physical, temporal, frustration, effort) and the situational context: interruption, device, social setting (HS-04, HS-06).
9. **Evidence type for the row:** `inspection` / `rendered-check` / `participant` / `analytics`. A row can't be stronger than its weakest cell that a finding depends on.
10. Leave a cell empty rather than inventing content. An empty Emotion column is acceptable. An invented one is not.

## Blank template

| # | Step | Perception | Cognition (carried items; recognition/recall) | E-observed | E-self-reported | E-inferred (alt; test) | Action (control; motor; keyboard) | Feedforward / Feedback | Error / Recovery | Workload / Context | Evidence type |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | | | | | | | | | |

## Filled example — reviewer inspection only (synthetic)

**Scenario facts** (synthetic, shared with `case-1-dashboard-comparison.md`): a coordinator reviews 12 fictional workshop sessions over 8 weeks. S04 has enrollment 14 of capacity 30, rating 4.6 from 5 responses. S09 has enrollment 27 of 30, rating 3.9 from 22 responses. Task T2 is to compare the two with the same units and scales. The design is the **"before"** design described in case 1: a card grid, a detail drawer that replaces the view, a collapsible week filter, and 16px row icons.

| # | Step | Perception | Cognition | E-observed | E-self-reported | E-inferred (alt; test) | Action | Feedforward / Feedback | Error / Recovery | Workload / Context | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Notice which sessions are under 60% occupancy | Occupancy shown as unlabeled donuts on 12 cards; no threshold line | Must estimate % from donut angle and compare to a remembered 60% threshold (recall) | — (no session run) | — | Uncertainty about whether S04 "counts" as low (alt: coordinator knows these sessions well and doesn't hesitate; test: first-click and time-to-identify in a task session) | Visual scan; no action | None: no threshold marker (no feedforward about what "low" means) | Misclassifying 58% vs 62% sessions; no prevention | Mental demand; glance use at start of week | inspection |
| 2 | Open S04 details | Card title; drawer opens over the grid | Must remember S04's occupancy after the grid is hidden (carried item 1) | — | — | — | Click card (large target, fine) | Drawer animation; no persistent "comparing" state | Opening the wrong card; recover by closing | Low | inspection |
| 3 | Note S04 rating | "4.6 ★" with no response count | Must carry rating and **must infer** reliability without n (carried item 2; missing information) | — | — | Possible over-confidence in 4.6 (alt: coordinator already knows n is small; test: ask participants to rank the two sessions on quality and to justify) | Read | — | Misjudging quality from 5 responses; no prevention (n hidden) | Mental | inspection |
| 4 | Close drawer, open S09 | Grid returns and scroll position resets to top | Carried items 1–2 still held; must re-find S09 (recall of position) | — | — | Frustration from lost place (alt: none needed if the grid is short; test: count re-scrolls and back-and-forth opens) | Scroll plus click | No feedback that S04 is "held" for comparison | Comparing against a mis-remembered S04 value; no recovery aid | Mental + effort; possible interruption between opens | inspection |
| 5 | Compare the pair | Two values never co-visible | Compare 46.7% vs 90% and 4.6 (n=5) vs 3.9 (n=22) from memory; units consistent but not co-located | — | — | — | Mental comparison | — | Wrong conclusion ("S04 is better quality") | Mental; decision stakes moderate (which session gets attention) | inspection |

**What the worksheet shows:** carried items peak at four (two occupancies, two ratings) plus one missing element (n). This points to HS-02 (co-locate comparison) and to lane01's rating-with-n requirement, not to "fewer cards". The emotion column contains only hypotheses, each with a test. None is presented as a finding.

## How a participant observation would be recorded (format only, no data)

| E-observed | E-self-reported |
|---|---|
| `[behavior, e.g., reopened the week filter N times within M seconds]` → *(interpretation: possibly unsure of current scope)* | `"[participant's verbatim words]"` or `[post-task rating on the stated scale]` |

## Mapping Kyle's original scenario (for provenance)

In U15, the emotions "apprehension about his oral hygiene or relief after brushing" [0009] come from Kyle's *hypothetical* persona Kevin Brooks. In this worksheet they would belong in **E-inferred** (source: author's hypothetical scenario), each with an alternative and a test. That isn't a criticism of the proposal. It's how the worksheet keeps Kyle's instinct — emotion matters at every step — while distinguishing it from observed evidence.
