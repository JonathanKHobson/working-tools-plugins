# Analyze Video Content: Technical Reference

## Domain-specific notes

- Use scene-aware sampling plus targeted timestamp frames; uniform sampling is a fallback.
- Word timestamps support cut snapping and output-timeline captions; phrase summaries are a reading optimization, not the source of truth.
- Deduplicate frames using perceptual or frame-delta thresholds so held slides do not consume the budget.
- For long videos, index by chapters, questions, or time windows and progressively deepen analysis.
- Build cut-boundary views that combine frames and waveforms around ±1–2 seconds.

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
