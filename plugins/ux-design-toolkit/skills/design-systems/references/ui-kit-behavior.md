# Behavior, isolation and adoption

Use when a component is intended for reuse or a non-happy path changes. The showcase is one consumer, not the component runtime.

## Independent adoption

Separate reusable behavior, page bootstrap and demonstration services. Initialize within an explicit root and avoid returning from the whole initializer because an unrelated specimen is absent. Absence of a component family is normal; a component declaring a missing required target is a configuration defect that needs a diagnosable result.

Exercise a fixture containing only the target component and another containing two instances with distinct IDs and independent state. Define repeated initialization, teardown, route remount and listener ownership where the host lifecycle needs them. Avoid duplicate listeners, global ID collisions and accidental cross-instance updates. State and focus must stay with the intended instance.

Provide actual imports or selectors and minimal required markup, styles, tokens and dependencies. A component that works only when the full gallery is present is not independently reusable. A framework wrapper does not inherit proof from a native fixture automatically; test its mounting and prop/update behavior.

## Actions and feedback

Define pending, confirmed success, unchanged/no-op, failure and retry using the authoritative operation, not a timeout. Keep feedback on the invoking control when useful and give it a screen-reader equivalent. Preserve work and focus during pending. Consider edits made before a delayed response, cancellation, repeat clicks, out-of-order responses and navigation away. A stale response must not confirm a newer unsaved edit.

Make each state observable in a bounded fixture. Local demonstrations must say what they actually save or simulate. Do not claim a backend, account, email, payment or search service exists merely because a control looks complete.

Messages have distinct triggers and lifetimes. Inline validation may persist until corrected; a temporary toast may acknowledge an event. A banner may describe a broader condition. Do not remove one as duplicate without understanding its purpose. Critical recovery should not depend solely on a disappearing message. For announcements choose urgency and repetition deliberately, preserving native semantics and avoiding unnecessary interruptions.

## Disclosure contracts

- **Tooltip:** supplemental information only. Check keyboard access, pointer transit across the trigger/content gap, persistence, dismissal, blur/re-entry and viewport edges. Escape should dismiss the visible tooltip without stealing focus where that is the contract. Judge the actual [hover/focus criterion](https://www.w3.org/WAI/WCAG22/Understanding/content-on-hover-or-focus.html), including its exceptions; a decorative gap alone is not the full finding.
- **Menu/popover:** establish menu vs ordinary disclosure semantics; test opener, interior and outside interactions, placement, return focus and immediate Escape. Keep essential information available without hover.
- **Dialog/drawer:** determine modality, accessible name, initial focus, containment where appropriate, close/cancel behavior, background interaction, scroll and focus return. Nested overlays need explicit ownership.
- **Accordion/details:** preserve heading structure, expanded relationships and meaningful tab order. Critical instructions or unresolved errors should not disappear into an unexplained closed region.
- **Tabs:** distinguish panel selection from route navigation. Choose and document activation behavior; ensure selected/focused meanings remain distinguishable and offscreen focus is revealed.

Use native semantics where they meet the task. Consult the [WAI-ARIA Authoring Practices patterns](https://www.w3.org/WAI/ARIA/apg/patterns/) for the selected composite interaction; examples are starting patterns and still require testing in the actual product.

## Content is part of the workflow

The example must provide the information required to act. A compare-and-rate flow needs both things being compared before the question. Search needs a defined query/results/no-results/recovery path. Optional questions distinguish unanswered, selected and skipped. Inputs need meaningful labels, examples, hints and validation without inventing universal phone, currency or address formats.

Choose password reveal, autocomplete, phone country context, numeric parsing, locale and timezone behavior according to real tasks. Do not use numeric input for identifiers merely because they contain digits. Keep clipboard/password-manager support unless a justified requirement says otherwise. Content and behavior review belongs alongside visual review, not after the page is frozen.
