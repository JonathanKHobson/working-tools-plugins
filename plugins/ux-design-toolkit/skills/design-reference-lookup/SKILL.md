---
name: design-reference-lookup
description: Browse local Site templates, public design galleries and transition references, or search offline palettes, typography and patterns when a visual decision is unresolved.
---
# Design reference lookup

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


For a Site template gallery, visual comparison, or a named Design Library template, read [Design Library](references/design-library.md) and call its browse tool. Selection resolves an existing template and hands it to Sites; it does not create or publish an application. Otherwise use the offline reference workflow below.

Use the existing product system and explicit brief first. Search only the unresolved design question. From this skill directory run the available Python 3 runtime with `scripts/search.py "<query>" --domain typography -n 3`; domains include color, style, ux, chart, landing, product and web. Stack guidance uses `--stack <verified project stack>`.

Use `--design-system -f markdown` only when the task actually needs a new coordinated system. Do not select a framework, persist generated files, install packages or update the corpus merely to answer a lookup. Offline results are suggestions whose relevance must be checked against the audience, current platform requirements and approved design. Validate contrast and rendered behavior rather than treating a stored example as proof.

The scripts and data are bundled locally. Do not run upstream download/update commands without an explicitly requested update. `design-studio` owns implementation and visual verification. Exact optional command formats remain in [reference workflow](REFERENCE-WORKFLOW.md); its historical always-generate/default-stack instructions are superseded by this entrypoint.

For charts, a palette result is a candidate, not the final category mapping or accessibility verdict. Use [dashboard color guidance](../dashboard-design/references/chart-meaning-and-color.md) when the unresolved decision concerns a chart: preserve identity across filtering, distinguish sequential from diverging meaning, and check actual marks/backgrounds. Remote font URLs in catalog output stay references; local-first artifacts require already available or separately reviewed local fonts.

## Scoped Atlas reference

For local ux concepts, frameworks, activities or source definitions, read [the scoped Atlas library](../../references/atlas-library.md). Use its relevant-only search and full-source selection before adaptation; human browsing and assistant retrieval share the same source records.

For a fresh direction, supplied gallery or unresolved web/app/deck/motion detail, read [public design resources](references/public-design-resources.md). It gives agents direct access routes to Godly, Transitions.dev, Deck.gallery and Animos, with a reference-to-original-output workflow and rights-aware reuse. Public research within the authorized task needs no separate lookup approval; preserve approved designs and keep browsing bounded.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports UI Designer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
