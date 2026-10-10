# Compose Slideshow Video: Source Index

These are the sources directly used to shape this skill. The plugin-wide registry and policy live in `../../../../research/sources.lock.json`.

- [FFmpeg documentation](./ffmpeg.md) — invoke-external-tool; Baseline media probe, decode, filter, encode, mux, loudness, subtitles, transitions and quality checks.
- [MoviePy](./moviepy.md) — optional-integration; Python composition convenience layer; prefer FFmpeg for fragile, high-volume, or codec-sensitive stages.
- [Editly](./editly.md) — research-and-optional-integration; Declarative JSON/JavaScript video editing patterns and transitions.
- [librosa](./librosa.md) — runtime-dependency-optional; Beat tracking, onset strength, RMS energy, spectral and temporal music features.
- [MediaPipe Tasks Vision](./mediapipe.md) — optional-integration; Face and object detection for subject-aware reframing and crop suggestions.
- [Pillow](./pillow.md) — runtime-dependency; Image normalization, title cards, contact sheets, simple animation frames, and text measurement.
- [browser-use/video-use](./video-use.md) — adapt-ideas-with-attribution; Conversation-driven editing, word-level transcript workflow, EDL, staged FFmpeg render, self-QA.

No third-party source code is vendored in this skill. Ideas adapted from permissively licensed projects remain attributed; unlicensed or incompatible sources are research-only or invoked as external tools.
