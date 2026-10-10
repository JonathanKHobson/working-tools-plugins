---
name: install-video-toolchain
description: Diagnose and establish the local video toolchain needed for a project. Use when binaries, packages, codecs, fonts, GPU support or cross-platform setup block reproducible work.
---

# Install Video Toolchain

## Core principle

Establish a minimal, diagnosed, license-aware production environment and add optional tools only when a project requires them.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Workflow

For a Resolve setup request, use [Edit DaVinci Resolve](../edit-davinci-resolve/SKILL.md)
to check the edition/build and supported route before adding a connector. Its
private editing profile belongs in the owning project; Free 21.1 uses file import
and app controls, while native MCP and Python scripting are Studio capabilities.

1. Run the bundled diagnostic before installing anything.
2. Classify requirements as baseline, project-specific, renderer-specific, acceleration, or cloud/API.
3. Resolve existing FFmpeg/ffprobe binaries before installing duplicates. Check explicit overrides, the plugin-local runtime, and PATH.
4. Install FFmpeg/ffprobe and the plugin Python package as the baseline when no suitable verified runtime exists.
5. Choose one environment strategy: uv/venv/pipx for Python and project-local npm for JavaScript renderers.
6. Verify codec/filter availability rather than assuming every FFmpeg build is equivalent.
7. Install optional analyzers or renderers one at a time and rerun diagnostics.
8. Record versions, license constraints, architecture, GPU runtime, and paths.
9. Run a synthetic smoke render before touching user media.

## Required artifacts

- `toolchain-report.json`
- `install-log.md`
- `environment-lock.md`
- `license-decisions.md`

Create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- Never install every optional dependency by default.
- Never paste API keys into project manifests, logs, source folders, or skill files.
- Do not assume Homebrew commands work on Linux or Windows.
- Do not treat a binary being on PATH as proof required codecs or filters are present.
- Verify Remotion and other custom licenses for the actual organization and use case.

## Technical quick reference

- Baseline: Python 3.10+, FFmpeg, ffprobe, Git, and a readable system font.
- Register non-PATH binaries with `python scripts/configure_runtime.py --ffmpeg <path> --ffprobe <path>`.
- Runtime lookup honors `VIDEO_WORKFLOW_FFMPEG`, `VIDEO_WORKFLOW_FFPROBE`, `.runtime/bin`, and PATH.
- Recommended Python extras: librosa/soundfile/pyloudnorm for music, PySceneDetect/faster-whisper for analysis, OTIO for interchange.
- Use project-local Node dependencies for HyperFrames, Motion Canvas, or Remotion to avoid global version drift.
- Check encoders with `ffmpeg -encoders`, filters with `ffmpeg -filters`, hardware with platform-specific probes.
- Prefer CPU-correctness first; hardware acceleration is an optimization after visual equivalence is tested.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **ingest-video-assets**, **render-video-project**, **validate-video-quality**, **evolve-video-workflow**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Video Producer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
