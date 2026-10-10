---
name: create-motion-graphics
description: Design motion graphics, code-authored animated stories, narration-led explainers, kinetic typography, diagrams, overlays or reusable video animation components. Use when producing time-based animated media; interactive UI behavior belongs to UX motion and performance.
---

# Motion Design and Graphics

## Core principle

Select the simplest licensed renderer that fits each animation slot, author deterministic motion, render a normalized asset, and integrate it without coupling the editorial timeline to one engine.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.

## Complete animated stories

For a standalone motion-designed film, channel introduction, continuous visual story or animation beneath authentic recorded narration, read and apply [code-authored motion storytelling](references/code-authored-motion-storytelling.md). It owns the full brief → semantic event map → motion/audio/type → preview → cover/export → rendered QA sequence. Graphic Design Studio’s `motion-design` owns visual direction through time; UX Design Toolkit’s `motion-and-performance` owns interactive behavior. Use the slot workflow below for isolated animation assets.

For explanatory graphs, process maps or sequence diagrams, apply [animated-diagram production](references/animated-diagram-production.md) for semantic fidelity, layout ownership, edge timing, camera framing and diagram-specific QA.

For procedural JavaScript films, an Animate drawing style, a Charlie motion brief or a chosen HyperFrames project, read [procedural video methods](references/procedural-video-methods.md). This routes full pinned source methods, local execution boundaries and the tested deterministic canvas example.

When an approved project selects Remotion for 2D composition, read [Remotion implementation and review](references/remotion-implementation-and-review.md). It translates the storyboard and event map into frame-driven React scenes, local rendering and exact-output review; it is not a reason to select Remotion by default.

When the film adapts an article or research source, carry the [source/article-to-video contract](../design-video-storyboards/references/source-article-to-video.md) through the semantic event map, narrated claims, visual scale and final editable-source handoff.

## Default art direction

For original motion pieces and substantial visual redesigns, apply [art-directed motion](references/art-directed-motion.md) by default before choosing a renderer: concrete typography and photography/imagery, evolving composition, a coherent movement grammar and a justified 2D/2.5D/3D choice. Render a bounded representative passage and inspect playback before extending an unresolved treatment. More effects, 3D or a named model are not proof of visual quality; isolated approved slots retain their bounded workflow.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Animation-slot workflow

1. Define one animation slot with message, duration, dimensions, frame rate, alpha requirement, style tokens, and payoff timing.
2. Choose the renderer by content and environment, not habit.
3. Keep each slot isolated with its own dependencies, source, render, and reasoning log.
4. Storyboard the animation at key frames before implementation.
5. Use semantic motion and easing with explicit holds; sync payoff frames to narration or music evidence.
6. Render a draft and inspect first, payoff, final, and alpha frames.
7. Normalize dimensions, frame rate, codec, pixel format, alpha mode, and color metadata.
8. Reference only the rendered slot in the editorial manifest so the core renderer stays neutral.

## Animation-slot artifacts

- `animation-brief.md`
- `renderer-decision.md`
- `slot-source/`
- `render.mov-or-webm`
- `alpha-check.png`
- `slot-qa.json`

For full films, use the artifact contract in code-authored motion storytelling; an opaque MP4 does not need an alpha check. For slots, create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- Do not default to Remotion merely because the agent knows React.
- Do not put unrelated animations in one agent or source file.
- Avoid linear easing unless constant-rate motion is semantically correct.
- Do not reveal independent elements at the same time when comprehension matters.
- Verify license and alpha support before investing in an engine.

## Technical quick reference

- FFmpeg/PIL: simple cards, counters, wipes, masks, image sequences, and utility overlays.
- HyperFrames: browser-native HTML/CSS/JS, product UI, kinetic type, deterministic web capture.
- Motion Canvas: TypeScript generator animation and explanatory motion.
- Manim: equations, graphs, geometric transformations, and formal diagrams.
- Blender: 3D, camera, particles, tracking, compositing, and VSE; Remotion: React component systems when license and ecosystem fit.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **design-video-storyboards**, **create-video-typography**, **render-video-project**, **validate-video-quality**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

For text behind an element, tracked labels, masks or selective foreground/background blur, read [tracked layer compositing](references/tracked-layer-compositing.md). The method applies to arbitrary filmed or authored elements, with explicit tracking/matte distinctions, occlusion handling, temporal QA and the current core renderer boundary.

For a short portfolio, product or social showcase made from owned images/video, read [browser showcase templates](references/browser-showcase-templates.md). Animos is an optional on-demand browser tool with a free-resolution limit; it is not a new renderer dependency or an assumed API.

Static graphics belong to `graphic-design-studio:graphic-design`; approved-file scheduling belongs to `social-content-studio:social-publishing`. Neither request requires generating motion.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Motion Designer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->

For image-generated artwork animated in code, apply [generated assets for motion](references/generated-assets-for-motion.md): measured bounds and registration, moving joints, saved artwork and controlled comparisons. For a reusable film, capture its [executable template](../evolve-video-workflow/references/production-learning-transfer.md#capture-the-executable-template) alongside production.
