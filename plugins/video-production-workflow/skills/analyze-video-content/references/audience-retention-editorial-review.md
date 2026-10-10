# Audience retention to a bounded editorial experiment

Use when a user requests pacing/retention diagnosis or supplies video-level retention
evidence. This is conditional analysis; do not revise released lessons merely because
analytics exist. Marketing owns traffic, audience and format comparisons; Instructional
Design owns whether learners can perform the objective. Retention is viewing evidence,
not proof of learning or a causal explanation.

## Intake and timeline identity

1. Record the video ID/URL, analyzed version, final-render SHA-256, duration, analytics
   export/screenshot date, reporting window, metric labels and units, available view
   counts, audience segment, traffic context and comparison basis. Keep raw evidence
   immutable in the project. If the hosted version cannot be linked to local bytes,
   state that uncertainty and verify timing on the actual hosted player before mapping.
2. Reuse the final output-timed transcript/captions and chapter map with their hashes.
   Source transcript times need the verified EDL mapping first. A trim, reorder, speed
   change or replaced upload invalidates prior timing analysis. Never guess duration
   or infer whether an unlabeled CSV axis means seconds, a fraction, or a percentage
   just from its maximum. Read headers/metadata; ask for the missing unit if material.
3. Use only the relevant evidence. If CSV export is unavailable, an observed Studio
   chart with approximate intervals is valid with its resolution limit stated. Check
   current Studio controls instead of promising a fixed export path. Do not scrape,
   create accounts, or upload private analytics to a new service.

## Observe before explaining

Map a few material intervals to the exact reviewed timeline. Retain both sides of a
drop/spike and enough surrounding speech and screen activity to understand the task.
Inspect the actual frames and audio at those moments; a transcript alone cannot show
cursor progress, text readability, private UI, or a completed demonstration.

| Interval / precision | Observed metric movement and units | Said / shown, evidence | Possible explanations | Editorial choice |
| --- | --- | --- | --- | --- |
| 01:10–01:20, chart estimate | 64% to 52%, 12 percentage points | Output transcript + sampled frames: demonstration ends, recap begins | Seeking next task, leaving after payoff, repetitive recap | Try a shorter signpost in the next comparable lesson; preserve the task result |

The example is synthetic, not an actual performance result. Percent-point change is
not percent change. Treat dips as skipping or stopping possibilities; spikes can
reflect useful rewatching, sharing, or unclear content. Normal taper, a chapter seek,
changed traffic, or a task successfully completed can change the curve. Label each
explanation as a hypothesis; do not say a sponsor, long pause, opening, or edit caused
the loss from curve shape alone. Do not classify a curve using universal retention,
CTR, or drop thresholds. Compare similar purpose, duration, format and audience when
data permit; report small samples, unavailable segments and changing cohorts.

Before recommending expensive editing, inspect the title/thumbnail promise against
the opening, first demonstrated action, and actual payoff. Separate a misleading
promise from a slow explanation and from a valid teaching pause. Route packaging
strategy to Marketing and truthful thumbnail design to Graphic Design Studio.

## Choose one useful experiment

Rank candidates by reader/learner value, evidence confidence, editing cost and risk
to meaning. Select one bounded experiment or explicitly retain the existing edit.
The project experiment record must include:

- Observation and exact interval, evidence/hash and uncertainty.
- Hypothesis plus a plausible alternative explanation.
- One change: e.g. preview the resulting artifact before setup, add a topic signpost,
  shorten a redundant recap, or clarify a confusing screen action.
- Must-keep prerequisites, caveats, instructional pauses, complete demonstration,
  speaker meaning, accessible captions and privacy masks.
- Evaluation: relevant comparable video/window/segment when available; source and
  denominator for metrics; task-completion or learner feedback if learning matters.
- Decision rule tied to this project's objective, and a stop/review condition if
  evidence remains inconclusive. No guaranteed uplift or causal claim from a before/
  after comparison with multiple changes.

For an authorized edit, `edit-dialogue-footage` owns the EDL and output-time remap;
`validate-video-quality` owns the actual render and final hashes. Recompute captions,
chapters and retention mapping after every timing change. For an excerpt that has its
own useful payoff, use the existing course Shorts procedure. A retention spike alone
does not establish that an excerpt is coherent or appropriate to promote.

Return the observed interval map, one editorial decision/experiment, and the exact
next owner. Distinguish analysis prepared, edit rendered, audiovisual review completed,
released and experiment evaluated. Historical source gates do not override current
user authorization or review holds.

## Source basis

Adapted selectively from Jake Schincariol's `yt-retention` at commit
`a2feb2104981a375ffd4f87ee04f4f5344ac43c6` (MIT), preserved inactive with supporting
code and license under [source preservation](../../../libraries/youtube-agent-methods/PROVENANCE.md).
The original's universal healthy/leaking thresholds, guaranteed causal diagnoses,
mandatory copy/paste approval question, CSV-axis guessing and code were not adopted.
No downloaded helper is executed by this method.

Official [YouTube retention help](https://support.google.com/youtube/answer/9314415?hl=en),
verified 2026-10-01, controls current metric meanings and Studio capabilities; recheck
it at use time. It explains dips, spikes, intro and audience segments, not a universal
success target.
