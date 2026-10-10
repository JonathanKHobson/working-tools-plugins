# Exchange Video Timelines: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Identify the receiving tool, adapter, supported feature set, frame rate, and timecode convention.
2. Normalize source paths to stable asset IDs and build a media relink map.
3. Export the simplest interchange format that preserves the required editorial meaning.
4. Bake or render effects that cannot travel while retaining notes and source parameters.
5. Validate clip order, source ranges, output duration, track assignment, and transitions after import.
6. Package fonts, captions, proxies, LUTs, audio stems, and provenance only when rights allow.
7. Document unsupported features and any manual finishing work.
8. Round-trip a synthetic or small timeline before handing off a large project.

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
