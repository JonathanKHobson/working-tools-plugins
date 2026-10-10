# Component coverage and contracts

Use while inventorying a kit or specifying an affected component. Account for relevant families without manufacturing work. Existing project requirements determine which families are implemented, documented or deferred.

## Coverage map

| Family | Typical members | Contract questions that prevent omissions |
| --- | --- | --- |
| Actions | Primary, secondary, quiet/tertiary, destructive, icon, split and toggle buttons; links | Action or navigation? Priority within which action group? Pending, repeat click, selected, unavailable and recovery behavior? |
| Text entry | Text, textarea, password, email, phone, numeric/amount, search | Label, hint, example, validation timing, autocomplete/input mode, parse vs display, clear/reveal, long content, privacy? |
| Selection | Native select, listbox, combobox, checkbox/group, radio/group, switch | Single/multiple/tri-state? Selection vs immediate setting? Search and no results? Keyboard model and controlled value? |
| Disclosure | Accordion, details, popover, tooltip, menu, dialog, drawer | Trigger semantics? Modal or nonmodal? Placement, dismissal, focus return, outside interaction, nested layers? |
| Navigation | Header, sidebar/rail, mobile disclosure, tabs, breadcrumbs, pagination, stepper | Location vs panel? Deep links, active/current state, overflow, resize transitions, completed steps and back behavior? |
| Feedback | Inline help/error, error summary, banner, alert, toast, badge, progress, skeleton | Urgency, announcement, persistence, timeout, dismissal, retry and origin of success? |
| Content and containers | Cards, panels, lists, dividers, avatars, icons, hero, section/frame, footer | Structure and reading order? Click target vs nested controls? Meaningful vs decorative image? |
| Data and discovery | Tables, grids, sorting, filters, search results, saved views | Empty/loading/error/stale? Keyboard model? URL state, reset, counts, pagination and mobile strategy? |
| Files and time | Upload, attachment, date entry, calendar, date range, time picker | Types/limits, progress/cancel/retry, timezone/locale, invalid ranges, accessible manual entry? |
| Advanced, only when needed | Tree, slider, range, command palette, editor, resizable panels, chart, carousel | Does a native or simpler pattern meet the task? Full navigation, non-drag alternative, discoverability and rendering cost? |
| Page patterns | Onboarding, authentication, account, settings, learning, commerce, editorial, dashboard | End-to-end context, service boundaries, first visit, error recovery, empty and repeat visit? |

“Card”, “drawer”, “chip” and “toast” describe presentations, not automatic ARIA roles. A route tab, panel tab and segmented value selector need different semantics even if they look alike. Select a semantic interaction before drawing its skin.

## Contract fields

Assign a stable ID and owner. For each relevant component record:

- Purpose, suitable uses, exclusions, status and dependencies.
- Anatomy and slots; actual import/export, selector or native symbol; verified design-library node when one exists. Clearly label proposed APIs.
- Variants and orthogonal axes: intent, emphasis, size, density, theme, orientation, expression and state. State allowed combinations and precedence; avoid a separate handcrafted asset for every permutation.
- Geometry: units, min/preferred/max dimensions, hit area vs visible bounds, padding, gap, radius, borders, icon size, line height, wrapping, overflow, focus ring width/offset, and constraints under text growth.
- Content: label, description, placeholder, help, error, empty, pending, success and recovery copy; localization and bidirectional text where supported. Placeholders do not replace labels.
- State transitions: trigger, visible result, semantic/ARIA change, authoritative data condition, focus movement, cancellation and clearing condition.
- Input: keyboard, pointer, touch, pen and assistive technology as relevant. Identify unavailable modes without claiming them tested.
- Adaptation: content-driven sizing, container/viewport changes, safe areas, reduced motion, forced colors, text spacing, zoom and relevant locale.
- Examples: ordinary use, one difficult use, isolated adoption and multiple instances if reusable behavior exists.
- Evidence and limitations: exact tested states/environments, source/test identities, unresolved defects, visual acceptance scope and next gate.

## State grammar

Consider rest, hover where available, focus-visible, active/pressed, selected/checked, expanded, disabled, read-only, invalid, pending, success, error and no-op. These are not all mutually exclusive: a focused invalid field and a selected disabled option are possible. Define visual precedence without suppressing necessary meanings. “Unclicked” is usually rest, while “pressed” is transient activation; persistent selection is a separate value state.

Disabled and read-only communicate different capabilities. Specify whether unavailable actions remain focusable to explain requirements; choose semantics deliberately. Pending may preserve focus while blocking duplicate submission. Never infer success from animation completion. A local demo must identify its local outcome.

For forms, distinguish untouched, touched, editing, valid/invalid, submitting, server-rejected and saved. Keep the entered work after recoverable failure. A user-selected skip is different from unanswered; missing task material cannot be repaired by adding a rating widget.

Use the [record template](ui-kit-records.md) for affected components. A broad coverage map can remain concise; the implemented slice requires complete contracts.
