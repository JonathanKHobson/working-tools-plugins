# Validate Video Quality: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Probe the output and compare streams, dimensions, duration, frame rate, codecs, pixel format, color, and audio to the manifest.
2. Run black, freeze, silence, clipping, loudness, and missing-stream checks appropriate to the project.
3. Generate first/last/midpoint frames, contact sheets, and cut-boundary views from the rendered output.
4. Validate caption timing, reading speed, overlap, safe-area placement, contrast treatment, and final-layer visibility.
5. Review representative reframes for faces, hands, products, diagrams, and text.
6. Normally watch the complete output at normal speed with sound; then spot-check muted and at small display size. Honor user-requested quiet testing: mute only the test player, preserve delivered audio, use silent signal/structural checks and disclose any unperformed listening review.
7. Classify issues by severity, confidence, location, evidence, and proposed fix.
8. Fix, rerender, and rerun targeted checks; cap blind self-iteration and report unresolved risks.

For a Short or course lesson, compare source and final output hashes, probe the final stream duration, and check the last caption against the final audible frame after every trim, retime, or join. Inspect the separate 9:16 cover and any 16:9 or square variants at their intended destination crop. Record whether listening, timed-caption review, local visual QA, and native playback/readback each actually happened. A source file's resolution, a Studio processing badge, and observed watch-page playback quality are three separate facts; pass platform observation to `social-content-studio:social-publishing` for readback on the stable video ID.

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

Before evidence readers, apply the [media-freeze sequence](../../evolve-video-workflow/references/production-learning-transfer.md#freeze-media-before-deriving-review-evidence). Review contact-sheet labels, timestamps, clipping and frame scale as part of the evidence check; regenerate evidence after a media mutation.
