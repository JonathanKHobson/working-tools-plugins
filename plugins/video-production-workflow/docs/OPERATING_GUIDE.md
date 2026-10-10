# Operating Guide

## Start a project

```bash
python -m video_workflow.cli new project.json --id my-video --preset landscape-1080
python -m video_workflow.cli inventory source/ --output work/asset-manifest.json
python -m video_workflow.cli check --output work/toolchain-report.json
```

If FFmpeg is available but not on PATH, register it without changing the system:

```bash
python scripts/configure_runtime.py --ffmpeg /path/to/ffmpeg --ffprobe /path/to/ffprobe
```

Fill the brief, assets, delivery targets, timeline, audio, captions, provenance, and QA expectations. Use `plan-video-production`, `ingest-video-assets`, and the relevant analysis skills before rendering.

## Build an evaluable draft

1. Generate/update storyboard and manifest.
2. Run `video-workflow audit-project project.json`.
3. Render at target aspect ratio with a fast preset.
4. Generate contact sheet, timeline views, waveform, and QA report.
5. Watch the draft and record timestamped feedback.
6. Revise the highest-level source of truth that represents the feedback.

## Recover from failure

Keep the error log and intermediate files. Check inputs → manifest → dependency → analysis → segment render → transition/composite → audio → captions → encode → QA. Reproduce with the smallest fixture. Add a regression test. Delete or invalidate only the cache stage affected by the fix.

## Finalize

Render a high-quality master, run full QA, perform a complete watch-through, then conform platform variants from the validated master. Recheck machine-readable elements from compressed frames. Package manifest, source/provenance map, captions, audio stems, relevant project code, QA report, and checksums.

Before a lesson, Short or workshop publishing handoff, run the read-only shared CLI
`preflight-delivery` with the existing project's delivery record. Use the
[conditional contract](../skills/conform-video-delivery/references/delivery-preflight.md)
for file roles and review hash bindings. Correct only missing/invalidated stages;
local readiness and platform-saved state remain separate evidence.
