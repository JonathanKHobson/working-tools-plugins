# Product experience methods

Complete original methods for task structure, commerce/conversion, wireframes, mockups and implementation handoffs. Read only the matching section and its named internal support. The Studio owns these methods; authoring applications and real service integrations retain their execution contracts. Existing [UX Oracle](../../../libraries/ux-oracle/SKILL.md), frontend and design-system methods supply deeper evidence and implementation support without separate method packs.

## Information architecture

1. Inventory actual content, objects, actions, audiences and permission differences. Define the decisions/findability tasks, entry channels and scope. Remove duplicates only after checking source authority and historical links.
2. Group by users' concepts and recurring tasks. Compare plausible structures such as object-based, task-based and chronological against the same findability questions. Name categories with recognizable language; use supplied research rather than internal team names as evidence.
3. Define navigation levels, global/local/contextual links, search/filter, current location and back/return. Account for deep links, empty categories, denied access and deleted/moved content. Critical tasks must not depend on hover or an undiscoverable icon.
4. Build a small sitemap/content map using real labels and representative records. If evidence is uncertain, test category understanding with card sorting or task-based tree testing; the [usability procedure](usability-testing.md) defines participant/evidence discipline. Choose sample for the question; a fixed count is not proof of coverage.
5. Exercise “find X from entry Y” with at least one ambiguous case and a return path. Deliver the map, label rules, migration/deep-link behavior, observed confusion and limits. Example: invoices belong to Billing because the task is reviewing/payment; project references link there without duplicating invoice records.

## User flows and state contracts

1. Name actor, trigger, starting state, goal and confirmed outcome. Distinguish user intent, interface state, server state and external handoff.
2. Map the main path and branches for permission, validation, empty data, loading, cancellation, failure/retry, interruption and repeated actions. Record input/output and saved state per transition; use [Interaction Resilience](../../interaction-resilience/SKILL.md) for complete recovery mechanics.
3. Make irreversibility, cost and consent clear before commitment. Keep valid inputs during recoverable failures. Define what back, refresh and return after time away do. A visual arrow is not evidence of working persistence.
4. Exercise the flow from an unseeded start with representative fixtures. Observe each important transition and the action control itself. Deliver the state/transition contract and tested path, labeling unimplemented services.

Example: Draft → Validating → Saving → Saved. Validation failure returns to Draft with inline errors; save failure preserves input and offers retry; duplicate submit during Saving has no additional effect; confirmed Saved references the authoritative result. A mock should disclose its simulated save in the review handoff.

## Wireframes and high-fidelity mockups

Start from actual content and the main task, then choose low fidelity for unresolved sequence/grouping or high fidelity for visual decisions. Sketch entry, primary action, result and a consequential non-happy state. Label controls using real words, use representative lengths/data and avoid lorem ipsum where it hides a hierarchy problem. Annotate behavior that the static view cannot show.

Compare candidate structures against the same task and source constraints. Select one coherent direction; retain existing tokens/components for an incumbent product. High fidelity specifies type, spacing, color, component states, imagery, density and responsive treatment. Use [Design Systems](../../design-systems/SKILL.md) for token/component contracts and [interface craft](interface-craft.md) for bounded detail polish. Illustrations and image production use the existing Graphic owner; do not make asset generation a required preflight.

Map 3–8 source/viewport anchors and render at the intended viewing size. Check real text, long/empty content, focus/state visibility, contrast and narrow layout. A static mockup can prove composition only; use [prototyping](product-prototyping.md) for working navigation and state checks. Deliver editable source, selected direction/rationale, annotations and the limits of the chosen fidelity.

## Website and landing-page composition

Define the reader, entry expectation, intended next action, offer/content authority and proof available. Arrange the page so readers can recognize purpose, assess relevance, inspect credible support and take a clear action. Use actual content needs rather than a mandatory hero-feature-testimonial formula. Put important terms, exclusions and practical information near the decision. Use semantic headings, meaningful link text and readable content lengths.

Choose layout, type and assets from the project's identity; reference discovery stays with [Design Reference Lookup](../../design-reference-lookup/SKILL.md). Keep decorative effects subordinate to content and use [Motion and Performance](../../motion-and-performance/SKILL.md) only when motion serves a task. Test the primary CTA, destination, forms, narrow reading, keyboard and recovery. Report which claims/proof are verified; never invent testimonials, customers or results. Implement via the [prototype method](product-prototyping.md), then verify requested delivery stage.

## Conversion and ecommerce

