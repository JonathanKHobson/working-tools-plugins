---
name: stitch-flow-prototyping
description: Map and test a multi-screen Stitch journey with navigation, forms and recovery states. Use when connecting screens or defining interaction before implementation.
---

# Stitch Flow Prototyping

Use [Workbench](../stitch-workbench/SKILL.md) to inspect the current interface and [Design system](../stitch-design-system/SKILL.md) for shared components.

1. Choose one audience and task with a start and a successful finish. Map the minimum screens and branch states. Use real content, including long labels, missing data, and interrupted progress.
2. Separate navigation from actions: global destinations, page-local anchors, disclosures, form submissions, external booking/contact, and back/cancel behavior. Preserve a clear route home and predictable browser history when implemented.
3. Create linked screens using currently observed prototype controls, if available. If the tool only produces separate screens, record the intended links explicitly; do not claim the flow is interactive.
4. Test the happy path plus important alternate paths: invalid input, empty/loading, unavailable destination, back/cancel, recovery, and completion. Include keyboard and focus expectations in the handoff, even when the prototype cannot implement them.
5. For contact flows, specify visible labels, required/optional fields, input errors, sending lock, duplicate prevention, preserved text after failure, success status, retry guidance, and fallback contact. Include network timeout, rate-limit, and server-error states if the chosen integration can produce them.
6. Do not submit real forms or messages merely to test a design. Use mocked/local tests where sufficient; perform a real delivery test only within existing user authorization. A simulated success message or API acknowledgement does not prove inbox delivery.
7. Record what is interactive, simulated, static, or not yet built. Keep essential instructions and status accessible without relying on motion, color, or hover alone.

## Handoff

Deliver the flow map, screen/state references, actual prototype location, tested paths, and implementation requirements. Use [Export handoff](../stitch-export-handoff/SKILL.md) to verify files and [Design review](../stitch-design-review/SKILL.md) to inspect the implementation. Do not label a prototype production-ready because its screenshots look finished.
