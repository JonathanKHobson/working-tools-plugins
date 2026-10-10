# Ingest Video Assets: Source Index

These are the sources directly used to shape this skill. The plugin-wide registry and policy live in `../../../../research/sources.lock.json`.

- [ffprobe documentation](./ffprobe.md) — invoke-external-tool; Machine-readable stream, format, duration, color and codec inspection.
- [FFmpeg documentation](./ffmpeg.md) — invoke-external-tool; Baseline media probe, decode, filter, encode, mux, loudness, subtitles, transitions and quality checks.
- [Pillow](./pillow.md) — runtime-dependency; Image normalization, title cards, contact sheets, simple animation frames, and text measurement.
- [PyAV](./pyav.md) — optional-integration; Pythonic FFmpeg bindings for frame/packet-level analysis and custom processing.
- [yt-dlp](./yt-dlp.md) — optional-integration; Media acquisition only when the user has rights and the site permits access.
- [browser-use/video-use](./video-use.md) — adapt-ideas-with-attribution; Conversation-driven editing, word-level transcript workflow, EDL, staged FFmpeg render, self-QA.
- [bradautomates/claude-video](./claude-video-watch.md) — adapt-ideas-with-attribution; Video understanding through captions, scene-aware frame extraction, detail budgets, and setup checks.

- [MediaInfo](./mediainfo.md) — optional-integration; Detailed container, stream, codec, color, HDR, timecode and metadata inspection beyond the baseline ffprobe report.
- [ExifTool](./exiftool.md) — invoke-external-tool-no-code-copy; Broad camera, image, audio and video metadata inspection and controlled metadata edits; retain original files and use write operations cautiously.

No third-party source code is vendored in this skill. Ideas adapted from permissively licensed projects remain attributed; unlicensed or incompatible sources are research-only or invoked as external tools.

- [Course recording procedure](../../../edit-dialogue-footage/references/google-vids-course-editing.md) — generalized first-party workflow; private event locators are excluded. Inspect current UI before use.
