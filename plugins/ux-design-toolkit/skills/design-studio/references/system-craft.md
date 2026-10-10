# System craft checks

Use for a token/theme change, a shared component revision, or repeated visual failures. Existing project decisions are the starting point; a routine one-screen correction should not trigger a system rebuild.

## Test pairs, roles and real content

Identify the actual foreground/background combinations used by normal text, secondary text, links, control labels, focus indicators and status content. Distinguish text, meaningful non-text and purely decorative roles. Check the rendered pair, including opacity or an image behind it, instead of assuming that a named palette or isolated hex value passes contrast.

Keep accent, selection and status meanings clear. A status color is not interchangeable with decoration; where a brand shares hues, add explicit labels or shapes and test whether meaning remains clear. Review light and dark appearances separately when both are in scope. Inversion alone does not establish usable surfaces, muted text, borders or status colors.

Exercise long labels, realistic data density, empty results, errors and enlarged text in the affected shared component. Tokenized padding can still produce crowded content or uneven visible alignment. Review visible glyphs, artwork bounds and reading fields rather than trusting element rectangles.

## Include browser-native details

When the path uses them, inspect text selection, caret visibility, keyboard focus, links and underlines, native form states and numeric alignment. Use tabular numerals for columns or values whose changing width disrupts comparison; do not impose them on all prose. Preserve reliable platform behavior. Custom scrollbars, cursors or decorative loading choreography are not a polish requirement.

## Fix the shared cause when warranted

If one token or component causes the same observed defect across several artifacts, correct that existing owner within the authorized scope and recheck representative affected uses. Record the failure and its correction where the system is maintained. Do not make every isolated preference into a global rule or start a new validator, registry or background review job without a demonstrated need.

Passing a parser, a contrast calculation or a detector is limited evidence. Inspect the changed visual anchors and exercise the affected interaction before claiming rendered or behavioral quality.

## Provenance and scope

Original local synthesis from the existing UX guidance, [Impeccable craft guidance at revision 114ea1d](https://github.com/pbakaus/impeccable/tree/114ea1d3838fca73b253af45f873b9c4f5f213c8/skill/reference), and Kyle's Shareables `design-system/style-sources/quality-gates.md` and `design-system/research/shareables-design-system-contrast-spacing-feedback.md` (inspected 2026-09-29). The latter is a planning note, not approval of its themes or galleries. Source and adoption details are in [design sources](design-sources.md). This reference itself adds no source templates, code, palettes or automatic hooks; the separately packaged [native runtime](native-design-runtime.md) is conditional.
