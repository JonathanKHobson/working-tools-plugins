# Analyze Music Pacing: Source Index

These are the sources directly used to shape this skill. The plugin-wide registry and policy live in `../../../../research/sources.lock.json`.

- [librosa](./librosa.md) — runtime-dependency-optional; Beat tracking, onset strength, RMS energy, spectral and temporal music features.
- [Essentia](./essentia.md) — invoke-or-optional-separate-environment; Advanced music descriptors and structure; keep licensing implications explicit.
- [aubio](./aubio.md) — invoke-external-tool-no-code-copy; Low-latency onset, beat, tempo and pitch analysis.
- [pyloudnorm](./pyloudnorm.md) — runtime-dependency-optional; Python implementation of ITU-R BS.1770 loudness measurement and normalization helpers.
- [ITU-R BS.1770](./itu-bs1770.md) — audio-reference; Algorithms for programme loudness and true-peak audio measurement.
- [EBU R 128](./ebu-r128.md) — audio-reference; Broadcast loudness normalization guidance built on BS.1770.
- [FFmpeg documentation](./ffmpeg.md) — invoke-external-tool; Baseline media probe, decode, filter, encode, mux, loudness, subtitles, transitions and quality checks.

No third-party source code is vendored in this skill. Ideas adapted from permissively licensed projects remain attributed; unlicensed or incompatible sources are research-only or invoked as external tools.
