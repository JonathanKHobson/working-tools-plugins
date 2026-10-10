# Portable template design specifications

Apply when creating, maintaining or packaging a design artifact or reusable
template: websites, documents, presentations, spreadsheets, PDF sources and
graphics. Keep a concise `DESIGN.md` beside the editable source or at the skill
root; link it from `SKILL.md` when a template skill exists. Reuse and update an
existing specification rather than creating a parallel brand system. A small
artifact can use one short document. Advice, text-only changes and metadata
audits do not require a new design artifact or visual review.

## Source first

Document the actual design, its audience/use, visual hierarchy, colors and their
uses, typography roles, layout/spacing, components, assets, adaptation rules and
fidelity checks. Identify the source file, XML part/style or CSS selector and
units behind measurements. Separate direct formatting from inherited values;
an unused theme definition is not an active design decision. Do not invent a
brand philosophy, missing measurement, license, state or fallback.

Current user instructions govern intentional changes. Within the retained
template, editable source and its measured values are authoritative; reviewed
renders show appearance in a recorded environment. The specification describes
that evidence. Resolve disagreements before declaring fidelity. Preserve custom
source dialects and explain their interoperability limits.

Use the existing [DESIGN.md handoff](design-md-handoff.md) for its pinned Google
alpha format: ordered Markdown sections with optional verified YAML tokens.
`version: alpha` identifies that format, not the template's release version.
Keep document/release revisions and source SHA-256 fingerprints in separate
provenance metadata. Native pt, twip, EMU, cell-width and print units belong in
prose or explicitly documented extensions, not silently converted CSS tokens.
Google DESIGN.md is an emerging open format; the Agent Skills specification
does not mandate it, and a file's presence does not establish conformance.

## Separate reader, content, structure and style

Before changing the template, identify four decisions in the existing design
entry or brief. **Reader and job** say who needs to do what and in which context.
**Content** says which facts, evidence, qualifications and actions support that
job. **Structure** says how those items are arranged and revealed. **Style** says
how the approved identity expresses them through type, color and other visual
properties. A style change should retain the chosen content, reading order and
behavior; a medium or task change can require a different content selection and
structure. Keep intentional exceptions explicit. These are working distinctions,
not a requirement to split every native document into four files.

Reuse current requirements. For a new or materially adapted template, fill the
following compact contract in `DESIGN.md`, or update the corresponding existing
section. Ask only for missing information that could change the result. Do not
make the user complete a questionnaire before a bounded edit.

```markdown
### Reader and content contract
- Reader and context: [who, prior knowledge, viewing or interaction conditions]
- Job and next action: [what the reader should understand or do]
- Include: [required facts, evidence, qualification, action, source pointers]
- Exclude or relocate: [nonessential material and its retained destination]
- Priority: [reading order; what stays when space is constrained]
- Budget: [per region/slot, and what to do on overflow]
- Check: [observable task, content and fit checks at named sizes/states]
- Structure and style: [existing template/layout and identity references]
```

Budgets are task-specific design defaults. A limit can constrain words, lines,
items, chart detail or reading sequence; justify it in the actual viewing
context. Do not use a universal word cap, force a report into a slide budget or
shrink type to hide overflow. Recompose, split a claim, or retain a readable
linked detail when needed. An expanded disclosure still needs structured,
readable content. Never remove an essential qualification merely because the
budget is exceeded. Keep a claim's scope, uncertainty and source attributable
at the point of use; fuller evidence can be linked or supplied in a companion.
Keep removed material in its authoritative source, and identify the destination
only when it actually exists.

### Worked contract: a fictional pilot report

This example supplies design decisions, not observed research or performance.
The source record says: “Four of six pilot participants completed setup without
help; two needed help choosing a file. One small pilot does not establish a
population success rate.” Its meaning must survive every projection.

| Medium and reader job | Include | Exclude or relocate | Priority and budget | Check |
| --- | --- | --- | --- | --- |
| Web summary for a stakeholder deciding the next test | Four of six result, small-pilot limitation, file-choice issue, next-test action and report link | Session-level detail stays in the report | Finding, scope, next action; draft target of one short finding paragraph and one action block | Reader can find the result, its limitation and proposed next test without opening the report; check narrow and wide layouts |
| Reference report for a teammate inspecting the finding | Session evidence, method, scope, failures and sources | Promotional language | Evidence navigation, finding, method; no fixed total word cap, use labeled sections | Reader can trace the claim to the six sessions; inspect expanded details and long-content fit |
| Presentation for a group choosing an action | “Four of six completed setup in this small pilot”, labeled 4/6 comparison, file-choice issue and test decision | Session notes remain in the companion report | One finding plus one decision per slide; split if the smallest offered stage cannot fit readable labels | Title sequence conveys the reasoning; limitation and 4/6 label survive the actual slide export |

