---
name: design-taste-gate
description: Use as a lightweight design-quality reviewer for frontend UI, artifacts, screenshots, prototypes, and product surfaces when the work needs a final visual/craft pass, anti-slop review, or design polish. Trigger for phrases such as design taste gate, anti-slop-review, design-polisher, make this less template-like, make this less generic, review this artifact, polish this UI, or review context-insensitive design patterns. This skill critiques and sharpens output; it is not a full frontend builder, UX research method, copy-only rewrite skill, or Impeccable-style command suite.
aliases:
  - anti-slop-review
  - design-polisher
---

# Design Taste Gate

Review user-facing UI and artifact output for design intent, visual quality, and context-insensitive patterns. Act as a compact taste gate: find the few changes that most improve credibility, specificity, and craft.

This skill is influenced by public design-skill patterns such as Anthropic `frontend-design`, Anthropic `web-artifacts-builder`, Impeccable, and Claude Artifacts guidance, but it does not vendor or require those upstream skills.

Additional 2026 harvest note: this local gate now also incorporates reviewed
static guidance from `Leonxlnx/taste-skill`, `garrytan/gstack` design-review
patterns, `nextlevelbuilder/ui-ux-pro-max-skill`, `Eldergenix/SUPER-DESIGN`,
`Sukrit-bit/builder-skill-suite`, `rhnfzl/slide-sage`, and selected
HTML-topic design/presentation repos. Upstream installers, hooks, browser
tooling, and skill-pack setup scripts are not required.

## Use This Skill When

- The user asks for design polish, anti-slop review, or a less generic visual result.
- A frontend, Shareables artifact, app mockup, dashboard, landing page, or component looks plausible but templated.
- `frontend-ux` has already handled structure, state coverage, accessibility, and responsiveness, and a final craft pass would help.
- `ux-writer` finds that weak wording is really being caused by hierarchy, density, or visual presentation.
- An artifact needs human-scannable hierarchy, visual restraint, or a credibility pass before sharing.

Do not use this skill for copy-only rewrites, heuristic scoring, Figma implementation, full app scaffolding, or security/install review.

For this maintained gate, read the [conditional decision method](../../skills/design-review/references/intentional-design.md) when generic-output patterns are the concern. It governs interpretation of aesthetic flags: require a concrete consequence, distinguish evidence from preference, and permit retain/investigate decisions. A rationale alone does not prove effectiveness.

## Core Rules

- Review after meaning, accessibility, state coverage, and implementation basics. Taste does not outrank usability.
- Be opinionated but contextual. A product dashboard, portfolio page, public landing page, and local review artifact should not share the same defaults.
- Name concrete fixes, not vibes. Prefer exact layout, type, spacing, color, motion, or copy-placement changes.
- Identify the style source before critique: existing product system,
  reference image/site, design-system style source, portfolio proof surface,
  editorial report, dashboard/ops surface, or brand campaign. A generic design
  often fails because it has no declared source.
- Start with a one-line design read: surface type, audience, register, and
  aesthetic family. The audience picks the aesthetic, not the agent's default
  taste.
- Set four control dials before critique when the surface is visual: variance,
  motion, density, and trust. Use restrained values for dashboards, public-sector,
  regulated, or operational tools; allow higher variance for brand, editorial,
  portfolio, or campaign surfaces.
- When no style source or design system is supplied, use `$ux-design-toolkit:design-reference-lookup` as a
  local evidence source for product-category styling, palettes, typography,
  charts, landing patterns, and anti-patterns before deciding what "good" means
  for the surface.
- For landing pages and portfolios, require a real visual asset strategy.
  Text-only or fake-screenshot pages are incomplete unless the user explicitly
  asks for a text-only artifact.
- Inspect common template patterns for task or content mismatch: centered hero plus
  three equal cards, purple/blue glow gradients, warm beige/brass premium
  palettes, all-eyebrow section rhythm, same CTA intent under multiple labels,
  placeholder logos, generic glass cards, and repeated split-header sections.
- For image-led surfaces, treat text/image integration as a craft issue. Strong
  background art is not enough if important copy crosses busy texture, props,
  map lines, faces, or similar-value colors. Prefer a crop/position adjustment
  or a local, theme-native reading field before flattening the whole image.
- For slide-like Shareables, decks, and visual explainers, viewport fit is a
  design-quality requirement. Split overloaded slides/screens instead of
  shrinking everything, and verify short-height desktop plus mobile portrait.
- For reusable UI, inspect whether the work has semantic tokens, deliberate
  variants, and complete states before judging polish. Untokened color/type/
  spacing choices usually read as accidental even when they look attractive.
