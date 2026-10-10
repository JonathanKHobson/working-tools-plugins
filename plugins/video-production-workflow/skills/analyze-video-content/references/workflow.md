# Analyze Video Content: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Resolve the user question and scope before choosing frame density or transcription depth.
2. Reuse cached analysis when the source hash and analysis settings match.
3. Acquire word-level transcript and speaker information when speech matters.
4. Detect shots/scenes and extract representative frames with deduplication.
5. Add frames at transcript-cued moments and ambiguous cut points rather than sampling uniformly forever.
6. Run subject/face/object analysis only when reframing or selection needs it.
7. Measure blur, exposure, motion, silence, and continuity as flags—not as automatic editorial verdicts.
8. Produce a compact markdown index linking timestamps to evidence files.

## Checkpoints

- **Intent checkpoint:** the approved strategy and acceptance criteria are explicit.
- **Evidence checkpoint:** source and analysis data exist and match current hashes.
- **Draft checkpoint:** a low-cost, target-aspect artifact is inspectable.
- **Technical checkpoint:** schema, timing, stream, and file assertions pass.
- **Review checkpoint:** an independent reviewer inspects actual outputs.
- **Handoff checkpoint:** downstream skill, exceptions, and reversible choices are documented.

## Change discipline

A revision should change the highest-level artifact that expresses the feedback. Change the brief for strategy, storyboard for shot design, manifest for timing/layout, an isolated slot for animation, audio map for mix, and delivery matrix for export. Avoid patching a rendered MP4 when the editable source of truth exists.

## Recovery

On failure, preserve logs and intermediates. Identify whether the root cause is input, manifest, dependency, analysis, editorial choice, renderer, encoder, or QA threshold. Reproduce with the smallest fixture, add a regression test, and rerun only invalidated cache stages.
