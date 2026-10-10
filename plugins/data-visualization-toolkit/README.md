# Data Visualization Toolkit

Make data understandable and truthful for a specific reader and decision. Start with the question, source data or known values, intended audience, and where the result will appear. The toolkit chooses a fitting visual method, routes to the complete relevant procedure, and checks the rendered result when one is produced.

Try a first request:

- “Here is a CSV and the question our team needs to answer. Choose and build the clearest chart for a one-page report.” Result: a chart with readable labels, source-aware caveats, and checked export.
- “Review this dashboard screenshot and its source data for misleading scales and missed uncertainty.” Result: prioritized findings and concrete repairs.
- “Explain these project dependencies as a diagram that a new teammate can navigate.” Result: a structurally faithful diagram and an appropriate source/export format.

Use [data-visualization](skills/data-visualization/SKILL.md) for a broad request or to choose the right method. For a known job, pick a specialist from the [task-to-skill map](docs/use-case-map.md), such as `statistical-evidence`, `maps-and-cartography`, `web-chart-engineering`, or `visualization-verification`. If the user asks what this plugin can do, orient to the relevant outcome, input, and result, then proceed with the task. This README is a human entry point and is not automatically loaded by the assistant.

This package includes a local saved-table Data Explorer MCP App and full method library. See [installation](docs/installation.md). External chart engines and native conversation rendering are separate dependencies. Its preserved methods guide work in the host's actual document, slide, web, analysis, or conversational visual runtime; availability and current provider contracts must be checked there. The [project map](docs/project-map.md) explains the complete source library and verification boundary.

## Source and maintenance

Maintain the active discovery heads in `skills/` and keep the full Build Web Data Visualization source library intact under `libraries/`. Validate changed heads, relative links, the manifest, and the source hashes before reinstalling through the supported plugin path. A successful build or export is a different state from rendered QA or publication.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->

Public version 0.2.0 has13 discovery skills. [Distribution scope](PUBLIC_DISTRIBUTION.md) identifies excluded proprietary/unlicensed libraries and [third-party notices](THIRD_PARTY_NOTICES.md) retain eligible source terms. Scientific work uses full MIT statistical, export and testing methods. Interactive work uses original procedures, complete web methods and the bundled MCP App.

Check the complete library and package with `python3 scripts/verify_public.py`. Run a real fictional stdio task with `.runtime/venv/bin/python examples/sample_stdio.py`; it uses a temporary dataset directory and closes its own subprocess. Rendering/native-host delivery remain separate acceptance checks.

The package also includes portable `mcp.json`; run the same sample with `--portable` to check that route.
