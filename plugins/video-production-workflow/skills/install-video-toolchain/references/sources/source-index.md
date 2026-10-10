# Install Video Toolchain: Source Index

These are the sources directly used to shape this skill. The plugin-wide registry and policy live in `../../../../research/sources.lock.json`.

- [FFmpeg documentation](./ffmpeg.md) — invoke-external-tool; Baseline media probe, decode, filter, encode, mux, loudness, subtitles, transitions and quality checks.
- [ffprobe documentation](./ffprobe.md) — invoke-external-tool; Machine-readable stream, format, duration, color and codec inspection.
- [librosa](./librosa.md) — runtime-dependency-optional; Beat tracking, onset strength, RMS energy, spectral and temporal music features.
- [pyloudnorm](./pyloudnorm.md) — runtime-dependency-optional; Python implementation of ITU-R BS.1770 loudness measurement and normalization helpers.
- [PySceneDetect](./pyscenedetect.md) — optional-integration; Shot-change detection, scene lists, splitting and CLI workflows.
- [faster-whisper](./faster-whisper.md) — optional-integration; Local Whisper transcription via CTranslate2, including word-level timestamps.
- [OpenTimelineIO](./opentimelineio.md) — optional-integration; Editorial timeline interchange model and adapters; media remains external.
- [Remotion](./remotion.md) — optional-integration-only; React-based programmatic video renderer. Verify current commercial license before adoption.
- [HyperFrames](./hyperframes.md) — optional-integration; HTML/CSS/JavaScript frame-accurate renderer suited to UI motion and kinetic typography.

- [MediaInfo](./mediainfo.md) — optional-integration; Detailed container, stream, codec, color, HDR, timecode and metadata inspection beyond the baseline ffprobe report.
- [ExifTool](./exiftool.md) — invoke-external-tool-no-code-copy; Broad camera, image, audio and video metadata inspection and controlled metadata edits; retain original files and use write operations cautiously.
- [Netflix VMAF](./vmaf.md) — optional-integration; Full-reference perceptual video quality metric for comparing encodes or delivery variants when a trusted reference master exists.
- [Shaka Packager](./shaka-packager.md) — optional-integration; DASH and HLS packaging, encryption and manifest generation after editorial mastering; not a creative renderer.

- [MediaConch](./mediaconch.md) — invoke-external-tool; Policy and implementation conformance checking for audiovisual containers; verify current package/component licensing before redistribution.
- [QCTools](./qctools.md) — invoke-external-tool-no-code-copy; Signal-level plots, waveform/vectorscope views, broadcast-range and temporal artifact analysis for difficult masters and archival QC.

No third-party source code is vendored in this skill. Ideas adapted from permissively licensed projects remain attributed; unlicensed or incompatible sources are research-only or invoked as external tools.
