# Validate Video Quality: Source Index

These are the sources directly used to shape this skill. The plugin-wide registry and policy live in `../../../../research/sources.lock.json`.

- [ffprobe documentation](./ffprobe.md) — invoke-external-tool; Machine-readable stream, format, duration, color and codec inspection.
- [FFmpeg documentation](./ffmpeg.md) — invoke-external-tool; Baseline media probe, decode, filter, encode, mux, loudness, subtitles, transitions and quality checks.
- [browser-use/video-use](./video-use.md) — adapt-ideas-with-attribution; Conversation-driven editing, word-level transcript workflow, EDL, staged FFmpeg render, self-QA.
- [W3C captions guidance](./wcag-captions.md) — accessibility-reference; Captions provide synchronized text for speech and meaningful non-speech audio.
- [WCAG contrast guidance](./wcag-contrast.md) — accessibility-reference; Contrast criteria and rationale for readable text; video overlays still require contextual judgment.
- [ITU-R BS.1770](./itu-bs1770.md) — audio-reference; Algorithms for programme loudness and true-peak audio measurement.
- [EBU R 128](./ebu-r128.md) — audio-reference; Broadcast loudness normalization guidance built on BS.1770.
- [AgriciDaniel/claude-shorts](./claude-shorts.md) — adapt-ideas-with-attribution; Longform-to-shorts pipeline, scoring, word/silence boundary snapping, reframing, captions, export validation.

- [MediaInfo](./mediainfo.md) — optional-integration; Detailed container, stream, codec, color, HDR, timecode and metadata inspection beyond the baseline ffprobe report.
- [Netflix VMAF](./vmaf.md) — optional-integration; Full-reference perceptual video quality metric for comparing encodes or delivery variants when a trusted reference master exists.

- [MediaConch](./mediaconch.md) — invoke-external-tool; Policy and implementation conformance checking for audiovisual containers; verify current package/component licensing before redistribution.
- [QCTools](./qctools.md) — invoke-external-tool-no-code-copy; Signal-level plots, waveform/vectorscope views, broadcast-range and temporal artifact analysis for difficult masters and archival QC.

No third-party source code is vendored in this skill. Ideas adapted from permissively licensed projects remain attributed; unlicensed or incompatible sources are research-only or invoked as external tools.

- [Course recording procedure](../../../edit-dialogue-footage/references/google-vids-course-editing.md) — generalized first-party workflow; private event locators are excluded. Inspect current UI before use.
