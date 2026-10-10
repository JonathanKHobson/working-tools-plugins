# Adoption Map

Reviewed sources:

- `charlie947/social-media-skills`
- `langchain-ai/social-media-agent`
- `jqaisystems/jqai-ai-skills`
- `Dirtytrii/codex-skills` social/content skills
- `aliciajia399-ops/skillbook`
- `blacktwist/social-media-skills`
- `BrianRWagner/ai-marketing-claude-code-skills`
- `wshuyi/x-article-publisher-skill`
- `06ketan/substack-ops`
- `conorbronsdon/substack-mcp`
- `king-of-the-grackles/reddit-research-mcp`
- `firecrawl/firecrawl-mcp-server`
- `acamolese/google-search-console-mcp`
- `AutomateLab-tech/seo-performance-mcp`
- `Brandcode-Studio/brandsystem-mcp`

Adopted locally:

- Voice foundation files: `about-me.md`, `voice.md`, and format-specific voice
  profiles.
- Content matrix by pillars and formats.
- Hook generation, post drafting, scoring, and brand voice linting.
- Public proof campaign tracker with alt text, copy, reply bank, and follow-up.
- Release announcement copy that separates source facts from interpretation.
- Human-in-the-loop social agent pattern from LangChain without runtime install.
- Platform strategy, content calendar, repurposing, thread, carousel, caption,
  hook, audience growth, and performance-review modes.
- Substack/newsletter and X Article preparation patterns without editor
  automation.
- Reddit/community research as a public-source input lane, routed through
  `research-methodology-local:current-social-research`.
- SEO and campaign measurement handoff to `marketing-strategy-operator`.
- Native Social Post Previewer is used only as an available provider app for generation and mock previews; this plugin does not vendor its engine or treat preview as publication.

Fenced:

- Authenticated posting, scheduling, OAuth, cron jobs, Slack posting, CRM
  updates, and social APIs unless the exact action is authorized and a suitable
  current provider is available. `social-publishing` owns action and readback;
  this content skill does not imply authorization.
- Paid scraping or browser-session scraping.
- Instagram/Reels video scraping and Gemini video analysis.
- Chinese social platform publishing/scraping helpers.
- SkillBook app install. It is a discovery surface, not a local runtime need.
- Substack Notes publish automation, X Article editor automation, Reddit API or
  scraping runtimes, Firecrawl, Google Search Console, SEO-performance MCP,
  BrandSystem MCP, and any credentialed account/history access until separate
  security review and explicit approval.
