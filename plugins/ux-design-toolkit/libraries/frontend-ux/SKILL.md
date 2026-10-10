---
name: frontend-ux
description: Use for UX-first frontend development review during HTML, CSS, JavaScript, TypeScript, React, Vue, Svelte, Tailwind, and UI component work. Trigger when Codex is writing, generating, reviewing, debugging, or planning frontend code and needs to evaluate UX quality, accessibility, state coverage, interaction patterns, design tokens, responsive behavior, clarity of labels and errors in code, or design-to-implementation decisions. Also use for requests like review my frontend, build this component, code this UI, how should I code this page, make this accessible, check my code for UX issues, or debug this component behavior. This skill is an advisory UX layer for frontend work, not a replacement for copy-only UX writing or Figma-node implementation workflows.
---

# Frontend UX

## Overview

Use this skill to keep frontend implementation decisions grounded in user experience. Treat each component or page as a UX hypothesis in code: check whether it communicates clearly, behaves predictably, includes the right states, and remains usable across devices and abilities.

Stay advisory. Shape implementation, reviews, and debugging through a UX lens, but do not take over specialized workflows that belong to narrower skills.

## Working Rules

- Classify the task first: implementation guidance, code review, debugging, planning, accessibility audit, or state-coverage review.
- Ground recommendations in the user's moment: what they are trying to do, what they just did, what they need next, and what emotional state they are likely in.
- Check meaning before polish. Fix clarity, state coverage, and accessibility before spacing tweaks or motion details.
- Prefer semantic HTML, visible focus, plain language, and design tokens over clever custom abstractions.
- Treat missing loading, empty, error, success, disabled, and edge states as bugs, not refinements.
- For visually important UI, use `references/codex-design-harness.md` before coding so art direction, content hierarchy, design-system reuse, rendered QA, and polish passes are explicit.
- For design-system or reusable component work, write the token and state
  contract before styling: semantic tokens, component variants, interaction
  states, empty/error/loading states, responsive rules, and minimum target
  sizes. Treat hardcoded one-off visual literals as a maintainability risk.
- When no strong design system is supplied, use `$ux-design-toolkit:design-reference-lookup` as a local
  searchable design-system generator for product-category styling, palettes,
  typography, landing-page patterns, chart recommendations, and stack-specific
  UI guidance. Treat its output as a starting recommendation, then adapt it to
  the actual audience, task, content, and constraints.
- For redesign or "make it premium" requests, choose the style source before
  coding: existing product system, adjacent best-in-class reference, image-led
  direction, editorial/portfolio direction, dense operational workspace, or
  experimental campaign surface. Do not mix several style sources casually.
- For landing pages, portfolios, and visual Shareables, declare a one-line
  design read before coding: page kind, audience, register, and aesthetic
  family. Then set variance, motion, density, and trust dials so the UI does
  not fall into default AI patterns.
- When using an image-first or design-reference-first workflow, translate the
  reference into layout, typography, color, spacing, motion, and component
  rules before coding. Do not merely mimic the mood.
- Check package dependencies before importing third-party UI, icon, motion,
  chart, or design-system libraries. If the project already uses an icon system,
  keep one family. If no dependency exists, use the repo's established install
  path or ask before adding one.

## Coordination and MCP Awareness

- Start with this skill when the task is UX-aware frontend planning, review, debugging, or implementation guidance.
- Use `$focus-ops-manager` when the user is stuck on priorities or shipping sequence rather than interface quality.
- Use `$pattern-picker` when the user first needs help choosing a thinking framework before frontend decisions are made.
- Use `$ux-heuristic-compass` when the work becomes a bounded heuristic audit, launch-readiness review, UX finding set, or report-ready critique of a visible interface. Use the UXHC MCP tools when they are exposed; otherwise use the standalone UXHC skill.
- Use `$plain-to-dev` when the task is mostly terminology translation or turning vague product language into engineering-ready structure.
- Use `$ux-writer` when the problem is copy-only and does not need frontend behavior review.
- Use `$html-presentation-builder` when the frontend surface is really a slide
  deck, browser-native presentation, visual explainer, or slide-like Shareables
  artifact. Its viewport-fit and density gates should govern the build.
- Use `$learning-experience-designer` when the interface is supporting a
  course, mini-course, lesson, worksheet, workshop, or learner practice flow.
- Use `$design-taste-gate` for final visual/craft review after semantics, state coverage, accessibility, responsiveness, and implementation basics are handled.
- Use `$ux-design-toolkit:design-reference-lookup` when the work needs a quick local lookup for design
  systems, product-category styling, palettes, typography, charts, stack
  patterns, or UI anti-patterns. The installed local version is offline and
  data-backed; do not run its network/update CLI paths without a separate
  security review.
