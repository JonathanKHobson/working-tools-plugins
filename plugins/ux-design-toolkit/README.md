# UX Design Studio

Design, review and improve product interfaces, from usable wording and responsive layouts to interaction states, design systems and evidence-backed audits.

## What you can do

- Critique an observed screen or implement a bounded UI improvement.
- Design robust onboarding, recovery, responsive behavior or purposeful motion.
- Browse Site templates, consult selected UX methods, or produce a formal UX Heuristics Compass audit.

## How to start

1. Select this plugin in a supported host, or name the workflow in your request. Describe the result you want and provide the inputs listed below.
2. Start with one useful task. The assistant should explain the relevant capability, required input/access and expected result briefly when that helps; an explicit task can begin immediately.
3. Check the result and its reported state. A draft, local file, sent message and published result are different outcomes. Ask “what else can this plugin do?” or “help me get started” whenever you need the wider menu.

## Try a first task

| Ask | Bring | Expect |
| --- | --- | --- |
| “Review this screen and fix its three most consequential usability problems.” | Current source or visible interface, target viewport and user task. | Prioritized corrections with rendered and interaction checks. |
| “Show me a Site template for a research evidence report.” | Audience and the information the reader needs to explore. | Relevant Design Library options and a checked template handoff; selection alone does not publish. |

If you are starting from scratch, bring one real screen or a short content sample
and name the reader's next action. The assistant should choose one useful first
result and use the existing design where available. For example, “Turn this
pilot report into a short web summary while keeping its evidence and limits”
yields a content contract, adapted layout and checked render. A proposed
contract can reuse the [filled example](skills/design-systems/references/template-design-contract.md#worked-contract-a-fictional-pilot-report); a setup tour or completed questionnaire is unnecessary for a concrete task.

## Choose a skill

The table is a selection guide. Once a task matches, read that complete skill; follow only its applicable support-file routes.

| Skill | Use it for |
| --- | --- |
| [dashboard-design](skills/dashboard-design/SKILL.md) | Design or review a dashboard's information hierarchy, coordinated views, chart meaning, color, customization and delivery contract. |
| [design-reference-lookup](skills/design-reference-lookup/SKILL.md) | Browse local Site templates, public design galleries and transition references, or search offline palettes, typography and patterns when a visual decision is unresolved. |
| [design-review](skills/design-review/SKILL.md) | Critique, audit or polish a visible interface using observed design, accessibility and performance evidence. |
| [design-studio](skills/design-studio/SKILL.md) | Review a visible interface or coordinate UX/UI and web design, critique, and source-to-rendered verification. |
| [design-systems](skills/design-systems/SKILL.md) | Inventory, document, extract or evolve reusable UI tokens and components while preserving a coherent design system. |
| [interaction-resilience](skills/interaction-resilience/SKILL.md) | Design first-use flows and robust interface states for empty data, errors, recovery, retries and interrupted actions. |
| [motion-and-performance](skills/motion-and-performance/SKILL.md) | Design and review UI motion across state changes, feedback, interruption, focus and reduced-motion behavior; diagnose rendering performance when needed. |
| [responsive-design](skills/responsive-design/SKILL.md) | Adapt an interface across viewports, input modes, orientation, locale and native device constraints. |
| [spreadsheet-usability](skills/spreadsheet-usability/SKILL.md) | Design or review the human interaction layer of a workbook, tracker, model or spreadsheet decision tool. |
| [stitch-design](skills/stitch-design/SKILL.md) | Use when the user explicitly asks to work in Google Stitch through its current UI, export or integrate a selected Stitch result, review a Stitch design, or recover existing Stitch projects. |
| [ux-heuristic-compass](skills/ux-heuristic-compass/SKILL.md) | Run formal UX Heuristics Compass audits with the 14-heuristic rubric, evidence limits, audience-calibrated severity and structured reports. |
| [ux-writer](skills/ux-writer/SKILL.md) | Write or review product-interface words, including buttons, navigation, errors, onboarding, empty states, helper text and confirmations. |

## Tools, setup and access

Three optional connections have distinct owners: `ux-heuristic-compass` for formal structured audits ([bridge](skills/ux-heuristic-compass/references/mcp-bridge.md)); Design Templates' `design-library` for human template browsing and verified handoffs ([guide](docs/design-library.md)); Activities Templates' `atlas-ux` for scoped method retrieval ([guide](references/atlas-library.md)). The last two require their separately installed owners and authorized recipient data. For an ordinary UXHC start use `get_started(topic="brief")`; load deeper schemas only when the output needs them. AI-only Atlas search does not open a widget. Design Library is a chooser, not a Site publisher.

Figma, Stitch, Sites and other authoring providers retain their own tool/access requirements. Screenshots support visual findings, not claims about untested keyboard behavior or participant outcomes.

Installation makes a package available; it does not establish a working server or permission for every action. Portable hosts discover the Compass bridge through root `mcp.json`; compatibility hosts retain `.mcp.json`. Configure the backend through a recipient-owned binding and verify tool discovery plus one harmless scoped read. Design Templates and Activities Templates have their own setup and source access. The pinned Impeccable assets and adapter are included; macOS arm64 recipients acquire the exact executable through the [separate runtime release asset](docs/design-runtime.md#recipient-runtime-acquisition), then run `verify`. Keep credentials in the provider’s supported setup, never in a chat or this README. Report missing configuration, unreachable service, insufficient permission and an empty search as different conditions.

## Optional method providers

The Studio includes its complete first-party workflows and licensed design methods. Three branches use separately installed publishers: [Product Design](libraries/product-design/PROVIDER.md), [UI UX Designer](libraries/uiuxdesigner/PROVIDER.md), and [Spreadsheet Human UX](libraries/spreadsheet-human-ux/PROVIDER.md). Spreadsheet Human UX is required for the full spreadsheet-usability method. Each route identifies the exact skill, setup, host boundary and behavior when unavailable. The provider's full instructions and resources are read at use time; this package does not distribute or relicense them.

## Reading routes for the assistant

- For a concrete task, go directly to the selected `SKILL.md`; this README is not required reading for every run.
- For a capability/help question, use the introduction, first-task examples, skill table and relevant setup section, then recommend one first request. Skip maintainer notes unless the question concerns an update. On first relevant use, give a brief task-specific orientation; do not replay a tour on every invocation or claim the user has been permanently onboarded.
- Load the full selected procedure and its required support. References explain methods; scripts execute only the authorized operation; templates/assets are output material. Preserved libraries are conditional depth, not a bulk context load.
- Check actual callable tools and action/resource scope before promising access or completion.

## Maintainer and existing integration notes

Read the matching entrypoint in `skills/` and only the references needed for the current output. Design Templates owns the Design Library Site-template browsing app and shared chooser; UX retains a compatibility route through `design-reference-lookup`; see [its operation and source contract](docs/design-library.md).

Design Studio combines frontend UX, visual craft, research inputs and asset direction. Deep local libraries preserve uncommon workflows without adding competing automatic triggers. Figma, Stitch, Graphic Design Studio, Sites, Build Web Apps and document runtimes remain separate execution owners. Oppia, teaching and game design stay distinct.

This public edition has a per-file [source and output inventory](PROVENANCE.json), [license scope](LICENSE-SCOPE.json) and [third-party notices](THIRD_PARTY_NOTICES.md). Historical private audit snapshots and installed-cache details remain with the maintainer. Provider APIs, authentication, personal data and architecture-specific native binaries are not bundled in Git source.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->
