# Design Studio task routing

Read the section that matches the current task. These routes preserve the conditional guidance from the Design Studio entrypoint; shared evidence, implementation, and verification rules remain in [the entrypoint](../SKILL.md).

## Reviews and specialist ownership

For an authorized interface review involving a user flow, recurring usability issues, or release/handoff evidence, proactively consider `ux-heuristic-compass` without requiring its name. Use a bounded tool-backed triage when it fits the requested review, and briefly state what it contributes. Offer the formal rubric, grades and report when that depth would help the decision; infer neither a complete audit nor a score from ordinary polish. Routine isolated edits stay in this workflow.

Go directly to the specialist for copy-only work (`ux-writer`), formal scored audits (`ux-heuristic-compass`), dashboard hierarchy and customization ([dashboard-design](../../dashboard-design/SKILL.md)), an explicit Stitch UI/export/library task ([stitch-design](../../stitch-design/SKILL.md)), chart meaning or correctness (`data-visualization-toolkit:data-visualization`), an explicitly named provider such as Sites or Graphic Design Studio, UX research/design-review follow-up communication, or framework selection (`pattern-picker`). Bespoke web chart code can still use the installed Build Web Data Visualization specialists. Asset-heavy work uses the [asset integration library](../../../libraries/visual-asset-integration/SKILL.md) only when needed. Consult [provider boundaries](providers.md) only when a handoff is needed. A draft, local preview or review request stops at that requested stage; an authorized publish request continues through the provider's delivery verification.

Read only the relevant reference: [review](review.md), [product and web](product-web.md), [Figma and Stitch](figma-stitch.md), [shared graphic principles](graphic-design.md), [UX writing](ux-writing.md), [data visualization](data-visualization.md), [verification](verification.md), [device and application routing](device-routing.md), [spreadsheet usability](spreadsheet-usability.md), or [providers](providers.md). Teaching and game design are outside this skill. Graphic Design Studio remains a separate production specialist; a poster-only task can go straight there.

## Interactive surfaces and charts

For a bounded interactive widget embedded in a product, chat or side panel, read [widget UX guidance](conversational-widgets.md) to choose the task, interaction model, states and evaluation. Apply its conversation-continuity guidance when the widget participates in a conversation. For library options presented for human choice inside chat, also read the [compact library chooser pattern](mcp-app-widgets.md). Build MCP owns protocol and supported host capabilities; AI-only backend retrieval stays separate from human-facing presentation.

For motion graphics within a requested website or Sites build, use [motion prompts and Sites handoff](../../motion-and-performance/references/motion-prompts-and-sites.md) alongside the chosen provider. Consider one purposeful motion moment; preserve the brief rather than adding animation by default. Graphic Design Studio supplies visual direction when needed.

