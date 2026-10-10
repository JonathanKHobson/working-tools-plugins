---
name: analyze-music-pacing
description: Map music tempo, onsets, phrases, energy and silence into edit timing evidence. Use when scenes, photos, type or animation should respond to a soundtrack.
---

# Analyze Music Pacing

## Core principle

Translate audio features into a confidence-aware pacing map and editorial cut windows without reducing music to a raw waveform or cutting every beat.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Workflow

1. Probe duration, channels, sample rate, peak/clipping, and silence before musical interpretation.
2. Extract a consistent analysis waveform without changing the source master.
3. Estimate tempo and beat timestamps; record confidence and half/double-tempo alternatives.
4. Compute onset strength and multi-resolution energy envelopes.
5. Infer candidate bars, phrases, drops, breakdowns, fills, and section changes from converging features.
6. Inspect lyrics or a word-level vocal transcript when vocals are present. Mark breaths, sustained syllables, complete phrases, and unresolved cadences.
7. Choose a pacing mode from narrative-led, phrase-led, strict beat sync, or ambient.
8. Generate multiple cut-window candidates with minimum/maximum hold lengths.
9. Validate every selected excerpt by listening from before the proposed start through after the proposed end.

## Required artifacts

- `music-analysis.json`
- `waveform.png`
- `energy-envelope.csv`
- `section-map.md`
- `cut-windows.json`
- `pacing-recommendation.md`

Create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- A waveform shows amplitude, not meter, phrase, emotional meaning, or editorial importance.
- Never cut on every beat unless that is an explicit aesthetic choice.
- Do not present a tempo estimate without uncertainty or alternate pulse interpretations.
- Do not use loudness normalization to erase intentional dynamics before analysis.
- Keep music licensing and attribution in the asset provenance record.
- Never cut inside a spoken or sung word, at an awkward breath, or before an obvious phrase resolution.

## Technical quick reference

- Beat tracking should output beat times and tempo; onset strength offers local transient evidence.
- Use smoothed RMS/energy at several windows to distinguish micro-accents from section-scale changes.
- Candidate phrase boundaries strengthen when beat-grid, novelty, energy, harmonic, and silence cues agree.
- Assign major visual changes to phrase/section boundaries; reserve individual beats for accents or micro-motion.
- Expose snap tolerance so an editor can preserve narration or visual continuity when a perfect beat cut harms meaning.
- A trimmed music asset must record `boundary_review.start_natural`, `boundary_review.end_natural`, and the listening method in the manifest.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **plan-video-production**, **design-video-storyboards**, **compose-slideshow-video**, **mix-video-audio**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Video Editor. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
