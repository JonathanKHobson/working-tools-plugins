---
name: social-content-studio
description: Plan, draft, score, lint, repurpose, and track human-reviewed social content across LinkedIn, X, newsletters, reels, profile copy, launch notes, and public proof campaigns. Use when the user asks for posts, content matrix, hooks, voice profile, newsletter voice, social campaign, LinkedIn profile, reels script, social proof tracker, or content performance review.
---

# Social Content Studio

Build public content systems that are specific, source-aware, human-reviewed,
and safe to publish. Drafts are useful only when they match the user's voice,
evidence, channel, proof boundary, and approval state.

This skill integrates useful static patterns from `charlie947/social-media-skills`,
`langchain-ai/social-media-agent`, `jqaisystems/jqai-ai-skills`, and local
communication/research skills. The 2026-06-19 marketing/social pass adds static
patterns from `blacktwist/social-media-skills`,
`BrianRWagner/ai-marketing-claude-code-skills`,
`wshuyi/x-article-publisher-skill`, Substack MCP repos, Reddit research MCP,
Firecrawl MCP, Google Search Console/SEO-performance MCP, BrandSystem MCP, and
marketing strategy skill packs. Runtime-heavy scraping, scheduling, auth, and
auto-posting stay behind explicit approval.

## Use This Skill When

- The user asks for a LinkedIn post, X thread, hooks, content calendar, content
  matrix, social proof campaign, newsletter voice, social profile rewrite,
  release announcement, or reel script.
- The user asks for platform strategy, content repurposing, carousel copy,
  caption variants, thread writing, audience growth tracking, content pattern
  analysis, performance interpretation, or optimization advice.
- The user asks for Substack/newsletter drafts, X Article preparation, or
  long-form social/article packaging.
- The user wants content based on notes, transcripts, a project, GitHub repo,
  public link, or launch.
- The user wants to score or lint social copy.
- A public artifact needs a launch/posting plan with evidence and safety notes.

Use `current-social-research` first when the content depends on what people are
currently saying. Use `marketing-strategy-operator` first when the user needs
campaign strategy, channel prioritization, SEO, paid-ad angles, launch planning,
or measurement before posts. Use `communication-story-crafter` when the primary
task is a message, story, pitch, or teaching explanation rather than a social
workflow.

## Operating Boundaries

- Drafts only by default. Do not auto-post, schedule, comment, DM, connect,
  email, upload, scrape behind login, or mutate a platform without explicit
  user approval for that specific action.
- Do not run paid scrapes or API calls unless the user approves the cost and
  the exact tool.
- Prefer supplied exports, public URLs, local cached data, and manually
  approved source lists.
- Do not invent metrics, engagement results, audience demographics, client
  names, testimonials, or public links.
- Keep private analytics, cookies, account IDs, emails, phone numbers, exports,
  and local paths out of public copy.

## Workflow Router

Choose the narrowest mode:

1. Voice foundation: create `about-me.md`, `voice.md`, or a compact voice guide.
2. Content matrix: combine 3-5 pillars with proven formats.
3. Hook generation: produce short, testable hook variants.
4. Post writing: draft one channel-ready post from source material.
5. Post scoring: compare against voice, source evidence, and available
   performance data.
6. Platform adaptation: turn one source into channel-fit variants without
   changing the claim.
7. Content calendar: plan cadence, themes, source basis, proof objects, and
   manual-review status.
8. Newsletter/Substack draft or issue plan.
9. Reel/video script: transform one approved idea into spoken script, caption,
   visual notes, and comment trigger.
10. Profile optimization: headline, about, experience, featured section, and
   visual prompts.
11. Release/launch announcement.
12. Public proof campaign: copy, asset order, alt text, reply bank, tracker.
13. Performance review: compare available metrics, source evidence, and
    content patterns without inventing missing data.
14. Outreach drafting: one personalized draft with human review, never sending.

## Voice Files

When voice matters, look for these local files in the project:

- `about-me.md`
- `voice.md`
- `voice-guide.md`
- `newsletter-voice.md`
- `outreach-profile.md`

If they are missing, either create a compact voice profile from supplied
samples or state that voice matching is limited.

## Content Matrix

Use this format for ideation:

Columns:

1. Actionable
2. Motivational
3. Analytical
4. Contrarian
5. Observation
6. X vs Y
7. Present vs Future
8. Listicle

Rows: 3-5 content pillars. Every cell must contain a specific post headline,
not a generic theme.

## Channel Adaptation Rules

- LinkedIn: prefer concrete proof, clear stakes, useful detail, and comments
  that invite real conversation. Avoid fake authority and engagement bait.
- X/Twitter: use tighter hooks, threadable claims, and source links where
  useful. X Article publishing is a preparation lane only unless a separate
  approved runtime handles the editor.
- Newsletter/Substack: preserve a clear editorial promise, issue structure,
  source basis, and draft/publish boundary. Do not assume Notes are draft-only.
- Reels/video: provide spoken script, visual beats, caption, and accessibility
  notes; route visual asset work to `visual-asset-integration`.
- Carousels: one idea per slide, strong first frame, proof or example near
  claims, and alt text for the final asset.
- Reddit/community: do not draft promotional posts unless the community norm,
  value exchange, and anti-spam boundary are explicit.

## Post Draft Gate

Before drafting, confirm:

- channel and audience
- source material or topic
- proof/evidence allowed
- voice source
- call to action
- off-limits claims

Draft rules:

- Lead with one concrete hook.
- Put proof near claims.
- Keep line breaks mobile-readable.
- Avoid generic AI tells, vague hype, and unsupported authority claims.
- Use no hashtags unless the voice profile or user requests them.
- End with the CTA style the user actually wants.

## Scoring And Linting

Score against available evidence:

- hook strength
- voice match
- value density
- structure and channel fit
- publish readiness
- proof-to-claim alignment
- platform norm fit
- human-review status

If performance data is available, use it. If it is stale, private, paid, or
missing, say so and score against voice plus public best-practice heuristics
instead of pretending.

Use a brand-voice lint pass for em dashes, buzzword clusters, hedge language,
vague superlatives, AI-tell phrases, unsupported claims, and CTA vagueness.
Report-only by default; edit only when asked.

## Public Proof Campaign

For shipped project work, produce:

```markdown
## Campaign
- Proof object:
- Primary link:
- Audience:
- Platform:

## Copy

## Asset Order And Alt Text

## Reply Bank
- Thank-you:
- Technical:
- Client-value:
- Quiet follow-up:

## Tracker
| Asset | Platform | Status | Link | Follow-up |
| --- | --- | --- | --- | --- |
```

## Runtime Gates

Credentialed or automated lanes require a separate review:

- Apify, Firecrawl, LangGraph, Arcade, LinkedIn/Twitter APIs, Slack, Supabase,
  Google/Vertex, Gemini video analysis, browser automation, or cron jobs.
- Substack MCPs, Reddit research MCP, X Article publisher automation,
  Google Search Console/SEO-performance MCPs, ad platforms, CRMs, schedulers,
  and BrandSystem/brand-account integrations.
- Any action that posts, schedules, comments, connects, sends, uploads, updates
  a CRM, or mutates an external system.
- Any workflow that reads account history, private exports, cookies, browser
  profiles, or direct messages.

## Output Contract

Return the usable content first. Then add:

```markdown
## Source And Safety Note
- Source basis:
- Voice basis:
- Claims to verify:
- Human action still required:
```
