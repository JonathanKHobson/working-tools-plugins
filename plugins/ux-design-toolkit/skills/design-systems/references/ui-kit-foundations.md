# Foundations, measurements and working tokens

Use for new kit foundations, geometry drift or token implementation. Preserve incumbent values unless the task authorizes a new direction.

## Define roles before values

| Foundation | Decisions to specify |
| --- | --- |
| Color | Text, muted text, surface, border, action emphasis, focus, selection and semantic status across supported themes; state pairs and image backgrounds |
| Typography | Display, page/section heading, body, label, helper, data and code roles; family/fallback, weight, size, line height, tracking, wrapping, max reading width |
| Space and layout | Spacing scale, container limits, gutters, columns, alignment, component gaps, section rhythm, viewport/container adaptation |
| Shape | Radius by role, nested corner relationships, stroke weight, clipping and hit boundaries; optical exceptions |
| Elevation | Layer order and purpose, border/surface/shadow alternatives, sticky/fixed overlap, dialogs and popovers; forced-colors behavior |
| Motion | State purpose, duration/easing tokens where reused, interruption, reduced-motion alternative and focus continuity |
| Icons | Family/source, license, stroke/fill style, optical size, alignment, meaning, accessible name, bidirectional treatment |
| Voice | Label grammar, consequence language, help, errors, pending and confirmed outcomes; restrained tone under stress |

Expressive headings work in brief editorial moments; reading and task copy need durable legibility. Heading semantics follow document hierarchy independently of visual size. An established wordmark can have a named exception. Do not turn one hero's display type into all labels. Keep actual text live whenever it conveys information or action.

## Action hierarchy

Choose a primary action per meaningful decision group, with secondary alternatives and quiet auxiliary actions. This is a hierarchy convention, not a rule forbidding two independent primary actions on an entire page. Destructive consequence is an intent axis; it does not automatically make an action primary. A link navigates; a button performs an action, including disclosure. Do not choose semantics merely to obtain a visual style.

Define state recipes using role tokens, not ad hoc brightness changes. Confirm text/background and focus/non-text distinctions at the actual rendered combinations. Pair status color with words, icons or shape. Hover must not be the only way to discover an action. Focus remains visible when hover/selection/error coexist.

## Units and authority

For each measurement identify unit, source class and rationale. CSS px, physical image pixels, Apple points and Android dp/sp are not interchangeable. A comfortable control target is a project choice unless tied to a stated platform requirement. WCAG 2.2 target-size minimum is an AA criterion using 24 × 24 CSS px with specified exceptions; the 44 × 44 enhanced criterion is AAA with its own exceptions. A 16px body default, 8-unit scale or round button is a convention to test, not a universal conformance requirement. Read the [minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) and [enhanced](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html) criteria before attributing compliance.

Specify minimum height rather than an exact height when text needs to grow. Distinguish outer padding from internal gap and the visible shape from its hit area. For an external ring of width r and offset o, check whether surrounding clipping/scroll space accommodates r + o; an intentional inset indicator is another option. Verify actual appearance and applicable criterion rather than diagnosing failure from that equation alone.

## Token architecture and validation

Primitive values describe raw choices; semantic tokens describe purpose; component tokens encode useful recipes or exceptions. Use the layers the system needs, without unnecessary aliases. Keep theme, density, expression and state axes separate. Preserve the current token dialect unless interoperability is an explicit requirement.

If exchanging tokens, declare the format/version, supported types, aliases, modes, units, transformations and omissions. The [DTCG 2025.10 format](https://www.designtokens.org/tr/2025.10/format/) is a community-group specification; a custom JSON file or a partial checker is not proof of full compatibility. Document losses when moving among code, design variables and platform values.

Validation has four distinct layers:

1. Parse/schema and unresolved/cyclic reference checks for the declared subset.
2. Resolved semantic pairs and variant/theme recipes, with transparent/gradient/image cases checked at the actual context.
3. Build/transform output and the selectors/components that consume it.
4. Controlled mutation of representative tokens in an isolated fixture: changing height, radius, padding or focus must alter the intended consumers while preserving documented exceptions. Restore the baseline afterward.

A table matching the JSON only proves documentation consistency. A generated CSS file that no component consumes is unused output. Compare documented measurements to computed and rendered values. Choose one authoritative value when they disagree, repair all relevant consumers, and record any intentional exception with a reason and review trigger.
