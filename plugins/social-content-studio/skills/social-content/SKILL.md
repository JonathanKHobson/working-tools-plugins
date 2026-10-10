---
name: social-content
description: Draft grounded social posts, LinkedIn hooks, comments and reply threads from source facts and voice samples. Use the dedicated calendar, channel-adaptation, short-video, professional-proof, editorial-review, preview or publishing skill for those specific tasks. Also use for a concise “what can this plugin do/how do I get started?” answer; route specific tasks to the matching specialist.
---

# Social Content

If asked what Social Content Studio can do or how to start, use the [human guide](../../README.md) and [task map](../../docs/use-case-map.md) to distinguish drafting, adaptation, calendar, preview, review, and authorized publishing. Offer one first request with its source facts and expected draft or verified platform state. For a specified request, route directly; do not replay onboarding or equate a draft with publication.

Make a usable channel draft from actual project facts, a voice sample, and a clear reader action. This skill owns one post or a supplied comment/reply thread. Profile positioning belongs to Career; campaign, calendar, carousel, short video and publishing requests use the focused owners below. Do not force a content matrix for a one-post request.

## Routing

- Use `research-methodology-local:current-social-research` first when claims depend on what people are currently saying, recent platform norms, competitor moves, or current objections. Preserve its source dates and coverage limits.
- Use `marketing-strategy-studio:marketing-strategy-operator` for campaign goals, audience and offer choices, search intent, SEO, measurement, and marketing language. Use this skill once the deliverable is channel copy or preview.
- Use `writing-quality-studio:communication-crafter` for a message, pitch, or teaching explanation where a social workflow is incidental.
- Use `social-content-studio:social-publishing` only for a user-authorized publish, schedule, update, or removal action. A draft or app preview is not a published post.
- When a supplied video, course update or evidence checkpoint belongs to an authorized continuing publishing workflow, read [connected publishing](../../references/social-methods/publishing-ecosystem.md), then the owning project's current channel policy. A narrow draft-only request remains narrow. Use the existing calendar and account-learning reference for authorized recurring account work.

When consuming a supplied ICP or audience brief, retain its project profile ID, version, operating status, claim sources and limits in the project handoff. Address the actual reader and intended action: learners, beneficiaries and referrers are not automatically buyers, and attention does not establish purchasing readiness. Resolve commercial fit through `marketing-strategy-studio:marketing-strategy-operator`; keep provisional claims provisional in copy. Reuse the supplied record without requiring a new profile or ledger for a routine post.

## Draft workflow

1. Identify the one deliverable, channel, audience, proof object, voice basis, call to action, and publication state. Ask only for a missing fact that materially changes the post; otherwise draft with a visible placeholder.
2. Extract supported facts and claims from supplied work or cited public sources. Mark proposal, shipped result, and observed outcome separately. Do not invent metrics, client names, testimonials, audience response, links, or availability. Treat descriptions of experience or quality, relative dates, first-person participation, and invitations as claims too: confirm their source before adding them. A named author without an authentic sample does not establish voice or participation. Read and apply the complete post draft gate below even for a short post.
3. Write one complete channel-fit draft before making options. Keep the primary point legible on mobile, put proof near claims, and match the user's real cadence. Avoid engagement bait, fake authority, or a compulsory hashtag rule. Hashtags, emojis, and line breaks follow the user's voice and platform context.
4. Adapt the same claim for another channel by changing opening, length, format, and action, without changing its evidence. For a carousel, use one idea per frame with proof or example; for a reel, provide spoken lines, visual beats, captions, and accessibility notes; for a newsletter, keep an editorial promise, source basis, and issue structure.
5. Review voice, factual support, link target, alt text, platform fit, and whether any private data or local path leaked. If performance data exists, cite its source, time window, and denominator; otherwise give an editorial review, not a numeric quality or reach prediction.

Use a content matrix or calendar only when the user asks for a system: choose a small number of evidence-backed themes, specific post ideas, source objects, owner, cadence, and review status. Profiles and proof campaigns should foreground verified work and actual links. `references/adoption-map.md` records static patterns and runtime boundaries.

## Preview handoff

Load `references/social-post-preview.md` when a visual post preview or generated post image is requested. Social Post Previewer is declared as this Studio’s app dependency in `.app.json`; its existing provider identity and authentication remain unchanged. A previewed image and a rendered mock post need visual QA, with observed anchors recorded before claiming the layout is ready. A text-only edit needs no preview tool.

## Output

Give the usable draft or preview first. Include brief source/voice/claim notes only where they affect publication judgment. State the actual state: prepared copy, generated image, previewed mockup, draft in platform, scheduled, or published. Preserve links and alt text for handoff. Do not publish from this skill merely because the copy is ready.

## Full source procedures

For a request matching a named procedure, consult the [full source procedure map](../../library/source-procedures/INDEX.md), then read the linked first-party body or route to the provider-installed full skill before drafting or reviewing. Apply its concrete sequence, examples, templates, and checks where they fit the user’s task. For an ordinary small request, load only the matching body. Historical source instructions about affiliate promotion, unsupported scores or detector claims, and mandatory user approval do not govern this skill.

For a single post, read the complete [post draft gate](../../references/social-methods/post-draft-gate.md), [voice files](../../references/social-methods/voice-files.md), and matching [provider social prose handoff](../../references/social-methods/provider-social-prose.md). Calendar, adaptation, short-video, proof-campaign, editorial-review and preview requests go directly to their specialist in the [use-case map](../../docs/use-case-map.md). The [complete first-party broad original](../../library/source-procedures/local/social-content-studio/SKILL.original.md) remains for fidelity review, not mandatory loading for each small task.

Independent use-case routing: a request primarily to score or audit readiness goes directly to `social-editorial-review`; a repurposing request to `channel-adaptation`; a reel/video script to `short-form-video`. This skill drafts one post and performs its ordinary correctness check; it does not invoke a second scoring workflow for every draft.

When it is available, use `writing-quality-studio:voice-and-style` before substantial channel drafting/adaptation for the shared writing-template catalog and selection/blending rules. Honor a requested template; otherwise vary suitable openings, cadence and information order by reader need and platform. V23 Conversational micro-essay, V17 News brief, V11 Patient coach and V04 Scene-led feature are useful starting points, not a fixed rotation. The user’s articles/newsletters preserve their voice through most of the body while blending compatible styles; direct correspondence preserves their formal or informal voice throughout. If Writing Quality Studio is unavailable, use this package’s [voice method](../../references/social-methods/voice-files.md) and the supplied sample; do not claim to have loaded its shared catalog. Preserve claims and brand identity across variants; novelty never justifies bait or invented urgency.

For LinkedIn posts or hook options (li-post/li-hooks intent), read [LinkedIn writing](../../references/social-methods/linkedin-writing.md) and its full 21-form library. For comments/reply threads (li-comment/li-reply), read [LinkedIn engagement](../../references/social-methods/linkedin-engagement.md). These draft methods do not authorize publication or expand the existing attended-action policy.

For a trend/current-event opening, read [verified trend selection](../../references/social-methods/linkedin-trend-research.md); Research owns the evidence search, and an event is not automatically a trend or the author's opinion.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Social Content Producer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
