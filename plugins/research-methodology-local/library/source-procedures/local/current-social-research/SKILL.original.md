---
name: current-social-research
description: Research what people are currently saying about a person, company, product, tool, event, controversy, job market signal, or creative trend across public web and community sources. Use when Codex needs recent sentiment, community language, live objections, hiring/market signals, social proof, or a source-backed brief from the last 7-60 days. Do not use for timeless factual lookup, private account scraping, credentialed browser sessions, or automated platform scraping without an explicit security review.
---

# Current Social Research

Produce a recent, source-backed read on what people are actually saying, not a
generic web summary. This skill is local-first guidance inspired by public
current-web/social research tools, but it does not install or run external
scrapers, MCPs, browser sessions, or API-key workflows.

Local support files:

- `scripts/current_social_plan.py` builds a safe Last30Days-style source plan,
  query variants, risk gates, and coverage ledger template without network,
  account, cookie, API-key, or paid-provider access.
- `references/last30days-adoption.md` records the reviewed Last30Days adoption
  decision and the exact surfaces that stay behind explicit approval.

## Operating Rules

- Browse live sources for any current claim. Do not answer from model memory.
- Start with a time window: default to 30 days, but use 7 days for fast-moving
  news and 60 days for sparse topics.
- Separate community signal from editorial coverage, first-party posts,
  official docs, job postings, GitHub activity, and prediction/market data.
- Plan source lanes before searching. For named people, companies, products, or
  repos, include aliases/handles/repos when known instead of relying on a bare
  keyword query.
- Quote sparingly and attribute clearly. Prefer paraphrase plus source links
  unless the exact community wording carries the insight.
- Report source coverage and uncertainty. A thin-source result is still useful
  if the limits are visible.
- Weave community language into the synthesis when it materially improves the
  read. Do not bury every useful quote in a raw appendix, and do not overquote.
- Do not log into accounts, use private cookies, read browser profiles, bypass
  platform limits, or run scraping scripts unless the user explicitly approves a
  separate security-reviewed runtime lane.
- When the result should become a polished HTML brief, route the final artifact
  through Shareables after the research is gathered and source-reviewed.

## Coordination

- Use `$personal-security-check` before installing, running, wiring, or adapting
  external research tooling such as `last30days`, browser scrapers, API clients,
  or MCP servers.
- Use `$shareables` workflow guidance when the user asks for a public-safe or
  reusable brief, report, packet, or dashboard from the research.
- Use `$job_application_compass` only when the research is for a specific job
  application workflow; keep external market/current-role signals scaffold-only
  until they are connected to Kyle's actual evidence.
- Use `$social-content-studio` when the research should become a content
  matrix, hooks, LinkedIn/X/newsletter/reel drafts, profile copy, launch copy,
  or a public proof campaign.
- Use `$marketing-strategy-operator` when the research should become a
  campaign brief, SEO refresh plan, launch plan, channel strategy, ad-angle
  matrix, or measurement plan.
- Use `$writing-quality-studio:communication-crafter` when the research needs to become a pitch,
  outreach message, teaching explanation, launch note, or narrative.
- Use `$critical-compass` when the task needs claim skepticism, bias checks,
  controversy handling, or a decision recommendation from conflicting signals.

## Workflow

### 1. Frame the query

Write a compact query frame before searching:

- topic and aliases
- time window
- likely communities, sources, or platforms
- what decision the research should inform
- excluded sources, private surfaces, or risky methods

If the user gave a named person, company, product, or repo, resolve official
handles/pages first where possible. Do not confuse similarly named entities.

For non-trivial research, use the local planner before browsing:

```bash
python3 <plugin-root>/skills/current-social-research/scripts/current_social_plan.py \
  "$TOPIC" \
  --mode topic \
  --decision "$DECISION"
```

Use `--mode person`, `--mode company`, `--mode product`, or `--mode repo` when
that better matches the subject. Add `--aliases` for handles, founders, repo
names, product names, or common misspellings.

### 2. Gather across source lanes

Use the best available public sources for the task. Examples:

- community discussion: Reddit, Hacker News, forums, Discord exports supplied by
  the user, GitHub issues/discussions, product communities