- Use `$visual-asset-integration` when frontend UX depends on screenshots, hero
  media, image placement, generated assets, proof visuals, icons, backgrounds,
  responsive crops, or asset source status.
- Use `$playwright` or `$playwright-interactive` when visual quality depends on seeing the rendered page, comparing against references, or checking desktop/mobile behavior.
- Use `$communication-story-crafter` when the artifact's visual quality depends on narrative, portfolio framing, stakeholder trust, or public-facing proof.
- Use `$mac-environment-conventions` when local runtime/storage conventions on this Mac affect frontend setup or tooling choices.
- Use the `figma` MCP when implementation decisions depend on a concrete Figma node or design-system context.
- Use `knowledge_atlas` when framework, glossary, standards, lens-card, or related-concept context would sharpen design-to-implementation reasoning.
- Use the `playwright` MCP when the best next step is validating live UI behavior in a browser instead of continuing abstract advice.

### Artifact and App Routing

- Use Shareables when the user needs a durable single-file human-facing artifact for scanning, comparison, review, copy/export, or public-safe packaging.
- Use `$chatgpt-apps` only when the target is a ChatGPT Apps SDK project with MCP tools and widget UI.
- Treat Claude web artifacts as a separate artifact lane; do not assume their build/bundle workflow maps to ChatGPT Apps SDK widgets.
- Use a separate app plan when the request needs persistent state, backend behavior, complex editing, or app-like workspace interaction.

## Optional Design Partner Handoff

When one design decision would benefit from a visual mockup or independent critique,
use an available Stitch design skill or `kyle-mac-design-partners` when installed.
Send a compact audience/task brief and selected sources; request one bounded output.
Preserve accepted decisions and treat generated advice as a proposal. Verify exported
files, reconcile tokens and components, and inspect the implemented render before
claiming success. Do not make every frontend task consult every design tool.

## Workflow

### 1. Inspect context and user state

- Identify the surface: component, form, page, navigation pattern, data table, modal, settings screen, onboarding step, or error recovery step.
- Infer the user's job, likely device constraints, and likely stress level before evaluating the UI.
- Note whether the task is build, review, debug, or plan so the response matches the need.

### 2. Check aesthetic direction before building

For build or redesign work, commit to a short direction before code:

- Purpose: what problem this interface solves
- Register: product UI, dashboard, brand/marketing page, portfolio, local artifact, widget, or app-like prototype
- Audience: who uses it and what credibility they need
- Memorable idea: the one visual or interaction choice that makes this specific rather than templated
- Constraints: framework, design system, accessibility, performance, content, and device limits

Keep the direction proportional. Operational tools usually need quiet, scan-friendly craft; brand and portfolio surfaces can carry stronger visual identity.

For visually important work, read `references/codex-design-harness.md` and
write the compact harness brief before coding. This applies to polished
landing pages, dashboards, app prototypes, portfolio surfaces, Shareables,
ChatGPT app widgets, and "make it beautiful / less generic" requests. Keep the
brief short, but make these decisions explicit:

- visual thesis
- content thesis
- surface register
- dominant idea
- style source and design control dials: variance, motion, density, and
  reference source
- design-system inventory
- token plan
- generic-risk list

If there is no supplied design system, run a compact `$ux-design-toolkit:design-reference-lookup` query and
fold the result into the harness brief:

```bash
python3 "$UX_DESIGN_PLUGIN_ROOT/skills/design-reference-lookup/scripts/search.py" \
  "<product type> <industry> <surface> <style keywords>" \
  --design-system \
  -p "<Project Name>" \
  -f markdown
```

Use domain searches only when they answer a concrete decision: `--domain ux`
for interaction/accessibility risks, `--domain chart` for data visualizations,
`--domain typography` for font pairings, `--domain landing` for page structure,
or `--stack <stack>` for implementation-specific guidance.

After implementation, inspect the rendered UI with browser tooling when
feasible, then run a layout polish pass and a detail polish pass before final
signoff.

### 3. Check structure and interaction

- Verify the hierarchy makes the main action obvious.
- Check whether the interaction model matches common expectations for forms, dialogs, menus, tabs, filters, and destructive actions.
- Prefer systemized patterns over one-off behaviors.

### 4. Check state coverage

Review the implemented or planned states:

- default
- hover
- focus
- active
- loading
- success
- error
- empty
- disabled
- edge cases such as long text, zero items, many items, RTL, and narrow screens

If a state is absent, call it out directly and recommend the minimum viable fix.

