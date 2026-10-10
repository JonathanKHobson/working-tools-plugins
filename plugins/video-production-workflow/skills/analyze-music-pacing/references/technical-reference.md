# Analyze Music Pacing: Technical Reference

## Domain-specific notes

- Beat tracking should output beat times and tempo; onset strength offers local transient evidence.
- Use smoothed RMS/energy at several windows to distinguish micro-accents from section-scale changes.
- Candidate phrase boundaries strengthen when beat-grid, novelty, energy, harmonic, and silence cues agree.
- Assign major visual changes to phrase/section boundaries; reserve individual beats for accents or micro-motion.
- Expose snap tolerance so an editor can preserve narration or visual continuity when a perfect beat cut harms meaning.

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
