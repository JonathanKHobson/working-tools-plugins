# Compose Slideshow Video: Technical Reference

## Domain-specific notes

- Default hold range: roughly 1.5–6 seconds, then adjust for music, reading, importance, and narrative.
- Ken Burns motion should overscan enough to avoid borders and use eased paths with stable end holds.
- Mixed orientation options: crop with subject anchor, contain with designed background, split layout, collage, or aspect-specific replacement.
- Crossfade duration changes perceived pace; 0.15–0.4 seconds feels brisk, 0.5–1.2 seconds feels softer, but context decides.
- Normalize all generated segments to common dimensions, frame rate, time base, pixel format, audio rate, and codec before concat/xfade.

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
