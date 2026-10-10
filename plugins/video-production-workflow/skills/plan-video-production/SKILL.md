---
name: plan-video-production
description: Turn a new or substantially revised video request into a usable brief, beat sheet and project manifest. Use when audience, story, assets, style, rights, accessibility or delivery are unresolved, including supplied Google Slides recording or generated-footage planning. Also use for video production workflow capabilities or getting-started questions.
---

# Plan Video Production

For a broad capabilities or first-use question, consult the [human guide](../../README.md) and identify the likely source media, target video, and verification needed. If the user already requests a specific stage, use its owner below and do the task; do not make orientation a recurring ceremony or record fictional onboarding state.

## Core principle

Turn an ambiguous request and available media into an approved production brief, acceptance criteria, beat sheet, and renderer-neutral project manifest.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.

## Default art direction

For original motion production or a substantial visual redesign, establish a concrete visual thesis before renderer code: typography, photography/imagery, evolving composition, justified depth and a coherent motion grammar. Apply the [art-directed motion contract](../create-motion-graphics/references/art-directed-motion.md), then test a representative passage before extending an unresolved direction. Reuse an approved treatment for continuation; routine trims/exports do not reopen art direction. Delegated production proceeds without an invented approval hold.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Supplied course deck

When an approved Google Slides lesson needs a Google Vids recording, use the conditional [course recording path](../edit-dialogue-footage/references/google-vids-course-editing.md#record-from-a-supplied-lesson-deck). Reuse the supplied teaching sequence and existing project; an already specified recording does not need competing creative approaches or a new scaffold. Continue through dialogue editing, audio review, and validation as needed.

## Generated footage and narrative handoff

When the brief calls for generated clips or names Sora, use [generated clip planning](references/generated-clip-planning.md). It preserves shot/prompt craft and records that the old Sora app/API path is unavailable; do not invoke the legacy runner. If the task is writing a screenplay, scene, dialogue or canon rather than producing footage, hand that work to `creative-writing-studio:story-book-router`, then translate the approved narrative beats into this production brief.

When a supplied video is a creative reference for an original piece with changed subject, words, product, or format, use [reference-led adaptation](references/reference-led-adaptation.md). It turns observed timing and visual relationships into a bounded, editable treatment. This is a planning method; reference access, generated media, and renderer setup remain separate decisions.

## Workflow

For an already specified task, go directly to the owning stage: supplied course
files → `ingest-video-assets`; excerpt editing → `edit-dialogue-footage`; finished
variants/handoff → `conform-video-delivery`; review → `validate-video-quality`.
Reuse the approved brief and existing manifest. Do not reopen strategy or load the
whole skill/reference family for a routine continuation. Platform scheduling and
saved-state readback route to `social-content-studio:social-publishing`.

For original video or motion production, route the beat plan through `design-video-storyboards` and its [participation workflow](../design-video-storyboards/references/video-style-discovery.md#shared-storyboarding-collaborative-or-autonomous). Prefill a useful storyboard from the idea. Collaborative work opens the shot editor; autonomous work uses its backend without an obligatory human checkpoint. Do not insert this stage into a routine trim/export.

1. Read the conversation and inspect the project directory before asking anything already known.
2. Inventory goals, audience, runtime, aspect ratios, channels, assets, deadlines, brand constraints, rights, accessibility, and must-keep or must-avoid material.
3. Separate facts, user preferences, inferred choices, unresolved risks, and reversible taste decisions.
4. Propose two or three editorial approaches with a recommended direction and explicit trade-offs.
5. Define the narrative arc and pacing mode before assigning clips or animations.
6. Create acceptance criteria that can be checked after rendering.
7. Create or update the declarative project manifest; do not jump straight to renderer code.
8. Respect an explicit strategy-approval hold before expensive generation or final-quality rendering. If the user delegated the direction and authorized production, record the chosen strategy and proceed within that scope; do not invent a new checkpoint.

## Required artifacts

- `creative-brief.md`
- `asset-rights.csv`
- `acceptance-criteria.md`
- `beat-sheet.md`
- `project.json`

Create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- Do not infer media rights from file possession.
- Do not lock the project to Remotion, FFmpeg, or another renderer during creative planning.
- Do not use a fixed questionnaire when the conversation already supplies answers.
- Mark platform safe zones and technical limits with a review date.
- Keep project-specific aesthetics out of reusable global rules unless repeated evidence supports them.
- Preserve placeholders when dates, links, prices, availability, accommodations, or other publishable facts are not verified.

## Technical quick reference

- Use four pacing modes: narrative-led, phrase-led music sync, strict beat sync, and ambient/long-hold.
- Define a shot purpose for every planned segment: orient, explain, prove, feel, transition, breathe, or call to action.
- Express assumptions with confidence and a validation step.
- Treat target duration as a budget with ranges per narrative beat, not a single number to hit blindly.
- Record delivery variants early because 16:9, 9:16, 1:1, and 4:5 can require different compositions.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **ingest-video-assets**, **analyze-video-content**, **analyze-music-pacing**, **design-video-storyboards**, **conform-video-delivery**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

## Complete generated-footage source

For generated-shot planning or a Sora-era workflow, **read the full [Sora source procedure](../../libraries/sora/SKILL.md)** for its intent decision tree, augmentation template, invariants and worked examples. Also read the full [prompting guide](../../libraries/sora/references/prompting.md), then [cinematic templates](../../libraries/sora/references/cinematic-shots.md), [social-ad templates](../../libraries/sora/references/social-ads.md), [sample prompts](../../libraries/sora/references/sample-prompts.md) and [troubleshooting](../../libraries/sora/references/troubleshooting.md) as the clip requires. Preserve their concrete examples and steps; the generated-clip-planning reference is a current provider adapter, not a replacement method.

All source files, including the old CLI, API contract, assets and license, are retained unchanged. The Sora API execution path is historical and unavailable per the dated official verification in [the provider adapter](references/generated-clip-planning.md); do not run the old API commands or apply old model limits as present-day facts. The prompt/shot craft is active. Use a currently available, authorized provider and its documented contract for actual generation, while retaining the original planning and iteration methods. Read historical CLI/API/network files when diagnosing old projects, without treating them as current service availability.

For image-led production of a website/product still, poster, document illustration or storyboard asset, use `graphic-design-studio:graphic-design`, which now owns the complete Visual Production Workflow. Load that full source and its asset/provenance/export checks. This handoff does not replace this skill's UI behavior or motion/audio responsibilities.

## Public title, thumbnail and opening promise

For a public teaching/demo video, record the supported title/thumbnail promise and the
first actual demonstrated payoff before expensive production. Keep prerequisites and
learning objectives intact. Marketing owns audience/search intent and packaging strategy;
Graphic Design owns truthful thumbnail concepts and rendered review. If retention data
informs a revision, use [audience retention editorial review](../analyze-video-content/references/audience-retention-editorial-review.md)
to separate observations from hypotheses before choosing one bounded change.

For mixed recorded/generated/footage-led production or asynchronous media jobs, use [production routes and job control](references/production-routes-and-job-control.md). Choose a route per scene, preserve real-demo evidence, and track submitted jobs before retries.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Video Producer, Cinematographer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->

For recurring original motion, load the existing project's selected [style record](../create-motion-graphics/references/art-directed-motion.md#reuse-a-selected-direction-through-project-evidence) and its accepted frame/clip evidence before inventing a new treatment. Keep provisional options and actual approvals distinct.

For a reusable template or multi-producer handoff, use [production learning transfer](../evolve-video-workflow/references/production-learning-transfer.md) to reconcile actual variants, source/review evidence and current scope before assigning work.

For FilmCraft editing or EffectCraft compositing, use `artcraft-design-toolkit:artcraft-apps` for installed CLI, MCP or Computer Use operations. This studio retains editorial decisions, motion direction, audio and final QA. Resolve-specific work uses the dedicated Resolve toolkit when installed, with the existing Resolve skill as the current fallback; verify its edition and connection.
