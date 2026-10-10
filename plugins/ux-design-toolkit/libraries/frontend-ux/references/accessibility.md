# Accessibility Reference

Use this file for accessibility audits, widget behavior checks, or any frontend task where WCAG or ARIA details matter.

## Core rules

- Ensure all functionality works by keyboard.
- Keep focus visible. Do not remove outlines without a clear replacement.
- Use semantic HTML first; add ARIA only when native elements are insufficient.
- Associate every form control with a visible `label`.
- Do not rely on color alone for meaning.
- Provide text alternatives for images and icons when they convey meaning.

## WCAG 2.2 priorities

### Perceivable

- Use meaningful `alt` text for informative images and `alt=""` for decorative images.
- Meet contrast targets:
  - text: at least 4.5:1
  - large text and UI components: at least 3:1
- Support reflow at narrow widths without horizontal scrolling where possible.
- Avoid text embedded in images when real text can be used.

### Operable

- Keep tab order aligned with visual order.
- Avoid keyboard traps.
- Provide skip links for repeated navigation on larger page shells.
- Ensure touch targets are large enough to activate reliably.
- Let users pause or stop auto-updating or auto-playing content when relevant.

### Understandable

- Use clear labels and instructions.
- Do not trigger unexpected navigation or submission on focus or simple input changes.
- Show validation errors in text and explain how to recover.
- Avoid asking the user for the same information repeatedly within a flow.

### Robust

- Use valid HTML, unique IDs, and correct element nesting.
- Expose name, role, and value for custom widgets.
- Announce status changes programmatically when content updates dynamically.

## Widget patterns

### Dialog / Modal

- Move focus into the dialog on open.
- Trap focus while open.
- Close on `Escape`.
- Return focus to the trigger on close.
- Provide an obvious dismiss action.

### Accordion

- Toggle `aria-expanded`.
- Connect trigger and content with `aria-controls` and `aria-labelledby`.
- Keep headers keyboard reachable.

### Tabs

- Use `tablist`, `tab`, and `tabpanel`.
- Keep only the active tab in the natural tab order.
- Support arrow-key movement between tabs.

### Combobox / Autocomplete

- Keep focus in the input.
- Use `aria-expanded`, `aria-controls`, and `aria-activedescendant` correctly.
- Support arrow keys, `Enter`, and `Escape`.

### Alerts and status messages

- Use `role="alert"` for urgent errors that must interrupt.
- Use `role="status"` or polite live regions for confirmations and background updates.
- Do not hide critical messages before a user can read them.

## Common failures

- Clickable `div` instead of `button`
- Placeholder used as the only label
- Icon-only button without accessible name
- Invisible or low-contrast focus state
- Modal without focus management
- Error indicated only by color
- Toast that disappears before it can be perceived
- Positive `tabindex` values used to force tab order

## Manual checks

### Keyboard-only

- Tab through the full flow.
- Confirm all interactive elements are reachable.
- Confirm focus is always visible.
- Confirm dialogs and menus can be exited.

### Screen reader spot check

- Confirm the page title and heading structure make sense.
- Confirm buttons and links have descriptive names.
- Confirm form hints and errors are announced.
- Confirm dynamic updates are announced when necessary.

## Tooling

- Use axe DevTools or axe-core for automated checks.
- Use Lighthouse as a secondary audit, not the only audit.
- Pair automated checks with manual keyboard and screen-reader testing.
