# Install Video Toolchain: Detailed Workflow

## Preflight

Confirm the project root, output location, source immutability, tool availability, current manifest, and whether prior analysis can be reused by hash. Define a bounded deliverable and a validation plan before execution.

## Execution sequence

1. Run the bundled diagnostic before installing anything.
2. Classify requirements as baseline, project-specific, renderer-specific, acceleration, or cloud/API.
3. Install FFmpeg/ffprobe and the plugin Python package as the baseline.
4. Choose one environment strategy: uv/venv/pipx for Python and project-local npm for JavaScript renderers.
5. Verify codec/filter availability rather than assuming every FFmpeg build is equivalent.
6. Install optional analyzers or renderers one at a time and rerun diagnostics.
7. Record versions, license constraints, architecture, GPU runtime, and paths.
8. Run a synthetic smoke render before touching user media.

## Checkpoints

- **Intent checkpoint:** the approved strategy and acceptance criteria are explicit.
- **Evidence checkpoint:** source and analysis data exist and match current hashes.
- **Draft checkpoint:** a low-cost, target-aspect artifact is inspectable.
- **Technical checkpoint:** schema, timing, stream, and file assertions pass.
- **Review checkpoint:** an independent reviewer inspects actual outputs.
- **Handoff checkpoint:** downstream skill, exceptions, and reversible choices are documented.

## Change discipline

A revision should change the highest-level artifact that expresses the feedback. Change the brief for strategy, storyboard for shot design, manifest for timing/layout, an isolated slot for animation, audio map for mix, and delivery matrix for export. Avoid patching a rendered MP4 when the editable source of truth exists.

## Recovery

On failure, preserve logs and intermediates. Identify whether the root cause is input, manifest, dependency, analysis, editorial choice, renderer, encoder, or QA threshold. Reproduce with the smallest fixture, add a regression test, and rerun only invalidated cache stages.
