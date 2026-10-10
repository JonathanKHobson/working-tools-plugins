# Research and adoption record

Reviewed 2026-09-27 for an instruction-only extension of the existing UX Design Toolkit. Inputs were the user's two dashboard/visualization briefs and two pasted research summaries. Their embedded implementation prompts were treated as proposals, not independent authorization to install packages or modify a product.

## Decision

**Proceed** with original local guidance and existing installed providers. Confidence is high about this narrow change's absence of added execution surfaces; this is not a security certification of any named upstream repository. No third-party package, executable, renderer, database, font, image or source archive was downloaded to disk, installed or run. Remote text was inspected read-only through the web tool before adaptation. No new MCP, hook, credential, telemetry or service is introduced.

Existing owners were inspected first: Data Analytics `build-dashboard`/`visualize-data` and shared Data app; Build Web Data Visualization router and specialist guidance; UX Toolkit's design/data reference and bundled UI UX Pro Max; Graphic Design Studio. The personal plugins are maintained source trees; vendor caches remain generated provider artifacts.

## Adopt / adapt / defer

| Source and exact inspected surface | Evidence / license | Decision and local destination |
| --- | --- | --- |
| [Karthik color skill](https://github.com/skthewimp/karthik-data-visualization-skill/blob/main/dataviz-color/codex/SKILL.md) and [license](https://raw.githubusercontent.com/skthewimp/karthik-data-visualization-skill/main/LICENSE) | MIT, copyright Karthik S; selected instruction file only | Adapt chart-specific palette judgment into chart-meaning-and-color. Reject semantic-color priority over applicable accessibility and automatic median-as-neutral. Do not adopt its MCP/tool dependencies. |
| [chart-dashboard layout](https://github.com/raghuramsirigiri/raghuram-skills/blob/main/plugins/chart-dashboard/skills/chart-dashboard/references/layout.md), [main skill](https://raw.githubusercontent.com/raghuramsirigiri/raghuram-skills/main/plugins/chart-dashboard/skills/chart-dashboard/SKILL.md), [editable mode](https://raw.githubusercontent.com/raghuramsirigiri/raghuram-skills/main/plugins/chart-dashboard/skills/chart-dashboard/references/editable.md), [license](https://raw.githubusercontent.com/raghuramsirigiri/raghuram-skills/main/LICENSE) | MIT, copyright Raghuram Sirigiri; selected documentation | Adapt deriving composition from the analysis. Keep product filtering and annotation dependencies intact. Defer custom renderer: its documented smoothing/gap behavior needs tests; its edit-mode restrictions are not this workflow's rules. |
| [AntV creator](https://raw.githubusercontent.com/antvis/Infographic/main/skills/infographic-creator/SKILL.md), [search loader](https://raw.githubusercontent.com/antvis/Infographic/main/src/resource/loaders/search.ts), [license](https://raw.githubusercontent.com/antvis/Infographic/main/LICENSE) | MIT, copyright AntV; selected instruction and source inspection | Conceptual structure/theme separation informs Graphic Design Studio. Do not install: inspected creator uses an unpinned unpkg runtime and the icon loader requests a remote service. Any future adoption needs pinned local engine/assets and runtime denial tests. |
| [Dashboard Design Patterns](https://dashboarddesignpatterns.github.io/patterns.html) | Research design space, not an effectiveness ranking | Original task/composition cards; no copied diagrams or corpus. |
| [Munzner nested model](https://www.cs.ubc.ca/labs/imager/tr/2009/NestedModel/) | Primary design/validation framework | Distinguish problem, task/encoding and implementation validity in acceptance. |
| [Segel and Heer narrative visualization](https://idl.uw.edu/papers/narrative), [Heer and Bostock graphical perception](https://idl.uw.edu/papers/crowdsourcing-graphical-perception) | Primary research | Guided explanation and exploration are different modes; avoid treating memorability/style as accurate comparison. |
| ONS, W3C and Carbon pages linked in the chart/color and pattern references | Primary institutional guidance | Original concise guidance with attribution; no palette dataset, figures or webpage text bundled. |

UI UX Pro Max is already locally available; no duplicate install or corpus refresh. Anthropic frontend-design, Impeccable, visual-explainer, scientific chart runtimes and further renderer options were deferred as unnecessary for this upgrade. Their descriptions in the supplied briefs are research leads, not fresh security clearance. Public availability alone does not permit redistribution; for example, do not vendor Wilke's manuscript or illustrations without checking its restrictions.

## Threats checked and limits

- **Source spoofing:** read maintainer GitHub paths and primary institutional pages; no mirror installers or search-ad downloads.
- **Tampering/provenance:** live branch text is mutable. Nothing executable was acquired. No signed-release, dependency-graph or full-repository audit was performed; future code adoption needs exact commit/version/hash review.
- **Install scripts/persistence:** no third-party installers, package runners, lifecycle hooks, background processes or automatic updates were added.
- **Sensitive data:** research used public URLs; no task dataset, private file, credential or browser profile was uploaded to a source service.
- **Prompt injection/tool poisoning:** external instructions and tool names were treated as untrusted source material. Upstream mandates to install, call tools, use a CDN or prefer branding over access were not inherited.
- **Network:** AntV's inspected loader and template create a clear offline mismatch. All future dependencies retain an acquisition gate; local-process execution alone never establishes offline inference or runtime.
- **License:** three candidate MIT licenses were inspected. This package contains original synthesis and links, not upstream software or substantial copied instruction text. If upstream files are later vendored, retain their actual notices and record version/hash then.

Commands used for local work: file reads, authoring, existing Python validators, routing audit and Codex's local-plugin reinstall. Not run: external install scripts, npx/uvx, package installation, cloned code, third-party MCP, or candidate renderer. This record supports the narrow instruction-only decision; it does not claim the resulting dashboard workflow has won a comparative benchmark.
