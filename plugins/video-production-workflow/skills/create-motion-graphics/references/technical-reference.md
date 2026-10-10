# Create Motion Graphics: Technical Reference

## Domain-specific notes

- FFmpeg/PIL: simple cards, counters, wipes, masks, image sequences, and utility overlays.
- HyperFrames: browser-native HTML/CSS/JS, product UI, kinetic type, deterministic web capture.
- Motion Canvas: TypeScript generator animation and explanatory motion.
- Manim: equations, graphs, geometric transformations, and formal diagrams.
- Blender: 3D, camera, particles, tracking, compositing, and VSE; Remotion: React component systems when license and ecosystem fit.

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
