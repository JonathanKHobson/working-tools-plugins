# Compose Slideshow Video: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Inventory and visually inspect every asset; remove duplicates and flag low-resolution or rights issues.
2. Choose story order and pacing mode before calculating durations.
3. Map asset importance and information density to hold length; do not allocate equal time blindly.
4. Resolve contain, cover, background-fill, collage, or designed-frame treatment for each orientation mismatch.
5. Apply subtle motion only when it improves focus or continuity; preserve faces and important edges.
6. Use phrase boundaries for major image changes and beat accents for local motion when music drives pacing.
7. Render a proxy at the actual target aspect ratio and review every transition.
8. Revise the manifest, then render and validate final variants.

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
