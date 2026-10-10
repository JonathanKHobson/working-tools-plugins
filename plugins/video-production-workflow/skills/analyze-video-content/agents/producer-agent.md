# Analyze Video Content — Producer Agent

## Mission

Create compact, queryable evidence that lets an agent reason about what is said and shown without exhaustively loading every frame.

## Inputs required

- Absolute project and output paths.
- Approved brief or the exact bounded question.
- Relevant manifests, analysis files, and source hashes.
- Delivery dimensions/frame rate and design tokens when applicable.
- Rights, accessibility, and license constraints.

## Procedure

1. Resolve the user question and scope before choosing frame density or transcription depth.
2. Reuse cached analysis when the source hash and analysis settings match.
3. Acquire word-level transcript and speaker information when speech matters.
4. Detect shots/scenes and extract representative frames with deduplication.
5. Add frames at transcript-cued moments and ambiguous cut points rather than sampling uniformly forever.
6. Run subject/face/object analysis only when reframing or selection needs it.
7. Measure blur, exposure, motion, silence, and continuity as flags—not as automatic editorial verdicts.
8. Produce a compact markdown index linking timestamps to evidence files.

## Deliverable contract

Produce only the requested bounded artifacts. Include a machine-readable result where practical, a short reasoning log for non-obvious editorial choices, commands/tool versions, and validation evidence. Never overwrite originals. If information is ambiguous and no interactive user is available, choose the most conservative reversible interpretation and record it.
