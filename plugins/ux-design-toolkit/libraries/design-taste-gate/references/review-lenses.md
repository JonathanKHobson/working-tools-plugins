# Design Taste Gate Review Lenses

Use these lenses to review UI and artifact outputs for specificity, credibility, and craft. Do not apply them mechanically; context and user goals decide which findings matter.

## Source Inspiration

This local skill is informed by public design-skill ideas, without copying or requiring upstream packages:

- Anthropic `frontend-design` (https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md): distinctive aesthetic direction before frontend implementation.
- Anthropic `web-artifacts-builder` (https://github.com/anthropics/skills/blob/main/skills/web-artifacts-builder/SKILL.md): complex Claude artifacts need a build/bundle lane and should avoid common generic AI aesthetics.
- Impeccable docs and GitHub (https://impeccable.style/docs/impeccable/ and https://github.com/pbakaus/impeccable): design register, design vocabulary, and explicit anti-pattern checks.
- Claude Artifacts guidance (https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them): artifacts should be substantial, self-contained, reusable, and worth revisiting outside the chat.

## 1. Surface And Register

First classify the surface:

- Product UI: design should serve repeated use, scanning, and task completion.
- Dashboard or operations tool: prioritize density, hierarchy, comparison, and low-drama styling.
- Brand or marketing page: allow stronger art direction, imagery, and memorable composition.
- Portfolio or case-study surface: make proof, authorship, and artifact captions visible.
- Local review artifact: optimize for reading, comparison, filtering, and export rather than spectacle.
- ChatGPT app or widget: follow app/tool contracts before visual polish.

If the register is unclear, state the assumed register and review against that.

## 2. Composition And Hierarchy

Look for:

- A clear primary task or message in the first scan.
- Sections that are shaped by content, not repeated card grids.
- Intentional alignment, asymmetry, density, or whitespace.
- A visible path through the page or artifact.
- Important actions placed where the user expects to act.

Common fixes:

- Replace generic centered stacks with a layout that reflects the task.
- Reduce repeated panels when hierarchy can be expressed with spacing, columns, tables, or bands.
- Make the most important object visibly larger or earlier than supporting copy.
- Use cards only for repeated items, modals, and truly framed tools.

## Visual Anchor Map

For screenshot-based or rendered-surface critique, label the evidence before
making visual claims. Use a compact table:

`ID | source/viewport | region/ref | observation | action | verification`

Anchor IDs can be simple labels such as `A1`, `B2`, `Card03`, `Button02`, or
`Nav01`. Regions can be approximate grid cells, normalized coordinates,
Playwright element refs, selectors, route names, or component names. Use these
IDs in findings and final QA notes so every critique points back to something
visible. Keep the map lightweight: enough handles to prevent vague references,
not a second artifact.

## Design Control Dials

Before changing or critiquing a visually important surface, set the smallest
useful set of dials so taste feedback becomes concrete:

| Dial | Low | Medium | High |
| --- | --- | --- | --- |
| Variance | tight system, few component variants | selected moments of contrast | expressive, editorial, or campaign-like |
| Motion | none beyond state feedback | subtle orientation and affordance | expressive or brand-defining movement |
| Density | sparse and guided | scan-friendly with grouped details | dense operational workspace |
| Reference source | existing app tokens | adjacent best-in-class product | custom moodboard, image, or brand world |

Use these dials to decide what to change, not to decorate. For example, an
operations dashboard usually wants medium/high density, low/medium variance,
and low motion; a portfolio proof page may justify higher variance and stronger
imagery. When a design feels generic, say which dial is wrong and what concrete
replacement would make it specific.

## 3. Typography

Look for:

- Distinct roles for display, section, body, labels, metadata, and controls.
- Legible line length, line height, and scale.
- Type choices that match the register.
- Avoidance of default-looking type when brand or public presentation matters.

Common fixes:

- Use one strong display choice and one readable body choice when the project allows custom fonts.
- For app UIs, keep type quieter and optimize scanning.
- Tighten metadata and labels instead of making every heading large.
- Avoid tiny gray text as the main explanation.

## 4. Color, Contrast, And Theme

Look for:

- A coherent palette with deliberate neutrals and accents.
- Color that supports meaning, priority, and state.
- Sufficient contrast in text, controls, warnings, and disabled states.
- Dark mode or colored surfaces that keep text readable.

Common fixes:

- Replace generic purple-blue gradients when they are only decorative.
- Use one or two accents with clear jobs instead of evenly distributing color everywhere.
- Tint neutrals slightly when the surface feels sterile.
- Do not use color alone to communicate state.

## 5. Spatial Rhythm

Look for:

- Consistent spacing scale.
- Enough padding for touch and focus states.
- No cramped toolbars, filters, forms, or cards.
- Stable dimensions for repeated controls and tiles.

Common fixes:

- Normalize spacing around repeated modules.
- Give dense dashboards tighter but consistent rhythm.
- Give marketing/portfolio pages larger composition-level spacing.
- Prevent long labels or dynamic states from shifting layout.

## 6. Motion And Visual Effects

Look for:

- Motion that explains change, rewards action, or helps orientation.
- Reduced-motion respect.
- Avoidance of dated bounce/elastic easing or random floating decoration.
- Effects that match the surface rather than shouting over it.

Common fixes:

- Prefer one purposeful motion moment over many scattered effects.
- Use short transitions for state changes and layout affordances.
- Remove motion from high-frequency operational controls unless it helps feedback.
- Avoid dark glows, glass panels, and decorative blur when they do not serve the task.

## 7. Interaction States

Look for:

- Visible hover, focus, active, selected, loading, success, error, empty, disabled, and permission states.
- Touch targets that are large enough and well spaced.
- Clear destructive, primary, secondary, and disabled actions.
- Recovery paths after errors or empty states.

Common fixes:

- Add focus styles before visual polish.
- Make selected and disabled states readable without relying only on opacity.
- Pair errors with next actions.
- Make empty states specific to the user's likely next step.

## 8. Responsiveness

Look for:

- Whether the layout remains intentional on narrow screens.
- Text that wraps without overlap or clipped controls.
- Charts, tables, filters, and navigation that remain usable.
- Media and fixed-format areas with stable aspect ratios.

Common fixes:

- Convert multi-column layouts into prioritized stacks.
- Use overflow patterns for dense tables instead of shrinking everything.
- Set responsive constraints for boards, grids, tiles, and toolbars.
- Test long labels, zero items, many items, and narrow viewports.

## 9. UX Writing Placement

Look for:

- Copy that carries the task rather than decorating the interface.
- Headings and labels that match visible actions.
- Empty, loading, error, and success text that is specific.
- Over-explaining caused by weak structure.

Common fixes:

- Move explanatory copy closer to the decision point.
- Replace generic CTAs with action-specific verbs.
- Remove helper text that repeats the control label.
- Hand off to `ux-writer` when the words are the main issue.

## 10. Generic AI UI Tells

Flag these when they make the work feel templated or unearned:

- Purple/blue gradient hero with centered text and generic cards.
- Inter, Arial, or default system font used without a reason on public-facing creative work.
- Nested cards, uniform rounded rectangles, and icon tiles above every heading.
- Glassmorphism, glow, grain, or blur used as decoration rather than function.
- Same-size cards for content with clearly different priority.
- Corporate filler copy such as "unlock insights" or "seamless experience."
- Decorative dashboards with fake metrics but no user task.
- Over-polished UI that lacks error, empty, disabled, or responsive states.

Do not stop at naming the tell. Always propose the specific replacement.

## Artifact Routing

- Direct answer: short explanation, command, status, or plain advice.
- Markdown: prompts, code, specs, logs, schemas, or LLM re-ingestion.
- Shareables: local human-facing artifacts that need scanning, comparison, review, copy/export, or public-safe packaging.
- ChatGPT Apps: Apps SDK projects with MCP server tools and widget UI.
- Full app plan: persistent state, backend behavior, complex editing, or app-like workspace interaction.

Use the smallest artifact lane that serves the human.
