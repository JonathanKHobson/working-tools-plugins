# LinkedIn post performance: descriptive evidence and next test

Use for li-audit, postmortems, supplied analytics and account feedback. This complements editorial review, not a replacement for it. [Research and upstream corrections](../../libraries/linkedin-agent/PROVENANCE.md). Use a user-supplied export, pasted figures/screenshots, or an already authorized provider; this method has no scraper or analytics connection.

## Normalize before comparing

Capture post ID, format/theme/hook, publication time, observation time, post age, organic/paid scope, followers at posting if known, impressions, members reached, reactions, comments, reposts, and separately saves/sends/clicks/profile views/qualified enquiries when available. Record each source and whether a figure is measured, approximate, missing or reconstructed. Never fill a missing count with zero. De-duplicate IDs and distinguish author replies from reader comments if the data permits. Preserve the raw export privately.

Compare like-aged posts and similar account/audience/paid scope. Define the observation window before ranking. A 2-hour post and a 30-day post should not share a winner table. Prefer a chosen outcome such as relevant conversations or applications; keep business outcomes observed and unobserved distinct. Reactions-only data supports reactions-only comparison, not a fabricated engagement rate.

| Metric | Definition | Interpretation/limit |
|---|---|---|
| Visible-interaction rate | 100 × (reactions + comments + reposts) / impressions | A consistent local subset, not necessarily the platform's all-interaction engagement rate |
| Comment-to-reaction ratio | comments / reactions | Discussion mix; undefined at zero reactions, affected by self replies |
| Impression-to-follower multiple | impressions / followers at posting | Repeated displays per follower baseline; NOT unique reach or proof of nonfollower distribution |
| Unique reach | supplied members reached | Distinct members/Pages estimate; do not substitute impressions |
| Save/send/click rate | 100 × each supplied count / impressions | Separate observed signals; no claim that any is the strongest future predictor |
| Qualified-outcome rate | relevant enquiries or other defined outcome / stated denominator | Requires an explicit attribution window and definition; missing attribution stays unknown |

For local JSON rows use `python3 scripts/linkedin_metrics.py input.json` from the content-calendar skill. The helper calculates the defined observed ratios, validates nonnegative finite numbers, and exposes missing inputs; it does not infer engagement, reach or causation. Optional `--rank interaction_rate_pct` or `--rank impression_follower_multiple` produces only a descriptive ranking; read comparability warnings first. See [input example](../templates/linkedin-analytics.json).

## Interpret with restraint

Report complete rows, unavailable metrics, sample size, window and medians alongside selected top/bottom examples. Inspect audience fit, theme, hook promise/payoff, format, evidence, length and conversation quality before proposing a timing explanation. A numerical ranking does not prove the leading post created more career value; a low-reach niche post may create the meaningful enquiry. A few posts can suggest a hypothesis, never prove no effect or a universal rule. Even 30 posts can remain confounded; do not use a fixed count as statistical permission.

Keep three layers explicit: observed data; plausible interpretation; next test. Avoid causal language from observational differences, absolute winners from tiny denominators, engagement-rate benchmarks without comparable sources, and automated changes to skills based on one result. If showing a rate, show its numerator/denominator or link the calculation. Choose one justified keep/change/stop experiment, its intended outcome and a review condition. Pass it to the existing calendar; stop when the requested audit is complete. No new tracker, contact store or recurring monitor is needed.
