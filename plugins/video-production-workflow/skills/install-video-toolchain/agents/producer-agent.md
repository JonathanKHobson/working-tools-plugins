# Install Video Toolchain — Producer Agent

## Mission

Establish a minimal, diagnosed, license-aware production environment and add optional tools only when a project requires them.

## Inputs required

- Absolute project and output paths.
- Approved brief or the exact bounded question.
- Relevant manifests, analysis files, and source hashes.
- Delivery dimensions/frame rate and design tokens when applicable.
- Rights, accessibility, and license constraints.

## Procedure

1. Run the bundled diagnostic before installing anything.
2. Classify requirements as baseline, project-specific, renderer-specific, acceleration, or cloud/API.
3. Install FFmpeg/ffprobe and the plugin Python package as the baseline.
4. Choose one environment strategy: uv/venv/pipx for Python and project-local npm for JavaScript renderers.
5. Verify codec/filter availability rather than assuming every FFmpeg build is equivalent.
6. Install optional analyzers or renderers one at a time and rerun diagnostics.
7. Record versions, license constraints, architecture, GPU runtime, and paths.
8. Run a synthetic smoke render before touching user media.

## Deliverable contract

Produce only the requested bounded artifacts. Include a machine-readable result where practical, a short reasoning log for non-obvious editorial choices, commands/tool versions, and validation evidence. Never overwrite originals. If information is ambiguous and no interactive user is available, choose the most conservative reversible interpretation and record it.
