# Instagram short-form research: creator-relative outliers

Use this method when the user wants to know what is working among comparable Reels: "what's working in my niche", "build a swipe file", "why did this reel do numbers", "what should I make next". It lives under `short-form-video` and feeds its scripts. Published-post review of the user's own analytics stays with `content-calendar`. That review reuses the baseline rules in this file, so the two analyses stay consistent.

[Source and adaptation](../../libraries/instagram-agent/PROVENANCE.md): MIT `ig-viral`, `swipe.py`, `ig-audit` and hook forms.

- **Adopted:** ranking views against each creator's own baseline, reading unclassified hooks by hand, attribution, copying a structure rather than content, and stating sample limits.
- **Not adopted:** bulk collection, copied `yt-dlp` commands, the follower-count baseline fallback, the "3x is a signal" threshold, predictive hook scores, and home-folder swipe files.

## Boundaries

- **Find accessible observations.** Use Research Studio and available authorized browsing/search to locate relevant public accounts and posts, or use supplied records, Saved collections, insights and exports. Record exact URLs and what was actually accessible. Inspect a bounded set of pages through approved read-only tools; never harvest a feed, collect credentials, bypass access controls, run a crawler or start a background loop. If counters or media are inaccessible, retain that gap and request supplied evidence. This workflow must not fabricate current niche research from memory.
- **Reading is not engaging.** No following, liking, saving, commenting or messaging happens as part of research.
- **Adapt a mechanism into original work.** Attribute every row. Never reproduce someone's script, footage, audio or edit.
- **Cross-platform samples are hypothesis sources.** YouTube Shorts, TikTok or other observations may suggest a hook shape. They are not evidence of Instagram performance, and the report keeps them in a separate table.
- **No predictive scores.** Hook formula labels describe shape. Text heuristics may flag obvious problems such as a greeting, a preamble or nothing concrete in the opening. The source reports a YouTube hook experiment, but its dataset and measurement code are absent. Those results are unverified author claims and cannot validate a score. No text score ranks or gates hooks.
- **No benchmark claims.** Never state industry norms such as "good hold rate is X" or "3x is viral" without supplied, comparable data.
- **Storage.** Write the comparison table and findings into the user's project, if a file is wanted. Never use a default home-folder store.

## Step 1: define the question and comparison set

State in one line what decision the research informs. Example: "Which opening shapes to test for the next four contract-clause Reels." If no decision exists, say the research is exploratory and shrink it.

Use the supplied account set or select a small justified set within the requested niche, recording your criteria. Ask only when a missing niche or consequential scope choice prevents useful research:

| Group | Purpose | Caution |
|---|---|---|
| Direct peers | Same audience and offer, similar size | Most comparable |
| Adjacent | Same audience, different topic | Format ideas only |
| Larger accounts | Format reference | Audience and reach not comparable; excluded from size-relative claims |
| User's own Saved items | Taste-filtered ideas | Survivor-selected by definition; hypothesis only |

Record each account's size and audience context when available. Similar follower counts do not establish similar distribution, audience or purpose.

## Step 2: record observations

One row per post. Collect at the user's own pace and from views they can legitimately see.

```
account | platform | post_id/url | posted_date | observed_date | age_days |
format | length_s | views | views_basis | paid_or_boosted (y/n/unknown) |
collab/remix (y/n/unknown) | pinned (y/n) | hook_spoken | hook_onscreen |
cta | notes
```

Rules:

- Capture only the short opening excerpt needed for analysis, spoken and on-screen separately, with attribution and source location. Use a paraphrase for longer material; do not reproduce a full third-party script.
- Record `views_basis` exactly as displayed (for example "views counter on grid", "insights: plays"). Displayed definitions differ between surfaces and can change; never merge different bases.
- **Missing is not zero.** Leave unknown blank. Record a genuine displayed 0 as 0 and flag it.
- Record post age. A post seen at 2 days and one seen at 90 days are not comparable.
- Mark paid/boosted, collab, pinned and remix status as known or unknown. Each can inflate or redirect distribution.

## Step 3: build each creator's baseline

For each account, the baseline is the **median views of that account's comparable posts**: same platform, same views basis, a similar format, and ages within a stated window (for example "posts aged 14–90 days at observation"). The candidate post itself is excluded from its own baseline.

Report the baseline with its inputs:

