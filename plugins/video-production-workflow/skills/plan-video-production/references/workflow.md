# Plan Video Production: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Read the conversation and inspect the project directory before asking anything already known.
2. Inventory goals, audience, runtime, aspect ratios, channels, assets, deadlines, brand constraints, rights, accessibility, and must-keep or must-avoid material.
3. Separate facts, user preferences, inferred choices, unresolved risks, and reversible taste decisions.
4. Propose two or three editorial approaches with a recommended direction and explicit trade-offs.
5. Define the narrative arc and pacing mode before assigning clips or animations.
6. Create acceptance criteria that can be checked after rendering.
7. Create or update the declarative project manifest; do not jump straight to renderer code.
8. Obtain strategy approval before expensive generation or final-quality rendering.

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
