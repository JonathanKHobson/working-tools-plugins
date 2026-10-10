# Evolve Video Workflow: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Read project memory, render logs, QA reports, user feedback, and current installed skill/plugin inventory.
2. Separate one-off project decisions from recurring techniques, fragile operations, and discovery/routing gaps.
3. Build a capability matrix before choosing whether to extend, merge, cross-reference, or create a skill.
4. Write pressure scenarios or retrieval tests and observe baseline failure before editing skill guidance.
5. Prefer deterministic scripts for mechanical repeated work and compact skill guidance for judgment.
6. Update cross-references, manifests, source registry, tests, examples, and migration notes together.
7. Run plugin validation, skill tests, integration renders, and plugin-eval before and after.
8. Preserve backwards compatibility or document a deliberate migration/deprecation path.

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
