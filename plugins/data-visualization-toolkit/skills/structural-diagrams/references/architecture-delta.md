# Explain a topology change without inventing movement

Use for a migration, service extraction, integration or deployment redesign with two evidenced system states. If only attributes change, use a comparison table. A before/after diagram alone does not establish migration order, causality, downtime or rollback safety. For repository evidence, read [repository-evidence](repository-evidence.md).

## Build the comparison

1. Name the two snapshots with versions/dates and establish their sources. Give each persistent component and relationship a stable ID independent of its label, geometry and display order. A renamed surviving object retains its ID; a replacement gets removal/addition IDs. Never recycle an ID across component/relationship kinds.
2. Start After from Before's coordinates and scale. Keep retained objects stable unless movement is itself meaningful. Use aligned views with a shared internal coordinate system; independently auto-layouting both states can manufacture an apparent change. For a large system, split into named subsystems while preserving necessary edges and an overview. A numeric node quota must not remove facts.
3. Compare presence, semantic attributes, component position and ordered relationship endpoints separately. A connection can reroute to meet a moved component without changing its relationship identity. A changed display name belongs to semantic change when it matters to the story.
4. Produce an exact change ledger: one entry per (stable ID, change kind), naming the old and new value or relationship. Do not include unchanged objects or use vague “updated” entries. An object can have two changes, such as changed and moved.
5. Draw Before / Changes / After with comparable dimensions and clear reading order. Use quiet unchanged context, labels plus non-color markers for differences, and brand-appropriate colors. Keep text readable; use a focused/scrollable accessible comparison on narrow screens rather than shrinking labels. Print/export should preserve the comparison and ledger together.

| Change | Meaning | Required explanation |
|---|---|---|
| ADDED | Present only after | New object and responsibility/relation |
| REMOVED | Present only before | Removed object and consequence |
| CHANGED | Same ID, different semantic attributes | Explicit old → new values |
| MOVED | Same component, different meaningful position | Relocation; distinguish diagram rearrangement |
| REWIRED | Same relation, different ordered endpoints | Old source/target → new source/target |

Use text and a badge, shape or line treatment in addition to color. A removed node needs a removal entry, not just absence from After. Do not substitute an added edge for a rewire to avoid explaining identity.

## Optional machine-readable contract

When repeated comparison/validation merits structured data, retain for each object: snapshot, kind, stable ID, status set, semantic signature, bounds for components, and source/target IDs for relations. Signatures describe relevant semantic attributes deterministically; exclude ID, snapshot, status, color, coordinates and endpoints. Keep attribute ordering stable. Only a semantic change changes that signature. Preserve meaningful size changes as an explicit property rather than silently treating them as movement.

Presence dictates added/removed; retained IDs keep kind. Changed signatures must match CHANGED entries; meaningful component movement must match MOVED; ordered endpoint changes must match REWIRED. Endpoints resolve within their own snapshot. A route bend alone is not a rewire. Ledger pairs must exactly match declared changes, with no duplicates or unknown IDs. This local method does not claim compatibility with an upstream HTML validator or require an extra runtime.

## Acceptance

Cross-check the two inventories, semantic attributes, endpoint sets and ledger against the actual sources. Verify that unchanged positions remain stable, all required relations survive, every change has redundant visual encoding, and connector endpoints meet the right objects. Inspect rendering for collisions, hidden/occluded labels, crossings, legibility and narrow-screen navigation. Check keyboard/text alternatives where interaction is provided. Attribute correctness does not establish browser rendering or truth of a migration story. Report those separately; keep actual migration sequencing and rollback in their own operational plan.

Adapted from [Diagram Design architecture delta](https://github.com/cathrynlavery/diagram-design/blob/f903933a534ba92cde1c85a28186267b3a317bb2/skills/diagram-design/references/type-architecture-delta.md), MIT. [Notice](diagram-design-LICENSE.txt). Retained complete identity/change/ledger procedure; excluded upstream fixed palette, arbitrary budgets, mandatory onboarding/profile mutation, HTML-specific grammar, scripts and all other diagram families already owned by this toolkit.
