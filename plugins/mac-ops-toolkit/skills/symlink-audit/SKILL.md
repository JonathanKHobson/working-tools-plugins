---
name: symlink-audit
description: "Inspect a broken or confusing filesystem redirect and distinguish storage policy from runtime locks or sockets."
---

# Symlink audit

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


Inspect a broken or confusing filesystem redirect and distinguish storage policy from runtime locks or sockets.

## Complete procedures to load

Select by the triggers below. Read the complete chosen procedure and its required support; skip unrelated variants. These links preserve the full methods.

- [Full symlink rules](../mac-environment-conventions/references/symlink-rules.md) — For a redirect audit or repair; permitted link behavior and native-path exceptions.
- [Storage role context](../mac-environment-conventions/references/storage-layout.md) — When the link crosses drives; resolve the target volume before repair.

## Workflow

1. Inspect the link itself, its target, target mount and permissions without following an assumed similarly named volume.
2. Use the full rules and current catalog evidence; separate runtime singleton links from persistent storage redirects.
3. Repair only the authorized incorrect link after preserving original target information; check consumer access.

## Deliver and verify

Return exact link/target evidence and consumer verification, with unresolved mount dependencies explicit.

## Example boundary

Good: distinguish archive-volume label from runtime-volume label before a redirect. Bad: treat every nested socket symlink as a migration candidate.

Use current host facts rather than assuming historical absolute paths apply elsewhere. Work Management owns task coordination; Master Security owns software/permission threat review. Existing authorization carries through routine reversible steps.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports IT Operations Specialist. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
