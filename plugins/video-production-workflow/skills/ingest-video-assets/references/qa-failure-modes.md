# Ingest Video Assets: QA and Failure Modes

## Required checks

- Inputs and output paths resolve and originals remain untouched.
- Manifest and generated JSON validate.
- Timing is nonnegative, ordered where required, and within source bounds.
- Output streams, dimensions, duration, frame rate, audio, pixel format, and color metadata match the delivery contract.
- Captions, text, safe areas, contrast treatment, and subject crops are visually inspected on rendered frames.
- Audio edits, loudness, peaks, silence, sync, and intelligibility are listened to and measured.
- Rights/provenance and source review dates are present.
- Actual output is reviewed, not merely code or source assets.

## Known failure patterns

- destructive source conversion
- filename as identity
- missing rotation metadata
- orphaned proxy
- unknown rights

## Severity model

- **Blocker:** corrupt/unplayable, materially misleading, rights violation, missing essential stream, severe accessibility failure.
- **Major:** wrong timing/aspect, clipped subject/text, hidden captions, loudness/clipping problem, broken continuity.
- **Minor:** polish, small alignment, subtle pacing, metadata omission with no immediate delivery impact.
- **Taste:** plausible alternatives requiring user preference rather than technical correction.

## Recovery loop

Record the exact file, timestamp, frame, stream, command, or manifest field. Fix at the earliest source of truth, add or update a regression check, rerender only invalidated stages, and compare before/after evidence. Stop after repeated inconclusive self-iterations and surface the ambiguity.
