# First-value flows and robust interaction states

Use for onboarding/first-run/first-value flows and for any interactive path where default/error/accessibility coverage in [product and web](product-web.md) is not enough on its own. Scope every check to the actual product's real screens and data, not a generic checklist walked in the abstract.

## First-run, first value and return visits

Identify the actual first thing a new user must do to get value, and check that path with no seeded data, no prior account state and no assumed familiarity. Separately check a returning user's path: does state from a prior session (drafts, filters, partial setup) reappear correctly, or does the return visit silently discard it?

For an invitation or direct link, follow the user's implied intent end to end. If the link already communicates intent to enter, join or open, check whether a second explicit action is necessary for consent, security or a real choice. Keep one prominent next action for the current state; suppress header or global calls to action that repeat or divert from the in-context path. Reveal secondary routes and options when they become useful, without hiding a required decision.

Record the actual first-visit sequence as evidence: initial screen, delayed loading, ready but unjoined, action pending, server-confirmed joined/success, and recoverable failure where feasible. Pending, unjoined and joined must have distinguishable wording and controls, not only a spinner or button color. The action the person used should visibly acknowledge its own result; a status sentence beside it is supplementary. Keep the outcome visible long enough for the user to know what happened and what to do next; use a persistent state acknowledgement when the state itself persists. Match feedback strength to the action. Celebration or animation is optional and should not obscure the next task.

Onboarding help, tours or setup steps must be skippable without trapping the user in a state with no way forward: confirm skip actually lands on a usable screen, not a dead end or a forced restart. If a step is required (e.g., permission grant needed for core function), the skip path must make that requirement clear rather than silently failing later.

## Reduce friction with sensible defaults

Minimize unnecessary actions and optional setup before the user reaches the intended experience. Make the intended, low-risk behavior the default, with a clear, easy opt-out. Respect saved choices and applicable system or accessibility preferences; a default must not override a prior preference.

For example, an atmospheric invitation can play 15 seconds of music when the guest deliberately selects Enter, with a visible Mute toggle before entry and an easy mute control afterward. A separate checkbox to opt into that brief entrance adds an unnecessary action. Honor an existing mute preference, and keep entry usable when audio is muted or playback is unavailable.

This is not a blanket rule against opt-in. Preserve explicit, meaningful consent for purchases, subscriptions, privacy-sensitive actions and behavior that can disrupt accessibility. Reduce friction by removing needless choices, never by hiding consequences or treating silence as consent.

## Extreme and malformed data

Exercise the affected surface with data the design likely wasn't tuned for: empty/zero, single item, very long strings or names, unusually large numbers, missing/null optional fields, and unexpectedly large collections. Confirm layout doesn't break, truncation (if any) doesn't hide the meaning needed for the task, and empty states offer a real next action rather than a blank void.

## Interrupted and stale interactions

Check what happens when a user interrupts an in-flight action: navigates away mid-submit, backgrounds the app during a multi-step flow, or triggers a second async request before the first resolves. Confirm a stale response (from an earlier, now-superseded request) cannot overwrite a newer one on screen — this is a common real defect, not a hypothetical. If the surface allows a permission or auth state to change mid-session (token expiry, revoked access, role change), confirm the UI detects and responds rather than silently operating on stale authorization or crashing.

## Retries, duplicates and recovery

Test what happens when a user resubmits a form (double-click, retry after a timeout, back-button-then-resubmit): confirm duplicate submission is prevented or safely deduplicated, and that the user gets a clear indication of what happened on the invoking control, not just a disabled button or adjacent explanation. Exercise the empty/unchanged branch too: a manual Save clicked with no changes must visibly acknowledge the click without claiming a new write. For Save, a confirmed write could turn the button into a clear green-check "Saved" state; an unchanged click could show "Already saved" or a specific empty-state action. A button that stays at "Save" while nearby text changes fails this check. For an action that can fail (network error, validation failure, server error), confirm there is a specific, actionable recovery path — not just a generic "something went wrong" with no way to retry or correct the input that caused it.

Do not treat a local click handler, optimistic state or navigation as proof of success. Verify the authoritative response and the rendered state after it resolves; if the response is delayed or fails, the interface must not imply completion. Reload or revisit when feasible to check that confirmed state persists and retries remain idempotent.

## Worked example: workshop invitation

In a workshop entry review, the owner reported that loading, ready-but-unjoined and joined looked too similar; a successful Join action lacked a clear visible acknowledgement. A prominent header Join link competed with the in-context path, and a direct invitation still required a second Join click. These are owner-reported observations, not findings from a participant study or proof of the current implementation. An API success or manual happy-path click would establish only that a request completed; it would not show whether a newcomer understood the state or stayed on the intended route. The bounded check is a fresh, unseeded direct-link visit with delayed loading: inspect the primary action and competing header, submit once, compare pending with the server-confirmed membership and persistent joined screen, then exercise failure/retry and reload where feasible. At each state ask what the newcomer can do, how they know it worked, and how they can recover. Record any state not actually exercised instead of awarding it a passing heuristic rating.

## When an action also sends email

Treat the saved product state and notification delivery as separate outcomes. A Save confirmation can be true while email remains queued; show pending, failed or unconfirmed delivery honestly when that status matters to the user. For bursty autosaves, consider a durable quiet-window summary rather than an email per edit. No-op saves should acknowledge the user without producing duplicate notifications. Test interrupted delivery and retries with controlled data; ambiguous provider acceptance must not automatically become either “received” or a blind resend. Keep queue/claim implementation and the chosen delay in the owning product. If delivery requires an open browser, explain that dependency instead of claiming server-side background delivery. A controlled provider test is not proof of arrival in the recipient's inbox.

## Scope discipline

Do not invent hypothetical states the actual product's data model or permission model cannot produce. Check the real state machine (loading/empty/error/success/disabled/stale/interrupted) for the screens actually in scope for the current task, and report which of these were exercised versus which remain unverified due to environment limits (no test account, no way to simulate network failure, etc.).

## Provenance and scope

Original local synthesis addressing gaps identified when comparing existing UX guidance against Impeccable's onboarding and robust-state review methods (source inspected via [design sources](design-sources.md), revision 114ea1d, 2026-09-29). No Impeccable text or tooling is reproduced.

For multi-step exploratory state, read [the complete commit/reset/undo method](exploration-recovery.md). Its history size and synthetic task are examples; trivial controls may need only an obvious local reversal. For linked analytical views, Data Visualization owns the coordinated scope, comparison and scenario truth cards; preserve that single source of method detail.

Preserved state alone does not restore the person’s intention. For suspendable work, read the complete [task resumption card](human-systems/task-resumption.md): record cues before interruptions, distinguish pending and committed state, reconcile stale records and hide sensitive drafts until authenticated. Use the existing [consequence guidance](ux-writing.md) and [confirmation-strength matrix](../../../libraries/frontend-design-premium/skills/frontend-design-premium/references/decision-matrix.md) for prevent/confirm/recover decisions; do not create a second risk table.
