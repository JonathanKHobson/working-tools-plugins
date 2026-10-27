---
project: graphic-design-studio
type: plugin-guide
status: active
tags: [graphic-design, flyers, posters, advertising]
---

# Graphic Design Studio

Current edition **0.4.0** uses the [Compass licensing model](LICENSING.md): first-party code AGPL-3.0-only; first-party docs, prompts, skills, methods and eligible creative templates CC BY-SA 4.0. Upstream grants and prior release permissions remain valid. Author: Jonathan Kyle Hobson.

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
| [source-image-reconstruction](skills/source-image-reconstruction/SKILL.md) | Rebuild a supplied still using source-aware editorial, graphic or collage direction when selected |
| [image-stickers-and-memes](skills/image-stickers-and-memes/SKILL.md) | Make source-aware stickers and exact-caption memes with built-in image editing or bounded local composition |
| campaign-format-adaptation | Recompose a design for print, feeds, stories, and ad placements |
| motion-design | Direct styleframes, kinetic type, and visual continuity across beats |
| graphic-design-review | Review the rendered work with specific visual anchors and a taste pass |
| print-and-export-preflight | Check dimensions, image resolution, live text, QR destinations, and deliverable files |
| [hatch-pet](skills/hatch-pet/SKILL.md) | Produce and check a bounded animated pet asset with the retained scripts and recipient-owned host setup |
| [html-presentation-builder](skills/html-presentation-builder/SKILL.md) | Build a readable browser presentation from supplied evidence and inspect the rendered result |
| [lavish-axi](skills/lavish-axi/SKILL.md) | Use the complete graphic wrapper around a separately installed Lavish AXI runtime |

For the full task list and direct links, see the [use-case map](docs/use-case-map.md).

The plugin contains original synthesis of existing local marketing, communication, design, and visual-integration skills plus [graphic-design research](skills/graphic-design/references/research.md). It does not require those source plugins, a particular design application. Creation and export do not imply publication, sending, ad spending, or printing.

For a supplied image, choose [source-image reconstruction](skills/source-image-reconstruction/SKILL.md) when a selected editorial, flat graphic or collage treatment should change the composition. The detailed visual grammar, art-direction, hierarchy and quality references apply only to that selected direction; the user's brief and project identity remain primary. Built-in ChatGPT image editing executes the source-aware edit when available.

For a sticker or meme, [image-stickers-and-memes](skills/image-stickers-and-memes/SKILL.md) can use built-in ChatGPT image editing for opaque-photo isolation or an expressive poster layout. Its separate Pillow command handles deterministic transparent or masked stickers and native-size top/bottom captions. That helper requires an existing Python 3.9+ runtime with Pillow 10.1+; no setup or install runs. It writes only to the selected output path, with a same-directory temporary file during explicit overwrite. A subject cutout through the helper requires real alpha or a supplied mask; a mask is a stencil and still needs edge and identity review. The built-in tool can change source details, so inspect its actual output before acceptance. A supplied still can also take the [still-image motion](skills/motion-design/references/still-image-motion.md) route when a short animation is requested; if no native video tool is available, the result is an unrendered shot brief.

See [project map](docs/project-map.md), [integration decisions](docs/integration-map.md), and [distribution checks](docs/distribution.md). Current platform and printer specifications must be checked for the actual job.

## Guided images

Ask “Show me the image workflows” to browse 16 reusable recipes, or “Prepare a product-photo prompt” for direct assistance. Pick a workflow, describe the subject, set composition/detail preferences, and edit the visible prompt. Send it to the conversation to request generation, or copy it when the host cannot send. References are attached through the host conversation, not uploaded by this widget.

The library uses Design Templates’ maintained chooser. Install that package and set `DESIGN_TEMPLATES_ROOT` for separate installs; sibling packages in this repository are detected. The existing local UX chooser remains a compatibility source when present. Prepare the MCP interpreter as documented in [installation](docs/installation.md), or keep an existing recipient-owned studio-tools interpreter binding. Search/read/prepare run without the chooser; rendering the app needs the chooser. It has no image-provider credentials or generation runtime. Aspect ratio and detail are prompt preferences. See [workflow guidance](skills/graphic-design/references/image-workflows.md).

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->


The earlier public 0.3.2 edition included twelve workflows, complete eligible methods, 16 original image recipes, synthetic previews, the four-tool MCP app, standard-library Iconify helper and PDF preflight. This edition adds the source-image reconstruction and sticker/meme routes above. See [distribution scope](docs/distribution.md) and [license attribution](THIRD_PARTY_NOTICES.md). Generation uses a supported host imagegen capability; selecting or preparing a prompt does not generate an image.

## Presentations, local review and pet atlases

Version 0.3.0 adds three full standalone workflows, bringing the package to twelve skills. Use [HTML Presentation Builder](skills/html-presentation-builder/SKILL.md) for browser decks and viewport-fit review; [Lavish AXI](skills/lavish-axi/SKILL.md) for a source-grounded optional local annotation/poll review loop; and [Hatch Pet](skills/hatch-pet/SKILL.md) for the complete Apache-licensed pet preparation/assembly/inspection pipeline. See [requirements and host boundaries](docs/standalone-visual-workflows.md). Provider generation, native custom-pet support and Lavish runtime availability are separate checks. No private client assets or paid-provider execution is implied.
