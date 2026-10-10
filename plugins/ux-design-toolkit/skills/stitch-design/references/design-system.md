# Stitch Design System

Use [Workbench](workbench.md) to establish the live project. Inspect representative pages before defining a system.

1. Identify the authoritative source: existing implemented tokens, an approved Figma library, an attached Stitch theme, or an accepted reference design. Preserve intentional audience differences. Do not let a newly generated theme silently replace the approved one.
2. Inventory the small set that controls continuity: type scale and line length; semantic colors; spacing; radii; surfaces; imagery/crop style; icon family; focus treatment; motion; and component states. Record actual values when available, and distinguish inferred values from exported values.
3. Define the shared shell once: logo/home target, global header height, menu destinations/order, mobile disclosure behavior, contact action, footer, and sticky offsets. Define page-local navigation separately. A case-study contents list must not impersonate or overwrite global navigation.
4. Map intentional exceptions to a reason. An event page may have different artwork and accent colors while keeping wayfinding and interaction conventions. Do not flatten distinct businesses, portfolios, or brands into one entity.
5. Apply the system to one representative page and one contrasting subpage. Check the shortest and longest real labels. Then propagate through shared implementation components rather than manually drifting copies.
6. If current UI offers theme or DESIGN.md import/export, inspect the file before use. Current DESIGN.md specifications may include machine-readable YAML tokens plus prose; verify the current official spec when authoring a portable file. Do not assume an older prose-only template remains conformant. Never add a server solely to use this manual workflow.
7. Reconcile generated output against the authoritative tokens before integration. A prompt, theme, and imported stylesheet must not compete as three conflicting sources.

## Verification

Use [Design review](design-review.md) for anchors and responsive checks. Confirm every navigation destination remains visible or intentionally accessible through the menu, keyboard usable, and correctly linked. A no-horizontal-overflow result alone cannot establish this.

Deliver a compact token/component map, documented exceptions, and the verified pages. Keep DESIGN.md only when it is a useful reusable artifact, not ceremonial paperwork.