For a product surface containing charts, scales or trait scores, apply the [reader-comprehension gate](../../dashboard-design/references/delivery-and-qa.md#reader-comprehension-acceptance): default to lay readers, accurate everyday labels, meaningful ends and middle with numeric ranges, distinct upfront questions, compact familiar layout, a named details button and ordinary web reading text at least 16px. Preserve uncertainty and distinguish targets from observations. Model agreement cannot establish empirical validity. This gate is a bounded review within the current task, not a dashboard rebuild.

## Research and experience direction

For new or redesigned surfaces whose hierarchy or expression is unresolved, read [product-grounded design direction](distinctive-direction.md) before choosing a template. Use its positive decisions and bounded checks alongside the applicable existing identity; do not force novelty into conventional work screens or approved designs.

For unresolved audience/problem assumptions, use [research inputs](research-inputs.md). For competing interaction directions or optional simulated task perspectives, read [decision alternatives](decision-alternatives.md); it keeps hypotheses distinct from observed user evidence and routes independent work to the existing Work Management owner. Survey construction belongs to the separate Survey Studio plugin: use `survey-strategist` for survey design, implementation and exports. Keep interaction and rendered review here; do not duplicate its survey engine. For an actual type or brand decision, use [typography and brand](typography-brand.md). These are conditional inputs, not prerequisites for a routine UI change.

For a fuzzy first app idea or an existing app experience that has lost its throughline, use [beginner app planning and checkup](beginner-app-planning.md); load its deeper Vibe Check library references only for the relevant question.

When the user asks to learn from a named website's visual language for another design, use [reference-site analysis](reference-site-analysis.md). It turns observed composition and supported style values into a bounded transfer brief. A mentioned URL alone does not activate it; the user's design question sets the scope.

For the layout or review of a collaborative whiteboard, use [collaborative board hierarchy](collaborative-boards.md). It covers one clear active task, evidence on demand, comparisons, and laptop-scale QA. Figma Studio owns editor execution; Workshop Facilitation owns the group process. Do not turn a requested board into a website or force a full workshop design onto a narrow visual correction.

For broad UX method choice or research framing, the [UX Oracle library](../../../libraries/ux-oracle/SKILL.md) retains the full source method and examples. For a substantial frontend design implementation, use the [frontend UX library](../../../libraries/frontend-ux/SKILL.md); for a focused final craft critique, use the [design taste library](../../../libraries/design-taste-gate/SKILL.md). These are conditional depth sources under this entrypoint, not separate default routes.

## Systems and implementation depth

Before efficiency-focused implementation of a person-facing feature, use [human expectations in the implementation handoff](implementation-expectations.md) when the interaction requirements are unsettled. Define the required comprehension, actions, states, accessibility and recovery from the actual task. Work Management retains business scope; Development Studio `implement-software` minimizes code only after the complete experience is defined. Existing specifications and tiny settled edits bypass a new design phase.

For a maintained system needing inventory, extraction or migration, use [design system evolution](design-system-evolution.md); a routine small fix does not need it. For onboarding/first-value flows or robust-state work beyond default/error/accessibility basics (malformed data, interrupted or stale async actions, retries, recovery), use [interaction resilience](interaction-resilience.md). For added or changed motion, or a reported/suspected performance problem, use [motion and performance](motion-performance.md). For adapting a surface across device, input, orientation, safe areas or locale beyond responsive shrinking, use [context adaptation](context-adaptation.md). Each is conditional: load only the one the current task needs.

When the task calls for the native detector, advisory design hooks, local live variants, or a native palette/font/component utility, load [native design runtime](native-design-runtime.md). It routes the pinned engine and licensed playbooks through the owned adapter; ordinary design judgment does not need the runtime.

## Delivery, production, and special formats

For delivered design artifacts and templates, maintain a concise source-grounded `DESIGN.md` using [the existing design specification contract](../../design-systems/references/template-design-contract.md). A template's `SKILL.md` links it, and its bundle retains all linked support. Keep routine changes proportional by updating the incumbent specification; do not create a new brand system or extra UI to document an existing design.

For image-led production of a website/product still, poster, document illustration or storyboard asset, use `graphic-design-studio:graphic-design`, which now owns the complete Visual Production Workflow. Load that full source and its asset/provenance/export checks. This handoff does not replace this skill's UI behavior or motion/audio responsibilities.

For pointing, carried memory, feedback, interrupted work, consequential error, workload or emotion claims, select and read the complete task-matching card through [human-systems decisions](human-systems-decisions.md). This maintained guidance supersedes inherited fixed visible-option caps and checklist-count workload scores; it preserves useful effort and applies accessibility criteria at their stated conformance level.

For a bounded component/detail polish request involving nested corners, optical alignment, icon weight/render size, image edges, text wrapping or transition timing, read the [interface craft adapter](interface-craft.md) and its complete task-matching source method. It preserves the existing system and treats upstream values as testable examples, with no automatic runtime or global aesthetic mandate.

### Scoped Atlas reference

For local ux concepts, frameworks, activities or source definitions, read [the scoped Atlas library](../../../references/atlas-library.md). Use its relevant-only search and full-source selection before adaptation; human browsing and assistant retrieval share the same source records.

For a new visual direction, a supplied gallery or an unresolved reference question, use [public design resources](../../design-reference-lookup/references/public-design-resources.md). Agents can browse Godly, select Transitions.dev examples and route deck/showcase references to their existing owners within the authorized task. Capture observed anchors and original adaptations; preserve approved design and keep the search proportional.

For an explicitly requested browser presentation, PPTX-to-web conversion or existing HTML deck revision, read [HTML presentations](html-presentations.md). Native slides remain the owner when that is the requested output; keep browser stage, faithful conversion, notes privacy and actual save/export behavior explicit.

<!-- BEGIN PROFESSIONAL-AGENTS -->
### Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../../references/professional-agents/README.md); this method supports UX Designer, Web Designer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->

For an explicit application appearance theme, preview, font selection or supported export/apply request, read [application appearance](application-appearance.md). Use actual current native controls and original palette design; a legacy catalog/codec is not claimed equivalent. Keep prepared palette, rendered preview, supported export and verified application distinct.

For product task context or resuming a prototype, read [task context](product-task-context.md). For URL/screenshot-to-code, app bootstrap, interactive prototypes or preview delivery, read [product prototyping](product-prototyping.md). For IA, flows, mockups, landing pages, commerce/conversion or implementation handoff, select the matching section of [experience methods](product-experience-methods.md). For neutral task-based participant studies, read [usability testing](usability-testing.md). These complete internal methods need no separately installed method pack; actual authoring runtimes remain with their execution owners.

For current complaints or UX pain research on a named product, read [source-grounded pain research](product-pain-research.md). For a saved-source setup/read/update request, use [task-context persistence](product-task-context.md#save-inspect-and-update-design-sources); save only explicitly requested project references. Source-driven builds use [design comparison QA](design-comparison-qa.md). Phone simulations use [the selected runtime contract](mobile-prototype-runtime.md), distinct from responsive web or native app builds.