- Avoid automatic bans. Familiar patterns can be valid when they serve a deliberate product or brand reason. A motif is not evidence of AI authorship.
- Keep the gate lightweight: report only material findings, with no minimum count. An appropriate design may need no changes.
- Preserve existing brand, design-system, and accessibility constraints when supplied.
- When code or a live artifact exists, critique the rendered UI or screenshots whenever feasible; do not rely only on prose, CSS, or component names for final taste judgment.

## Coordination

- Use `$frontend-ux` when the problem is interaction behavior, frontend state coverage, semantics, responsive bugs, or implementation guidance.
- Use `$ux-writer` when the problem is user-facing words: labels, CTAs, helper text, errors, empty states, or tone.
- Use `$visual-asset-integration` when the craft issue depends on asset purpose,
  image placement, proof-vs-illustration integrity, repeated imagery, generated
  visual credibility, responsive crops, or source status.
- Use `$html-presentation-builder` when the artifact is a deck, browser-native
  presentation, visual explainer, data story, or slideshow-style Shareable.
- Use `$ux-design-toolkit:design-reference-lookup` when a critique needs industry/style/stack lookup rather
  than only visual judgment. The installed local version is offline and
  data-backed; do not run its network/update CLI paths without a separate
  security review.
- Use `$ux-heuristic-compass` when the user needs a formal heuristic audit, severity scoring, evidence limits, or UX report artifacts.
- Use `shareables` MCP when the output should become a durable local visual artifact for human review, comparison, or public-safe packaging.
- Use `$chatgpt-apps` only when the target is a ChatGPT Apps SDK app with MCP tools and widget UI.
- Use a separate app or web-game plan when the user needs persistent state, backend behavior, complex editing, or gameplay.

## Workflow

1. Identify the surface and register: product UI, brand/marketing page, portfolio, dashboard, local artifact, widget, or app-like prototype.
2. Infer the audience, primary task, and credibility need from the prompt or visible surface.
3. Load `references/review-lenses.md` for any non-trivial review.
4. Check first-order usability: hierarchy, state clarity, accessibility constraints, and responsive viability.
5. If implementation exists, ask for or inspect rendered evidence: browser view, screenshot, Figma frame, PDF render, Shareables preview, or exported artifact.
6. For screenshots or rendered surfaces, create a small visual anchor map before critique: `ID | source/viewport | region/ref | observation | action | verification`.
7. Set the design control dials from the reference lenses: variance, motion,
   density, and reference source. Use the dials to explain what should change.
8. If no design system exists, run a small `$ux-design-toolkit:design-reference-lookup` query before final
   judgment:

```bash
python3 "$UX_DESIGN_PLUGIN_ROOT/skills/design-reference-lookup/scripts/search.py" \
  "<product type> <industry> <surface> <style keywords>" \
  --design-system \
  -p "<Project Name>" \
  -f markdown
```

9. Run the design lenses: composition, typography, color, spatial rhythm, motion, interaction states, responsiveness, UX writing placement, visual assets, and context-insensitive patterns.
10. Run the mechanical pre-flight: button contrast, CTA wrapping, nav wrapping,
    hero viewport fit, mobile collapse, focus states, alt text, imports/deps,
    favicon/meta when page-like, and no dead `#` links unless intentionally disabled.
11. Grade the result mentally against design quality, originality, craft, functionality, content believability, and safety/accessibility; call out only the scores that materially affect whether the work is shippable.
12. Return the smallest set of changes that would make the work feel intentional, specific, and shippable. Cite anchor IDs such as `A1`, `B2`, or `Card03` when visual evidence was used.

## Output Contract

Use this shape unless the user asks for another format:

```markdown
Mode: Design Taste Gate
Surface: [surface/register]
Verdict: [Ready with polish / Needs polish / Needs rethink]

## Highest-Leverage Fixes
- [Anchor ID or issue]: [why it weakens credibility or usability]. Fix: [specific change].
- [Issue]: [why]. Fix: [specific change].

## Keep
- [1-3 things that should not be disturbed]

## Handoff
[Use frontend-ux / ux-writer / Shareables / chatgpt-apps / no handoff needed]
```

For very small requests, answer in prose with the top 1-3 fixes.

## Reference Files

- `references/review-lenses.md`: design-quality lenses, artifact routing, and generic-AI UI tells
- `skills/design-reference-lookup/`: installed local
  searchable design-system database and generator

## Default Reminder

Make the output feel designed for this exact user, task, and surface. Remove generic polish before adding more decoration.
