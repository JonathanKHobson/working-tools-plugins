# Create Video Typography: Source Index

These are the sources directly used to shape this skill. The plugin-wide registry and policy live in `../../../../research/sources.lock.json`.

- [W3C captions guidance](./wcag-captions.md) — accessibility-reference; Captions provide synchronized text for speech and meaningful non-speech audio.
- [WCAG contrast guidance](./wcag-contrast.md) — accessibility-reference; Contrast criteria and rationale for readable text; video overlays still require contextual judgment.
- [fontTools](./fonttools.md) — optional-integration; Font metadata, subsetting and variable-font inspection; does not grant font redistribution rights.
- [FFmpeg documentation](./ffmpeg.md) — invoke-external-tool; Baseline media probe, decode, filter, encode, mux, loudness, subtitles, transitions and quality checks.
- [Pillow](./pillow.md) — runtime-dependency; Image normalization, title cards, contact sheets, simple animation frames, and text measurement.
- [DojoCodingLabs/remotion-superpowers](./remotion-superpowers.md) — adapt-ideas-with-attribution; Modular Remotion production rules, audio-first timing, media generation, review and CI rendering patterns.
- [AgriciDaniel/claude-shorts](./claude-shorts.md) — adapt-ideas-with-attribution; Longform-to-shorts pipeline, scoring, word/silence boundary snapping, reframing, captions, export validation.

No third-party source code is vendored in this skill. Ideas adapted from permissively licensed projects remain attributed; unlicensed or incompatible sources are research-only or invoked as external tools.
