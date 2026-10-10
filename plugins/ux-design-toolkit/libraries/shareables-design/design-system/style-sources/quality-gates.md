# Style Source Quality Gates

V5.6 turns contrast, type size, focus, spacing, and dark-theme behavior into shared design-system gates instead of one-off visual QA feedback.

## Global Gates

- Every style source needs contrast-paired text, surface, control, and focus roles.
- Body text should stay at 16px or larger.
- Functional labels, overlines, chips, control labels, and wayfinding text should stay at 14px or larger.
- Focus-visible states are required on links, buttons, tabs, segmented controls, form fields, and copy/export controls.
- Fixed-width or dense content needs responsive constraints or an overflow wrapper.
- Catalog docs, registry records, explorer cards, thumbnails, and rendered previews must agree on runtime status.
- Each style source should declare its default design dials: variance, motion,
  density, and reference source. Rendered previews should make those choices
  visible rather than relying on prose.
- Research/current-web artifact styles need visible slots for date window,
  source coverage, uncertainty, excluded sources, and inline source chips.
- Review-loop or annotation-assisted authoring must stay out of exported style
  sources: no shipped annotation chrome, local queue endpoint, Lavish SDK,
  `localhost` reference, or copied CDN fallback when a registered style source
  or project token set exists.

## Source-Specific Gates

| Style source | Dark status | Required contrast posture |
|---|---|---|
| `shareables-foundation` | Not dark | Ink-first hierarchy on warm off-white paper, compact headings, 8px frames, visible source/caveat and fallback areas. |
| `core-utility` | Not dark | Neutral surface, readable muted text, practical focus ring. |
| `warm-editorial` | Light style with dark panels | `paper-dim` or `paper` on dark panels; `leaf` or `ink` for connectors/overlines; `teal` decorative-only on paper. |
| `structured-bridge` | Not dark | Dense reference layouts with guarded tables, wrapping chips, and readable labels. |
| `product-studio` | Not dark | Product controls preserve 44px targets, status chips wrap, and dashboard toolbar density stays readable. |
| `dark-analytics` | Runtime promoted after V5.6 repair | Dark toolbar/control surfaces, readable unselected states, bright selected states with deep text, no white-on-light control failures. |
| `research-academic` | Not dark | Citation blocks, appendix tables, footnote labels, and source chips remain readable in print and mobile. |
| `annotated-portfolio` | Not dark, with optional dark reel panels | Terracotta is the primary CTA/selected-state color; steel is systems/annotation-only. Proof metrics, verification labels, method chips, artifact placeholders, and confidentiality notes remain readable on warm paper, cards, and printed pages. |
| `warm-field-report` | Not dark, with evidence/code panels | Field-report rail links, audio controls, code/evidence panels, byte comparisons, and status labels stay ink-first, focus-visible, print-safe, and at least 14px for functional text. |

## Feedback Sources

- `design-system/reviews/warm-editorial-website-ux-audit-2026-05.md`
- `design-system/research/shareables-design-system-contrast-spacing-feedback.md`
- `design-system/research/svg-visual-language-gate/quality-bar-study-warm-editorial.md`
