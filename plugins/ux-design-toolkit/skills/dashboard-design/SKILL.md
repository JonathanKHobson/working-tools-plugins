---
name: dashboard-design
description: Design or review a dashboard's information hierarchy, coordinated views, chart meaning, color, customization and delivery contract. Use for dashboard UX and visualization judgment; keep data analysis and rendering with their existing specialists.
---

# Dashboard design

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


Make the reader's next decision easier while keeping the data's meaning intact. Start with the existing dashboard, approved design and requested change. A single-chart repair uses only the relevant chart guidance; it does not require a new dashboard or a full design system.

Default to lay readers unless a scientific or academic audience is explicitly selected. Communicate at a glance with everyday labels and minimal decoding; put technical terms, raw IDs, coefficients, ordinal terminology, MATTR and opaque decimals in a named details view. Give every upfront visualization a distinct question. Preserve a compact familiar incumbent layout, use a details button for progressive disclosure instead of blanket accordions, and keep ordinary web reading text at least 16px. Apply the [reader-comprehension acceptance cases](references/delivery-and-qa.md#reader-comprehension-acceptance) before signoff.

## Resolve the decision before the layout

For a new dashboard or authorized redesign with open composition choices, apply [product-grounded design direction](../design-studio/references/distinctive-direction.md). Let the main question and supported current answer determine the first view; choose useful domain structure before generic KPI cards. Preserve approved systems and conventional tables where they serve the task. Keep zero, missing and failure states distinct and verify dependent totals after a representative action.

Identify the reader, question, decision, data scope and delivery mode. For ongoing monitoring, explain status and exceptions; for exploration, preserve context while users compare; for a one-time explanation, a short sequence of charts may serve better than a dashboard. Honor an explicitly chosen format. Do not invent a finding to fill a hero panel.

For substantial work, capture the [visualization contract](references/visualization-contract.md) in the existing project brief/spec. For a small change, record only affected fields. Reuse the application's schema, metric transforms, registry and renderer. This contract is a checklist to map onto them, not a replacement schema or mandatory file.

Choose a composition from the actual comparison using [dashboard patterns](references/dashboard-patterns.md). Give equally important peers comparable visual weight. Spend width on reading labels and comparing evidence; use progressive disclosure for controls and secondary detail. Aesthetic ambition is welcome: purposeful typography, spacing, composition and color should make the analytical structure clearer.

## Use the existing specialists

- **Data Visualization Toolkit:** choose and verify chart encodings, uncertainty, maps, visual stories and accessibility across surfaces. Use `data-visualization-toolkit:data-visualization` when the chart's meaning or form is the unresolved decision; this dashboard skill retains page hierarchy, customization and product interaction.
- **Data Analytics:** source profiling, metric definitions, aggregation and analytical evidence. If its shared Data app owns the artifact, retain its native React/Recharts runtime, chart specifications and neutral-title conventions; carry this skill's design decisions into those supported fields.
- **Build Web Data Visualization:** renderer, statistical, interaction, accessibility and export implementation in a custom web visualization. Read its current router and only the needed specialists. A layout decision here is not permission to replace the selected runtime.
- **Graphic Design Studio / infographic-design:** a composed static information graphic. For a lone chart use the existing visualization specialist directly; for a generic UI change use `design-studio`.

These are optional installed-provider handoffs, not new dependencies. If a provider is unavailable, use the existing project tools and state that limitation. Do not install a provider just because a reference names it.

For chart choice, accuracy or palette work, read [chart meaning and color](references/chart-meaning-and-color.md). Resolve meaningful differences through shape, position, labels or line style as well as hue. Keep entity identities stable across charts, filters and themes. Brand conventions do not waive applicable accessibility requirements.

## Preserve meaning through interaction

Separate presentation (theme, density, panel order), exploration (filters, grouping, drilldown), and analytical semantics (formula, denominator, normalization, scale transform). A presentation control cannot silently change a metric. A hidden series does not automatically leave its denominator. Share one transformed data/state source across charts, totals, titles, annotations and exports.

Use neutral titles for open exploration. If a supported claim is requested, recompute it for the current population and period or remove it when invalid. Keep authored notes distinct from computed findings. Allow chart switching only where the retained data and encoding support the same question. Provide visible active filters, reset and a non-drag alternative to rearranging panels when rearrangement is part of the task.

## Verify and deliver

Use [delivery and QA](references/delivery-and-qa.md) for local-first, customizable or shareable dashboards. For every substantive change verify a known value, the main interaction, and the rendered comparison at the promised viewing sizes. Capture 3–8 visual anchors (ID, source/viewport, region, selector if available, observed fact, intended action), then recheck affected anchors. A source-file inspection cannot establish visual quality.

Correctness, accessibility and unexpected network access are separate gates; attractive styling cannot compensate for failure. Report what was implemented, visually inspected, behavior-tested, exported or published with its actual evidence. Do not claim a better-performing workflow from a source review alone.

Maintainer source/adoption decisions: [research and security record](references/research-and-security.md). Read this only when extending the method or considering third-party downloads.

For deeper internal workflows and retained licensed methods, select and **read the complete matching procedure** from [this workflow’s source map](../../docs/procedures/dashboard-design.md), applying its [host adapter](../../docs/full-design-host-adapter.md). Load only the relevant method and required support.

For a multi-step dashboard or a request for distinct alternatives, read the complete [experience architecture selection method](references/experience-architecture-selection.md) after task framing and before chart choice. Preserve a requested format. For coordinated filters/comparison/scenarios, hand the task contract to Data Visualization `live-dashboards` and its complete exploration methods; do not apply them to a simple static chart.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports UI Designer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
