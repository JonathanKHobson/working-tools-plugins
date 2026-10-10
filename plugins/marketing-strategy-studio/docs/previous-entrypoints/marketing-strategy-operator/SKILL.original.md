---
name: marketing-strategy-operator
description: Plan, audit, and package marketing strategy and campaign visuals across positioning, offers, marketing language, SEO, campaigns, paid ads, lifecycle email, launches, analytics, experiments, and channel handoffs. Use for a marketing plan, GTM plan, campaign brief, marketing visual concept or asset, SEO refresh, landing-page promise, paid-ad angle, launch plan, offer audit, conversion path, funnel diagnosis, or performance review. Preserve action and account boundaries.
---

# Marketing Strategy Operator

Marketing Strategy Operator turns supplied business facts, audience evidence,
current research, and local project material into usable marketing decisions.
It is a planning and drafting skill, not an autonomous growth stack.

This skill adopts static workflow patterns from the P0/P1 marketing-social
harvest: `coreyhaines31/marketingskills`,
`indranilbanerjee/digital-marketing-pro`, `realkimbarrett/advertising-skills`,
`BrianRWagner/ai-marketing-claude-code-skills`,
`open-strategy-partners/osp_marketing_tools`,
`AutomateLab-tech/seo-performance-mcp`, Google Search Console MCP patterns,
Firecrawl MCP patterns, Reddit/Substack MCP patterns, BrandSystem MCP patterns,
and the Agent Skills/OpenAI Codex/MCP standards. See
`references/adoption-map.md`.

## Use This Skill When

- The user asks for marketing strategy, GTM, launch planning, campaign briefs,
  funnel diagnosis, offer design, positioning, customer research, competitor
  profiling, or channel prioritization.
- The user asks for SEO, programmatic SEO, site architecture, content refresh,
  answer-engine visibility, SERP quick wins, or Google Search Console-style
  performance interpretation.
- The user asks for paid-ad angles, headline matrices, scroll-stopping creative,
  retargeting strategy, landing-page conversion, objection handling, or offer
  framing.
- The user asks to explore, produce, adapt, or review marketing visuals for a
  campaign, ad, offer, product scene, launch, or related channel asset.
- The user asks for lifecycle email, newsletter, cold outreach, referral,
  community, PR, testimonial, or launch communication strategy.
- The user asks what to measure, how to evaluate a campaign, or how to design
  an experiment without making fake performance claims.
- A Shareables artifact needs a public-safe marketing brief, campaign board,
  launch packet, channel plan, SEO refresh report, or performance-readiness
  explainer.

## Coordination

- Use `research-methodology-local:current-social-research` before strategy when the plan depends on fresh
  community language, live objections, competitor movement, Reddit/Substack
  signals, or current search/social context.
- Use `social-content-studio:social-content` when the output becomes channel-specific posts,
  content calendars, hooks, profile copy, threads, newsletters, reels, or proof
  campaign drafts.
- Use `writing-quality-studio:communication-crafter` when the primary output is a pitch, landing
  page story, founder narrative, sales email, teaching explanation, or reader
  journey.
- Use `ux-design-toolkit:design-studio` for ad creative, social preview assets,
  landing-page proof images, brand visuals, and campaign asset QA.
- Load `references/visual-creative-production.md` for visual concept and asset
  work. It defines the campaign-to-creative brief and a conditional handoff to
  Creative Production's board provider when that tool is available. Keep
  Creative Writing Studio separate.
- Use `data-analytics:*` skills when the user supplies data requiring durable
  analysis, charts, dashboards, or KPI diagnostics.
- Use `safe-install-review` before installing, running, registering, or
  adapting MCP servers, CLIs, scrapers, browser automation, paid APIs, or
  account integrations.
- Use Shareables when the result should become a public-safe HTML artifact with
  sources, progressive disclosure, and visual QA.

## Operating Boundaries

