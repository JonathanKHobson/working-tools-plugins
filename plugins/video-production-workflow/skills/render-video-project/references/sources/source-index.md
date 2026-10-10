# Render Video Project: Source Index

These are the sources directly used to shape this skill. The plugin-wide registry and policy live in `../../../../research/sources.lock.json`.

- [FFmpeg documentation](./ffmpeg.md) — invoke-external-tool; Baseline media probe, decode, filter, encode, mux, loudness, subtitles, transitions and quality checks.
- [ffprobe documentation](./ffprobe.md) — invoke-external-tool; Machine-readable stream, format, duration, color and codec inspection.
- [browser-use/video-use](./video-use.md) — adapt-ideas-with-attribution; Conversation-driven editing, word-level transcript workflow, EDL, staged FFmpeg render, self-QA.
- [MoviePy](./moviepy.md) — optional-integration; Python composition convenience layer; prefer FFmpeg for fragile, high-volume, or codec-sensitive stages.
- [PyAV](./pyav.md) — optional-integration; Pythonic FFmpeg bindings for frame/packet-level analysis and custom processing.
- [Remotion](./remotion.md) — optional-integration-only; React-based programmatic video renderer. Verify current commercial license before adoption.
- [HyperFrames](./hyperframes.md) — optional-integration; HTML/CSS/JavaScript frame-accurate renderer suited to UI motion and kinetic typography.
- [Editly](./editly.md) — research-and-optional-integration; Declarative JSON/JavaScript video editing patterns and transitions.

No third-party source code is vendored in this skill. Ideas adapted from permissively licensed projects remain attributed; unlicensed or incompatible sources are research-only or invoked as external tools.
