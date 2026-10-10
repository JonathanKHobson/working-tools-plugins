# Context adaptation beyond responsive shrinking

Use when a surface must adapt across device, input method, orientation, locale or user context. This is more than a responsive layout pass: reflow, target size and narrow-width checks already covered in [verification](verification.md) and [product and web](product-web.md) are necessary but not sufficient.

## Adapt to the actual target context

Identify the real dimensions of variation for this task rather than assuming "shrink the layout" covers them: input method (touch, mouse, keyboard-only, stylus, voice), priority shift (what matters most changes between a quick mobile glance and a focused desktop session), navigation model (bottom nav vs. sidebar vs. command palette), orientation (portrait/landscape, and what should reflow versus what should stay fixed), and safe areas on devices with notches, home indicators or rounded corners. State which of these actually apply to the surface in scope; do not exercise dimensions the product doesn't have.

For touch versus pointer, confirm hover-dependent affordances (tooltips, hover-reveal menus, hover states as the only cue) have a working touch equivalent, not just a smaller hit target. For safe areas, confirm interactive controls and essential content are not obscured by device chrome or camera cutouts on the actual platform in scope.

## Internationalization and locale-sensitive data

Where multiple locales are in scope, test actual translated or representative expanded/contracted text for clipping and overlap. For RTL locales, distinguish direction-sensitive navigation and layout from assets that must retain their shape; test mixed-script text and bidirectional numbers in context rather than blindly mirroring all icons or forcing every numeral LTR. Check dates, numbers, currency and units with the intended locale. Do not add localization scaffolding when the task does not require it.

## Deliberate subtraction, not just fitting

Remove information, choices or containers that are redundant in the target context while preserving necessary domain complexity. A repeated explanation or empty wrapper may be removable; an icon's presence does not make its visible label redundant. Check meaning, discoverability, accessibility and the real outcomes of actions before subtracting them. Do not remove a needed filter, disclosure or domain field merely to fit a narrower viewport. That would change the product rather than adapt its presentation.

## Boundaries with other specialists

Graphic campaign adaptation (posters, social crops, print formats) stays with Graphic Design Studio; this reference covers interactive product/web adaptation only. Native platform-specific implementation (native safe-area APIs, platform navigation containers, native RTL mirroring behavior) stays with the relevant native platform specialist per [device routing](device-routing.md); this reference sets the design judgment, not the native code.

## Cross-context checks must exercise the actual path

A claim that a surface "adapts" needs the real path exercised at the relevant breakpoints/orientations/locales/input methods for this task, not an assumption from a single desktop mouse-driven review. State which contexts were actually checked and which remain unverified.

## Provenance and scope

Original local synthesis addressing gaps identified when comparing existing UX guidance against Impeccable's context-adaptation review methods (source inspected via [design sources](design-sources.md), revision 114ea1d, 2026-09-29). No Impeccable text or tooling is reproduced.
