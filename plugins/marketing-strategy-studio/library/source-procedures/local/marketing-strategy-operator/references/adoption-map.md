# Adoption Map

Reviewed during the 2026-06-19 marketing/social pass:

- `coreyhaines31/marketingskills` at commit `8bfcdffb655f16e713940cd04fb08891899c47db`
- `indranilbanerjee/digital-marketing-pro` at commit `17bab0b94603442ac7b653dfc37fef699978e956`
- `realkimbarrett/advertising-skills` at commit `45f4a4a1dabe24113193369b55b929b1de4ff04a`
- `BrianRWagner/ai-marketing-claude-code-skills` at commit `f36b34fc539a7a3b801839bfff2c26277fd7ec69`
- `open-strategy-partners/osp_marketing_tools` at commit `83f55198c4d4e7b315565f00792f63373ff9cc67`
- `AutomateLab-tech/seo-performance-mcp` at commit `ade605f78ffae67bb4f2960716c48d8570d80039`
- `acamolese/google-search-console-mcp` at commit `9f08e173c41c4b6327aa699a853e67954ccc55d3`
- `firecrawl/firecrawl-mcp-server` at commit `e30722e523f3187cd18ff1415326a464ffac8763`
- `Brandcode-Studio/brandsystem-mcp` at commit `62d33a65e4b3b765d07ee2b691c22cd2152bdb1c`
- `modelcontextprotocol/servers` at commit `7b1170d1da1e36bc9f553f51e76e64cbfd652b3e`
- `modelcontextprotocol/registry` at commit `fecef4f9ed5ad063b8c726dc7fca4eb69dba69a3`
- `agentskills/agentskills` at commit `5d4c1fda3f786fff826c7f56b6cb3341e7f3a911`

Adopted locally:

- A dedicated marketing operator trigger for campaign, GTM, SEO, ads,
  lifecycle, launch, offer, and analytics work.
- A single context spine: product, audience, buyer uncertainty, proof,
  constraints, channel, approval boundary, and measurement window.
- SEO refresh actions: refresh, expand, merge, kill, double-down, and manual
  review.
- Paid-ad angle matrix with offer, objection, proof, creative concept,
  landing-page path, and spend gate.
- Launch and campaign briefs with source basis, assets, approval gates, and
  post-campaign review.
- Runtime adoption gates for GSC, analytics, Reddit/Substack, Firecrawl,
  BrandSystem, OSP, browser automation, ad platforms, CRMs, and schedulers.
- A no-network scaffold script that produces a reviewable campaign or channel
  plan without credentials or account mutation.

Updated adjacent workflows:

- `social-content-studio`: channel-specific social/content atoms and runtime
  fences.
- `current-social-research`: public current-source lanes and runtime gates.
- `communication-story-crafter`: marketing strategy handoff boundary.
- `visual-asset-integration`: campaign/ad/social asset handoff boundary.
- Shareables MCP docs: marketing/social public artifact recipe.
- Job Application Compass docs: social proof and LinkedIn/job-search marketing
  boundaries.

Fenced:

- Any direct install of external marketing MCP servers.
- OAuth, account credentials, cookies, browser profiles, and private exports.
- Ad spend, campaign launch, posting, scheduling, sending, CRM mutation, and
  website/account changes.
- Firecrawl/browser scraping and platform-specific scrapers unless separately
  security-reviewed and explicitly approved.
- Blind copying large upstream skill packs into `.codex/skills`.

Security outcome:

- The P0/P1 repos were cloned read-only into quarantine and statically reviewed.
- No upstream code, setup script, package manager, MCP server, Docker image,
  browser automation, or test suite was executed.
- Static workflow knowledge was adapted; executable/runtime surfaces remain
  approval-gated.
