---
name: create-video-typography
description: Design and verify readable titles, captions, lower thirds, labels, callouts, credits or kinetic type. Use when text must work over changing imagery or across aspect ratios.
---

# Create Video Typography

## Core principle

Build measured, readable, brand-consistent temporal typography that remains legible against motion and platform overlays.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.

## Default art direction

In original motion work, type is part of the visual direction, not automatically a bottom label. Apply the typography and readability checks in [art-directed motion](../create-motion-graphics/references/art-directed-motion.md): role-specific character, scale, spacing, placement and purposeful behavior integrated with imagery. Static reading text, accessible captions and intentional lower thirds remain valid; do not animate every word or replace full captions with display fragments.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Workflow

1. Classify each text element by role: title, subtitle, body, caption, lower third, label, annotation, credit, or call-to-action.
2. Choose font families only after confirming availability and usage rights.
3. Measure text, line breaks, tracked-box bounds, safe-area collisions, and reading speed at target resolution.
4. Design local contrast treatment using scrims, boxes, outlines, shadows, blur, or tracked backgrounds.
5. Chunk captions by syntax, speech rhythm, and readability rather than a fixed word count alone.
6. Specify enter, emphasis, hold, and exit timing; use motion to reveal hierarchy, not decorate every word.
7. Create aspect-specific reflow and localization expansion rules.
8. Model left, right, top, and bottom platform reservations independently. Do not assume a symmetric safe margin.
9. Test representative frames and full-speed playback with captions and current platform overlays.

## Required artifacts

- `type-system.md`
- `caption-style.json`
- `captions.ass`
- `text-layout-report.json`
- `localization-notes.md`
- `safe-zone-overlays/`

Create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- Do not assume a font is redistributable because it is installed.
- Do not center text on the partial string during type-on animation when the final anchor should stay stable.
- Do not evaluate contrast against one still when the background changes over time.
- Do not put captions under later overlays in the final composite.
- Do not burn in captions as the only accessible deliverable when a sidecar is supported.
- Do not place essential text in a platform control lane or let text extend beyond its scrim or box.

## Technical quick reference

- Draft minimum contrast should follow WCAG logic, but moving video often needs stronger treatment than a static ratio alone.
- Use measured line width and explicit wrap points; avoid orphaned words and overly wide subtitle lines.
- Reading-speed thresholds depend on language, age, content, and caption style; flag rather than silently rewrite.
- ASS provides style, positioning, outline, box, and karaoke-like timing beyond SRT.
- Maintain subtitle/caption source separately from burned render so revisions and localization remain possible.
- Use `style.safe_area` for asymmetric platform reservations and record `reviewed_at` plus `source` whenever `delivery.platform` is set.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **design-video-storyboards**, **edit-dialogue-footage**, **create-motion-graphics**, **conform-video-delivery**, **validate-video-quality**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

For meaningful word emphasis, kinetic caption treatment or a full caption-style change, read [expressive captions](references/expressive-captions.md). It separates transcript/timing from style, supports selective color/weight/size/font/position choices, preserves complete captions and handles font-metric reflow without inventing renderer capabilities.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Motion Designer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->

For reusable motion templates, carry actual font/custom-glyph identity into the [executable template](../evolve-video-workflow/references/production-learning-transfer.md#capture-the-executable-template). Review full prop and camera trajectories across each reading interval, including end-card bounds, using encoded frames near crossings as well as key poses.
