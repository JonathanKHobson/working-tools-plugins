---
name: visual-asset-integration
description: Plan, generate, select, place, validate, and publish visual assets across websites, apps, games, dashboards, docs, decks, shareables, landing pages, portfolios, and public artifacts. Use when Codex needs to integrate images, screenshots, proof artifacts, generated art, icons, logos, backgrounds, hero media, social previews, evidence visuals, or decorative texture with clear asset purpose, source status, responsive crop rules, alt text, visual anchor maps, rendered QA, and publish-readiness checks.
---

# Visual Asset Integration

Use this skill when visual assets are part of a product, site, portfolio, game,
doc, deck, dashboard, shareable, or public artifact. The goal is to make every
asset earn its place: what it does, where it goes, what it can claim, how it
crops, and how it will be verified.

This skill coordinates adjacent skills. It does not replace them.

- Use `imagegen` for live image generation or edits.
- Use `frontend-ux` for frontend behavior, accessibility, and responsive UI.
- Use `design-taste-gate` for final craft, credibility, and anti-generic review.
- Use `portfolio-crafter` when assets support portfolio evidence or case proof.
- Use `communication-story-crafter` when assets support reader journey, claims,
  pitches, hooks, or proof loops.
- Use `html-presentation-builder` when assets need to work slide-by-slide in a
  browser-native deck, visual explainer, or Shareables slideshow.
- Use `social-content-studio` when the assets are social previews, proof
  campaign assets, reels visuals, profile imagery, release images, or post
  attachments.
- Use `marketing-strategy-operator` when the assets are part of paid ads,
  campaign briefs, launch kits, SEO/content refresh reports, landing-page
  conversion paths, offer pages, or marketing performance shareables.
- Use `project-structure-architect` before expanding project folders, build
  systems, manifests, or long-lived asset pipelines.

## Non-Negotiable Codex App Image Rule

When using Codex app image generation for any final asset, the chat preview is
not a source file. After every generated image, run the `imagegen` recovery gate,
copy the recovered bytes to a stable project path, verify the file, and use only
that absolute path afterward.

For icons, cutouts, badges, props, and UI symbols, generate **one asset per
image** when precise cropping matters. Use native transparency when supported by
the current tool; chroma key is a fallback with edge/spill QA costs. Preserve the
source before deriving a mask. A specifically authorized chroma workflow still
uses its own aperture and mask contract.

## Core Rule

Do not generate, pick, or place an asset until its purpose, source status,
placement, crop behavior, accessibility text, and verification path are known.

For generated icons, cutouts, badges, props, and UI symbols, plan one generated
image per asset using the current tool's supported background/alpha mode. Do not plan
single-image icon sheets when precise cropping or transparent derivatives are
needed.

## Text Over Image Rule

Do not place important text directly over a visually complex image region. A
background image can carry mood, proof context, or personality, but text needs a
quiet reading field.

Before shipping text over imagery, verify one of these is true:

- the text sits in genuine negative space with low texture and no competing
  shapes behind the words;
- the image is repositioned or cropped so the busy region moves away from the
  copy;
- a subtle local contrast treatment sits behind the copy, such as a parchment,
  paper, ink, or brand-appropriate translucent wash;
- a whole-image overlay is intentionally used and does not flatten the visual
  asset's purpose.

Prefer the smallest local treatment that solves readability. Do not remove or
mute a strong background when a crop, image-position, or local copy backing
would preserve the visual thesis.

## Workflow

1. Classify the surface: website, app, game, dashboard, doc, deck, shareable,
   landing page, portfolio, or mixed artifact.
2. Classify each asset purpose: `evidence`, `identity`, `interface`,
   `environment`, `editorial`, or `atmosphere`.
3. Inventory available sources: supplied files, screenshots, product captures,
   user photos, local evidence, brand assets, generated outputs, stock/reference
   material, or missing assets.
4. Create a visual anchor map before editing visual surfaces: 3-8 named regions
   with source, viewport or page, DOM hint if available, observed issue,
   intended asset role, and verification method.
5. Choose asset action per anchor: reuse source, crop source, edit source,
   generate new, replace placeholder, remove, or defer with a visible gap note
   outside public UI.
6. For generated assets, run the `imagegen` persistence gate immediately after
   each generation: recover the image from the Codex rollout JSONL if needed,
   copy it to a stable project path, verify it with `test -s` and `sips`, and
   use only that absolute file path.
7. Integrate with constraints: aspect ratio, dimensions, loading behavior, alt
   text, captions, source notes, responsive crop, contrast, repetition budget,
   and performance.
8. Run rendered QA when the asset affects a visible surface: desktop and mobile
   screenshots, overflow, clipping, text-over-image readability, contrast, text
   size, image load, broken references, and placeholder sweep.
9. Record final status: source, generated prompt if any, public-safety/source
   label, final file path, dimensions, alt text, verification evidence, and
   publish destination.

## Asset Purpose Model

- `evidence`: proves real work, product behavior, gameplay, artifacts, people,
  or outcomes. Prefer real screenshots, photos, exports, PDFs, maps, videos, or
  source-backed derivatives.
- `identity`: logo, favicon, brand mark, avatar, profile image, social preview,
  and reusable brand lockups.
- `interface`: icons, buttons, empty states, tool visuals, controls, system
  graphics, and UI states.
- `environment`: backgrounds, textures, table scenes, spatial atmosphere, world
  feel, section transitions, and immersive setting.
- `editorial`: images that explain, summarize, compare, annotate, or support a
  text argument in docs, articles, decks, reports, or case studies.
