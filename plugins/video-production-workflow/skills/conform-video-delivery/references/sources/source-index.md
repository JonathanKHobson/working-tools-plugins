# Conform Video Delivery: Source Index

These are the sources directly used to shape this skill. The plugin-wide registry and policy live in `../../../../research/sources.lock.json`.

- [YouTube recommended upload encoding settings](./youtube-upload.md) — delivery-reference-reverify; Container, codec, frame rate, aspect ratio and audio recommendations; recheck before final delivery.
- [YouTube aspect ratio guidance](./youtube-aspect.md) — delivery-reference-reverify; Player adaptation and native aspect-ratio guidance.
- [TikTok business video specifications](./tiktok-specs.md) — delivery-reference-reverify; Official advertising specs used as a cautious technical proxy; organic product UI may differ.
- [Meta Reels creative and technical guidance](./meta-reels.md) — delivery-reference-reverify; Reels aspect, media and creative guidance; user-interface overlays change over time.
- [LinkedIn video specifications](./linkedin-video.md) — delivery-reference-reverify; Supported video formats and constraints; recheck before export.
- [FFmpeg documentation](./ffmpeg.md) — invoke-external-tool; Baseline media probe, decode, filter, encode, mux, loudness, subtitles, transitions and quality checks.
- [ffprobe documentation](./ffprobe.md) — invoke-external-tool; Machine-readable stream, format, duration, color and codec inspection.
- [W3C captions guidance](./wcag-captions.md) — accessibility-reference; Captions provide synchronized text for speech and meaningful non-speech audio.

- [MediaInfo](./mediainfo.md) — optional-integration; Detailed container, stream, codec, color, HDR, timecode and metadata inspection beyond the baseline ffprobe report.
- [Shaka Packager](./shaka-packager.md) — optional-integration; DASH and HLS packaging, encryption and manifest generation after editorial mastering; not a creative renderer.
- [Netflix VMAF](./vmaf.md) — optional-integration; Full-reference perceptual video quality metric for comparing encodes or delivery variants when a trusted reference master exists.

No third-party source code is vendored in this skill. Ideas adapted from permissively licensed projects remain attributed; unlicensed or incompatible sources are research-only or invoked as external tools.
