---
name: compose-slideshow-video
description: Assemble photos, illustrations, screenshots, cards, music, narration or short clips into a paced montage. Use when a slideshow needs deliberate framing, transitions and text.
---

# Compose Slideshow Video

## Core principle

Produce an editable manifest and rendered montage that respects mixed orientations, music structure, story, subject framing, text, and delivery variants.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.


For an article/source companion assembled from diagrams, images or clips, apply the [source/article-to-video contract](../design-video-storyboards/references/source-article-to-video.md) before assembly; preserve claim anchors, meaningful caveats, captions/transcript and the distinction between editable timeline/assets and final MP4.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Workflow

1. Inventory and visually inspect every asset; remove duplicates and flag low-resolution or rights issues.
2. Choose story order and pacing mode before calculating durations.
3. Set a source-reuse policy. Repeating a source requires an editorial reason, not convenience.
4. Map asset importance, text reading time, and information density to hold length; do not allocate equal time blindly.
5. Resolve contain, cover, background-fill, collage, or designed-frame treatment for each orientation mismatch.
6. Apply subtle motion only when it improves focus or continuity; preserve faces, titles, hands, props, labels, and important edges.
7. Use phrase boundaries for major image changes and beat accents for local motion when music drives pacing.
8. Run `video-workflow audit-project` before rendering.
9. Render a proxy at the actual target aspect ratio and review every transition.
10. Revise the manifest, then render and validate final variants.

## Required artifacts

- `slideshow-plan.json`
- `project.json`
- `storyboard.md`
- `preview.mp4`
- `final.mp4`
- `qa-report.json`

Create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- Never stretch images to fill the frame.
- Do not crop a face, hand, caption, product, or essential edge merely to satisfy cover mode.
- Avoid random transition variety; build a small transition grammar.
- Do not animate every image identically.
- Keep text separate from image filenames and encode it explicitly in the manifest.
- Do not repeat an image inside one video unless the manifest records why that return matters.

## Technical quick reference

- Default hold range: roughly 1.5–6 seconds, then adjust for music, reading, importance, and narrative.
- Ken Burns motion should overscan enough to avoid borders and use eased paths with stable end holds.
- Mixed orientation options: crop with subject anchor, contain with designed background, split layout, collage, or aspect-specific replacement.
- Crossfade duration changes perceived pace; 0.15–0.4 seconds feels brisk, 0.5–1.2 seconds feels softer, but context decides.
- Normalize all generated segments to common dimensions, frame rate, time base, pixel format, audio rate, and codec before concat/xfade.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **analyze-music-pacing**, **design-video-storyboards**, **create-video-typography**, **render-video-project**, **validate-video-quality**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Motion Designer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
