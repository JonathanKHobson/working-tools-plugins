---
project: graphic-design-studio
type: plugin-guide
status: active
tags: [graphic-design, flyers, posters, advertising]
---

# Graphic Design Studio

Make posters, flyers, advertisements, and promotional graphics whose composition, typography, imagery, and message work together. Use motion design here for visual direction across time: styleframes, kinetic type, and continuity review. Video Production owns scenes, rendering, audio and narration.

Bring the audience, exact words and event facts, size/placement, existing artwork or brand references, and desired file format. For example: “Make an 11 × 17 workshop poster from these event facts, logo, and photo; deliver a print PDF and screen proof.” The result is a composed graphic, visible design review, and export checks. “Adapt this approved poster for a portrait story and square feed post” yields recomposed variants that keep the message. “Review this flyer for the three most consequential visual problems” yields anchored fixes against the actual render.

For a capabilities/getting-started question, [graphic-design](skills/graphic-design/SKILL.md) points to this guide and the relevant specialist. This README is a human entry point; AI tasks select the smallest skill and read its conditional supporting files. The optional Image Gen Templates prepares image prompts; official imagegen performs generation. Use the available design tools for the selected artifact.

For a first use, choose one outcome: compose a poster, adapt an approved graphic,
or fix a rendered problem. The assistant should infer routine decisions from
the supplied facts, explain the selected route briefly and return that result.
If an adaptation removes supporting details, expect a checked destination or
complete companion copy along with the image. The [worked medium example](skills/campaign-format-adaptation/references/medium-content-plan.md) shows what changes between a poster, feed image and story. A missing fact that changes the output may need clarification; a full brand questionnaire is unnecessary for a bounded job.

Start with **$graphic-design**. It selects only the specialist guidance the task needs:

| Skill | Job |
| --- | --- |
| graphic-design | Direct the brief, design, revision, and final handoff |
| promotional-design-copy | Shape the offer, hook, information hierarchy, and call to action |
| composition-and-typography | Resolve placement, balance, visual movement, type, and color |
| graphic-asset-compositing | Integrate images, cutouts, effects, masks, and text fields |
| campaign-format-adaptation | Recompose a design for print, feeds, stories, and ad placements |
| motion-design | Direct styleframes, kinetic type, and visual continuity across beats |
| graphic-design-review | Review the rendered work with specific visual anchors and a taste pass |
| print-and-export-preflight | Check dimensions, image resolution, live text, QR destinations, and deliverable files |

For the full task list and direct links, see the [use-case map](docs/use-case-map.md).

The plugin contains original synthesis of existing local marketing, communication, design, and visual-integration skills plus [graphic-design research](skills/graphic-design/references/research.md). It does not require those source plugins, a particular design application. Creation and export do not imply publication, sending, ad spending, or printing.

See [project map](docs/project-map.md), [integration decisions](docs/integration-map.md), and [distribution checks](docs/distribution.md). Current platform and printer specifications must be checked for the actual job.

## Guided images

Ask “Show me the image workflows” to browse 16 reusable recipes, or “Prepare a product-photo prompt” for direct assistance. Pick a workflow, describe the subject, set composition/detail preferences, and edit the visible prompt. Send it to the conversation to request generation, or copy it when the host cannot send. References are attached through the host conversation, not uploaded by this widget.

The library uses public Design Templates’ maintained chooser. Install that package and set `DESIGN_TEMPLATES_ROOT` for separate installs; sibling packages in this repository are detected. Prepare the MCP interpreter as documented in [installation](docs/installation.md). Search/read/prepare run without the chooser; rendering the app needs the chooser. It has no image-provider credentials or generation runtime. Aspect ratio and detail are prompt preferences. See [workflow guidance](skills/graphic-design/references/image-workflows.md).

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->


Public edition 0.3.0 includes all twelve workflows, complete eligible methods, 16 original image recipes, synthetic previews, the actual four-tool MCP app, standard-library Iconify helper and PDF preflight. See [distribution scope](docs/distribution.md) and [license attribution](THIRD_PARTY_NOTICES.md). Generation uses a supported host imagegen capability; selecting or preparing a prompt does not generate an image.

## Presentations, local review and pet atlases

Version 0.3.0 adds three full standalone workflows, bringing the package to twelve skills. Use [HTML Presentation Builder](skills/html-presentation-builder/SKILL.md) for browser decks and viewport-fit review; [Lavish AXI](skills/lavish-axi/SKILL.md) for a source-grounded optional local annotation/poll review loop; and [Hatch Pet](skills/hatch-pet/SKILL.md) for the complete Apache-licensed pet preparation/assembly/inspection pipeline. See [requirements and host boundaries](docs/standalone-visual-workflows.md). Provider generation, native custom-pet support and Lavish runtime availability are separate checks. No private client assets or paid-provider execution is implied.
