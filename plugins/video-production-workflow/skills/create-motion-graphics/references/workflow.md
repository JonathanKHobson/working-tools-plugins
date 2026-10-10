# Create Motion Graphics: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Define one animation slot with message, duration, dimensions, frame rate, alpha requirement, style tokens, and payoff timing.
2. Choose the renderer by content and environment, not habit.
3. Keep each slot isolated with its own dependencies, source, render, and reasoning log.
4. Storyboard the animation at key frames before implementation.
5. Use semantic motion and easing with explicit holds; sync payoff frames to narration or music evidence.
6. Render a draft and inspect first, payoff, final, and alpha frames.
7. Normalize dimensions, frame rate, codec, pixel format, alpha mode, and color metadata.
8. Reference only the rendered slot in the editorial manifest so the core renderer stays neutral.

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
