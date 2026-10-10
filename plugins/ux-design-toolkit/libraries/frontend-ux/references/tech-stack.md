# Tech Stack Reference

Use this file when the task involves framework tradeoffs, stack-specific UX risks, or frontend-system decisions.

## Selection heuristic

Choose based on the product shape first:

- content-heavy or SEO-sensitive app
- form-heavy workflow
- performance-critical interface
- design-system-driven product
- prototype that still needs UX guardrails

Team familiarity matters because rushed implementation quality often becomes UX debt.

## Recommended profiles

### React + Next.js + Tailwind + Storybook + Playwright

Best for medium to large product teams and component-driven apps.

Strengths:

- strong ecosystem for accessible primitives
- SSR and streaming patterns can improve perceived performance
- Storybook helps document states before they are forgotten
- Playwright plus accessibility tooling helps catch regressions

Risks:

- client-heavy rendering can hurt initial load if overused
- utility-class sprawl can hide state logic and accessibility issues
- component libraries can drift when stories are stale

Use this stack well by:

- reusing accessible primitives instead of rebuilding widgets from scratch
- mapping colors, spacing, and type to tokens instead of inline values
- documenting loading, empty, error, and disabled states in stories

### Vue + design system + Storybook + Playwright

Best for teams prioritizing readability and steady delivery.

Strengths:

- template syntax keeps structure and semantics easy to inspect
- scoped styling reduces accidental inconsistencies
- strong fit for progressively enhanced interfaces

Risks:

- smaller accessible-component ecosystem than React
- custom component abstractions can hide missing ARIA wiring

Use this stack well by:

- favoring composables for shared UX behavior
- auditing custom `v-model` components for labels, descriptions, and error semantics

### SvelteKit + design tokens + accessibility-first patterns

Best for lean, fast interfaces where bundle size and responsiveness matter.

Strengths:

- smaller bundles can improve real-world UX on slower devices
- direct reactivity reduces some UI state bugs
- route and page metadata are straightforward to manage

Risks:

- fewer mature accessible primitives
- more manual work for complex widgets and focus management

Use this stack well by:

- linting for accessibility from the start
- manually checking route-transition focus behavior
- testing widget behavior with keyboard and screen reader, not just visual inspection

### Remix + semantic HTML + progressive enhancement

Best for form-heavy products and resilient web-native workflows.

Strengths:

- strong default behavior without large client-side abstractions
- native forms reduce custom-validation mistakes
- browser behaviors like history and submission patterns stay predictable

Risks:

- requires discipline with web fundamentals
- smaller component ecosystem

Use this stack well by:

- leaning into native form controls and field grouping
- returning accessible server-driven validation states

### AI-generated or vibe-coded UI

Best for prototypes only if followed by a strict UX review pass.

Common risks:

- non-semantic markup
- missing labels and focus handling
- inconsistent spacing and color choices
- absent empty, error, and loading states
- poor mobile behavior

Minimum follow-up audit:

- replace fake buttons and links with semantic elements
- add labels, status messaging, and recovery copy
- normalize values into design tokens
- test keyboard flow, narrow screens, and edge states

## Universal principles

- Semantic HTML first.
- Design tokens over raw values.
- Keyboard and focus before hover polish.
- State coverage before animation.
- Shared components should document behavior and extremes, not just happy paths.

## Component documentation standard

Each component should make these visible somewhere, usually Storybook or equivalent:

- what the component is for
- when to use it and when not to
- supported props and defaults
- accessibility notes
- default, loading, empty, error, and disabled states
- extremes such as long text, many items, or narrow widths
