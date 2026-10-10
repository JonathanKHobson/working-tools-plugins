# Trim a recording and replace it without changing its Drive link

Use for a bounded opening/end trim of an existing Google Drive recording. Keep editorial redesign, publishing to other destinations and course changes outside this flow unless requested.

## Acquire and define the cut

- Record the existing Drive file ID, title, sharing state, requested start/end and source hash. Prefer the connector; if its account lacks access, use an already authorized, signed-in browser through the supported browser tools. Do not change sharing just to acquire the file.
- Preserve an unchanged local original in the owning project's private media workspace. An exported transcript can have a different clock from the video: the user's specified video timestamp is the cut contract. If ambiguous, resolve the timebase before replacing anything.
- Probe all streams, not just video: dimensions, frame rate, codecs, duration, audio channels/rate and embedded captions. Use existing FFmpeg/ffprobe installations.
- For browser downloads, register the supported download event on the tab that actually starts the download. Drive may open its large-file confirmation in a separate tab. Inspect that new tab; capture the download there. Do not mistake a click, timeout or blocked page for a downloaded file or bypass browser security protections.

## Trim without unnecessary quality loss

A stream-copy candidate is appropriate for a simple temporal trim when the target player honors MP4 edit lists. It is not automatically frame-accurate: inspect the first decoded frame against the requested source position and verify timestamps and sync. If that fails, use an accurate re-encode of the affected range or whole output as appropriate; do not silently move the requested cut to a convenient keyframe.

Avoid blindly copying embedded subtitle streams. A trim can leave incorrect subtitle timestamps or a container longer than the retained audio/video even when FFmpeg exits successfully. Extract source cues, retime them explicitly, then remux:

- `new_start = max(0, source_start - trim_start)`
- `new_end = min(output_duration, source_end - trim_start)`
- Discard cues ending at/before zero, starting at/after the output end, or having nonpositive duration. Preserve the text and speaker labels; reindex cues. Keep the original caption source.
- Copy verified video/audio where appropriate; encode the shifted subtitle input to the destination's supported caption codec. Compare each stream duration and the container duration after muxing, plus the first and last cues.

A mux pattern after preparing correctly shifted SRT cues is `ffmpeg -ss START -i ORIGINAL -i SHIFTED_SRT -map 0:v:0 -map 0:a:0 -map 1:0 -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=eng -movflags +faststart OUTPUT.mp4`. Adapt mappings to actual streams; do not use this for files without the selected streams. Build argument arrays and preserve existing outputs on reruns.

## Verify before replacement

Check duration against the retained range, inspect the opening/cut boundary, a representative middle and ending frame, and decode the retained audio/video to catch errors. For stream copies, compare retained compressed packet hashes to source and verify the first decoded frame. Packet identity proves preserved encoded data, not player sync or a listening review. Keep the exact final hash and a concise QA receipt with observed limits. Retain the existing ending unless the user requested an end trim.

If the user requests quiet testing, mute the test player before starting it or use silent frame/decoder/signal inspection. Preserve the output audio track. Do not mute the whole computer or other applications. Report any unperformed listening or full-duration watch-through rather than claiming it passed. An explicit quiet-testing instruction takes precedence over the normal listen-through recommendation.

## Replace the existing Drive version

Replacement requires user authorization; a local-edit request alone is not an upload request. Through the supported Drive API or UI, target the existing file ID. In the UI, inspect the current controls; File information → Manage versions → Upload new version is a known route, not a guaranteed permanent label. Use the supported file-chooser flow. Do not upload a separate file, delete/recreate the original, rename an unrelated item or change sharing to preserve a link.

Verify the edited file is listed as current and the original remains in version history. Keep the local original regardless of Drive's revision-retention policy. Reopen the original URL and independently download the current bytes; compare SHA256 with the reviewed output. Check the name, file identity and access have not unexpectedly changed.

Distinguish **upload completed**, **download integrity verified**, **preview processing**, and **playback verified**. Processing can continue after the correct bytes are available. Do not claim playback success from an upload receipt. Once playback is ready, check the new opening, runtime and caption alignment in a muted player when requested. If Drive has separate caption tracks or chapters, inspect whether they still refer to the old timeline; correct only the affected timing within the authorized edit, or report the unresolved mismatch. Do not assume embedded captions update every external track.

Save a small version receipt/screenshot in the project evidence location. Close only task-owned tabs, preserving the user's normal browsing and media playback. Keep source IDs, participant recordings and project-specific timestamps out of reusable plugin examples.