- `atmosphere`: decorative mood art, generated filler, side flourishes, flavor
  images, and non-proof emotional texture.

See `references/asset-purpose-model.md` for decision rules.

## Source Integrity Rules

- Never present generated imagery as evidence of real users, real people, real
  sessions, real product behavior, real gameplay, or real outcomes unless it is
  clearly labeled illustrative.
- Keep source status, prompts, temporary notes, and production scaffolding in
  manifests or docs, not visitor-facing UI.
- Public UI must not show internal placeholder IDs, production prompts, draft
  scaffolding, or asset slot labels. Preserve truthful historical work-stage
  labels and relevant original-source text when they help interpret the evidence.
- Repeated images weaken credibility. Set a reuse budget before duplicating a
  visual across a page or flow.
- For portfolios and public proof pages, put real artifacts near strong claims.
  Generated visuals can support mood, but they do not prove the claim.

See `references/evidence-and-source-status.md` for source labels.

## Design Tool Exports and Historical Evidence

For Stitch, Claude Design, or Figma outputs, record the source/version and actual
exported file, then reopen it before placement. Keep the original and a separate
crop/optimized derivative. Inspect the asset at its intended UI size and check
that important evidence survives the crop. Use the available tool-specific skill
for export mechanics; do not assume a rendered preview is a downloaded artifact.

Distinguish historical originals, historical iterations, new reconstructions,
new proposals, generated presentation artwork, and implemented results. A new
mockup can demonstrate new design work; it cannot prove an earlier launch or
outcome. Put a brief historical-stage label near a reconstruction when needed
for truthful interpretation, while keeping raw prompts and internal provenance
records private. Prefer original library recovery before reconstructing a gap.

## Placement Rules

- Hero media should support first-screen comprehension without inflating page
  height or forcing unnecessary scroll.
- Right-side hero art must be constrained by the hero's intended height; it
  should not define the hero height.
- Backgrounds and textures must preserve contrast and hierarchy.
- Icons should be real assets or system icons; pseudo-letter boxes are
  temporary scaffolding only.
- When the user bans site-owned glyph or SVG icons, use a coherent custom raster
  set and inspect it at actual UI sizes. This is a project constraint, not a
  global SVG ban; do not alter icons embedded in authentic source screenshots.
- Generated icons/cutouts should be produced one at a time; use supported
  transparency or a verified chroma-derived mask, preserving original bytes.
- Every placed image needs dimensions, responsive behavior, alt text, loading
  choice, and a mobile crop rule.
- Deck and slideshow images must have per-slide max dimensions and short-height
  behavior. If the image plus text cannot fit, split the slide rather than
  reducing text below readable size.
- Social preview assets need a channel crop plan, safe text zone, alt text, and
  proof/source status. Do not crop out the evidence detail that makes the claim
  credible.
- Campaign and ad assets need an approval boundary: draft concept, human review,
  account/spend gate, public-source status, claim/proof match, channel crop,
  and measurement note. Never treat a generated ad image as proof of user
  results, product adoption, or campaign performance.

See `references/placement-patterns.md` and
`references/responsive-image-qa.md`.

## North Star Rule

Use a North Star visual only when the surface is brand-defining, highly visual,
or likely to drift without a target. For smaller work, use a compact visual
direction brief instead:

- surface and audience
- asset purpose
- tone and credibility need
- source constraints
- placement and crop constraints
- verification path

## Output Contract

For planning or reviewing asset work, return:

```markdown
## Visual Asset Plan
- Surface:
- Audience:
- Asset goal:
- Source constraints:
- Verification path:

## Anchor Map
| ID | Region | Current issue | Asset purpose | Action | Verification |
| --- | --- | --- | --- | --- | --- |

## Asset Decisions
| Asset | Purpose | Source status | Placement | Crop/loading | Alt/caption | Risk |
| --- | --- | --- | --- | --- | --- | --- |

## QA Checklist
- Desktop:
- Mobile:
- Accessibility:
- Source integrity:
- Publish check:
```

## Reference Navigation

| Need | Read |
| --- | --- |
| Decide what job an asset is doing | `references/asset-purpose-model.md` |
| Place assets in common surfaces | `references/placement-patterns.md` |
| Generate or edit assets responsibly | `references/generated-asset-workflow.md` |
| Separate evidence from illustration | `references/evidence-and-source-status.md` |
| Build a visual anchor map | `references/visual-anchor-map.md` |
| Verify responsive selection, native resolution, contrast, no-JS use, and live bytes | `references/responsive-image-qa.md` |
| Adapt the workflow to sites, apps, games, docs, decks, dashboards, and portfolios | `references/cross-surface-patterns.md` |

## Stop Conditions

Stop and repair before claiming ready when:

- visible placeholder labels, prompt notes, or production scaffolding remain
- generated imagery is being used as proof without an illustrative label
- hero or side media causes excessive scroll, clipping, overflow, or unreadable
  text
- the same evidence image is repeated enough to weaken trust
- mobile crop behavior was not checked
- deck, reel, or social-preview crop behavior was not checked in its intended
  aspect ratio
- contrast, alt text, dimensions, or image loading are unknown
- the publish destination or repo path has not been verified

## Bounded production handoff

For multi-asset work, use the installed `visual-production-workflow` for serial
persistence, source hashes, scene/crop checks, immutable approved versions, and
image-heavy task rollover. Preserve this skill's historical-evidence and
responsive-image checks. For posters/flyers use `graphic-design-studio` for
format-specific composition and export.
