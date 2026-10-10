# Install Video Toolchain: Technical Reference

## Domain-specific notes

- Baseline: Python 3.10+, FFmpeg, ffprobe, Git, and a readable system font.
- Recommended Python extras: librosa/soundfile/pyloudnorm for music, PySceneDetect/faster-whisper for analysis, OTIO for interchange.
- Use project-local Node dependencies for HyperFrames, Motion Canvas, or Remotion to avoid global version drift.
- Check encoders with `ffmpeg -encoders`, filters with `ffmpeg -filters`, hardware with platform-specific probes.
- Prefer CPU-correctness first; hardware acceleration is an optimization after visual equivalence is tested.

## Shared project layout

```text
project/
├── source/          # untouched originals or immutable references
├── work/            # editable manifests, proxies, analyses, slots
├── cache/           # hash-keyed reusable artifacts
├── output/          # drafts, masters, variants, QA
├── project.json     # renderer-neutral editorial contract
├── provenance.json  # rights, hashes, lineage, tool/model versions
└── project.md       # session decisions and unresolved items
```

## Timing conventions

- Store seconds as floating-point values in the manifest and rational frame rate in delivery metadata.
- Derive frame indices at renderer boundaries; define rounding policy.
- Timeline item output end is `start + duration`.
- Transition overlap reduces cumulative output time.
- Source timestamps and output timestamps are different coordinate systems; never substitute one for the other.

## Cache key

Use a digest of source hash, relevant manifest fragment, script version, tool version, and analysis/render settings. Do not invalidate an expensive transcript because an unrelated title color changed.

## Command safety

Build subprocess argument arrays rather than shell-concatenated user input. Quote/filter-escape paths separately from shell escaping. Write logs with redacted secrets. Run in a project work directory and fail on nonzero commands.