```
@acct_a  baseline 10,700  (median of n=11 Reels, aged 14-90d, views counter;
         excluded: 1 pinned, 1 marked paid, 2 younger than 14d)
```

Baseline validity:

| Situation | Action |
|---|---|
| Representative comparable observations available | Calculate the median, report all input IDs/counts, selection rule and uncertainty; no sample size alone validates it |
| Sparse or selected-only observations | Describe what is available and flag instability/selection; withhold the ratio when it would misrepresent a typical post |
| Median is 0 or most values missing | **No baseline**; report why |
| Only follower count available | **No baseline.** Do not substitute followers. Followers are not typical views. |
| Mixed formats or bases | Split by format/basis or drop the mismatched rows, and say which |

Report the number of observations and the selection basis regardless. A median computed from hand-picked winners is not a typical-post baseline.

## Step 4: compute and rank

`multiple = views / creator baseline`, only where both are valid. Show the numerator and denominator for every row.

Compare multiples only within the same platform, native metric definition, format, paid scope, age window and declared cohort. The helper groups but does not rank; any manual ranking must retain those comparability checks. List the rows that could not be ranked, and why, beneath the ranking; do not drop them silently.

Do not set a "signal" threshold. Describe the distribution instead, for example "of 38 ranked posts, 6 exceeded 3x their creator's median, 21 were within 0.5–2x." Above-baseline posts are the starting point for structural reading, nothing more.

Confounds to state beside each top post when they apply:

- paid or boosted, or unknown
- collab, remix or trending audio not available to the user
- an outside event (news, a large account sharing it)
- post age at observation
- pinned or old posts surviving on the grid (survivor selection)
- the creator deleting weak posts, which inflates the median and is unknowable

### Local arithmetic and input contract

Run the bundled [observation helper](../../skills/short-form-video/scripts/reel_research.py) from the plugin root:

```sh
python3 skills/short-form-video/scripts/reel_research.py observations.json
```

Start from the [synthetic input example](../templates/reel-research.json), replacing every example with actual observations. Required row fields are `source_url`, `account`, `platform`, `views`, `baseline_views`, `metric`, `window` and `cohort`; an optional unique `id` aids lineage. Keep unavailable views/baselines null. Numeric inputs must be actual finite nonnegative numbers, not rounded strings such as `1.2M`; retain the original display separately and label any estimate.

Supply either an explicit `baseline_views` with its `baseline_count`, `baseline_source` and `baseline_window`, or `baseline_views: null` plus `baseline_samples` and that provenance. Samples must exclude the candidate and match its declared scope; include their actual IDs/exclusion rationale in the project evidence. The helper computes the median, but cannot verify that a sample is representative or collected from the same account. Conflicting explicit baseline and sample inputs are rejected.

Output preserves every valid row, distinguishes missing/zero/unavailable ratios and groups platform, metric, window and cohort. It performs no global ranking, fetch, file write or statistical inference. Put format, paid scope and duration/age matching into the cohort/window; different account observations need human comparability review even when labels match. Baseline provenance warnings are evidence gaps to resolve before interpreting ratios.

## Step 5: read structure, not scores

Where the sample supports comparison, define nonoverlapping high and low groups within a comparable cohort. State the group rule and counts; do not produce overlapping thirds or force a comparison from one or two posts.

1. **Formula vocabulary.** Label hook shapes using [26 optional hook forms](reel-hook-formulas.json) (for example Cost Confession, Nobody Tells You, Time Collapse, The Steal, Mid-Sentence Start). Label by hand. Leave a hook "unlabelled" when no shape fits; upstream classifier success rates are unverified and no imported classifier score is used.
2. **Unlabelled rows.** Read them all. Repeated unlabelled shapes are candidate new forms; give them a working name with examples.
3. **Observable structure.** Spoken/on-screen agreement, words before the first concrete detail, whether the payoff is visual, length band, where the ask comes, first-frame motion if noted.
4. **Counts with denominators.** "Time Collapse: 4 of 13 upper-third posts across 3 accounts; 1 of 13 lower-third." A shape that appears in one account only reflects that creator, not the niche.

State the confidence in plain words: **suggestive**, **weak** or **insufficient**. Base that judgment on representativeness, missingness, account coverage and confounds, not a fixed sample threshold. More observational data never makes the conclusion causal.

