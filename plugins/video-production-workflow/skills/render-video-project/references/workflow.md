# Render Video Project: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Validate the manifest and resolve every asset before rendering.
2. Choose a quality ladder: cut-check draft, evaluable preview, and final master.
3. Render or reuse normalized segments and isolated animation slots.
4. Assemble picture and transitions with verified output-timeline math.
5. Add overlays and compositing layers with explicit PTS offsets.
6. Mix or attach audio, then apply captions as the last visual layer unless intentionally designed otherwise.
7. Encode final variants with target codec, pixel format, color metadata, and fast-start/container settings.
8. Run probe and QA automatically; retain logs, hashes, and intermediate provenance.

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