- Strategy and copy work is read-only by default. If the user has already
  authorized an exact external action in the current conversation, carry it
  through its owning workflow without asking again. Do not infer permission to
  spend money, launch ads, post, schedule, send, comment, DM, upload, submit,
  mutate a CRM, or change a website/account from a request for a plan or draft.
- Do not use private cookies, browser profiles, password stores, account
  exports, or paid APIs without a separate security-reviewed runtime lane.
- Do not invent performance data, market size, audience demographics, customer
  quotes, testimonials, case results, conversion rates, search volume, ad spend,
  or revenue impact.
- Label hunches, guesses, stale evidence, and missing data. Do not polish them
  into claims.
- Treat platform policy, sender reputation, privacy, consent, and ad-platform
  review risk as marketing constraints, not implementation details.

## First Move

Classify the work before drafting:

1. Positioning, offer, or avatar/audience work
2. Marketing plan or GTM plan
3. Launch or release plan
4. SEO, AEO/GEO, content refresh, or site architecture
5. Paid ads, ad creative, angles, landing page, or conversion path
6. Lifecycle email, newsletter, cold outreach, SMS, or referral
7. Community, PR, partnership, testimonial, or directory/submission strategy
8. Analytics, attribution, experiment design, or performance diagnosis
9. Shareable/report handoff
10. Runtime integration review
11. Marketing visual concept, production, or review

Then define:

- Product or offer:
- Audience and buyer uncertainty:
- Goal:
- Allowed channels:
- Source evidence:
- Constraints:
- Approval boundary:
- Measurement window:

If a missing fact changes the plan, ask for it or mark it as
`[MISSING INFO: ...]`.

## Planning Workflow

1. Build the context spine: product, buyer, problem, proof, constraints,
   channel history, and the user's tolerance for publicness, cost, and manual
   work.
2. Choose the smallest viable lane. Do not open SEO, paid ads, content,
   outreach, and community all at once unless the user explicitly needs a
   portfolio of options.
3. Convert the lane into an artifact:
   - campaign brief
   - launch packet
   - SEO refresh list
   - ad-angle matrix
   - lifecycle sequence outline
   - performance diagnosis
   - Shareables report
4. Put proof near claims. If proof is missing, turn it into a research task or
   a clearly labeled assumption.
5. Record the existing authorization or the remaining decision needed before
   an external action. Make the final payload reviewable where a hold applies.
6. Define measurement honestly: input, leading indicator, lagging indicator,
   source, denominator, and review date.

For a quick local scaffold, use the bundled no-network helper:

```bash
python3 "${MARKETING_PLUGIN_ROOT:-.}/skills/marketing-strategy-operator/scripts/marketing_strategy_scaffold.py" \
  "Product or campaign name" \
  --mode campaign \
  --audience "target reader" \
  --goal "specific outcome" \
  --channels "LinkedIn, newsletter, SEO"
```

## Channel Rules

Load `references/channel-playbooks.md` when a task needs a channel-specific
checklist for SEO, paid ads, email/newsletter, launch, community/PR, or
analytics.

Load `references/search-language-and-seo.md` when wording a search-facing page,
refreshing an SEO page, writing metadata, or converting an offer into grounded
benefits. This skill owns marketing language and SEO; the research owner
supplies current sources and the social owner adapts approved claims into posts.

Core channel rules:

- SEO: separate technical issues, content quality, search intent, internal
  linking, refresh/merge/kill decisions, and GSC-like evidence.
- Paid ads: start with offer, audience, promise, proof, objection, creative
  concept, landing-page path, and spend gate.
- Email/newsletter: separate draft quality from deliverability, consent,
  segmentation, and manual-send boundaries.
- Launch: choose audience, announcement sequence, proof asset, reply handling,
  and after-action review.
- Community/PR: identify real communities, norms, value exchange, proof, and
  anti-spam constraints.
- Analytics: define denominator and decision before choosing a metric.

