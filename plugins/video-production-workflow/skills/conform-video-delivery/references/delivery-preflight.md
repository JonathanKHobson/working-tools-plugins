# Batch delivery preflight

Use after preparing final lesson, workshop or Short media, before handing it to
Social Publishing or another delivery adapter. Run from the plugin root:

```bash
python -m video_workflow.cli preflight-delivery /absolute/project/work/delivery.json
```

This command reads local files and prints deterministic JSON. It never edits,
renders, generates art, uploads, schedules, or publishes. Exit codes: `0` means
local checks and review attestations are current; `2` means outstanding work;
`1` means the manifest cannot be read or has a malformed top-level contract.
Inspect `items[].nextActions` and reuse the unaffected artifacts instead of
starting the entire job again. Keep the manifest in the media project's existing
work directory; its IDs are local delivery IDs, not platform account identities.

## Input contract

Root: `schemaVersion: 1`, nonempty `items` array. Each item has unique nonblank
`id`, `format` (`portrait` or `landscape`), `files` and optional `reviews`.
The four required file roles are `render`, `captions`, `transcript`, `cover`.
Optional `courseCard` is a separate square image, never a replacement for a cover.

Each file record requires `path` and expected lowercase `sha256`. Paths resolve
relative to the manifest; explicit absolute local paths are also accepted. Missing
files and hash mismatches are aggregated across the batch. Caption and transcript
records also require `renderSha256` matching the actual final render. Reuse source
transcripts to select clips, then provide the transcript of the delivered edit.

Optional explicit constraints:

- `width`, `height`, `minWidth`, `minHeight`: positive integers in pixels.
- `durationSeconds`: positive finite number, checked against ffprobe within 250ms.
- `maxBytes`: positive integer from the verified recipient limit.
- `aspectRatio`: two positive integers, checked with 1% relative tolerance.
- `requireAudio`: boolean on the render record; `true` checks for an audio stream.

The chosen media composition defaults to 9:16 for portrait or 16:9 for landscape;
`courseCard` defaults to 1:1. These are project design targets, not assertions
about universal platform eligibility. Override `aspectRatio` per variant when
the approved target differs. No current upload-size or minimum-pixel limit is
hardcoded. ffprobe measures the actual video; Pillow checks decoded image size
after EXIF orientation. Unsupported file constraint fields are reported, so a
misspelled limit cannot be silently ignored.

```json
{
  "schemaVersion": 1,
  "items": [{
    "id": "lesson-short-01",
    "format": "portrait",
    "files": {
      "render": {
        "path": "../output/short-01.mp4",
        "sha256": "ACTUAL_RENDER_SHA256",
        "width": 1080, "height": 1920, "durationSeconds": 42.5,
        "requireAudio": true
      },
      "captions": {
        "path": "../output/short-01.srt",
        "sha256": "ACTUAL_CAPTION_SHA256",
        "renderSha256": "ACTUAL_RENDER_SHA256"
      },
      "transcript": {
        "path": "../output/short-01.txt",
        "sha256": "ACTUAL_TRANSCRIPT_SHA256",
        "renderSha256": "ACTUAL_RENDER_SHA256"
      },
      "cover": {
        "path": "../output/short-01-cover.jpg",
        "sha256": "ACTUAL_COVER_SHA256"
      }
    },
    "reviews": {
      "visual": {"status": "pending"},
      "audio": {"status": "not-performed"},
      "captions": {"status": "pending"},
      "transcript": {"status": "pending"},
      "cover": {"status": "held"}
    }
  }]
}
```

The placeholders must be replaced by real hashes; the helper never stamps an
approval onto freshly observed bytes. A completed review attestation is:

```json
{
  "status": "passed",
  "evidence": "output/reviews/short-01-visual.md; anchors V1-V5 reviewed",
  "hashes": {"render": "EXACT_REVIEWED_RENDER_SHA256"}
}
```

Required review hash bindings: `visual` and `audio` → render;
`captions` → render + captions; `transcript` → render + transcript;
`cover` → cover + courseCard if supplied. Extra hashes must also match.
Retain pending, held or not-performed reviews honestly. An artifact replacement
invalidates only its dependent reviews. A corrected expected file hash does not
make an old review fresh. `evidence` is a human-supplied locator/explanation, not
a receipt whose contents this command authenticates.

## Output and limitations

`filesPassed` reports file, hash, dimensions, declared-limit and text/render-binding
checks. `localHandoffReady` additionally requires all five current review
attestations. `fresh-attestation` means hashes match; it does not prove a person
watched or listened, check caption wording/timing against speech, validate native
thumbnail crops, or certify a saved upload. UTF-8 caption and transcript files
are checked for nonempty text; use existing caption/package tools and actual
render review for cue structure, completeness and alignment.

The report includes actual paths, hashes, bytes, decoded dimensions, probed
duration, issues and outstanding actions. Share only the needed per-item result
with delegates. Hashes/probes are reused within one invocation, with stat checks
for files changing during the batch; no persistent probe cache is trusted.

Pass exact delivery hashes, complete captions/transcript and art roles to
`social-content-studio:social-publishing`. It owns platform IDs, account eligibility,
copy review, playlist/card destination, schedule and saved-state readback. Its
YouTube catalog packaging reference owns asynchronous Save and native crop
recovery; this preflight is not a replacement for those procedures.
