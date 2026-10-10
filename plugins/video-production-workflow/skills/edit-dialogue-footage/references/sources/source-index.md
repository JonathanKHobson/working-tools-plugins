# Edit Dialogue Footage: Source Index

These are the sources directly used to shape this skill. The plugin-wide registry and policy live in `../../../../research/sources.lock.json`.

- [browser-use/video-use](./video-use.md) — adapt-ideas-with-attribution; Conversation-driven editing, word-level transcript workflow, EDL, staged FFmpeg render, self-QA.
- [AgriciDaniel/claude-shorts](./claude-shorts.md) — adapt-ideas-with-attribution; Longform-to-shorts pipeline, scoring, word/silence boundary snapping, reframing, captions, export validation.
- [faster-whisper](./faster-whisper.md) — optional-integration; Local Whisper transcription via CTranslate2, including word-level timestamps.
- [WhisperX](./whisperx.md) — optional-integration; Forced alignment and diarization options for more precise word timing.
- [FFmpeg documentation](./ffmpeg.md) — invoke-external-tool; Baseline media probe, decode, filter, encode, mux, loudness, subtitles, transitions and quality checks.
- [bradautomates/claude-video](./claude-video-watch.md) — adapt-ideas-with-attribution; Video understanding through captions, scene-aware frame extraction, detail budgets, and setup checks.
- [W3C captions guidance](./wcag-captions.md) — accessibility-reference; Captions provide synchronized text for speech and meaningful non-speech audio.

No third-party source code is vendored in this skill. Ideas adapted from permissively licensed projects remain attributed; unlicensed or incompatible sources are research-only or invoked as external tools.

- [Course recording procedure](../google-vids-course-editing.md) — generalized first-party workflow; private event locators are excluded. Inspect current UI before use.
