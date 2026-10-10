---
name: exchange-video-timelines
description: Prepare or import an inspectable editorial timeline handoff using OTIO, EDL, XML or sidecars. Use when a code-generated edit must move between tools, editors or archives.
---

# Exchange Video Timelines

## Core principle

Preserve editorial decisions and source references across tools while making unavoidable losses, relinks, and unsupported effects explicit.

Treat the project manifest as the editorial contract. Use judgment for story and scripts for repeatable measurement.

## Required context

Open only the relevant local `references/` file: `domain-model.md` for concepts, `workflow.md` for sequence, `technical-reference.md` for implementation, `design-accessibility.md` for design, `qa-failure-modes.md` for recovery, or `examples.md` for worked cases. Use `references/sources/source-index.md` for evidence, licensing, and tool choices.

## Workflow

For Resolve import/export, editable project delivery or archive restoration, read
[Resolve round-trip acceptance](references/resolve-roundtrip.md). It identifies
the bundled exporters' limits and requires actual import/save/reopen/reimport
comparison. [Edit DaVinci Resolve](../edit-davinci-resolve/SKILL.md) owns app control.

1. Identify the receiving tool, adapter, supported feature set, frame rate, and timecode convention.
2. Normalize source paths to stable asset IDs and build a media relink map.
3. Export the simplest interchange format that preserves the required editorial meaning.
4. Bake or render effects that cannot travel while retaining notes and source parameters.
5. Validate clip order, source ranges, output duration, track assignment, and transitions after import.
6. Package fonts, captions, proxies, LUTs, audio stems, and provenance only when rights allow.
7. Document unsupported features and any manual finishing work.
8. Round-trip a synthetic or small timeline before handing off a large project.

## Required artifacts

- `timeline.otio`
- `timeline.edl`
- `media-map.csv`
- `handoff-notes.md`
- `unsupported-features.json`
- `relink-report.md`

Create only justified artifacts; separate source and analysis from editable decisions and renders.

## Hard rules

- Do not promise lossless interchange for effects, generators, nested timelines, speed ramps, or proprietary metadata.
- Do not export path-only references without stable IDs and relink information.
- Do not mix drop-frame and non-drop-frame timecode silently.
- Do not package copyrighted fonts or stock media without redistribution rights.
- Keep the original project manifest as the authoritative reasoning record.

## Technical quick reference

- OTIO represents editorial structure and metadata but generally references external media rather than embedding it.
- CMX3600 is broadly readable but limited; use it for simple cuts/dissolves and clear reel/source mapping.
- Frame-rate conversion can change timecode math; record rational frame rates and conversion policy.
- Bake motion graphics to normalized clips with alpha or backgrounds when the destination cannot reproduce them.
- Use checksums and a media manifest in handoff packages.

## Agent delegation

When delegating, use `agents/producer-agent.md` for bounded production and `agents/reviewer-agent.md` for independent evidence-based review afterward. Parallelize only independent assets or analysis windows; keep output filenames separate. Give each agent absolute paths, technical targets, design tokens, constraints, and a no-questions fallback when clarification is unavailable.

## Script entry point

Run `python scripts/run.py --help`, resolving the path from this `SKILL.md`.

## Neighboring skills

When another task becomes primary, route to: **plan-video-production**, **render-video-project**, **conform-video-delivery**, **validate-video-quality**.

## Completion contract

Report artifacts, assumptions and confidence, exact validation, unresolved risks, and the next owning skill. A render is final only after **validate-video-quality**.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Video Editor. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
