---
name: analyze-video-content
description: Locate and describe useful footage moments from transcripts, scene changes, frames, speakers, motion and quality signals. Use before selecting edits or reviewing a rendered video.
---

# Analyze Video Content

## Core principle

Create compact, queryable evidence that lets an agent reason about what is said and shown without exhaustively loading every frame.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Workflow

1. Resolve the user question and scope before choosing frame density or transcription depth.
2. Reuse cached analysis when the source hash and analysis settings match.
3. Acquire word-level transcript and speaker information when speech matters.
4. Detect shots/scenes and extract representative frames with deduplication.
5. Add frames at transcript-cued moments and ambiguous cut points rather than sampling uniformly forever.
6. Run subject/face/object analysis only when reframing or selection needs it.
7. Measure blur, exposure, motion, silence, and continuity as flags—not as automatic editorial verdicts.
8. Produce a compact markdown index linking timestamps to evidence files.

## Required artifacts

- `transcripts/`
- `scenes.json`
- `contact-sheets/`
- `timeline-views/`
- `subjects.json`
- `quality-flags.json`
- `analysis-index.md`

Create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- Do not claim to have watched a video from transcript alone.
- Do not classify visual intent from sparse frames without marking uncertainty.
- Do not re-transcribe unchanged sources.
- Do not let automated quality scores discard a uniquely important moment.
- Do not expose biometric identity claims without explicit need and evidence.

## Technical quick reference

- Use scene-aware sampling plus targeted timestamp frames; uniform sampling is a fallback.
- Word timestamps support cut snapping and output-timeline captions; phrase summaries are a reading optimization, not the source of truth.
- Deduplicate frames using perceptual or frame-delta thresholds so held slides do not consume the budget.
- For long videos, index by chapters, questions, or time windows and progressively deepen analysis.
- Build cut-boundary views that combine frames and waveforms around ±1–2 seconds.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **ingest-video-assets**, **edit-dialogue-footage**, **compose-slideshow-video**, **validate-video-quality**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

## Audience-retention evidence

For a requested retention or pacing diagnosis, read the complete [audience retention
editorial review](references/audience-retention-editorial-review.md). Map observations
to the correct output transcript/render, distinguish hypotheses from causes, and choose
one bounded experiment while preserving learning objectives and speaker meaning.

## Recording review and names

For recordings with multiple speakers or several downstream outputs, read [recording review and names](references/recording-review-and-names.md). Track actual review coverage, distinguish as-heard from confirmed names, and carry one correction through affected captions, graphics and social drafts.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Video Editor, Cinematographer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
