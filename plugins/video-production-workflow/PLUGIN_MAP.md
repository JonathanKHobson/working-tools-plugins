# Plugin Map

| Stage | Owning skill |
|---|---|
| Brief, intent, acceptance | `plan-video-production` |
| Generated footage or Sora-era clip planning | `plan-video-production` → `references/generated-clip-planning.md`; existing clips continue through ingest and QA |
| Adapt a reference video into an original editable piece | `plan-video-production` → `references/reference-led-adaptation.md` |
| Environment | `install-video-toolchain` |
| Sources, hashes, proxies, rights | `ingest-video-assets` |
| Transcript, scenes, frames, subjects | `analyze-video-content` |
| Beats, energy, phrases, loudness | `analyze-music-pacing` |
| Beat sheet, storyboard, design system | `design-video-storyboards` |
| Photos/cards/montage | `compose-slideshow-video` |
| Interviews/takes/shorts | `edit-dialogue-footage` |
| Native Resolve app operation, scripts, MCP route and saved project | `davinci-resolve-toolkit:davinci-resolve-studio` (Video Production Studio hands off the reviewed editorial package) |
| Captions/titles/labels/credits | `create-video-typography` |
| Diagrams/UI/3D/kinetic motion | `create-motion-graphics` |
| Dialogue/music/SFX master | `mix-video-audio` |
| Staged deterministic execution | `render-video-project` |
| OTIO/EDL/NLE handoff | `exchange-video-timelines` |
| Aspect/platform/client variants | `conform-video-delivery` |
| Structural + human review | `validate-video-quality` |
| Plugin learning/refactor | `evolve-video-workflow` |

## Shared deterministic layer

| Concern | Owner |
|---|---|
| Media-tool resolution and local runtime | `video_workflow.utils`, `scripts/configure_runtime.py` |
| Editorial constraint audit | `video_workflow.audit`, `video-workflow audit-project` |
| Asymmetric safe areas and measured wrapping | `video_workflow.layout`, `video_workflow.render` |
| Manifest validation and compatibility | `video_workflow.manifest`, `schemas/video-project.schema.json` |
| Rendered-output evidence | `video_workflow.qa`, `video_workflow.visualize` |

Original motion and substantial visual redesign: the existing planning/storyboard/type/motion/QA owners all reach `create-motion-graphics/references/art-directed-motion.md`. This default covers expressive photography and typography, temporal composition, justified depth and representative playback review.
