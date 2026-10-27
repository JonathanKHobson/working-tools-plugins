# Data Visualization Toolkit

Current edition **0.2.5** uses the [Working Tools licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

Make data understandable and truthful for a specific reader and decision. Start with the question, source data or known values, intended audience, and where the result will appear. The toolkit chooses a fitting visual method, routes to the complete relevant procedure, and checks the rendered result when one is produced.

Try a first request:

- “Use these local background and foreground images to build an interactive depth card.” Result: a self-contained HTML file with independent art-plane parallax, reactive foil, three finishes, optional flip and exploded views, keyboard controls and reduced-motion/static fallback. [Interactive Depth Cards](skills/interactive-depth-cards/SKILL.md) also has a project-local React route. The standalone builder uses Python and Pillow without a connected app or network service.

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

Version 0.2.5 has 14 discovery skills. [Distribution scope](PUBLIC_DISTRIBUTION.md) identifies excluded proprietary/unlicensed libraries and [third-party notices](THIRD_PARTY_NOTICES.md) retain eligible source terms. Scientific and interactive work can load complete, separately held provider procedures through [private source bindings](references/provider-methods.md). The public package includes the same entrypoints, complete MIT web/statistical/export methods, original procedures and the bundled MCP App. It does not include the optional providers' source bodies or rendering capabilities.

## Run the first sample

From the extracted or installed package root, create the dedicated environment described in [installation](docs/installation.md):

```sh
python3 -m venv .runtime/venv
.runtime/venv/bin/python -m pip install -r runtime/data-explorer/requirements.txt
.runtime/venv/bin/python examples/sample_stdio.py
```

The sample starts the actual local MCP server, creates four fictional rows in a temporary dataset directory, and checks mean 20, three known values and one missing value. It also checks rejection of an invalid column schema and closes its subprocess. Expect `status: passed` in the JSON result. Native conversation rendering is a separate check.

Run the sample with `--portable` to check `mcp.json`. For recipient-owned saved data and an external interpreter, follow the environment settings and private binding options in the installation guide. An existing Data Explorer binding retains its interpreter and saved-data location while the plugin runs its bundled server. Check source closure separately with `python3 scripts/verify_public.py`.
