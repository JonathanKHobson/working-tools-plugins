---
name: mix-video-audio
description: Edit and verify a balanced video soundtrack from dialogue, voiceover, music, room tone and effects. Use for sync, ducking, fades, loudness or delivery mix problems.
---

# Mix Video Audio

## Core principle

Create an intelligible, emotionally coherent, technically compliant audio mix while preserving intentional dynamics and reusable stems.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Google Vids scope

For course recordings in Vids, use the [audio scope check](../edit-dialogue-footage/references/google-vids-course-editing.md#balance-sound-with-an-explicit-scope). Confirm the project, selected track, and intended all-audio or this-track scope, then listen across affected scenes. Save status or a clicked setting is not evidence of a balanced mix.

## Narration and language versions

For synthesized voiceover, pronunciation repairs or translated/dubbed audio, read [narration and dubbing](references/narration-and-dubbing.md). It covers voice authorization, separate display/spoken text, stable segment IDs, measured speech fit, stale-take invalidation and language-track/caption verification through available authorized tools.

## Workflow

1. Inventory streams and stems; probe sample rates, channels, duration, peaks, clipping, silence, and loudness.
2. Edit and clean dialogue/voiceover first, preserving natural room tone and breaths intentionally.
3. Place music and ambience for emotional structure before adding decorative effects.
4. Use automation or sidechain ducking to protect intelligibility rather than one fixed music volume.
5. Add short fades/crossfades at every edit and align effects to visible or narrative events.
6. Measure integrated loudness, loudness range, and true peak using BS.1770-compatible tools.
7. Perform final normalization with a two-pass workflow when precision matters.
8. Listen on multiple playback conditions and retain stems plus mix decisions.

## Required artifacts

- `audio-map.json`
- `stems/`
- `mix-notes.md`
- `loudness-report.json`
- `preview-mix.wav`
- `master-mix.wav`

Create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- Dialogue intelligibility outranks music loudness.
- Do not claim one loudness target is universal across broadcast, podcast, social, cinema, and internal review.
- Do not hard-cut audio at edit boundaries.
- Do not use normalization to repair clipping or a bad mix.
- Do not discard stems after rendering a combined track.

## Technical quick reference

- Use 48 kHz working audio for video unless a delivery requirement says otherwise.
- Sidechain compression needs tuned threshold, ratio, attack, release, and makeup; verify pumping by ear.
- Short equal-power crossfades usually hide edits better than simple linear fades.
- Measure true peak because inter-sample peaks may exceed sample peaks after encoding.
- For final accuracy, measure first and feed measured values into a second loudnorm pass.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **analyze-music-pacing**, **edit-dialogue-footage**, **render-video-project**, **conform-video-delivery**, **validate-video-quality**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

## Limits of automated audio checks

For noise-floor, gating, silence, omitted-filler or splice-click findings, apply [audio measurement limits](references/audio-measurement-limits.md) before choosing repairs. Preserve unavailable measurements and listening limits rather than converting uncertain flags into a pass or automatic edit.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Video Editor. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->

For a reproduced soundtrack, retain original PCM/stems separately from delivery gain, measure the final encoded result and keep sample equality distinct from listening. Use the [media-freeze sequence](../evolve-video-workflow/references/production-learning-transfer.md#freeze-media-before-deriving-review-evidence) so audio reports identify finished bytes.
