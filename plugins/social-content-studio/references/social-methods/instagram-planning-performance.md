# Instagram planning and performance review

Use this method for an Instagram week plan, an account or post audit, or an evidence-bound next experiment. It combines the useful parts of `ig-plan` and `ig-audit` while removing fixed cadence, default timing, unsupported reach claims, home-directory storage, and fabricated benchmarks. Source provenance: [Instagram agent review](../../libraries/instagram-agent/PROVENANCE.md).

## Inputs and state

Start with the user's goal, audience, offer or teaching promise, themes, available source objects, assets, account identity, constraints, and current authorization. Read existing project records for voice, prior variants, published/scheduled states, and the last review window. Do not create `~/.claude/instagram` files or a second global calendar. Store any approved plan, log, swipe file, or raw analytics in the owning project using its existing records and privacy policy.

For planning, request only what materially changes the plan: what the account is trying to accomplish, who it serves, what actually happened recently, available assets, and the accounts or conversations that matter. A topic is not an angle. Each candidate needs a source or observed event, intended reader action, format, owner, variant ID, review state, and proposed timing with timezone. Proposed timing is a candidate until reconciled with the existing calendar and any native queue.

Do not require a universal weekly post count, Reel percentage, daily Story count, engagement quota, or time-of-day rule. Use the account's capacity, audience evidence, source inventory, and current cadence. If timing data is absent, say so and choose a reversible test window. Treat timing as a later variable after content, audience fit, and asset readiness have been checked.

## Plan format and engagement

Create a small sequence that varies useful formats and avoids repeating one source or hook without reason. For each slot provide:

```
date/time/timezone candidate | format | theme and specific angle | source/asset ID
hook or opening basis | reader action | owner | review state | risk or dependency
```

Include Stories only when they serve a clear conversation, proof, process, or offer. A comment or conversation list should contain supplied or verified public accounts, a genuine reason to contribute, and an opt-out or sensitivity note where relevant. It is a preparation list, not a reciprocal-engagement quota, contact-harvesting ledger, or instruction to comment unattended. Hand comment drafts to `instagram-engagement.md`.

## Account audit inputs

Use the strongest available source, in order: native insights export or supplied records with definitions, screenshots with collection dates, retention graphs, or a smaller set of post IDs and counts. Capture for each post when available:

- native post ID, URL, format, publication time and timezone;
- observation time, post age, account/follower context, and organic or paid scope;
- views or plays, reach, impressions, interactions, comments, saves, shares/sends, follows, profile actions, and non-follower share;
- Reel retention or average watch time when supplied;
- source/asset, theme, hook, length, visual treatment, and whether an attended reply occurred.

Never fill missing values with zero. Preserve each metric's native definition and collection date. Do not compare unlike formats, ages, scopes, or account periods without flagging the limitation.

## Descriptive metrics

Compute only when denominators and definitions are present. Show the working and label each result descriptive:

| Metric | Calculation | Interpretation limit |
| --- | --- | --- |
| Outlier multiple | post views or plays / the account's median for a defined comparable window | describes relative unusualness, not causality |
| Non-follower reach share | non-follower reach / total reach | indicates observed distribution within that account window |
| Early retention | viewers remaining at the supplied early interval / viewers who started | only use the interval actually supplied; do not assume a universal 3-second field |
| Average watch time | native average watch time | compare only with matching format and duration definitions |
| Sends per reach | shares/sends / reach | a descriptive sharing signal, not a guaranteed growth mechanism |
| Follows per reach | follows / reach | a profile conversion signal, not proof of content quality |

Rank by a declared metric only within comparable records. Use medians and small-sample warnings. A post with high attention and low follows may suggest a profile or offer problem; a low-reach post may still create a qualified enquiry. Keep that as a hypothesis until the account record supports it.

## Find a pattern without overclaiming

Compare clearly defined top and bottom examples, then inspect in this order:

1. opening or first meaningful beat;
2. source/theme and the claim or proof;
3. format and duration;
4. visual/audio/caption treatment;
5. attended conversation and profile path;
6. day and time only if the earlier variables do not explain the observation.

State each conclusion as `claim -> evidence -> limit -> confidence`. Six posts cannot establish a reliable account rule. A larger sample still cannot prove a causal algorithm explanation. Do not use “viral,” “works,” or “best” without defining the metric and cohort.

## Output and next test

```
INSTAGRAM AUDIT
window: <dates, observation dates, account and scope>
sample: <n, comparable cohort and missing fields>
TOP/BOTTOM: <declared metric, records, values and source>
WHAT THE DATA SUPPORTS:
1. <claim> -> <evidence> -> <limit> -> <confidence>
2. ...
DO NOT INFER: <causal, reach, authorship or policy claims not supported>
NEXT TEST: <one change, success measure, cohort, duration, owner>
PROFILE OR FORMAT FOLLOW-UP: <candidate with reason>
state: descriptive review; no publish or schedule action
```

Hand the conclusion back to the planning method and, when a separate research method exists, to the Reel pattern research owner. A public “viral” example is a prior, not proof for this account. Any pattern research must retain source URL/ID, capture date, niche, sample, rights/attribution, observed mechanism, uncertainty, and the original script's independent evidence. Do not import upstream crawler or `yt-dlp` guidance, heuristic PASS labels, or home-directory swipe files. Use the [local observation helper](../../skills/short-form-video/scripts/reel_research.py) and the research method’s input contract for arithmetic. Preserve baseline provenance, missingness and metric definitions. It does not establish representativeness or perform a causal analysis.
