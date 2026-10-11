# Research Toolkit

Investigate a bounded question using traceable sources, review claims against evidence, or turn findings into a decision or implementation handoff. Specialist routes cover supplied qualitative data, academic writing and current public social signals.

## Start with a real task

| Ask | Bring | You receive |
| --- | --- | --- |
| “Compare these two approaches against my requirements and show the evidence.” | Requirements and candidate sources | Source-linked comparison and open questions |
| “Analyze these interview notes for warranted findings.” | Authorized notes and study context | Findings tied to excerpts, with method and coverage limits |
| “Audit this research brief for unsupported claims.” | Draft and source set | Claim-by-claim issues and corrections |

If you already have a specific task, use the matching skill directly. A broad “what can this do?” request can use the [overview skill](skills/research-methodology/SKILL.md); the work itself should start without a mandatory tour.

## Choose the task owner

Use the [full task-to-skill map](docs/use-case-map.md). Narrow source discovery, evidence review, academic writing and handoff requests use their own skill directly.

| Task / skill | What it produces |
| --- | --- |
| [academic-writing](skills/academic-writing/SKILL.md) | Draft, revise or audit papers, theses, abstracts, literature syntheses, technical manuscripts, academic essays and reviewer responses from supplied evidence. |
| [critical-reasoning](skills/critical-reasoning/SKILL.md) | Compatibility route for the former Research Toolkit critical-reasoning skill; use reasoning-studio:critical-reasoning for new argument or content audits. |
| [current-social-research](skills/current-social-research/SKILL.md) | Research recent public community, social, creator, company, and market signals with dated sources and explicit coverage limits. |
| [evidence-review](skills/evidence-review/SKILL.md) | Audit a research report for unsupported claims, citation mismatches, outdated evidence, contradictions, and overstated causality. |
| [karpathy-guidelines](skills/karpathy-guidelines/SKILL.md) | Apply Karpathy-inspired principles when research leads to code, documents, protocols, purchases, repairs, or decisions that require clear assumptions, minimal scope, and verifiable outcomes. |
| [research-handoff](skills/research-handoff/SKILL.md) | Turn existing research into a bounded implementation specification, action plan, protocol, decision record, or continuation brief without silently implementing it. |
| [research-methodology](skills/research-methodology/SKILL.md) | Plan decision-linked interviews and usability studies; analyze supplied qualitative data; investigate products, literature, devices, markets or technology with traceable evidence. |
| [source-discovery](skills/source-discovery/SKILL.md) | Find and assess sources for a bounded research question with explicit date, provenance and coverage limits. |

## Availability and recovery

Research from supplied files can work without an MCP. `.mcp.json` declares an optional `research-compass` bridge using a recipient-owned binding; see [Research Compass integration](docs/research-compass-integration.md). [Atlas setup](references/atlas-library.md) describes a separate optional local source library. Their source configuration does not establish installed, reachable or authorized runtime access. Verify a relevant exposed route and scoped result before using it; otherwise use supported host retrieval and state the gap. Current external research needs working retrieval/network access.

Read [installation](docs/INSTALLATION.md), [integrations](docs/INTEGRATIONS.md), [provenance](docs/PROVENANCE.md), [project map](docs/project-map.md), and [validation](docs/VALIDATION.md) for distribution and maintenance. This is a customized local source; upstream and installed copies do not update automatically. A research plan or source list is not an executed study.

## Files and distribution

The maintained source is this directory. `.codex-plugin/plugin.json` declares identity and `skills/` contains the active methods. `integrations/remote-mcp.json` records optional public source endpoints. The main bundle uses the portable recipient-owned Research Compass binding example; no private backend is packaged. Building an archive or editing source does not install it in a host. Verify the selected package, installed copy and current tool exposure independently.

The five supplied research and Karpathy method files are author-licensed under CC BY-SA 4.0; see [source rights](SOURCE-RIGHTS.md). Published versions and installation instructions are listed in the [Working Tools catalog](https://github.com/JonathanKHobson/working-tools-plugins/blob/main/catalog/packages.json) and [installation guide](https://github.com/JonathanKHobson/working-tools-plugins/blob/main/docs/install.md). The [native method map](library/source-procedures/INDEX.md) selects complete academic, argument, study and artifact handoff methods. This customized Research Toolkit is distinct from the upstream curated plugin; [provenance](docs/PROVENANCE.md) records adaptations and exclusions. No publication, account configuration or executed study follows from these files alone.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->