### 5. Check accessibility and semantics

- Use semantic elements first: `button`, `a`, `label`, `input`, `nav`, `main`, `section`, `dialog`.
- Ensure keyboard access, visible focus, logical tab order, and screen-reader-readable labels.
- Use ARIA only when native semantics are insufficient.
- For widgets such as dialogs, tabs, accordions, comboboxes, alerts, and toasts, follow established APG behavior.

Read `references/accessibility.md` when the task involves an accessibility audit, interactive widgets, focus management, or WCAG-sensitive design choices.

### 6. Check clarity and UX writing in code

- Review labels, helper text, placeholders, empty states, and error messages as part of the interface, not as decoration.
- Prefer specific verbs on buttons and plain-language recovery guidance in errors.
- Flag placeholder-only labeling, vague button copy, jargon, and errors without a next step.

Read `references/ux-writing.md` when writing or reviewing microcopy embedded in frontend code.

### 7. Check consistency, tokens, responsiveness, and craft

- Prefer design tokens over hardcoded values.
- Check whether spacing, color, type, and interaction patterns match the existing system.
- Check whether design tokens cover color, type, space, radius, shadow, motion,
  and state. Prefer tokens and reusable classes over scattered literals.
- Confirm mobile and small-screen behavior before recommending polish.
- Keep one authoritative token source and shared global header/menu. Page-local
  navigation has a separate role; record intentional visual exceptions by audience.
- Wait for fonts, images, and layout to settle before visual measurement, including
  after 200% text resizing. At narrow widths, verify every required navigation
  destination remains visible or reachable through its intended menu. Passing a
  no-horizontal-overflow test does not prove all actions are accessible.
- Confirm interactive targets are at least 44px where touch is plausible.
- Treat motion as optional enhancement; respect `prefers-reduced-motion`.
- For landing/portfolio surfaces, reject generic structure before polish:
  centered hero plus three equal cards, repeated split headers, every-section
  eyebrows, duplicate CTA intent, placeholder logos, text-only "visual" pages,
  and fake product screenshots without an asset plan.
- For app/product surfaces, prefer state coverage and task density over
  decorative hero treatment. Operational tools should feel scan-friendly and
  repeatable, not campaign-like.
- After the UX basics pass, use `$design-taste-gate` when the surface still needs an intentional visual direction, anti-slop review, or final artifact polish.

Read `references/tech-stack.md` when the task involves framework tradeoffs, stack-specific UX risks, or documentation expectations for component systems.

## Output Contract

When reviewing or debugging, structure findings around these questions:

1. What user goal is this UI serving?
2. What UX risks or missing states exist?
3. What accessibility or semantics issues exist?
4. What concrete change should be made next?

Use direct, implementation-ready findings. Prefer exact fixes over abstract design commentary.

## Handoffs

- Use `ux-writer` for copy-only requests such as naming buttons, rewriting empty states, or tuning product voice without broader frontend implementation concerns.
- Use `design-taste-gate` for anti-slop review, visual polish, and final craft critique once the interaction, accessibility, state, and responsive basics are sound.
- Use `figma-implement-design` when the task is specifically to implement a Figma node or frame through the Figma MCP workflow.
- Use both this skill and a framework- or design-specific skill when the task needs a UX lens plus specialized execution guidance.

## Reference Files

Load only what the task needs:

- `references/accessibility.md` for WCAG 2.2, ARIA/APG patterns, keyboard and screen-reader checks, and common a11y failures
- `references/codex-design-harness.md` for polished first-pass visual UI, rendered screenshot QA, design critic loops, anti-generic rules, and two-pass polish
- `references/tech-stack.md` for stack selection guidance, framework-specific UX strengths and risks, and component documentation expectations
- `references/ux-writing.md` for labels, errors, empty states, loading and success copy, and inclusive frontend microcopy
- `skills/design-reference-lookup/` for the installed
  searchable design-system database adopted from `nextlevelbuilder/ui-ux-pro-max-skill`

## Quick Reminder

Before writing code: what experience is this building, for whom, and in what state?

After writing code: check states, semantics, focus, clarity, recovery paths, and responsiveness before polishing craft.

## Project organization guardrail

Before creating or expanding UX, design-system, prototype, or implementation project files, consult the `project-structure-architect` skill. Do not create expandable UX systems, design systems, websites, or app prototypes as monolithic single-file implementations unless the user explicitly requests a one-off single-file deliverable.

Organize research, synthesis, flows, wireframes, prototypes, content, design tokens, components, patterns, guidelines, assets, and implementation docs into clear folders when the work connects to future product expansion.
