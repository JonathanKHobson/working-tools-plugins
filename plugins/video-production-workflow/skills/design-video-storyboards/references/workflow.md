# Design Video Storyboards: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Read the approved brief, analysis indexes, and delivery variants.
2. Break the runtime into narrative beats with purpose, information load, and emotional role.
3. Assign the best available asset or an explicit asset gap to each beat.
4. Choose a focal point, composition, text role, and motion role for each shot.
5. Map audio moments and music cut windows to visual beats without sacrificing comprehension.
6. Define design tokens: palette, typography, spacing, grids, safe areas, border/radius/shadow, and motion curves.
7. Create aspect-ratio-specific boards where crops or text hierarchy materially differ.
8. Review the storyboard as still frames and as timed sequence before rendering.

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
