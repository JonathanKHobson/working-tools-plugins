# Oppia Research Corpus

Current edition **0.4.2** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

Find what Oppia’s historical UX research supports, then address a specific remaining question with an appropriate study method. This private package is for authorized Oppia research team members.

## Start here

- “What did prior research find about learners discovering lessons?” Bring a focused Oppia question. Expect evidence IDs, source context, conflicting findings and freshness limits.
- “Help me frame this proposed feature as a neutral research question.” Bring the decision and reported problem. Expect a bounded question and evidence gap, not an automatically launched study.
- “What can Oppia Research Corpus do?” Get a short explanation of retrieval, evidence review and the method choices below.

The bundled MCP searches a historical corpus; it does not read live Drive files or silently search the web. Start broad evidence questions with `oppia_research`, narrow queries with `search_oppia_research`, and retrieve selected evidence before quoting it. The recorded corpus build date limits freshness. Installation, a working tool connection and permission to reuse a record are separate.

## Choose a workflow

| Skill | When to use it / result |
| --- | --- |
| [oppia-competitive-analysis](skills/oppia-competitive-analysis/SKILL.md) | Conduct decision-focused competitive or analogous-product analysis for Oppia. Use when the team needs to compare features, interaction patterns, messaging, audience fit, or market alternatives across learning products and adjacent services. Do not treat competitor behavior as proof of Oppia user needs. |
| [oppia-cuj-research](skills/oppia-cuj-research/SKILL.md) | Define, audit, and revise evidence-backed Oppia critical user journeys (CUJs). Use when the team needs to map an end-to-end user goal, assess journey coverage or health, align research with acceptance tests and metrics, or propose a bounded CUJ change. Do not rewrite the full CUJ system for a single research question. |
| [oppia-heuristic-evaluation](skills/oppia-heuristic-evaluation/SKILL.md) | Plan, conduct, and synthesize Oppia heuristic evaluations for a defined persona, critical user journey, device, and release slice. Use for expert or trained-volunteer inspection of interface risks and severity. Do not present heuristic findings as observed participant behavior. |
| [oppia-interview-study-design](skills/oppia-interview-study-design/SKILL.md) | Design Oppia discovery interviews, semi-structured interviews, and post-test interview guides. Use when the research question concerns motivations, mental models, context, trust, discovery pathways, or meaning that participants can describe. Do not use interviews as proof of task performance when direct observation is required. |
| [oppia-netnography](skills/oppia-netnography/SKILL.md) | Provisional workflow for ethical, traceable netnography of public online communities relevant to Oppia. Use for questions about community discourse, language, peer recommendations, workarounds, or norms that cannot be answered by the Oppia corpus alone. Do not use public posts as representative proof of Oppia learner behavior. |
| [oppia-persona-research](skills/oppia-persona-research/SKILL.md) | Identify, validate, revise, and confidence-rate Oppia personas from research evidence. Use when the team needs to define meaningful user groups, assess whether an existing persona is supported, or turn cross-study behavioral patterns into a working persona. Do not invent demographic detail or treat a persona as a fictional profile. |
| [oppia-research-compass](skills/oppia-research-compass/SKILL.md) | Search and reuse Oppia historical UX research through the bundled Oppia Research Compass MCP. Use when an authorized Oppia team member asks what prior Oppia research found, wants evidence from studies or interviews, needs to compare Oppia findings, or needs to identify a specific research gap. Do not use for generic research that has no Oppia decision context. |
| [oppia-research-orchestrator](skills/oppia-research-orchestrator/SKILL.md) | Route Oppia UX research work between the historical-research MCP and focused research-method skills. Use for any Oppia research request that may involve prior evidence, study design, interviews, usability testing, competitive analysis, netnography, personas, heuristic evaluation, or critical user journeys. Oppia corpus retrieval always comes before new-research design. |
| [oppia-research-question-design](skills/oppia-research-question-design/SKILL.md) | Use when an Oppia team member needs to turn a vague request, reported problem, assumption, metric change, proposed solution, or question backlog into focused, neutral, decision-linked UX research questions. Do not use when the historical corpus already resolves the decision or when approved questions only need a study instrument. |
| [oppia-usability-testing](skills/oppia-usability-testing/SKILL.md) | Design moderated or unmoderated Oppia usability tests for real tasks, flows, prototypes, and critical user journeys. Use when the team needs to observe whether a target user can understand or complete an Oppia goal. Do not use for expert-only interface inspection; route that to Oppia heuristic evaluation. |

## Setup and recovery

Use the host-specific installation or source-run instructions below. Verify tool discovery and a harmless focused retrieval; do not assume the source database or runtime exists on another machine. If the server fails, check the declared Python environment and bundled/specified database path. An empty result is not a failed connection: narrow the query, inspect coverage and report a specific evidence gap. Never bypass the sanitized release process or expose the corpus to fix setup.

For a concrete task, load its selected full skill and applicable references. For help, explain a few relevant options, inputs and expected result; help alone does not query participant material or start research. Skip repeated tours when the user’s task is clear.

## Public source installation and updates

Install the prepared public package through the Working Tools marketplace (`oppia-research-compass@working-tools`) once its release is available, then start a fresh task. Select the full method matching the research decision. This installs ten methods and full optional read-only runtime source; provider startup remains explicit. The starter database contains zero rows in every research table.

For source runtime use, set up the declared reviewed Python/MCP dependencies, then run `python mcp/oppia-research-compass/server.py --help` to inspect current arguments. Select your own authorized compatible corpus using `OPPIA_RESEARCH_DB_PATH`; without an override the default is the empty packaged starter. The preserved MCPB manifest/launcher offers an alternative receiving-host integration. Neither route needs a live Drive connection or automatic web research. Report source availability, configured provider, tool discovery, authorized data and actual results separately.

For updates, preserve your recipient corpus outside the installed package, review schema/runtime compatibility and notices, validate the complete method/runtime source and test retrieval with synthetic evidence before reinstalling. Never publish real research evidence merely to distribute a code update. Original project edition history remains in its owning Compass repository; this portable source package replaces personal installation directions.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->

## Public source edition and first task

All ten complete methods, quality/routing contracts and all ten read-only MCP tools remain. The original code is AGPL-3.0-only; original documentation/methods retain CC BY-SA4.0 and notices. Private Oppia team evidence DB, corpus excerpts, respondent/study record handles and private Drive links/titles are excluded. The bundled SQLite file is newly generated from the original structural schema with zero records, not a sanitized copy of the team corpus. No historical research findings are supplied. Original private dataset hash is retained in PROVENANCE.json for exclusion evidence only; that hash grants no data rights.

Use Python>=3.10 and the declared `mcp>=1.12,<2` in a reviewed receiving environment for actual MCP use. SQLiteFTS5 is required for evidence search. Optional startup uses the preserved MCPB launcher or server CLI with an explicit OPPIA_RESEARCH_DB_PATH for an independently authorized schema-compatible corpus. Installation registers methods only; no MCP is started automatically. The empty starter preserves genuine zero-evidence behavior. A missing selected DB fails as missing, not as zero research evidence. The server remains read-only and does not import/reindex a corpus, open source files or perform external lookup. Source schema and synthetic fixtures document structure, not permission to copy any research data.

For “what have we learned about learner onboarding?” using the supplied starter, return the actual zero-result evidence gap and propose a bounded research plan. Do not invent an historical finding or treat empty setup as proof that research never occurred. An external-paper request remains an explicit supporting research handoff; the runtime performs no web lookup. Receiving teams retain consent, access and distribution restrictions for their supplied evidence.
