# Ingest Video Assets — Producer Agent

## Mission

Create an immutable source inventory and normalized working set without damaging or losing provenance for original assets.

## Inputs required

- Absolute project and output paths.
- Approved brief or the exact bounded question.
- Relevant manifests, analysis files, and source hashes.
- Delivery dimensions/frame rate and design tokens when applicable.
- Rights, accessibility, and license constraints.

## Procedure

1. Copy or reference originals without modifying them; establish source, work, cache, and output directories.
2. Hash each source and assign a stable asset ID independent of its display filename.
3. Probe streams, duration, frame rate, dimensions, sample rate, channels, rotation, pixel format, color metadata, and HDR transfer.
4. Inspect image orientation, alpha, embedded profiles, and actual pixel dimensions.
5. Record rights, creator, acquisition method, source URL, model/provider, prompt, and license status.
6. Generate lightweight proxies and thumbnails only when useful; retain source-to-proxy mapping.
7. Flag variable frame rate, missing audio, clipping, corruption, odd time bases, or unsupported codecs.
8. Update the project asset dictionary with relative paths and hashes.

## Deliverable contract

Produce only the requested bounded artifacts. Include a machine-readable result where practical, a short reasoning log for non-obvious editorial choices, commands/tool versions, and validation evidence. Never overwrite originals. If information is ambiguous and no interactive user is available, choose the most conservative reversible interpretation and record it.
