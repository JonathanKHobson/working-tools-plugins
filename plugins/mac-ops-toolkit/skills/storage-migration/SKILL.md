---
name: storage-migration
description: "Find what is taking Mac disk space, clean up authorized caches or unused runtimes, and move large files externally with verified volume identity, copy integrity and rollback."
---

# Storage migration

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


Diagnose Mac disk usage, remove authorized regenerable material, and carry out storage moves with verified volume identity, copy integrity and rollback.

## Complete procedures to load

Select by the triggers below. Read the complete chosen procedure and its required support; skip unrelated variants. These links preserve the full methods.

- [Storage roles](../mac-environment-conventions/references/storage-layout.md) — Before choosing a destination drive; verify volume roles and identity.
- [Install targets](../mac-environment-conventions/references/install-targets.md) — When choosing where an app or runtime should live; concrete placement roots.
- [Symlink constraints](../mac-environment-conventions/references/symlink-rules.md) — Before adding or changing a redirect; native-path and consumer constraints.
- For capacity cleanup, managed runtimes or moves while projects are active: [Cleanup and migration verification](../../references/recovery/storage-cleanup-and-migration.md).

For a requested backup recoverability check, read [bounded backup restore drill](../../references/recovery/backup-restore-drill.md). Test selected files into an isolated destination; storage inspection or a backup timestamp alone does not prove recovery.

## Workflow

1. Verify the source's actual filesystem, owning app/project, mounted destination and existing storage convention. Measure before choosing deletion, archive or a live redirect.
2. Apply the full storage and symlink rules; copy and verify before retiring a source. Preserve native directories that must remain real.
3. Check readability, writable state where needed and the app’s actual use of the moved material.

## Deliver and verify

Record source, destination, copy/permission checks and rollback. Report logical bytes handled separately from the measured change in free space. A completed copy does not prove the app uses it; a prepared finalization script is still pending.

## Example boundary

Good: retain the native Downloads directory and archive authorized contents. Bad: replace a required real workspace root with a symlink.

Use current host facts rather than assuming historical absolute paths apply elsewhere. Work Management owns task coordination; Master Security owns software/permission threat review. Existing authorization carries through routine reversible steps.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports IT Operations Specialist. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