The web summary is not a recolored report, and the presentation is not a
paginated web page. They share authoritative facts and an approved identity;
each serves a different reader job. Record the actual companion path before
using this pattern in a deliverable.

## Reuse components by information and behavior

Find the incumbent component first. A new color, label or border treatment
usually belongs to a variant of that component. A distinct reusable component
needs a distinct information arrangement, meaningful state model or responsive
behavior. Record only the boundaries the current task uses:

- Slots and required content, including evidence/qualification relationships.
- Content shape and budget, such as a comparison with labeled alternatives or a
  finding followed by a source link, rather than an arbitrary prose box.
- Relevant default, loading, empty, error, expanded and selected states, plus
  keyboard/focus behavior when interactive.
- Narrow and wide behavior, long-content handling and any change of control.

For example, a comparison component can stack labeled alternatives on a narrow
screen while keeping their shared measure visible. A blue and green version
with the same slots and behavior is one component with tone variants. A
collapsed evidence panel is reviewed expanded; hiding prose does not establish
readability or fit. Do not build a registry or new component library solely to
record these decisions in an existing native template.

## Review preconditions and deliberately failing cases

Use the artifact's current review and test owner. Before a fit or style check,
confirm the expected page/state exists and the required stylesheet, tokens,
fonts, images and runtime are present and applied. Check load failures and
computed values where available; a requested style name or completed font wait
alone is insufficient. For a native export, verify the actual retained or
substituted fonts/assets. An approved fallback is a separate named test case.
Missing assets invalidate that case's acceptance; they must not become a green
result for a smaller, unstyled page.

For a new or changed reusable rule or automated check, pair a valid case with a
minimal deliberately failing case. Keep fixtures in the owning project's test
or review records, and change one condition at a time. A routine text edit does
not need a new suite. Use this bounded matrix when it matches the change:

| Rule | Valid case | Deliberately failing case | Expected result |
| --- | --- | --- | --- |
| Required source and scope survive trimming | Fictional pilot finding retains 4/6, small-pilot scope and its source | Replace it with “Most users succeed” and remove scope/source | Reject content fidelity even if it fits |
| Style is actually tested | Intended tokens and required fonts resolve in the offered appearance | Request a style whose stylesheet is absent | Reject the precondition before reporting fit |
| Required component content exists | Comparison has labels, measure and relevant states | Remove a required label or supply an unknown component kind | Reject structure; do not silently count zero instances as a pass |
| Content fits its usable area | All required visible and expanded content fits at the stated size | Add one long block that escapes or clips | Reject fit; measure natural content against usable area, not a flex-assigned height |
| Interaction remains usable | Activate the selected control and continue by keyboard | Replace the focused control and leave focus on the document body | Reject the tested focus path |

Record which cases ran, which were only inspected in source and which remain
untested. A document containing this matrix is guidance, not proof that a
renderer or automated gate enforces it. A passing implementation check cannot
certify audience comprehension, every consumer, or every output medium.

## Check extraction coverage before summarizing a source

When deriving a reusable design or brand specification from native files, record
which relevant structure classes were inspected, not just the values returned.
Distinguish inspected-and-absent, present, unresolved and not inspected. An empty
extractor result does not establish a monochrome design or a missing asset.

| Source | Coverage that can change the interpretation |
| --- | --- |
| DOCX | Direct and inherited paragraph/run styles; table and cell shading/borders; section geometry; headers/footers; used theme references. Resolve used styles and local overrides rather than counting every style definition. |
| PPTX | Slide, layout and master inheritance; theme transforms; shape/text fills; table styles and cell overrides; chart roles and image-based artwork. |
| XLSX | Styled blank cells as well as populated cells; table styles, theme/indexed colors, conditional-format rules and their applied ranges/priority; number formats, inputs, formulas and print areas. A conditional color is a rule, not always the current cell color. |
| Web or vector | Used selectors/tokens and overrides at relevant states, viewport and theme; inherited SVG fills/strokes; embedded raster assets. Do not confuse the surrounding library UI with the template's identity. |
| PDF or raster only | Observed marks and geometry in the supplied view; identify reconstruction limits. Pixels alone do not prove an original font, hidden state, source hierarchy or exact production color profile. |

