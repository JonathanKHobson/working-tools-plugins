# Video Production Studio — Agent Operating Instructions

## Start here

1. Read the user’s full request and existing project conversation.
2. Inspect the project directory and current manifest before creating new files.
3. Route to the smallest owning skill under `skills/`.
4. Preserve source media; work under project-specific `work/`, `cache/`, and `output/` paths.
5. Use the manifest as the editorial contract and the shared CLI for deterministic operations.
6. Validate actual rendered output before completion.

## Canonical commands

```bash
python -m video_workflow.cli check
python -m video_workflow.cli inventory <paths...> --output asset-manifest.json
python -m video_workflow.cli probe input.mov --output probe.json
python -m video_workflow.cli analyze-music music.wav --output music-analysis.json
python -m video_workflow.cli pack-transcript transcript.json --output packed.json
python -m video_workflow.cli snap-ranges ranges.json transcript.json --output snapped.json
python -m video_workflow.cli storyboard project.json --output storyboard.md
python -m video_workflow.cli render project.json --output output/preview.mp4
python -m video_workflow.cli contact-sheet output/preview.mp4 --output output/contact-sheet.png
python -m video_workflow.cli timeline-view output/preview.mp4 --start 12 --end 16 --output output/cut-12.png
python -m video_workflow.cli qa output/preview.mp4 --output output/qa-report.json
python -m video_workflow.cli preflight-delivery work/delivery.json
python -m video_workflow.cli export-captions work/caption-exports.json --output output/captions
```

## Review gates

- Strategy is approved before expensive work.
- Draft is rendered at target aspect ratio.
- Every cut/transition and dense text region is inspectable.
- Audio is normally listened to and measured. Honor explicit quiet-testing requests: preserve output audio, keep test playback muted, measure silently and disclose that listening review was not performed.
- Captions and accessibility are reviewed.
- Final delivery is bound to exact hash and QA evidence.

## Plugin development

Use `evolve-video-workflow` before changing plugin boundaries. Add failing scenarios/tests first. Run:

```bash
python scripts/validate_plugin.py
pytest -q
python scripts/verify_release.py
```

## Original motion production

For original motion or material visual redesign, use `create-motion-graphics/references/art-directed-motion.md` by default. Establish a concrete visual identity, integrate typography and photography/imagery, justify spatial technique and inspect a representative rendered passage before expanding an unresolved direction. Technical validity alone does not establish art direction. Reuse approved direction for routine edits.
