---
name: updater-recovery
description: "Diagnose Codex desktop update or disk-capacity failures and verify a bounded recovery."
---

# Updater recovery

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


Diagnose Codex desktop update or disk-capacity failures and verify a bounded recovery.

## Complete procedures to load

Select by the triggers below. Read the complete chosen procedure and its required support; skip unrelated variants. These links preserve the full methods.

- [Full update recovery](../mac-environment-conventions/references/codex-storage-and-updates.md) — For an updater or capacity-related failure; protected paths and bounded recovery.

## Workflow

1. Inspect actual free space, separate support/session roots and updater evidence.
2. Apply the full safe-target and do-not-relocate rules; preserve active sessions, credentials and databases.
3. Check redirected/moved data and retry the update within the requested scope, verifying the running build or updater result.

## Deliver and verify

Return actual capacity/recovery and update state. Do not equate freed space with a completed update.

## Example boundary

Good: connect a no-space updater log to internal disk capacity. Bad: reset account credentials because a download failed.

Use current host facts rather than assuming historical absolute paths apply elsewhere. Work Management owns task coordination; Master Security owns software/permission threat review. Existing authorization carries through routine reversible steps.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports IT Operations Specialist. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
