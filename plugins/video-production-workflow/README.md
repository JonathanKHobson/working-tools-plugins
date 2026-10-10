# Video Production Studio

Current edition **0.4.3** uses the [scoped licensing model](LICENSING.md): first-party code AGPL-3.0-only and first-party documentation, prompts, skills and methods CC BY-SA 4.0. Retained upstream grants and prior release permissions remain in force. The canonical owner and public package maintain the same distributable implementation; private source media, host bindings and generated receipts stay outside that payload.

A production workflow that turns source footage, slides, images, audio, or a brief into a reviewable edit and verified video files. Bring the source media, audience, story or teaching goal, must-keep material, target duration/aspect ratio, and delivery destination. Start at the stage the project actually needs.

Try a first request:

- “Turn these interview clips and transcript into a 60-second vertical short with accurate captions.” Result: a selected edit, rendered preview, caption review, and delivery files after QA.
- “Make a paced photo montage from these images and this licensed song, keeping the final phrase intact.” Result: a music-aware timeline and rendered video with audio and visual checks.
- “Review this finished lesson video and prepare YouTube and vertical variants.” Result: a QA report and exact, hash-bound files that meet the current delivery requirements.
- “Finish this reviewed rough cut in DaVinci Resolve Free and give me an editable project.” Result: a checked timeline import, native finishing, saved project readback and reviewed render. [Resolve editing](skills/edit-davinci-resolve/SKILL.md) checks the installed edition; Free 21.1 uses file import and app controls. Native MCP requires supported Studio.

For an unclear or new project, start with [plan-video-production](skills/plan-video-production/SKILL.md). For a known stage, use the [task-to-skill map](docs/use-case-map.md) to go straight to ingest, editing, motion, audio, render, or delivery. A capabilities/getting-started answer should orient to the user's input and desired output, then carry out the selected task. This README is a human guide and is not automatically loaded into AI context. The workflow bundles no MCP server; media tools and optional renderers are local dependencies checked for the job.

The project manifest is the editable contract. FFmpeg is the baseline renderer, while optional engines remain isolated adapters. The plugin preserves source media, supports phrase-reviewed music excerpts, measures text against asymmetric platform-safe areas, audits reading time and source reuse, and requires rendered-output QA.

## Local toolchain setup

```bash
python3 scripts/check_environment.py
python3 scripts/configure_runtime.py --ffmpeg /path/to/ffmpeg --ffprobe /path/to/ffprobe
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/video-workflow check
```

Run `video-workflow audit-project project.json` before rendering. Run `python scripts/verify_release.py` with the declared development dependencies and FFmpeg available for the complete plugin release gate. [Optional integration requirements](docs/OPTIONAL_INTEGRATIONS.md) are separate from the core methods.

For finished lesson, workshop and Short handoffs, run the read-only
`video-workflow preflight-delivery work/delivery.json`. The
[delivery contract](skills/conform-video-delivery/references/delivery-preflight.md)
checks final files and current review hashes in one batch; native publishing
remains with Social Content Studio. See the
[efficiency audit](docs/evolution/efficiency-audit.md) for applied learnings and limits.

See [the operating guide](docs/OPERATING_GUIDE.md) for production use, [the plugin map](PLUGIN_MAP.md) for routing, and the [efficiency audit](docs/evolution/efficiency-audit.md) for dated source-learning limits. Historical project and evaluation records remain in the author's private archive.

## Procedural video styles and storyboards

Ask “Show me video styles,” “Storyboard this explanation in cut paper,” or “Build a deterministic JavaScript motion example.” When separately installed and verified, Video Templates can offer pinned Animate source styles with previews and license/source status. A Use request prepares a handoff; a separately available drawing widget can handle sketchable panels. Choosing a style does not render a video or approve a script.

The style chooser and storyboard editor are separately installed Video Templates capabilities. This package includes only an optional [compatibility launcher](scripts/video_style_library_mcp.py); it requires a recipient-selected Video Templates root or binding and is never auto-registered. Without that provider, continue with the included [storyboard method](skills/design-video-storyboards/SKILL.md) and supplied style references; do not claim catalog search, a created board or a rendered widget. See the [optional integration guide](docs/OPTIONAL_INTEGRATIONS.md) and [runnable canvas example](examples/deterministic-canvas/README.md). A fresh host connection may be needed after a separately authorized provider installation.


### Storyboard together or delegate it

With a separately verified storyboard backend, Video Studio can turn an idea into populated shot cards for collaboration or continue through a reviewed autonomous handoff. The external editor may support visual action, narration, duration, reordering, sketches and per-shot references; inspect its actual current controls and save/readback behavior. Without that backend, prepare the shot list and reviewable storyboard locally from supplied evidence. See [the participation workflow](skills/design-video-storyboards/references/video-style-discovery.md#shared-storyboarding-collaborative-or-autonomous).

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->

Original motion production starts with a concrete visual direction: expressive typography and photography/imagery, composition through time, purposeful movement and a justified spatial technique. A representative preview tests the direction before expansion; technical QA alone does not certify craft. See the [art-directed motion method](skills/create-motion-graphics/references/art-directed-motion.md). Routine approved edits reuse their existing direction.

For style selection, compare treatments using the same content and format; retain accepted frames and a playable excerpt in the existing project style record. That record, not a palette-only preset, carries the selected visual language into later work.