## Runtime Adoption Gates

Credentialed tools can be useful, but they are not silently adopted. Treat
these as separate lanes:

- Google Search Console, GA4, Matomo, Clarity, or analytics MCPs
- Reddit/Substack research MCPs
- Firecrawl/browser scraping
- BrandSystem or OSP content MCPs
- Playwright MCP or browser automation
- Ad platform APIs, CRMs, schedulers, email senders, social APIs

Before runtime use:

1. Identify exact repo/package/version and license.
2. Review scripts, package manifests, Dockerfiles, server cards, env vars,
   OAuth scopes, browser/session behavior, network writes, storage, and logs.
3. Confirm cost and credentials.
4. Run only a bounded, reversible, read-only first test when possible.
5. Keep public output behind Shareables/public-safety review.

## Output Contracts

For a marketing plan:

```markdown
## Marketing Strategy
- Objective:
- Audience:
- Offer or promise:
- Current evidence:
- Primary lane:
- Secondary lanes:
- Human approval gates:

## Plan
1. [Action]
2. [Action]
3. [Action]

## Measurement
| Metric | Source | Denominator | Review date | Decision it informs |
| --- | --- | --- | --- | --- |

## Risks And Missing Proof

## Next Concrete Action
```

For a campaign brief:

```markdown
## Campaign Brief
- Campaign:
- Audience:
- Buyer uncertainty:
- Promise:
- Proof:
- Channels:
- Assets needed:
- Approval boundary:

## Message Matrix
| Channel | Hook | Proof | CTA | Asset | Status |
| --- | --- | --- | --- | --- | --- |

## Launch Checklist
## Measurement Plan
## Post-Campaign Review Prompt
```

For an SEO/performance refresh:

```markdown
## SEO Refresh Review
- Site/page set:
- Evidence basis:
- Excluded sources:

| URL or page | Signal | Diagnosis | Action | Confidence | Review date |
| --- | --- | --- | --- | --- | --- |

## Risks
## Next Manual Check
```

## Verification

- Referenced files exist.
- Any helper script runs with `--help` and a no-network sample.
- No external runtime, MCP server, package install, ad spend, account mutation,
  posting, sending, or scraping was enabled by the skill itself.
- External sources and fenced runtime decisions are recorded in
  `references/adoption-map.md`.

## Full source procedures

For a request matching a named procedure, consult the [full source procedure map](../../../library/source-procedures/INDEX.md), then read the linked complete body for this skill before drafting or reviewing. Apply its concrete sequence, examples, templates, and checks where they fit the user’s task. For an ordinary small request, load only the matching body. Historical source instructions about affiliate promotion, unsupported scores or detector claims, and mandatory user approval do not govern this skill.

Before performing this work, read [the source/host adapter](../../source-host-adapter.md), select the matching route from [the complete procedure map](../../procedures/marketing-strategy-operator.md), then **read and apply that full original procedure and its required support files**. Every template, example, rule and exception remains available in the preserved source tree. Do not use this entrypoint as a method summary.

Positioning, audience evidence, offers, GTM choices and cross-channel strategy. Start from supplied facts and evidence; the current user request controls scope, tone, external actions and acceptance criteria. Distinguish proposed, prepared, sent, scheduled, published and measured. The source's named agents, MCPs, CLI commands and account stores are not automatically installed or authorized. Use the actual host provider and disclose missing execution capability. Strategy methods remain usable with supplied data even when an optional provider is absent.

For other recurring jobs, route within Marketing to `search-and-discovery`, `campaign-and-launch`, `paid-campaigns`, `conversion-and-offers`, `lifecycle-and-outreach`, `marketing-measurement`, `marketing-creative-production`. Live source research belongs to Research Studio; channel content and previews to Social Content Studio; image-led craft to Graphic Design; general editorial work to Writing Quality; connector/security work to Master Security and Work Management.
