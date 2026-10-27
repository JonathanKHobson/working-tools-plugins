---
name: validate-video-quality
description: Inspect a rendered preview, master or export for visual, audio, caption, timing, accessibility and delivery defects. Use before approval or when output quality is in question.
---

# Validate Video Quality

## Core principle

Produce machine evidence and a disciplined watch-through that catches silent technical failures without pretending automated metrics can certify editorial taste.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.

## Default art direction

For original or restyled motion, also apply the [art-direction playback checks](../create-motion-graphics/references/art-directed-motion.md#prove-the-direction-at-low-cost). Compare actual type/image integration, evolving composition, meaningful movement and justified spatial depth against the chosen direction and rendered anchors. Separate technical validity from craft and reference fidelity; transcripts/stills cannot prove temporal similarity. Routine approved trims retain their existing scoped QA.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Course recordings and learner delivery

For Vids projects, use the [review and export handoff](../edit-dialogue-footage/references/google-vids-course-editing.md#review-and-hand-off-exports). Distinguish project save, preview review, completed export, reviewed file, course attachment, and learner playback. Review edited speech against captions and visible actions; a transcript replacement alone does not verify the audio. Route course-page integration and the exact learner revision to Instructional Design Studio's `course-production-handoff`.

For existing Drive recording trims, use [trim/replacement verification](../edit-dialogue-footage/references/drive-trim-and-replace.md), including subtitle/container duration checks, same-file download integrity and preview-processing status.

For lesson Shorts and catalog handoffs, bind QA to the final output video, timed captions, cover variants, and their hashes. Record listening, visual, caption, and native destination checks separately; route saved platform state to `social-content-studio:social-publishing` rather than treating a local preview or handoff as remote proof.

## Workflow

1. Probe the output and compare streams, dimensions, duration, frame rate, codecs, pixel format, color, and audio to the manifest.
2. Run black, freeze, silence, clipping, loudness, and missing-stream checks appropriate to the project.
3. Generate first/last/midpoint frames, contact sheets, and cut-boundary views from the rendered output.
4. Validate caption timing, reading speed, tracked text boxes, asymmetric safe-area placement, contrast treatment, and final-layer visibility.
5. Review representative reframes for faces, hands, products, diagrams, and text.
6. Normally watch the complete output at normal speed with sound; then spot-check muted and at small display size. If the user requests quiet testing, keep only the test player muted, preserve the delivered audio, use silent structural/signal checks and explicitly record that listening review was not performed.
7. Classify issues by severity, confidence, location, evidence, and proposed fix.
8. Fix, rerender, and rerun targeted checks; cap blind self-iteration and report unresolved risks.
9. Run project-specific validators such as QR decode, exact-link, spelling, or source-uniqueness checks when the manifest requires them.

## Required artifacts

- `qa-report.json`
- `probe.json`
- `contact-sheet.png`
- `cut-boundary-views/`
- `waveform.png`
- `review-notes.md`
- `approval.json`

Create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- Never mark final based only on ffprobe or automated detectors.
- Always inspect the rendered output, not only source assets or code.
- Validate scannable or machine-readable elements again from a compressed video frame, not only their source PNG.
- Do not hide warnings to make a report pass.
- Do not treat intentional black, silence, freeze, grain, clipping, or stylization as errors without context.
- Approval must identify the exact file hash and review date.

## Technical quick reference

- Structural assertions: streams exist, duration tolerance, dimensions, frame rate, sample rate, codec, pixel format, channel layout, and color tags.
- Temporal detectors should report timestamp ranges and thresholds so reviewers can distinguish intent from defects.
- Cut-boundary QA samples approximately ±1.5 seconds around each edit with waveform and adjacent frames.
- Caption QA combines text metrics with frame-level collision and contrast checks.
- A final report separates automated pass, visual review, audio review, accessibility review, and unresolved exceptions.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **analyze-video-content**, **render-video-project**, **conform-video-delivery**, **evolve-video-workflow**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

When an edit includes tracked elements, occlusion, selective blur, expressive captions or grading, use the [temporal compositing checks](../create-motion-graphics/references/tracked-layer-compositing.md#temporal-acceptance), [caption composite checks](../create-video-typography/references/expressive-captions.md#check-the-final-composite) and [editorial treatment](../edit-dialogue-footage/references/editorial-treatment.md). Inspect the hardest motion/edge intervals and final delivery crops; generic probe/black/freeze/audio checks do not establish those effects are correct.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Media Quality Reviewer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->

For candidate-style review, check that [comparison conditions](../create-motion-graphics/references/art-directed-motion.md#compare-alternatives-fairly-when-selection-is-the-task) remain comparable. Diagnose type/composition/movement separately from content changes; save actual accepted/rejected evidence in the existing project style record, not an invented preference score.

For reusable films or production discoveries, apply [production learning transfer](../evolve-video-workflow/references/production-learning-transfer.md) to separate source, pose and encoded cadence; source reproduction, adaptation and listening; and review-sheet readability. Freeze final media before evidence readers and invalidate affected evidence after any output mutation.

For generated sprite acting, apply the [sprite motion review](../create-motion-graphics/references/generated-sprite-animation.md#preview-and-verify) to exact registered poses and encoded transitions. Verify meaning, identity, body proportions, contact and pose cadence separately from encoded frame rate.
