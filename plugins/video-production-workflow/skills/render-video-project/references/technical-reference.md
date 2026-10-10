# Render Video Project: Technical Reference

## Domain-specific notes

- Core pipeline: normalized opaque segments → sequential visual assembly/transitions → mapped audio mix → captions → delivery encode. Arbitrary overlays must be precomposited through a verified external editor/slot; this pipeline has no native layer-stack execution.
- Use output timestamps and `setpts`/`asetpts` carefully for delayed overlays and audio.
- Use xfade offsets from cumulative output duration, subtracting actual transition overlaps.
- Prefer a mezzanine/intermediate codec when multiple downstream encodes would otherwise compound loss.
- Record the full command, tool versions, manifest hash, asset hashes, and output probe in the render log.

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

## Advanced effect boundary

Read [tracked layer compositing](../../create-motion-graphics/references/tracked-layer-compositing.md#execution-boundary) before promising tracking, masks, selective blur, grading or keyed video reframing. Extra manifest keys can validate without being rendered. Precompose a complete picture slot using an available verified tool; preserve audio separately, normalize the asset, and verify the actual effect in the final output. Alpha metadata or a renderer recommendation is not execution.
