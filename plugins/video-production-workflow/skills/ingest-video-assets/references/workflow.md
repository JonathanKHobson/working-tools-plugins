# Ingest Video Assets: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Copy or reference originals without modifying them; establish source, work, cache, and output directories.
2. Hash each source and assign a stable asset ID independent of its display filename.
3. Probe streams, duration, frame rate, dimensions, sample rate, channels, rotation, pixel format, color metadata, and HDR transfer.
4. Inspect image orientation, alpha, embedded profiles, and actual pixel dimensions.
5. Record rights, creator, acquisition method, source URL, model/provider, prompt, and license status.
6. Generate lightweight proxies and thumbnails only when useful; retain source-to-proxy mapping.
7. Flag variable frame rate, missing audio, clipping, corruption, odd time bases, or unsupported codecs.
8. Update the project asset dictionary with relative paths and hashes.

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
