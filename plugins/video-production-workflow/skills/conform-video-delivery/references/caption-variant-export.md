# Export caption variants from reviewed cues

Read when a reviewed course package needs separate-part, combined or edited-Short
SRT files. Reuse its existing `.cues.json`; do not transcribe the whole recording
again or write a fresh offset script for each delivery. This command creates
local sidecars only and does not render or publish media.

```bash
python -m video_workflow.cli export-captions caption-exports.json
python -m video_workflow.cli export-captions caption-exports.json --output captions
```

The first command validates without writing. The second writes the SRT files and
`caption-export-receipt.json`, preserving originals and refusing differing existing
outputs. An identical rerun writes nothing. Use a new output directory after a
deliberate edit rather than overwriting approved files.

```json
{
  "schemaVersion": 1,
  "cues": {
    "path": "package/lesson.cues.json",
    "sha256": "EXACT_REVIEWED_CUES_SHA256"
  },
  "outputs": [
    {"id": "part-2", "segments": [{"sourceIn": 60, "sourceOut": 120}]},
    {"id": "combined", "segments": [{"sourceIn": 0, "sourceOut": 120}]},
    {"id": "short", "segments": [
      {"sourceIn": 5, "sourceOut": 16, "speed": 1.1},
      {"sourceIn": 75, "sourceOut": 86, "speed": 1.1}
    ]}
  ]
}
```

Use the existing package's combined cue timeline for **every** source time,
including separate parts. Paths are relative to the export manifest. Cue arrays
contain `startSeconds`, `endSeconds`, `text`, and an optional source `id`.
`sourceIn`/`sourceOut` and optional constant `speed` come from the approved edit
decision list. Each output concatenates ordered, nonoverlapping retained spans.
The renderer must use the same spans and speeds; arbitrary output gaps,
transitions that change duration and variable-speed ramps are not supported by
this exporter. Use the renderer's actual time map for those cases.

The command maps a whole cue as
`outputOffset + (sourceTime - sourceIn) / speed`, rounds to SRT milliseconds,
retains its wording and line breaks, and records input/output hashes, duration,
cue count and segment map. It rejects a boundary intersecting a cue instead of
guessing which words survived. Move the cut to a reviewed speech boundary or
provide a hash-bound, audio-reviewed split-cue source; do not truncate the text
by character count. Cue boundaries themselves are not proof of clean word cuts.

Inspect joins and compare the sidecar against the **final audible render**.
Complete text coverage, non-speech captions, actual speech alignment, pacing and
listening status remain review work. A generated receipt is mechanical evidence,
not editorial or human approval. Pass the resulting SRT and exact render hash to
the existing delivery preflight, then Social Publishing for native action.
