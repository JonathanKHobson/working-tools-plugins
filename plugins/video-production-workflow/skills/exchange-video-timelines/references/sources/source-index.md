# Exchange Video Timelines: Source Index

These are the sources directly used to shape this skill. The plugin-wide registry and policy live in `../../../../research/sources.lock.json`.

- [OpenTimelineIO](./opentimelineio.md) — optional-integration; Editorial timeline interchange model and adapters; media remains external.
- [ffprobe documentation](./ffprobe.md) — invoke-external-tool; Machine-readable stream, format, duration, color and codec inspection.
- [FFmpeg documentation](./ffmpeg.md) — invoke-external-tool; Baseline media probe, decode, filter, encode, mux, loudness, subtitles, transitions and quality checks.
- [MLT Multimedia Framework](./mlt.md) — optional-integration; Timeline-based multimedia engine used by nonlinear editors; candidate for future adapter.
- [Blender Video Sequence Editor and Python API](./blender.md) — invoke-external-tool-no-code-copy; Heavyweight VSE, compositing, 3D and scripting; keep Blender code/process isolated from permissive plugin code.

No third-party source code is vendored in this skill. Ideas adapted from permissively licensed projects remain attributed; unlicensed or incompatible sources are research-only or invoked as external tools.
