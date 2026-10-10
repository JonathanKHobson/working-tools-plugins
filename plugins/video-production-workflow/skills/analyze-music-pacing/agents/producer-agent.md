# Analyze Music Pacing — Producer Agent

## Mission

Translate audio features into a confidence-aware pacing map and editorial cut windows without reducing music to a raw waveform or cutting every beat.

## Inputs required

- Absolute project and output paths.
- Approved brief or the exact bounded question.
- Relevant manifests, analysis files, and source hashes.
- Delivery dimensions/frame rate and design tokens when applicable.
- Rights, accessibility, and license constraints.

## Procedure

1. Probe duration, channels, sample rate, peak/clipping, and silence before musical interpretation.
2. Extract a consistent analysis waveform without changing the source master.
3. Estimate tempo and beat timestamps; record confidence and half/double-tempo alternatives.
4. Compute onset strength and multi-resolution energy envelopes.
5. Infer candidate bars, phrases, drops, breakdowns, fills, and section changes from converging features.
6. Choose a pacing mode from narrative-led, phrase-led, strict beat sync, or ambient.
7. Generate multiple cut-window candidates with minimum/maximum hold lengths.
8. Validate the map by listening and visually checking several high-confidence and ambiguous regions.

## Deliverable contract

Produce only the requested bounded artifacts. Include a machine-readable result where practical, a short reasoning log for non-obvious editorial choices, commands/tool versions, and validation evidence. Never overwrite originals. If information is ambiguous and no interactive user is available, choose the most conservative reversible interpretation and record it.
