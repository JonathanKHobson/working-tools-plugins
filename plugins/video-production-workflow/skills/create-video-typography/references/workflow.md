# Create Video Typography: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Classify each text element by role: title, subtitle, body, caption, lower third, label, annotation, credit, or call-to-action.
2. Choose font families only after confirming availability and usage rights.
3. Measure text, line breaks, safe-area collisions, and reading speed at target resolution.
4. Design local contrast treatment using scrims, boxes, outlines, shadows, blur, or tracked backgrounds.
5. Chunk captions by syntax, speech rhythm, and readability rather than a fixed word count alone.
6. Specify enter, emphasis, hold, and exit timing; use motion to reveal hierarchy, not decorate every word.
7. Create aspect-specific reflow and localization expansion rules.
8. Test representative frames and full-speed playback with captions and platform overlays.

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
