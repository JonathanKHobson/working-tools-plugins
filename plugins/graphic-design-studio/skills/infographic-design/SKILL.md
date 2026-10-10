---
name: infographic-design
description: Design static information graphics and composed explainers that make processes, hierarchies, comparisons, or mechanisms easy to understand. Use for posters, one-page explainers, and editorial infographics; route quantitative chart decisions and data transformations to visualization specialists.
---

# Infographic design

Own the composition and readability of a static information graphic. Do not turn it into a dashboard, interactive application, or new rendering system. Start with the reader, the takeaway, the delivery size, and the evidence or source material.

## Choose the structure before styling

Write one sentence describing what the reader should understand. Identify which content is evidence, explanation, and decoration. Choose a structure that matches the actual relationship:

- Use a sequence for ordered steps or time; use branches for real alternatives.
- Use hierarchy for genuine containment or levels.
- Use aligned columns or a matrix for like-for-like comparisons.
- Use a map or spatial plan only when location carries meaning.
- Use a mechanism or relationship diagram when parts and connections are supported by the source.

Do not imply order, causation, scale, flow, or importance through placement or decoration unless the evidence supports it. Decorative arrow width, line weight, area, and icon size must not imply unmeasured amounts. Keep decorative treatment visually distinct from evidence-bearing marks.

## Keep evidence intact

Trace labels, claims, quantities, dates, and caveats to the supplied source. Preserve distinctions such as measured, estimated, illustrative, and unknown. Keep evidence-bearing values deterministic and legible; generated imagery may set context but must not invent or redraw numbers, labels, chart marks, or source notes.

When the brief includes quantitative evidence, use `data-visualization-toolkit:data-visualization` for chart form, scales, uncertainty, missing values, and quantitative encodings. Data Analytics retains source analysis, formulas, aggregation and its native app renderer; a bespoke web chart may still use Build Web Data Visualization's implementation depth. This skill decides how verified outputs sit within the composition and preserves their units, definitions, caveats, and source. Do not redraw a quantitative chart as decoration.

## Compose for understanding

Establish a clear first read, then a path through the supporting details. Group related material, align comparable items, and reserve emphasis for a supported takeaway. Use labels beside the element they explain. Keep wording concise without removing qualifications that change meaning. Prefer a useful diagram over decorative artwork; omit elements that do not help the reader understand the information.

Use type, spacing, shape, and color to clarify roles. Check contrast and size at the intended viewing distance. Do not rely on color alone to distinguish categories or states. Use only locally available or reviewed icons, fonts, and assets; do not add runtime downloads, remote font imports, CDN scripts, or service-backed asset search.

## Finish and review

Work in the requested static format and preserve an editable source when the tool supports it. Before visual claims, map three to eight anchors with source/page or viewport, region, observed fact, and intended action. Inspect the rendered graphic at its intended size and at a narrow or thumbnail view as relevant. Check reading order, label legibility, contrast, alignment, evidence-to-label matches, and accidental implications. Inspect the exported file itself; distinguish visual review from print or platform checks that were not performed.

For general composition and typography, use [composition-and-typography](../composition-and-typography/SKILL.md). For a rendered critique, use [graphic-design-review](../graphic-design-review/SKILL.md). For print and file checks, use [print-and-export-preflight](../print-and-export-preflight/SKILL.md). This skill adds no library, engine, runtime, or required provider.

## Conceptual reference

The inspected [AntV creator skill](https://github.com/antvis/Infographic/blob/main/skills/infographic-creator/SKILL.md) provides a vocabulary for separating information structure from visual expression; its [MIT license](https://github.com/antvis/Infographic/blob/main/LICENSE) was checked on 2026-09-27. This is original local guidance; no upstream code or assets are bundled. The inspected creator loads an unpinned CDN engine, and its [icon-search loader](https://github.com/antvis/Infographic/blob/main/src/resource/loaders/search.ts) makes remote requests. Neither was adopted. A future code/asset import needs personal-security-check review of the exact version, license and network behavior before download or installation.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Graphic Designer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