## Step 6: turn findings into the user's version

For the requested number of useful shapes, write the user's own hook in that shape, using their real story and numbers from the voice file or project. Use `{{your number}}` where a fact is missing. Hand each to `short-form-video`'s script workflow with the shape named, and propose a test. Example: "Use Time Collapse on the next two clause Reels. Compare each against your own median of comparable Reels at the same age."

Never hand back "make one like @acct's". Never promise the shape will perform.

## Output template

The following rows and dates are synthetic illustrations, not research findings.

```
INSTAGRAM RESEARCH  · decision: openings for next 4 clause Reels
observed 2026-10-03..10-15 · 7 accounts · 52 rows recorded

COVERAGE
  ranked:     38 (valid baseline, age 14-90d, Reels, views counter)
  unranked:   14 - 6 without representative baseline, 4 too young, 3 paid/boosted, 1 zero median
  cross-platform (hypothesis only, not ranked): 9 YouTube Shorts in a separate table

BASELINES
  @acct_a 10,700 (n=11) · @acct_b 3,200 (n=6, low-n) · @acct_c none (selected-only sample) ...

RANKED (upper third shown)
  18,400 / 4,100 = 4.5x  @acct_d  "Proposals took me five hours..."  Time Collapse
      age 21d · paid: unknown · collab: no
  ...

DISTRIBUTION  6 of 38 > 3x · 21 of 38 within 0.5-2x · median multiple 1.1x

WHAT DIFFERS (upper vs lower third, ranked rows only)
  Time Collapse   4/13 vs 1/13, 3 accounts      suggestive
  concrete number in first sentence 10/13 vs 5/13   suggestive
  unlabelled: 3 upper-third hooks open by reading a viewer comment aloud
              (candidate shape "Comment Read-Out")

LIMITS
  38 ranked posts, 5 accounts with valid baseline: weak.
  Survivor selection: grids show surviving posts; deletions unknown.
  Paid status unknown for 19 rows. No retention data. Not causal.

YOUR VERSION  (tests, not predictions)
  Time Collapse  "Contracts used to take me a day. Now {{your time}}."
  Comment Read-Out  "'{{verbatim question from your comments}}' - here's the clause."

STATE  research notes only · nothing posted, followed or messaged
```

## Using the same rules on the user's own posts

When `content-calendar` audits the user's account, apply Steps 3–5 to their insights:

- age-matched windows
- paid posts separated
- the native metric definitions as displayed, with collection dates
- missing ≠ zero

Upstream's distinction is a useful **hypothesis**, not a diagnosis:
- high reach to non-followers with low follows per reach points toward the profile (route to `instagram-profile.md`);
- low reach with weak early hold points toward the opening.

Check this only if those metrics were supplied. With few posts, say no pattern can be identified.

## Edge cases

- **The user wants automated or bulk collection.** Decline that part. Offer manual recording or a Research Studio route that is already authorized.
- **Only follower counts available.** Report the reach observations descriptively, without multiples.
- **One creator dominates the upper third.** Report per-account results and reduce confidence.
- **Very large outlier** (for example 100x). Check for a confound before reading structure; keep it in the table but do not let it define the finding.
- **Hooks in other languages.** Label shape in the original language; do not translate them into templates.
- **Few comparable accounts exist.** Report narrow coverage; use adjacent examples only as clearly labeled inspiration.
- **Trending audio or remix drives the post.** Mark "audio-led". A text hook finding does not transfer.
- **The user cites a benchmark or a platform rule from an article.** Treat it as an unverified claim. Research owns verification with dates.

## Acceptance checks

- [ ] Decision stated; comparison set supplied or justified within the authorized scope.
- [ ] Every row attributed, dated, aged, with views basis and paid/collab status or "unknown".
- [ ] Baselines report n, window and exclusions; no follower-count substitution; missing/zero baselines listed.
- [ ] Multiples show numerator/denominator; unranked rows listed with reasons.
- [ ] Cross-platform rows kept separate and labelled hypothesis-only.
- [ ] Formula labels descriptive; unlabelled rows read; no text score used to rank or gate.
- [ ] Confounds, survivor selection, sample size and confidence stated; no causal or benchmark claim.
- [ ] User versions use only verified facts or placeholders; framed as tests.
- [ ] No login, scraping, engagement or home-folder store; state reported as research notes.
