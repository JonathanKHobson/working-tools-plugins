# Marketing Strategy Studio

Version **0.4.0** retains portable MCP discovery through root [`mcp.json`](mcp.json) for the existing optional launchers. Their server identities, runtime bindings and compatibility declarations are preserved; backend availability remains a separate check.

Discover what a personal or organizational brand should express, develop a recognizable identity system, and turn supported audience/offer decisions into marketing work that can be acted on and checked.

## Start with a real task

For “Who is a good fit for this offer, and how is that different from my audience?”, bring an offer hypothesis and any customer evidence. The [customer-fit method](references/strategy-methods/customer-fit.md) returns a concise ICP, role/audience distinctions, explicit unknowns and the next test. It also works before customer evidence exists, as a labeled hypothesis. A personal-brand profile remains a separate core record.

| Ask | Bring | You receive |
| --- | --- | --- |
| “Help me discover a brand that feels like me across different roles.” | A few real episodes, examples and boundaries | Provisional themes, contextual expression map and a scoped brand profile |
| “Develop a recognizable brand design from this direction.” | Direction/profile, references and actual applications | Creative territories or a selected identity-system brief with testable rules |
| “Turn this service offer and customer evidence into a campaign brief.” | Offer, audience evidence and constraints | Positioning, claims, channels, deliverables and measures |
| “Review this page for search intent and useful copy.” | Page URL or copy and target audience | Prioritized search/content changes with evidence gaps |
| “Diagnose this campaign from these dated results.” | Metrics, dates, spend and objective | Findings, limitations and next test |

If you already have a specific task, use the matching skill directly. A broad “what can this do?” request can use the [overview skill](skills/marketing-strategy-operator/SKILL.md); the work itself should start without a mandatory tour.

## Choose the task owner

Use the [full task-to-skill map](docs/use-case-map.md). A settled channel or deliverable goes to its specialist; the strategy operator handles unsettled audience, offer or cross-channel decisions.

| Task / skill | What it produces |
| --- | --- |
| [brand-discovery](skills/brand-discovery/SKILL.md) | Personal, organizational or offer discovery; evidence, creative exploration, audiences, contextual relationships and a reusable brand profile. |
| [brand-design](skills/brand-design/SKILL.md) | Creative territories, verbal/visual/sensory identity, recognition, system rules and evaluated production handoffs. |
| [campaign-and-launch](skills/campaign-and-launch/SKILL.md) | Campaign planning, launches, partnerships, community, public relations and coordinated channel delivery. |
| [conversion-and-offers](skills/conversion-and-offers/SKILL.md) | Landing-page conversion, funnel diagnosis, pricing, offers, objections, onboarding, signup and retention experiments. |
| [lifecycle-and-outreach](skills/lifecycle-and-outreach/SKILL.md) | Lifecycle messages, service-sales proposals, qualified follow-up and marketing-to-delivery handoffs using existing sales/RevOps methods; sending remains a separate authorized action. |
| [marketing-creative-production](skills/marketing-creative-production/SKILL.md) | Campaign visuals, product-image concepts, ad copy and creative production briefs with official provider workflows when installed and exposed, and complete local methods and design handoffs. |
| [product-photo-ad-hypotheses](skills/product-photo-ad-hypotheses/SKILL.md) | Inspect one or more product images, develop three scored visual hypotheses, and create 3:4 portrait concepts with built-in image generation; optional local SVG drafts and analysis-only mode. |
| [marketing-measurement](skills/marketing-measurement/SKILL.md) | Marketing analytics, attribution, experiment design, cohort analysis, ROI, performance diagnosis and evidence-backed reports. |
| [marketing-strategy-operator](skills/marketing-strategy-operator/SKILL.md) | Choose marketing positioning, audience, offer, goals and channel priorities, or coordinate a strategy spanning several marketing workflows. |
| [paid-campaigns](skills/paid-campaigns/SKILL.md) | Evaluate advertising readiness, ad credits and grants under cash-budget constraints; plan Google/YouTube, Meta Facebook/Instagram and Reddit campaigns, creative tests and measurement using actual available providers. |
| [search-and-discovery](skills/search-and-discovery/SKILL.md) | SEO, AEO, GEO, search architecture, keyword research, technical search audits and content refresh. |

## Availability and recovery

The optional `atlas-marketing` MCP declared in portable `mcp.json` and compatibility `.mcp.json` runs `scripts/atlas_library_mcp.py` against an external private method index. See [Atlas setup and limits](references/atlas-library.md). Check actual exposure and a scoped lookup before claiming access; supplied evidence and local methods remain usable if the service is unavailable. Publishing, spending and account actions need their own live provider and observed result.

Included methods and execution-tool boundaries are in [the workflow guide](docs/provider-handoffs.md). The ten first-party skills and complete licensed source procedures cover ordinary work without separate prose or UX method plugins. The complete current MIT YouTube Summarizer method is included, but its separate transcript server and messaging integration need recipient setup and live verification; a supplied-transcript fallback does not perform fetching. Codex and Claude manifests point to the same optional Atlas launcher, which needs the recipient’s own local binding; package files alone do not prove the server starts.

The [project map](docs/project-map.md) and [use-case map](docs/use-case-map.md) preserve method and provider boundaries. Current brand facts, analytics, accounts and publication receipts belong to the owning project. A proposed plan is not a scheduled campaign or measured result.

Brand discovery can remain noncommercial. A profile separates observations, aspirations, proposals and approved-for-scope choices; it does not prescribe a personality. [Research basis](references/brand-methods/sources.md) and [specialist responsibilities](references/brand-methods/agent-handoffs.md) explain the evidence and handoff limits. These methods add no autonomous agents, account access or publishing permission.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->
