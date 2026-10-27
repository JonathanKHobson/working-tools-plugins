---
name: design-video-storyboards
description: Turn a production brief and source assets into a timed beat sheet, storyboard, shot list and motion plan. Use before rendering when editorial sequence or visual language needs definition.
---

# Design Video Storyboards

## Core principle

Design a coherent temporal visual system whose narrative, composition, text, motion, audio, and transitions have explicit purposes.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.

For choosing a procedural video style, exploring references or sketching beat panels with Draw and Think, use [video style discovery](references/video-style-discovery.md). Video Templates and Draw and Think are optional external catalog/storyboard integrations. Verify installed capability before use. The standalone CLI generates text storyboards from project manifests, and bundled licensed Animate kits supply style source. Preserve source hashes and review limits with either route.


For adapting an article, research source or authored argument into a concise video, use [source/article to video](references/source-article-to-video.md). It binds source revision and claim anchors to shots, caveats, captions, authorized personal voice and editable delivery.

## Default art direction

For original motion work, apply the [art-directed motion contract](../create-motion-graphics/references/art-directed-motion.md) by default. Each key beat specifies opening → transformation → readable payoff → ending, its type/image relationship and motivated spatial continuity or cut. Choose concrete photography, type and movement treatments; palette/font changes alone do not distinguish alternative directions. Reuse the incumbent approved system for faithful continuations.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Workflow

1. Read the approved brief, analysis indexes, and delivery variants.
2. Break the runtime into narrative beats with purpose, information load, and emotional role.
3. Assign the best available asset or an explicit asset gap to each beat.
4. Choose a focal point, composition, text role, and motion role for each shot.
5. Map audio moments and music cut windows to visual beats without sacrificing comprehension.
6. Define design tokens: palette, typography, spacing, grids, safe areas, border/radius/shadow, and motion curves.
7. Create aspect-ratio-specific boards where crops or text hierarchy materially differ.
8. Review the storyboard as still frames and as timed sequence before rendering.

## Required artifacts

- `beat-sheet.md`
- `storyboard.md`
- `shot-list.csv`
- `design-tokens.json`
- `motion-language.md`
- `timeline-draft.json`

Create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- One primary focal point per moment unless intentional complexity is justified.
- Do not use a transition to hide a weak narrative connection.
- Do not place essential text in a generic safe zone without checking the delivery UI.
- Do not reveal multiple independent information elements simultaneously.
- Every animation needs a communicative or emotional purpose.

## Technical quick reference

- Use shot functions such as orient, explain, prove, feel, transition, breathe, and call-to-action.
- Budget reading time separately from shot duration; dense cards need holds after the final reveal.
- Use an 8% generic title-safe inset only as a draft baseline, then test platform-specific overlays.
- Specify motion in semantic terms—enter, emphasize, connect, transform, exit—before choosing an engine.
- Design for reflow rather than scaling a 16:9 layout into 9:16.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **plan-video-production**, **analyze-music-pacing**, **create-video-typography**, **create-motion-graphics**, **compose-slideshow-video**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Storyboard Artist, Cinematographer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->

When the task is choosing among visual directions, use the [controlled comparison](../create-motion-graphics/references/art-directed-motion.md#compare-alternatives-fairly-when-selection-is-the-task): hold content, narration, factual assets and format steady, then compare styleframes and playable passages. The selected project record carries the grammar into later subjects.

For reusable templates or making-of evidence, use [production learning transfer](../evolve-video-workflow/references/production-learning-transfer.md): distinguish advance storyboard intent from encoded contact sheets and retain stage, source hash and capture role.

For image-generated character acting, carry the [sprite action ledger](../create-motion-graphics/references/generated-sprite-animation.md) from storyboard to asset requests: explicit anticipation, limb/expression changes, pick-up/hold/release, follow-through and entry/exit transitions with every output frame accounted for.
