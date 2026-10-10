# Analyze Music Pacing: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Probe duration, channels, sample rate, peak/clipping, and silence before musical interpretation.
2. Extract a consistent analysis waveform without changing the source master.
3. Estimate tempo and beat timestamps; record confidence and half/double-tempo alternatives.
4. Compute onset strength and multi-resolution energy envelopes.
5. Infer candidate bars, phrases, drops, breakdowns, fills, and section changes from converging features.
6. Choose a pacing mode from narrative-led, phrase-led, strict beat sync, or ambient.
7. Generate multiple cut-window candidates with minimum/maximum hold lengths.
8. Validate the map by listening and visually checking several high-confidence and ambiguous regions.

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
