---
name: edit-dialogue-footage
description: Select and edit interviews, tutorials, podcasts, performances or narrated footage from transcript and picture evidence. Use for clean cuts, b-roll, reframing, captions or short extracts.
---

# Edit Dialogue Footage

## Core principle

Create a coherent dialogue edit that preserves meaning and performance while removing errors, choosing strong takes, smoothing audio, and supporting the story visually.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Google Vids course footage

For recorded lessons, use [Google Vids course editing](references/google-vids-course-editing.md): contextual pause/filler removal, deliberate Edit/Replace handling, preview after changes, and caption/scene continuity. Preserve pedagogical pauses and the demonstrated action order even when a different narrative order might work for an interview.

For a vertical excerpt of a course lesson or screen demonstration, use [course Shorts repurposing](references/course-shorts-repurposing.md) for tighter dialogue, beat-based framing, selective caption emphasis, output timing, and rendered QA. Keep the full course release plan with the project. For each new Short, include a TikTok candidate assessment (selected / defer / unsuitable and reason) in the existing Social handoff. Reuse the clean reviewed master when suitable; Social Publishing owns TikTok metadata, current-account controls, disclosures and attended native future scheduling, without reopening existing YouTube releases. TikTok immediate/Now posting is prohibited. Direct source exports and custom edits, including authorized owned-account reuse, keep distinct variant IDs/hashes/receipts under the source; never overwrite a published variant. Hand off shared-source public readiness before Social schedules future slots on different account calendar days, at most one video per day.

## Trim an existing Drive recording

For a bounded temporal trim, especially when the existing share link must stay valid, use [Drive trim and same-file replacement](references/drive-trim-and-replace.md). This covers source backup, exact video timebase, caption retiming, quiet QA and verified version replacement.

## Workflow

When the requested edit must be assembled or finished inside Resolve, hand the
reviewed cut map to [Edit DaVinci Resolve](../edit-davinci-resolve/SKILL.md) for
edition-specific controls, timeline import and saved-project verification.

1. Transcribe each source with word timestamps and speaker labels where useful; cache by hash.
2. Pack transcripts into phrase-level reading views while retaining raw word data.
3. Mark slips, false starts, repeated ideas, must-keep peaks, reactions, and continuity constraints.
4. Choose the narrative order by beat, not necessarily source file order.
5. Snap cut points to word/sentence/silence boundaries and inspect ambiguous visual/audio edges.
6. Use J-cuts, L-cuts, room tone, b-roll, punch-ins, reframing, or reaction shots to smooth necessary edits.
7. Generate captions from the output timeline, not original source timestamps.
8. Review every cut boundary and the full piece at normal speed before delivery.

## Required artifacts

- `takes-packed.md`
- `editorial-brief.md`
- `edl.json`
- `broll-plan.md`
- `room-tone.wav`
- `captions.srt`
- `preview.mp4`

Create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- Never cut inside a word.
- Do not remove filler automatically when it changes personality, rhythm, or meaning.
- Do not use jump-cut concealment that creates misleading continuity.
- Preserve laughs, breaths, reactions, and silence when they carry the emotional beat.
- Do not publish quote edits that materially distort what a speaker meant.

## Technical quick reference

- Use word-level timestamps as cut anchors with small configurable padding to absorb alignment drift.
- Silence ≥400 ms is often a clean candidate, but visual continuity and performance still decide.
- Audio edits need short fades/crossfades and often a continuous room-tone bed.
- For a constant-speed segment, output caption time = (source word time − segment source start) / speed + segment output offset; split cues at edit boundaries.
- For shorts, judge hook, standalone coherence, pacing, value density, and payoff. Honor requested review holds; use the user's existing authorization for release.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **analyze-video-content**, **create-video-typography**, **mix-video-audio**, **render-video-project**, **validate-video-quality**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

## Analytics-informed editorial changes

When retention evidence is part of an authorized edit, first apply [audience retention
editorial review](../analyze-video-content/references/audience-retention-editorial-review.md).
Carry its observed intervals, uncertainty and must-keep constraints into the EDL;
recompute output captions and chapters after timing changes. Do not cut teaching pauses
or change speaker meaning merely to improve a curve.

For filler-removal candidates or sounds absent from a transcript, read [audio measurement limits](../mix-video-audio/references/audio-measurement-limits.md). Missing transcript text does not establish that the sound is filler; inspect the recording before cutting and preserve listening-review limits.

For a combined pacing/reframing/color/B-roll treatment across camera footage, screencasts or graphic sequences, read [editorial treatment](references/editorial-treatment.md). Preserve the existing timing and meaning checks; select effects by the brief rather than applying a demonstration prompt literally.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Video Editor. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
