---
name: conform-video-delivery
description: Prepare and verify final video variants for a specified platform, client, archive or presentation. Use when a finished edit needs aspect, codec, captions, localization or other delivery changes.
---

# Conform Video Delivery

## Core principle

Create verified delivery variants from a high-quality master without treating stale platform presets or one-size-fits-all crops as truth.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Workflow

For lesson recordings going into a course, follow the [course-video installation handoff](../ingest-video-assets/references/course-video-installation.md) after media QA. Reuse its package helper rather than regenerating caption offsets and transcript formats per lesson.

For an existing YouTube catalog upgrade, deliver the exact source render hash, source resolution, reviewed caption file, and thumbnail asset; hand platform edits and native readback to `social-content-studio:social-publishing` and its conditional YouTube catalog packaging reference. Keep source quality distinct from YouTube's later processing state.

For a Short cut from a course lesson, prepare a faithful 9:16 cover as its own variant alongside any 16:9 lesson cover or square course-card art. Preserve approved artwork and claims; review the portrait crop at the actual destination. Use imagegen for new thumbnail artwork and semantic visual edits; reuse approved matching assets when no design change is needed. Export compression is a separate step. The [delivery workflow](references/workflow.md) holds the asset and receipt checks.

1. Start from a validated high-quality master and the approved delivery matrix.
2. Recheck current platform/client specifications and note the date/source.
3. Choose aspect-specific composition, crop, reflow, or alternate edit—not automatic scaling alone.
4. Set container, codec, profile/level, pixel format, frame rate, color metadata, audio codec/rate, bitrate/quality, and fast-start behavior.
5. Generate burn-in and sidecar caption variants as required.
6. Create poster/thumbnail and metadata packages where useful.
7. Probe and visually inspect every variant, including representative current platform UI overlays and asymmetric control/caption lanes.
8. Write checksums and a delivery manifest with source master hash and spec review date.

## Required artifacts

- `delivery-matrix.md`
- `variants/`
- `captions/`
- `posters/`
- `delivery-manifest.json`
- `checksums.sha256`

Create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- Platform specifications and safe zones are time-sensitive data, not permanent skill facts.
- Do not derive every aspect ratio from a center crop.
- Do not trust file extension as proof of codec or pixel format.
- Do not strip captions, color metadata, or audio by accident during transcode.
- Do not deliver only a social upload encode as the archival master.

## Technical quick reference

- H.264/AAC MP4 with yuv420p is a broad compatibility baseline, not a universal master format.
- Use constant frame rate when the destination expects it; preserve source cadence intentionally.
- Vertical and square versions often require text reflow, subject re-anchor, and alternate shot duration.
- Fast-start moves MP4 metadata for progressive web playback.
- Retain a mezzanine or high-quality master plus captions, stems, manifest, and provenance.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

For part, combined or edited-Short captions from a reviewed cue package, use
`export-captions` and the conditional [variant contract](references/caption-variant-export.md).

For final media handoffs, use the shared CLI `preflight-delivery` and its conditional
[batch contract](references/delivery-preflight.md). It checks local artifact and
review freshness, reports only outstanding work, and performs no publishing.

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **create-video-typography**, **mix-video-audio**, **render-video-project**, **validate-video-quality**, **exchange-video-timelines**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Video Editor. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->

For reusable templates, follow the [cold-start and executable-template checks](../evolve-video-workflow/references/production-learning-transfer.md). Verify the declared source/assets/fonts/audio inventory, then test the advertised commands in a fresh location before claiming portability. Preserve each variant’s exact review scope.
