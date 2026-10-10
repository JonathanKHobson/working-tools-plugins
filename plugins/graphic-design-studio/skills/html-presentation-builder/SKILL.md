---
name: html-presentation-builder
description: Build browser-native HTML presentations, slide decks, technical walkthroughs, data-rich decks, visual explainers, and Shareables slideshow artifacts with viewport-fit, density, accessibility, and visual QA gates. Use when the user asks for slides, presentation, deck, PPT-to-web, visual explainer, architecture walkthrough, data story, or a progressive-disclosure HTML presentation.
---

# HTML Presentation Builder

Create readable, viewport-safe browser presentations. A deck is not a long page
with snap scrolling. Each slide has one job, one primary idea, and content that
fits without hidden overflow.

This skill integrates patterns from `frontend-slides`, `visual-explainer`,
`slide-sage`, Shareables slideshow templates, and local visual QA rules.

## Use This Skill When

- The user asks for a slide deck, talk deck, pitch deck, teaching deck, or
  browser presentation.
- A technical plan, project recap, diff review, architecture overview, or data
  story should become visual HTML.
- A PowerPoint/PDF needs to be converted into a web presentation.
- A Shareables artifact should use slide-by-slide progressive disclosure.

Use the bundled PowerPoint/document skills instead when the required output is
a native `.pptx` or DOCX/PDF file. Use Shareables directly when the output is a
long-form public HTML packet rather than a deck.

## Routing

- New HTML deck: use this skill.
- Data-heavy deck with charts/code/architecture diagrams: use this skill and
  load the data/diagram references needed.
- Technical visual explainer or comparison table: create a visual explainer;
  use Shareables `docs`, `packet`, `storyboard`, or `field-report-explainer`
  unless the user explicitly wants slides.
- Shareables slideshow: use Shareables `reel` template for concise
  screen-by-screen pacing.
- Native PPTX: use the PowerPoint/presentations toolchain.
- One-off public artifact: use Shareables, then apply this skill's
  viewport/density gate if it is slide-like.

## Non-Negotiable Viewport Gate

Every slide must fit the viewport:

- `.slide` uses `height: 100vh` and `height: 100dvh`.
- Slides use `overflow: hidden`; content that does not fit must split into
  another slide.
- Typography and spacing use `clamp()` or responsive tokens.
- Include short-height breakpoints for `700px`, `600px`, and `500px` heights.
- No intra-slide scrolling unless the artifact is explicitly a local reference
  viewer and the slide control communicates that.
- Images use `max-height: min(50vh, 400px)` or a slide-specific equivalent.
- Charts use `max-height: min(55vh, 420px)`.
- Code blocks use `max-height` and show only the essential 8-12 lines.

If in doubt, split. Never cram.

## Density Limits

Use these defaults unless the content and viewport prove otherwise:

- Title: 1 heading, 1 subtitle, optional meta line.
- Content: 1 heading plus 4-6 bullets or 2 short paragraphs.
- Feature grid: 6 cards maximum.
- Code: 8-12 lines maximum.
- Chart: 1 chart plus 1 takeaway.
- Diagram: 1 diagram plus 1 short caption.
- Quote: 1 quote, maximum 3 lines, plus attribution if supplied.

## Deck Workflow

1. Classify the deck: pitch, teaching, conference, internal, technical,
   evidence review, data story, or public shareable.
2. Inventory source material and required coverage.
3. Choose medium: Shareables `reel`, standalone HTML deck, or native PPTX.
4. Build an outline that covers every required source point. Add slides rather
   than dropping content.
5. Choose one style source and lock it. Avoid generic purple/blue gradients,
   emoji section icons, identical card grids, and default system fonts unless
   the project already requires them.
6. Define reusable CSS classes before using them. Do not repeat inline styles.
7. Add navigation: arrows, keyboard controls, touch/swipe if useful, progress
   indicator, and reduced-motion behavior.
8. Run visual QA on desktop and mobile before final handoff.

## Data, Diagrams, And Code

- Use semantic tables for comparisons and audits.
- Use Chart.js, ECharts, D3, or the Shareables data-visualization tools only
  when the data shape requires them.
- Use Mermaid for topology, flow, sequence, ER, state, or mind-map diagrams
  when auto-routing is useful.
- Use hand-built HTML/CSS/SVG for editorial diagrams, simple process flows, or
  tightly styled teaching diagrams.
- Keep diagram labels readable; prefer top-down for complex flows.
- Never define page-level `.node` when Mermaid is present.

## Visual QA

Before handoff:

- Open/render the deck or Shareables artifact.
- Create a visual anchor map with 3-8 anchors.
- Verify at minimum: desktop, mobile portrait, and one short-height viewport.
- Check text overlap, slide overflow, nav control visibility, focus states,
  image load, chart sizing, and print/static fallback when relevant.
- For Shareables, run `review_shareable_quality` and visual preview tools when
  a rendered shareable exists.

## Output Contract

```markdown
## Presentation Built
- Format:
- File:
- Slide count:
- Style source:
- Libraries used:
- Coverage:
- QA:
- Remaining checks:
```

For plans:

```markdown
## Deck Plan
- Audience:
- Purpose:
- Medium:
- Slide outline:
- Visual system:
- Required assets/data:
- QA plan:
```


## Public package boundary

This full original presentation procedure bundles no upstream installer, renderer, paid service or scraping tool. Resolve any host presentation/Shareables/chart provider only when available and needed. [Receiving-host guidance](../../docs/standalone-visual-workflows.md) names the boundaries; a static source check is not a rendered deck or actual audience acceptance.
