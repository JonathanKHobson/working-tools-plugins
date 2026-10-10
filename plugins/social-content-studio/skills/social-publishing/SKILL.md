---
name: social-publishing
description: Carry authorized social publishing or an established course/video/article handoff through account checks, native scheduling and verified readback. Distinguish drafts, reservations, schedules and publication; follow narrower user instructions first.
---

# Social Publishing

Execute the user's requested platform action using the available native app, connector, or platform UI. This skill owns the state transition and receipt. `social-content` owns copy and previews; `research-methodology-local:current-social-research` owns recent public evidence; `marketing-strategy-studio:marketing-strategy-operator` owns marketing strategy and SEO.

For source-triggered cross-channel work, read [connected publishing](../../references/social-methods/publishing-ecosystem.md) and the current project policy before producing or scheduling derivatives. An established authorized handoff can include YouTube, LinkedIn and Substack; a file attachment alone cannot. Use existing account reviews to reconcile deferred dates, with no extra watcher or scheduler by default.

For LinkedIn articles, current [official article guidance](https://www.linkedin.com/help/linkedin/answer/a522427) documents a Clock beside Publish and Manage settings for article URL, SEO title and description (checked October 2, 2026). Verify these controls in the account and read back the article's native future schedule; do not assume ordinary post limits or the article's companion are identical. See the [observed article controls](references/youtube-linkedin-scheduling.md#linkedin-article-controls) for publication selection, scheduling rejection and draft recovery. Helpful comments are separate attended actions, never presumed future scheduled records.

For a YouTube lesson or Short paired with a LinkedIn post, use [YouTube and LinkedIn scheduling](references/youtube-linkedin-scheduling.md) for inventory, link dependencies, native schedule limits, captions, provenance, and receipts. Recheck platform rules when publishing.

For an existing YouTube catalog upgrade, use [YouTube catalog packaging](references/youtube-catalog-packaging.md) for stable-ID inventory, thumbnails, playlists, native experiments, education metadata, cards, captions, and exact readback. Keep the current release schedule and user edits unless the requested change specifically alters them.

For authorized Substack article production or future publication, read [Substack publishing](references/substack-publishing.md) for source-to-article craft, observed editor/SEO/audience controls, purposeful formatting, native previews and saved schedule verification. Recheck audience and comments: an inspected blank draft defaulted to paid-only. Do not assume title/body autosave also saves each settings form.

For authorized TikTok preparation, curated backfill or attended native scheduling, use [TikTok native scheduling](references/tiktok-manual-publishing.md) for source selection, clean-master reuse, current-account controls, disclosures, queue readback and eventual public verification. TikTok videos must use future native schedules on different calendar days, at most one video per account calendar day; immediate/Now posting is prohibited. Both direct source exports and custom variants are supported with distinct IDs/receipts; authorized owned-account reuse is acceptable. Verify shared sources are public before scheduling, check the live queue/horizon and save date/time/timezone receipts. No posting API, external scheduler service, bot or unattended UI loop is added.

For a local release ledger, run `python3 scripts/inspect_queue.py <ledger.json> --as-of YYYY-MM-DD [--horizon-days 90]` from this skill folder for read-only JSON validation and advisory deferred LinkedIn candidates; confirm eligibility in the live composer.

## Before the action

1. Read the user's requested action and existing authorization. Do not ask for permission again when the current conversation already authorizes the exact post or schedule. If the user requested a draft or human approval, preserve that hold.
2. Make the action concrete: platform, account identity, final copy, ordered assets, alt text, link destination, audience/visibility, schedule and timezone if relevant. Resolve a material mismatch before acting. Do not silently use a different account, substitute an asset, or change a URL.
3. Apply `writing-quality-studio:natural-prose-editor` to the final outgoing text, including title/subject, body, captions and calls to action, before publishing, scheduling or updating. Use its editorial gate for articles/Substack/newsletters and route substantive source issues to `humanizer-deep-audit`. Reuse completed unchanged reviews, but recheck any later composer edits and every personalized variant. Kyle’s authored newsletter email editions contain no em dashes; preserve authentic quotations. Browser actions require final saved-text readback because the Gmail connector hook does not cover them. Then check supported facts, privacy, accessibility, platform norms, and any formatting limits in the actual composer. A preview mockup may help presentation review, but it does not confirm the platform's live composer or policy.
4. If credentials, cost, new integration setup, or a destructive deletion introduces a new decision the user did not authorize, make the boundary explicit. Routine navigation and reversible draft edits within the authorized action may proceed.

## Act and verify

Use the provider's actual publish, schedule, update, or removal action. Then read back the platform record: account, rendered content, assets, visibility, timestamp or scheduled time, and permalink or record ID. Check the link target where feasible. Distinguish:

- **Prepared/previewed:** local copy or mockup; no platform record.
- **Draft:** saved in a platform, not scheduled or posted.
- **Scheduled:** platform record with exact future time; not publicly posted yet.
- **Posted:** platform reports a published record.
- **Publicly verified:** published post visible at its actual URL or by an independent readback.
- **Failed/uncertain:** no reliable receipt or inconsistent state; report what the provider showed and avoid retrying blindly if a duplicate post is possible.

For an edit or removal, verify the changed or absent live record. If the action is not available through the current tools, prepare the exact final payload and state that no platform action occurred. Never call a preview result a publishing receipt.

For platform-specific conversation or inbox work, read the selected section of [platform-native cycles](../../references/social-methods/platform-content-cycles.md). Existing current authorization, attended-action boundaries and exact native receipt procedures govern; a new method or source trigger grants no extra action authority.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Social Media Manager. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
