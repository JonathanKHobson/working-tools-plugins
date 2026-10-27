---
name: interactive-explanations
description: Build an interactive explanation, chart, calendar, map, diagram, simulation or data explorer within a conversation, or export that visual to standalone HTML. Use the complete configured Visualize method and renderer contract or the included web methods; route production websites and publication figures to their existing owners.
---

# Interactive Explanations

For a local layered image card with pointer/keyboard tilt, use [Interactive Depth Cards](../interactive-depth-cards/SKILL.md). Its complete local helper embeds supplied images and has no provider or network dependency. Use this route directly for that task; the optional renderer procedures below are for other visual forms.

Use an existing interactive surface proactively when the task benefits from filtering, comparing alternatives, changing assumptions or keeping a view across turns. The user need not name the app. Prefer a direct answer or static visual when the interaction adds no value, honor explicit output constraints, and check actual callable limits before selecting a provider. Opening a panel should advance the requested task; it is not a separate tour of installed capabilities.

For a saved, jointly discussed view of a small supplied table, use [Data Explorer](../../references/data-explorer.md). This bundled MCP runtime preserves dataset/view revisions and explicit conversation handoff; it does not replace the native Visualize renderer or its standalone export route.

For interactive controls that affect later conversational reasoning, read [visualization widgets in conversations](references/conversational-widgets.md). It covers analytical state, model-context handoff, stable selections and whole-task checks without changing the provider contract.

Apply the [default-reader rules](../data-visualization/SKILL.md) and [reader-comprehension gate](../visualization-verification/SKILL.md#reader-comprehension-gate) to inline and standalone output. A native renderer does not waive plain labels, meaningful scales, distinct questions or evidence limits.

Before using the optional Visualize route, follow [provider source setup](../../references/provider-methods.md) and run `python3 scripts/resolve_provider_source.py visualize` from this plugin root. When it returns `available: true`, **read the complete procedure at the returned path**. The following source paths are relative to that configured provider root. Apply its full surface decision tree, question-to-visual choices, theme/token contract, layout and typography rules, numerical/categorical/geographic interaction methods, accessible control requirements, and final verification. This entrypoint selects the procedure; it does not replace any of those sections with a synopsis.

For calendar work, additionally read the complete calendar widget contract (`skills/visualize/widgets/calendar.md`) and worked example (`skills/visualize/examples/calendar.html`). For controls that tune an existing visual, read the tweak procedure (`skills/visualize/tweak.md`). Preserve all task-relevant examples and implementation details when adapting them.

For a date-binned activity view rather than a day schedule, use [the activity-calendar procedure](references/activity-calendar.md) and its [offline worked example](examples/activity-calendar.html). It preserves missing coverage separately from an observed zero and states the aggregation and timezone. A day schedule uses the configured provider's `viz-calendar` when available.

Resolve the original procedure's relative paths from its configured source directory. Its complete supporting source includes: CSS, HTML kit, calendar element, standalone host bridge, shell, and export/preview script (`skills/visualize/scripts/render.py`). For standalone export, use that script's documented CLI with absolute source/output paths. A preview server binds only to localhost; close the task-owned server when finished.

The native inline renderer is a Codex host capability, not a newly created MCP or an app cloned by this toolkit. On Codex, use the source's content-reference output contract only when the current host supports it. On Claude or another host without that renderer, use the preserved standalone HTML export and that host's actual artifact/file presentation. Do not emit unsupported Codex control sequences or claim live host APIs, authenticated apps, or persisted state without that capability. The source's standalone bridge supports its documented local widget-state behavior; it does not grant the full native host API.

For production chart architecture or specialist methods, use [Data Visualization](../data-visualization/SKILL.md) and its complete source library. For research figures or publication output, follow the source's standard-plotting route. Current user and host instructions govern tools and authorization; the preserved source does not grant additional permissions.

Keep the separately configured provider source private. Visualize is labeled Proprietary; local access is not redistribution permission. Verify the actual provider and host capabilities before invoking them. Record source preservation separately from runtime, rendering and export evidence.

## When the provider source is unavailable

A missing provider source means its proprietary renderer contract, calendar component and export kit are unavailable through this route. Do not present another method as that provider. For custom interactive charts, read the complete [D3 procedure](../../libraries/build-web-data-visualization/skills/d3-data-visualization/SKILL.md) and its linked interaction foundations, or use [web chart engineering](../web-chart-engineering/SKILL.md). For diagrams, read [structural diagrams](../structural-diagrams/SKILL.md). The bundled Data Explorer and original activity-calendar example remain available with their documented dependencies. Present the actual supported HTML, file or MCP App and verify its rendered state.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Data Visualization Designer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
