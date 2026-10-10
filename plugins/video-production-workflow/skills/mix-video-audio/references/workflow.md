# Mix Video Audio: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Inventory streams and stems; probe sample rates, channels, duration, peaks, clipping, silence, and loudness.
2. Edit and clean dialogue/voiceover first, preserving natural room tone and breaths intentionally.
3. Place music and ambience for emotional structure before adding decorative effects.
4. Use automation or sidechain ducking to protect intelligibility rather than one fixed music volume.
5. Add short fades/crossfades at every edit and align effects to visible or narrative events.
6. Measure integrated loudness, loudness range, and true peak using BS.1770-compatible tools.
7. Perform final normalization with a two-pass workflow when precision matters.
8. Listen on multiple playback conditions and retain stems plus mix decisions.

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

## Narration beneath B-roll and motion reveals

For a combined treatment, use the [audio continuity section](../../edit-dialogue-footage/references/editorial-treatment.md#maintain-audio-continuity-beneath-picture-changes). Preserve the voice timeline under picture changes, decide explicitly whether B-roll source audio contributes, align restrained effects to real events, and inspect ducking recovery and noise-reduction artifacts by ear. The core renderer strips segment audio; any intended clip sound must be mapped explicitly. Visual caption emphasis does not authorize changing a recorded voice.
