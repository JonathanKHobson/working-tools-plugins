---
name: render-video-project
description: Compile an approved video manifest, edit and media assets into deterministic preview or final files. Use when the timeline is ready for rendering, caching and failure recovery.
---

# Render Video Project

## Core principle

Execute the editorial contract through staged, inspectable renders while minimizing rework, encoding loss, and silent timing errors.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Workflow

1. Validate and audit the manifest, resolve every asset, and verify runtime tools before rendering.
2. Choose a quality ladder: cut-check draft, evaluable preview, and final master.
3. Render or reuse normalized segments and isolated animation slots.
4. Assemble picture and transitions with verified output-timeline math.
5. Add overlays and compositing layers with explicit PTS offsets.
6. Mix or attach audio, then apply captions as the last visual layer unless intentionally designed otherwise.
7. Encode final variants with target codec, pixel format, color metadata, and fast-start/container settings.
8. Run probe and QA automatically; retain logs, hashes, and intermediate provenance.

## Required artifacts

- `render-plan.json`
- `cache/`
- `segments/`
- `visual-master.mp4`
- `mixed-master.mp4`
- `captioned-master.mp4`
- `render-log.json`

Create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- Do not render final quality before an evaluable preview passes.
- Do not concatenate streams with incompatible dimensions, frame rates, time bases, codecs, or audio properties.
- Do not use stream copy for frame-inaccurate cuts or across incompatible GOP boundaries without verification.
- Do not burn captions before overlays that could occlude them.
- Do not rerender unchanged expensive stages when hashes prove they are reusable.
- Do not bypass a failed music-boundary, CTA-hold, text-pacing, or source-reuse audit merely because FFmpeg can encode the file.

## Technical quick reference

- Staged pipeline: normalized segments → visual assembly → overlays → audio mix → captions → delivery encode.
- Use output timestamps and `setpts`/`asetpts` carefully for delayed overlays and audio.
- Use xfade offsets from cumulative output duration, subtracting actual transition overlaps.
- Prefer a mezzanine/intermediate codec when multiple downstream encodes would otherwise compound loss.
- Record the full command, tool versions, manifest hash, asset hashes, and output probe in the render log.
- Resolve FFmpeg and ffprobe through explicit overrides or the plugin-local runtime when they are not on PATH.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **compose-slideshow-video**, **edit-dialogue-footage**, **create-motion-graphics**, **mix-video-audio**, **validate-video-quality**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Video Producer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->

For reusable renders, read the cadence and cold-start checks in [production learning transfer](../evolve-video-workflow/references/production-learning-transfer.md). [Finish all media writers](../evolve-video-workflow/references/production-learning-transfer.md#freeze-media-before-deriving-review-evidence) before deriving evidence; any later remux invalidates checks bound to earlier bytes.
