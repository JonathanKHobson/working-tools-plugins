---
name: current-social-research
description: Research recent public community, social, creator, company, and market signals with dated sources and explicit coverage limits. Use for current sentiment, language, objections, platform norms, competitor movement, or a source-backed social/marketing handoff. Do not use for timeless lookup or private account scraping.
---

# Current Social Research

Answer a current question with public, dated evidence. This is a focused research lane within Research Methodology Local; a quick platform read does not require the full research-methodology workflow. The local `scripts/current_social_plan.py` creates query variants and a coverage ledger without network or credentials. `references/last30days-adoption.md` records the source-planning pattern and runtime boundary.

## Route and scope

- Use this skill when the user asks what people are saying now, recent objections, creator or community language, current platform norms, a recent market/job signal, or competitor movement. Use ordinary research for stable factual questions.
- Hand source-backed findings to `social-content-studio:social-content` for posts or previews, `marketing-strategy-studio:marketing-strategy-operator` for positioning, campaigns, search strategy, and SEO, or the career owner for a specific application. A research finding is an input, not a publishable claim by itself.
- Use the already available public web or provider sources for live claims. The planner does not gather evidence. Distinguish a source observation from an action in a social or analytics app. Never imply that a preview, draft, or observed post was published by this workflow.

## Workflow

1. Frame the named subject, aliases or official handles, decision, time window, and likely source lanes. Default to 30 days; use 7 for fast-moving topics or 60 for sparse ones. Verify entity identity where names collide.
2. For non-trivial work, run `scripts/current_social_plan.py` from this skill folder with the topic, `--mode`, `--aliases` if useful, and `--decision`. It emits a no-network plan and ledger template.
3. Gather public sources across lanes that matter: community posts, first-party updates, creator/social posts, editorial coverage, job or market signals, public product/repo records, and public search observations. Include source URL, publication or observation date, source type, observed signal, and confidence. An engagement count is a clue, not a representative sample.
4. Group findings by signal rather than platform. For each pattern, show the strongest sources, any meaningful disagreement, source coverage, and why it affects the user's decision. Paraphrase and cite; quote briefly only when wording matters.
5. Mark thin, missing, stale, and excluded lanes. Separate community language (“people said”) from a claim the user can safely publish. A small or selected sample cannot establish broad sentiment.

## Output

Give the date window, question, 2–5 source-linked findings, coverage limits, and decision takeaway. Use a comparison table when comparing subjects. Preserve dates, citations, and exclusions in any social-content or public-report handoff.

## Access boundary

Public browsing and supplied exports are within this research lane. Do not log into accounts, read cookies or profiles, bypass platform limits, use paid APIs, install scrapers/MCPs, or start watchlists/webhooks merely to complete the research. Such runtimes require their own exact-source, credential, cost, and security review. Follow the user's existing authorization for any separately requested app action; the research skill itself does not post or schedule.

For this domain, read the [complete pre-migration current-social-research procedure](../../library/source-procedures/local/current-social-research/SKILL.original.md) and its relevant support before applying the brief routing summary above. Preserve the full mode-specific methods and examples. Current user and tool instructions govern any external action.

For substantial topic research, comparisons, discovery, recommendations, hiring signals, follow-up or an authorized research library, read [complete recent research](references/complete-recent-research.md). It routes the full bundled source methods through this owner and preserves the separate runtime authorization boundary.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Researcher. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
