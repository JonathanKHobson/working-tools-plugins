# Video Production Workflow

Current edition **0.4.2** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

An executable video production system by Jonathan Kyle Hobson (Kyle Hobson). Version 0.4.2 is the portable public edition of the maintained workflow: 19 skills, production/review agents, a Python CLI, FFmpeg rendering, measured media QA, caption and timeline operations, synthetic examples, and separately licensed motion method libraries.

## Quick start

Install Python 3.10+ and FFmpeg/ffprobe separately, then from this directory:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install '.[dev]'
video-workflow check
bash scripts/render_example.sh
bash scripts/render_variants.sh
python -m pytest -q
```

If FFmpeg/ffprobe are outside PATH, set `VIDEO_WORKFLOW_FFMPEG` and `VIDEO_WORKFLOW_FFPROBE` to existing executable paths. No private home path or media binary is included. The generated eight-second sample combines synthetic wide, portrait and square images with synthetic tone music, transitions and burned-in captions. Open `examples/music-slideshow/output/preview.mp4` and `contact-sheet.png` after rendering. Automated QA supports inspection; it does not establish visual craft or listening acceptance.

The standalone CLI supports asset inventory/probing, transcript packing and range snapping, storyboard generation, music pacing analysis, rendering, contact sheets/timeline views/waveforms, measured QA, interchange, delivery preflight and hash-bound caption/provenance exports. Run `video-workflow --help` and consult the [operating guide](docs/OPERATING_GUIDE.md) and [manifest reference](docs/MANIFEST_REFERENCE.md).

## Agent installation

The root `plugin.json` declares portable identity. Native descriptors are retained in `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`; both discover `skills/`. Add this directory using the current host's native plugin manager. Version 0.4.1 passed native Codex and Claude marketplace installation and installed-file parity on 2026-10-10. This verifies installation, not native editor control or every optional provider. No private marketplace or MCP connection is modified by this package.

Start with `plan-video-production`, then select the smallest owner for ingest, analysis, storyboard, slideshow/dialogue editing, Resolve, typography, motion, audio, rendering, interchange, conform and quality validation. `evolve-video-workflow` maintains the system. The [project map](docs/project-map.md) explains the boundaries.

## Rights and boundaries

Original code is AGPL-3.0-only; original methods and creative fixtures are CC BY-SA 4.0, copyright Jonathan Kyle Hobson. Separately licensed retained method libraries keep their own MIT or Apache-2.0 licenses, copyright notices and provenance. See [third-party notices](THIRD_PARTY_NOTICES.md) and [distribution provenance](PUBLIC_DISTRIBUTION.md). Upstream library procedures are conditional source material; their optional tools/providers are not installed or automatically invoked.

Specialized renderer adapters and external studio integrations retain explicit setup requirements. The core FFmpeg workflow works independently. Review [optional integrations](docs/OPTIONAL_INTEGRATIONS.md) before choosing a provider, font, model, browser renderer or native editing tool. There is no upload/publishing adapter.

## Review packets and walkthrough scripts

Two full first-party standalone methods are now included: [Loom Review Packet](skills/loom-review-packet/SKILL.md) and [Loom Walkthrough Scripting](skills/loom-walkthrough-scripting/SKILL.md).

The packet helper extracts transcript timestamps, sorts a recipient cue CSV, copies supplied screenshots or captures video frames with separately installed FFmpeg, preserves raw input and writes an explicit complete/partial manifest plus linked feedback. It never downloads a Loom or sends feedback. Walkthrough scripting retains the full spoken-route, evidence-state and recording-readiness procedures, with a full fictional replacement for its private client case. Actual recordings, Figma access, stakeholder notes and authenticated browsers remain recipient inputs.

Run `python examples/loom-review-synthetic.py --output /your/new/sample-folder` for a real synthetic packet. Add `--capture` to exercise local FFmpeg frame capture. The helper refuses an existing packet output, and tests cover invalid timestamps, missing frames, explicit partial staging, input preservation and complete packet hashes. Fictional fixtures are not real UX observation or delivered stakeholder feedback.
