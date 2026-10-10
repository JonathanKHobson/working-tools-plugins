# Codex Design Harness

Use this harness when a frontend or visual artifact needs to feel polished on
the first serious pass, not merely functional. It is a local workflow wrapper
around `frontend-ux`, `playwright`, `design-taste-gate`, and, when the page
depends on narrative, `communication-story-crafter`.

The goal is not to make Codex imitate Claude. The goal is to make Codex behave
like a careful product designer: choose a direction, build from evidence,
inspect the rendered result, invite skeptical critique, and polish the top
issues before signoff.

## Trigger

Use this file for:

- landing pages, portfolios, dashboards, app prototypes, Shareables, ChatGPT
  app widgets, and visually led HTML artifacts
- prompts such as "make this beautiful", "make it less generic", "Claude made
  this look better", "polished first pass", "artifact", "prototype", or
  "design harness"
- work where screenshots, Figma nodes, Claude output, mood boards, brand
  references, or existing design systems are available

Do not use the full harness for tiny bug fixes, copy-only edits, purely
backend work, or UI changes where the user explicitly wants only a mechanical
patch.

## Before Coding

Write a compact design brief before implementation:

- Visual thesis: one sentence naming the mood, material quality, and energy.
- Content thesis: what the viewer should understand or feel in the first five
  seconds.
- Surface register: operational tool, dashboard, brand page, portfolio,
  artifact, widget, game, or app-like prototype.
- Dominant idea: the one composition, interaction, visual anchor, or narrative
  choice that makes the surface specific.
- Design control dials: choose variance, motion, density, and reference source
  before coding so "polished" has a concrete target.
- Design-system inventory: existing components, tokens, typography, icon
  system, imagery, routes, state patterns, and data-loading conventions to
  reuse.
- Token plan: background, surface, primary text, muted text, accent, border,
  shadow, radius, spacing rhythm, and typography roles.
- Risk list: the ways this could become generic, cluttered, off-brand,
  inaccessible, or overbuilt.

If strong visual references exist, treat them as source-of-truth for hierarchy,
spacing, typography scale, imagery treatment, and responsive behavior. If there
are no references, choose a named visual direction before coding instead of
defaulting to a generic SaaS pattern.

## Design Defaults

Prefer:

- one dominant visual idea per viewport
- composition before components
- real content, believable data, and action-specific copy
- repo-native components and tokens before new primitives
- whitespace, alignment, contrast, scale, and cropping before decorative chrome
- sections, columns, dividers, tables, and media blocks before card grids
- meaningful imagery or product/state views when the surface needs a visual
  anchor
- text placed over images only when the rendered copy has a quiet reading field,
  either through true negative space, image repositioning, a local translucent
  backing, or an intentional overlay that preserves the visual thesis
- purposeful motion that clarifies hierarchy, feedback, or state change

Avoid unless the product or brand explicitly calls for it:

- purple/blue gradient defaults
- hero cards, stat strips, pill clusters, floating badges, and icon rows
- nested cards or card-like wrappers that do not carry interaction or grouping
- generic copy such as "unlock insights" or "seamless experience"
- dashboard layout for non-dashboard tasks
- one-note palettes, decorative blur, glass panels, glows, or abstract
  background effects used as the main idea
- stopping after the build passes without seeing the rendered UI
- letting a beautiful image sit directly behind important copy where similar
  colors, map lines, props, or texture compete with the text

## Builder And Critic Loop

Use two roles inside the same work loop:

- Builder: implement the strongest restrained version of the visual thesis
  using existing repo patterns.
- Critic: review the rendered UI skeptically and name the top issues that
  weaken credibility, specificity, usability, or craft.

The critic should grade these criteria:

| Criterion | Question |
| --- | --- |
| Design quality | Does the surface feel like one coherent whole with a distinct mood and identity? |
| Originality | Are there deliberate custom decisions, or mostly template/default AI patterns? |
| Craft | Are type, spacing, alignment, contrast, color, and responsive behavior competent? |
| Functionality | Can the user understand the surface and complete the primary task? |
| Content believability | Do the words and data feel specific, truthful, and useful? |
| Safety/accessibility | Are focus, contrast, semantics, motion, and state coverage acceptable? |

If any criterion is clearly weak, fix the highest-impact issues before
finalizing. Do not turn every minor taste preference into a patch; prioritize
changes that materially affect credibility, usability, or visual coherence.

## Rendered QA

For implemented UI, verify the surface in a browser whenever feasible:

- desktop around `1440px`
- tablet or medium width around `1024px` when layout complexity warrants it
- mobile around `390px`
- loading, empty, error, success, disabled, focus, hover/selected, and long-text
  states when those states exist or are being introduced

Use `playwright` or `playwright-interactive` for browser validation. Compare
against screenshots, Figma, Claude output, or the written visual thesis. If
browser automation controls Chrome, complete the browser handoff before
signoff.

Before making visual claims from screenshots or rendered pages, create a small
visual anchor map. Use 3-8 anchors such as `A1`, `B2`, `Card03`, or `Button02`
with:

- source and viewport or screenshot path
- approximate grid region or normalized coordinates
- Playwright ref, selector, route, component, or DOM hint when available
- observed issue or visual fact
- intended action
- verification result after the fix

Use those IDs in critique, code-change rationale, and final QA notes instead of
vague references like "the card on the left." If the surface is tiny, one or two
anchors are enough; do not turn anchor mapping into a separate deliverable.

## Polish Passes

Run two focused polish passes when the work is visually important:

1. Layout pass: composition, hierarchy, spacing rhythm, alignment,
   responsiveness, overflow, and interaction states.
2. Detail pass: typography, color, imagery, motion, microcopy placement,
   contrast, text-over-image readability, and generic AI tells.

Stop when the surface is shippable for the user's current need. Defer larger
evals, new skills, example libraries, or design-system rebuilds unless the
current task specifically requires them.

## Final Signoff

For visually important work, the final answer should briefly state:

- visual direction chosen
- files changed
- rendered viewports or screenshots checked
- visual anchor IDs verified, when an anchor map was used
- polish passes completed
- remaining tradeoffs or deferred follow-up

If this was only a plan, audit, or Markdown-only skill edit, say that rendered
visual QA was not applicable.

## Source Patterns

- OpenAI Codex skills: progressive disclosure, concise descriptions, and
  reference files for task-specific workflow.
- OpenAI frontend guidance: visual references, design-system reuse, real
  content, Playwright inspection, and explicit anti-generic constraints.
- Anthropic harness design: separate generation from skeptical evaluation and
  make subjective design quality gradable.
- Claude Design and Claude skill catalogs: design-system awareness, handoff
  bundles, skill/agent/persona separation, and cross-agent portability without
  installing external packages by default.
- Taste/UI skill harvests: use concrete control dials for variance, motion,
  density, and reference source rather than importing duplicate design skills.
