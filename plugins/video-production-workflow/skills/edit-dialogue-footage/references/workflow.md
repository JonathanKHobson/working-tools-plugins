# Edit Dialogue Footage: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Transcribe each source with word timestamps and speaker labels where useful; cache by hash.
2. Pack transcripts into phrase-level reading views while retaining raw word data.
3. Mark slips, false starts, repeated ideas, must-keep peaks, reactions, and continuity constraints.
4. Choose the narrative order by beat, not necessarily source file order.
5. Snap cut points to word/sentence/silence boundaries and inspect ambiguous visual/audio edges.
6. Use J-cuts, L-cuts, room tone, b-roll, punch-ins, reframing, or reaction shots to smooth necessary edits.
7. Generate captions from the output timeline, not original source timestamps.
8. Review every cut boundary and the full piece at normal speed before delivery.

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
