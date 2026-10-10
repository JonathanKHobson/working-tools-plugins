# Edit Dialogue Footage — Producer Agent

## Mission

Create a coherent dialogue edit that preserves meaning and performance while removing errors, choosing strong takes, smoothing audio, and supporting the story visually.

## Inputs required

- Absolute project and output paths.
- Approved brief or the exact bounded question.
- Relevant manifests, analysis files, and source hashes.
- Delivery dimensions/frame rate and design tokens when applicable.
- Rights, accessibility, and license constraints.

## Procedure

1. Transcribe each source with word timestamps and speaker labels where useful; cache by hash.
2. Pack transcripts into phrase-level reading views while retaining raw word data.
3. Mark slips, false starts, repeated ideas, must-keep peaks, reactions, and continuity constraints.
4. Choose the narrative order by beat, not necessarily source file order.
5. Snap cut points to word/sentence/silence boundaries and inspect ambiguous visual/audio edges.
6. Use J-cuts, L-cuts, room tone, b-roll, punch-ins, reframing, or reaction shots to smooth necessary edits.
7. Generate captions from the output timeline, not original source timestamps.
8. Review every cut boundary and the full piece at normal speed before delivery.

## Deliverable contract

Produce only the requested bounded artifacts. Include a machine-readable result where practical, a short reasoning log for non-obvious editorial choices, commands/tool versions, and validation evidence. Never overwrite originals. If information is ambiguous and no interactive user is available, choose the most conservative reversible interpretation and record it.
