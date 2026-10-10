---
name: ingest-video-assets
description: Inventory, probe and prepare incoming media with hashes, rights and format evidence. Use when photos, footage, audio, captions, fonts or generated assets enter a video project.
---

# Ingest Video Assets

## Core principle

Create an immutable source inventory and normalized working set without damaging or losing provenance for original assets.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Exported course clips

For repeated course-video installation (combined clips, chapters, timed transcripts and course handoff), use [course-video installation](references/course-video-installation.md). It includes the local sidecar packager and bounded delegation contract; the target project's runbook owns service-specific integration.

When an authorized course/workshop intake also includes cross-channel release,
use the conditional [derivative handoff](references/cross-channel-course-handoff.md).
Reuse the verified media/transcript once for YouTube parts/Shorts, LinkedIn
companions, and source-supported Substack or later LinkedIn adaptations. Native
channel policy, spacing and saved-state readback remain with Social Publishing;
course edits require their own actual instruction.

Use the [course export handoff](../edit-dialogue-footage/references/google-vids-course-editing.md#review-and-hand-off-exports) for grouped lesson recordings. Inspect embedded timed captions before retranscribing; verify repeated part names against content, preserve sequence/chapter mapping, and retain standalone tips as separate assets when the course plan calls for it. Instructional Design Studio owns lesson-page placement and learner launch checks.

## Generated-media handoff

For generated image or video inputs, use `$graphic-design-studio:graphic-asset-compositing` and its conditional generated-media handoff reference. Choose the operation before the model, validate required source assets and model-specific options, and retain a receipt linking source hashes, rights, prompt, model/provider, task ID, approved cost, output hash and actual decoded properties. A submitted generation job is not a downloaded, playable asset. Continue this ingest workflow and **validate-video-quality** before editorial acceptance. This route uses available authorized tools; it does not install or activate Open Generative AI.

## Workflow

1. Copy or reference originals without modifying them; establish source, work, cache, and output directories.
2. Hash each source and assign a stable asset ID independent of its display filename.
3. Probe streams, duration, frame rate, dimensions, sample rate, channels, rotation, pixel format, color metadata, and HDR transfer.
4. Inspect image orientation, alpha, embedded profiles, and actual pixel dimensions.
5. Record rights, creator, acquisition method, source URL, model/provider, prompt, and license status.
6. Generate lightweight proxies and thumbnails only when useful; retain source-to-proxy mapping.
7. Flag variable frame rate, missing audio, clipping, corruption, odd time bases, or unsupported codecs.
8. Update the project asset dictionary with relative paths and hashes.

## Required artifacts

- `asset-manifest.json`
- `probe/`
- `hashes.sha256`
- `proxies/`
- `rights-and-provenance.csv`
- `ingest-report.md`

Create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- Never overwrite, rotate, rename in place, or strip metadata from source media.
- Do not download remote media without authorization and applicable site permission.
- Do not equate a generated asset with unrestricted commercial rights.
- Normalize working copies, not evidence originals.
- Treat color metadata and display appearance as separate facts.

## Technical quick reference

- Use ffprobe JSON for machine parsing and store the raw response alongside summarized fields.
- Use content hashes as cache keys for transcript, scene, waveform, proxy, and render stages.
- Normalize proxies to constant frame rate and a common audio sample rate while preserving exact source timing maps.
- Detect HDR transfer functions such as PQ and HLG before creating SDR proxies.
- Store mixed-orientation images as-is; fit/crop choices belong to editorial/layout stages.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **plan-video-production**, **analyze-video-content**, **analyze-music-pacing**, **render-video-project**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

When a storyboard has missing footage, use [shot acquisition](references/shot-acquisition.md) for bounded candidate search, item-level rights and actual-interval review before downloading or generating replacements.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Video Editor. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->

For a portable media/source bundle, use the read-only inventory verifier and declared-closure limits in [production learning transfer](../evolve-video-workflow/references/production-learning-transfer.md#reproduction-is-a-production-step). Retain selected generated artwork and its measured crop/anchor map by hash; a prompt alone is not the asset.