Retain detailed coverage in the existing evidence record, not a mandatory new
manifest. Compare the source render against the extracted palette, typography
roles and a distinctive layout/component before generating a final guide. If a
visible purple table header is absent from the extracted colors, inspect its
native style or asset and resolve that conflict; do not repaint the source to
fit the documentation. If the source cannot be inspected, the affected fidelity
claim remains unverified while the rest of the authorized work can continue.
Represent semantic input, warning or data colors separately from decorative
brand accents so applying an identity does not change information meaning.

For a collection, track coverage per identity/template. Inspect representative
source anchors for each item and focus deeper review on conflicts, exceptional
structures and changed regions. A contact sheet can triage; one attractive pilot
or a successful extraction script does not prove the entire collection faithful.
Report actual page/state coverage without turning sample inspection into an
exhaustive claim.

An identity reference can be shared by several templates while each retains its
own medium rules and version. Keep one authoritative value for each fact and
generate or explicitly reconcile its guide, token, preview and bundle consumers.
Declare supported token formats separately: the [DTCG 2025.10 format](https://www.designtokens.org/tr/2025.10/format/)
is a design-token interchange specification, not a complete brand schema or W3C
Standard. Do not label a custom JSON palette DTCG-conformant without checking
its types, values and references against that format. The
[Agent Skills specification](https://agentskills.io/specification) governs skill
packaging, not a required brand document inventory. This coverage method is a
local procedure; the filename alone proves neither format nor fidelity.

## Choose support by actual need

`DESIGN.md` is the useful entry point, not just a list of files. Summarize the
template's distinctive rules there. Link optional support when it has enough
independent detail to help execution:

- `TYPOGRAPHY.md`: used type roles, inheritance, weights, sizes, leading,
  fallback/embedding limits and source locations.
- `COLORS.md`: semantic or observed element roles, exact values, direct/theme
  overrides and relevant foreground/background pairs.
- `LAYOUTS.md`: page/slide/sheet/route structures, geometry, responsive and print
  changes, reading order and source anchors.
- `COMPONENTS.md`: editable reusable patterns, states and bindings to the
  source's styles, cells, masters or selectors.
- `ADAPTATION.md`: permitted content/format changes, invariants, overflow,
  localization, alternate sizes and verification implications.

Keep these in an existing support folder or a small `design/` folder. Do not
create empty files, repeated general tutorials or a second `STYLE.md` that
duplicates `DESIGN.md`. Machine-readable evidence can preserve detailed native
structure beyond the concise prose. Retain fonts/media and their actual notices;
record unknown licensing rather than granting rights. A PDF should retain or
identify its editable source when available; label reconstruction when absent.

## Execution and delivery

Keep execution instructions in `SKILL.md`: read the design entry, copy/import
the native source with an available compatible tool, replace authorized
content, preserve relevant structures, render and verify. Name real
dependencies and supported alternatives. Missing editing tools are a capability
gap, not permission to claim a generated file. A persona is not a fidelity
mechanism. Add `AGENTS.md` only for a source repository that needs distinct
maintainer commands/constraints; it must not duplicate or outrank the template
skill. Do not assume every AI host reads it.

Bundle the skill, design entry, transitive relative references, editable assets,
previews and retained notices. Link the design entry from install/create-once
instructions as well as the skill. Have the owning builder copy the documents
and fail on missing references, mismatched source fingerprints, unsafe paths or
installed/bundled drift. Test from an extracted ZIP, including private/public
exclusions. A source file edit requires refreshed documentation and references.

Verify source measurements and rendered representative anchors; distinguish
structural coverage from exhaustive visual or cross-model acceptance. For a
fidelity claim, run the same bounded adaptation through the relevant receiving
models/tools and compare structure, appearance and behavior against named
invariants. Record renderer/fonts and untested combinations. Specifications
reduce ambiguity; they cannot guarantee identical rendering across engines.

Writing-only templates use the writing owner's authoritative guide and a
compact `STYLE.md` entry when useful. Keep voice, structure, mechanics, examples
and QA linked to their actual sources; there is no claim that this local filename
is a universal writing standard. Historical authority documents remain evidence
and attribution, not automatically a complete execution specification.