Define the actual conversion event, eligible population, measurement period, baseline/denominator and competing outcomes such as cancellations, returns, support and trust. Start with observed funnel/task evidence. A low completion rate may reflect poor fit, stock/price/permission limits or instrumentation errors rather than a confusing button. Test that explanation before changing the interface.

For shopping, map discovery/filter, product comprehension, variant/quantity, availability, cart, delivery/tax/cost, account/guest, payment, review, confirmed order and post-purchase recovery. Keep price/currency, recurring terms, delivery limits and material exclusions visible before commitment. Preserve cart/input through recoverable failures. Distinguish stock reserve, payment authorization and completed order; don't imply success from button animation or a mock response. Avoid invented scarcity, hidden subscriptions, preselected consent and obstructive cancellation.

Prioritize a change by affected task, evidence, expected mechanism, reversibility and failure cost. Write a testable hypothesis: “Showing total delivery cost before checkout reduces cost surprise; assess completion and cancellation/support outcomes.” Choose comprehension/usability testing for task friction and a properly designed experiment for causal conversion claims. Specify assignment/unit, metric, guardrails, observation window and stopping rule with the statistical owner if an experiment is requested. Do not declare a percentage uplift from a heuristic critique or before/after traffic with confounds.

Acceptance includes finding a suitable item, understanding variant/price/availability, completing a simulated or authorized purchase path once, recovering from payment failure and identifying confirmation/status. Test a sold-out variant, unexpected costs and returning cart. Live charge/order actions require the user-authorized environment and actual integration checks. Deliver findings/hypothesis or the implemented change with observed tasks and measurement limits.

## Evidence-grounded personas, journeys and research plans

Use the complete [UX Oracle method](../../../libraries/ux-oracle/SKILL.md) with [method selection](../../../libraries/ux-oracle/references/methods-deep.md) and [artifact templates](../../../libraries/ux-oracle/references/templates.md) as applicable. [Research inputs](research-inputs.md) governs current evidence constraints: no mandatory sample count, simulated evidence or forced extra method. Choose the research question and the decision it will change before choosing a template.

For personas, represent sourced task patterns, environment, constraints and accessibility needs; label inferred motivations. For journeys, map the trigger, stages, actions, touchpoints, breakdowns and backstage dependencies with evidence IDs. Keep emotions as reported or explicitly hypothesized. For research plans, state question, method fit, recruitment/coverage, consent/privacy, guide/tasks, analysis and the contradictory observation that would change the design. Deliver source lineage, confidence/limits and design implications. Interview, study and survey execution use existing research/survey owners when their native support is needed; the UX artifact method remains available here.

## Design-to-code and handoff

Inspect the real source/component system before defining tokens or copying markup. Specify route/entry, component hierarchy, content, states, semantics, keyboard/focus, responsive behavior, assets/rights, data and backend boundaries. Link each requirement to source evidence and an acceptance task. Use the complete bundled [Frontend UX](../../../libraries/frontend-ux/SKILL.md) or licensed [Frontend Design Premium](../../../libraries/frontend-design-premium/skills/frontend-design-premium/SKILL.md) when its implementation depth is needed. Existing Development owns larger engineering changes.

For Figma, use the supported Figma workflow and actual node/source capabilities; if absent, provide an editable source/annotated contract without claiming a Figma file. For mobile, use [Responsive Design](../../responsive-design/SKILL.md) plus the actual native build owner when needed. Designers' screenshots do not define backend response, tokens or accessibility automatically.

Handoff includes source/node/asset links, changes and deliberate keeps, state/responsive contracts, implementation status, rendered anchors, interaction checks and unresolved decisions. Review the implementation in the same viewport; check shared-component consumers where changed behavior can affect them. Build success alone is not design acceptance. [Design Review](../../design-review/SKILL.md) governs critique; [UX Heuristic Compass](../../ux-heuristic-compass/SKILL.md) governs formal scored audits.

## Tool selection and capability help

Answer help by mapping the requested outcome to this Studio's maintained skill table and one useful task. Select tools by editable output, integration needs, recipient access and verification, not marketplace branding or affiliate promotion. Local files/code support prototypes; actual Figma tools support Figma authoring; native spreadsheet tools support workbook operations; current browser tools support observed interactions; actual hosting tools support deployment. A missing app connection limits that operation and should produce a useful portable artifact where the task allows it. No separate UI/UX method package is a normal prerequisite.

Portfolio narratives and career interviews belong to Career Studio when that is the requested output. Pass real role, contribution, evidence, constraints and result to its portfolio/interview method; do not invent impact metrics, participant quotes or ownership. UX can verify the design evidence and case-study source. Tool recommendations must distinguish methods, applications and real runtime dependencies.
