---
name: evolve-video-workflow
description: Turn recurring video workflow failures or feedback into tested plugin improvements. Use when evidence suggests a skill, method, boundary or tool should change.
---

# Evolve Video Workflow

## Core principle

Convert repeated evidence into tested reusable improvements without overfitting one project, duplicating installed skills, or silently breaking existing workflows.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Workflow

1. Read project memory, render logs, QA reports, user feedback, and current installed skill/plugin inventory.
2. Separate one-off project decisions from recurring techniques, fragile operations, and discovery/routing gaps.
3. Build a capability matrix before choosing whether to extend, merge, cross-reference, or create a skill.
4. Write pressure scenarios or retrieval tests and observe baseline failure before editing skill guidance.
5. Prefer deterministic scripts for mechanical repeated work and compact skill guidance for judgment.
6. Update cross-references, manifests, source registry, tests, examples, and migration notes together.
7. Run plugin validation, skill tests, integration renders, and plugin-eval before and after.
8. Preserve backwards compatibility or document a deliberate migration/deprecation path.

## Required artifacts

- `capability-matrix.md`
- `lesson-candidates.md`
- `baseline-evals/`
- `design-spec.md`
- `implementation-plan.md`
- `migration-report.md`

Create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- No new skill merely because a project had a unique preference.
- Do not edit skills without a failing scenario, gap, or measured reason.
- Do not duplicate a capability that an installed skill already owns coherently.
- Do not copy unlicensed or incompatible third-party code.
- Do not claim improvement without before/after evidence.

## Technical quick reference

- Skill descriptions should describe triggers, not summarize the workflow in a way that lets agents skip the body.
- Keep frequently loaded SKILL.md files compact; move heavy references and executable details outward.
- Evaluate routing cost, trigger precision, broken links, reference discoverability, script determinism, and coverage.
- Use synthetic fixtures to keep tests reproducible and free of proprietary media.
- Track source review date and tool/version assumptions so future changes are visible.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **plan-video-production**, **install-video-toolchain**, **validate-video-quality**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Video Producer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->

For multi-producer handoffs, reusable templates or lessons from completed production, apply [production learning transfer](references/production-learning-transfer.md). Preserve observation, source change, rendered verification and user acceptance as separate states; promote only the reusable mechanism into its existing owner.
