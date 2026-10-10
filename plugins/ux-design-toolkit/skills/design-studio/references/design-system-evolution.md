# Evolving an existing design system

Use when a maintained product's system needs inventory, extraction, normalization or migration. A routine one-screen or small fix does not need this; go to [system craft checks](system-craft.md) instead.

## Find current authority before writing anything

Missing PRODUCT.md or DESIGN.md does not mean the system is undefined. Inspect shipping components, token files, theme providers and the routes that actually render. They establish current behavior, while the user's approved design and task requirements establish intended behavior. A stale document is a hypothesis to check, not a reason to discard current constraints. When sources disagree, record Change / Keep / Defer and preserve the user's chosen authority rather than assuming that whatever shipped is correct.

Inventory only the scope the task touches: the component/token family and its known call sites. Do not catalog the whole system for a change to one family. Record, per item: current values/variants in use, where they are consumed, and any inconsistent duplicate that has drifted from the nominal definition.

## Normalize and migrate by intent, not shape

Group variants by the interface or role they actually serve (for example "destructive action," "secondary surface," "compact table row"), not by superficial visual similarity such as matching hex values or matching corner radius. Two components that look alike but serve different intents (a disabled state versus a muted informational tag) should not be collapsed into one token just because they render similarly today. Two components that look different but serve the same intent (an inline error and a toast error) are candidates for consolidation if the task calls for it.

When migrating call sites to a normalized token or component, migrate by matching the original *intent* of each call site to the new definition, not by pattern-matching old class names or prop shapes. State the intent match explicitly (for example "these five buttons all trigger irreversible deletion, mapped to `destructive`") so the mapping can be checked.

## Check incrementally, not exhaustively

After normalizing, verify a representative sample of affected surfaces rather than every call site: pick instances that cover each distinct context (dense table, form, empty state, dark mode if applicable) and confirm the rendered result still matches the original intent with no regression. Do not claim full-system verification from a sample; state which representative instances were checked and which remain unverified.

## Do not over-scaffold

A maintained product that already has working conventions does not need a new PRODUCT.md/DESIGN.md, a rebuilt component library, or a new governance document produced to fix one inconsistency. Reserve new system documentation for cases where the task is explicitly to establish or repair that documentation, or where the extracted intent mapping itself is the deliverable and needs to be recorded for future migrations. Otherwise, make the fix in the existing system and note the drift you found without generating scaffolding nobody asked for.

## Provenance and scope

Original local synthesis addressing gaps identified when comparing existing UX guidance against Impeccable's existing-system and extraction methods (source inspected via [design sources](design-sources.md), revision 114ea1d, 2026-09-29). No Impeccable text, scripts or extraction tooling is reproduced; this is local judgment guidance only.