- first-party signal: official blog, changelog, release notes, founder/company
  posts, GitHub commits/releases
- social/video signal: public posts, YouTube videos/transcripts, TikTok/shorts
  summaries when accessible without private session scraping
- niche and creator signal: recurring hooks, objections, proof formats,
  creator positioning, audience questions, and channel language that can safely
  inform human-reviewed drafts
- marketing/social intelligence: public Reddit discussions, Substack/newsletter
  pages, public founder or company posts, public content patterns, public
  competitor pages, public search-result observations, and public directory or
  community norms
- SEO and content-performance context: public pages, changelogs, search-result
  pages, open crawl notes, or user-supplied GSC/analytics exports; do not claim
  live GSC, GA4, Matomo, Clarity, or rank data unless the user supplied or
  approved that data source
- market/job signal: career pages, job postings, pricing changes, funding/news,
  procurement pages, public customer stories
- editorial coverage: news, blogs, reviews, analyst notes, newsletters

Keep a source ledger with URL, date, source type, observed signal, engagement or
authority clue when available, and confidence.

Prefer public, zero-credential lanes first. Treat paid APIs, browser-session
surfaces, watchlists, webhooks, and platform-specific scraping as optional
runtime lanes that require a separate explicit security approval.

For marketing/social runtime candidates such as Firecrawl MCP, Reddit research
MCP, Substack MCPs, Google Search Console MCP, SEO-performance MCP, Playwright
MCP, or BrandSystem MCP, keep the default pass static and source-led. Runtime
use requires `safe-install-review`, exact package/version/license, credential
and cost review, and explicit user approval before install, registration, or
execution.

### 3. Synthesize by signal, not by source list

Group findings into 3-7 signal clusters. Each cluster should include:

- claim or pattern
- strongest sources
- what people say in their own language, if useful
- confidence: strong, moderate, thin, conflicting, or stale
- why it matters to the user's decision

Do not end with a raw link dump. Include links inline where they support the
claim.

### 4. Output contract

Use this structure unless the user requested a different format:

```markdown
WINDOW: [date range]
QUESTION: [what this research answers]

WHAT PEOPLE ARE SAYING:
1. [pattern] - [plain synthesis with source links]
2. [pattern] - [plain synthesis with source links]
3. [pattern] - [plain synthesis with source links]

SOURCE COVERAGE:
- Strong: [source lanes]
- Thin or missing: [source lanes]
- Excluded: [private/risky/unavailable sources]

DECISION TAKEAWAY:
[what this means for the user's next action]

OPEN QUESTIONS:
[only the missing research that would materially change the answer]
```

For comparison topics, use a short side-by-side table plus the same source
coverage and decision takeaway.

## Shareable Brief Handoff

When converting the research into a Shareables artifact:

- preserve the date window and source coverage
- keep inline citations or source chips close to the claims they support
- include uncertainty and excluded-source notes
- avoid embedding raw private data, cookie-backed content, or copied long
  comments
- validate the artifact and run visual QA before publish or handoff

## Social Content Handoff

When research becomes social content:

- preserve the date window, source coverage, and excluded-source notes
- pass only source-backed claims to `social-content-studio`
- separate "people are saying" language from publishable claims
- mark stale, private, paid, or thin signals before they become hooks
- do not auto-post, schedule, comment, connect, DM, or scrape behind login
  without a separate explicit approval and security review

## Runtime Adoption Gate

Do not install or run external current-web research tools by default. A future
runtime adoption pass must prove:

- the exact package/repo/version and license are acceptable
- scripts, install commands, browser/session behavior, API keys, and storage
  paths pass `personal-security-check`
- output quality beats this manual/source-backed workflow for a real task
- credential use is optional, scoped, and never reads private browser profiles
  without explicit approval
- generated artifacts follow local Shareables and citation/privacy gates

The reviewed `mvanhorn/last30days-skill` repo is useful as a source-planning
and synthesis pattern, but its full install remains gated because it can read
browser cookies/profiles, consume sensitive API keys, run an MCP wrapper, and
send webhook/watchlist notifications. Use `references/last30days-adoption.md`
for the detailed adoption decision.
