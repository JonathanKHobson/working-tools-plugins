# Validate Video Quality: Technical Reference

## Domain-specific notes

- Structural assertions: streams exist, duration tolerance, dimensions, frame rate, sample rate, codec, pixel format, channel layout, and color tags.
- Temporal detectors should report timestamp ranges and thresholds so reviewers can distinguish intent from defects.
- Cut-boundary QA samples approximately ±1.5 seconds around each edit with waveform and adjacent frames.
- Caption QA combines text metrics with frame-level collision and contrast checks.
- A final report separates automated pass, visual review, audio review, accessibility review, and unresolved exceptions.
- A delivery receipt identifies the exact source, output video, caption, and cover hashes, final output duration and last caption time, plus each review status. Mark native status `unverified` until the platform owner reads back the saved asset and playback state; do not infer it from a prepared handoff.

## Shared project layout

```text
project/
├── source/          # untouched originals or immutable references
├── work/            # editable manifests, proxies, analyses, slots
├── cache/           # hash-keyed reusable artifacts
├── output/          # drafts, masters, variants, QA
├── project.json     # renderer-neutral editorial contract
├── provenance.json  # rights, hashes, lineage, tool/model versions
└── project.md       # session decisions and unresolved items
```

## Timing conventions

- Store seconds as floating-point values in the manifest and rational frame rate in delivery metadata.
- Derive frame indices at renderer boundaries; define rounding policy.
- Timeline item output end is `start + duration`.
- Transition overlap reduces cumulative output time.
- Source timestamps and output timestamps are different coordinate systems; never substitute one for the other.

## Cache key

Use a digest of source hash, relevant manifest fragment, script version, tool version, and analysis/render settings. Do not invalidate an expensive transcript because an unrelated title color changed.

## Command safety

Build subprocess argument arrays rather than shell-concatenated user input. Quote/filter-escape paths separately from shell escaping. Write logs with redacted secrets. Run in a project work directory and fail on nonzero commands.
