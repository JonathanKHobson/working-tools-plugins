---
name: app-window-recovery
description: "Recover an app that is running without a usable window while preserving user state."
---

# App window recovery

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


Recover an app that is running without a usable window while preserving user state.

## Complete procedures to load

Select by the triggers below. Read the complete chosen procedure and its required support; skip unrelated variants. These links preserve the full methods.

- [Window recovery](../../references/recovery/invisible-window-or-app-open-with-no-window.md) — When the app runs without a usable window; the least-destructive recovery sequence.
- [Narrow reset](../../references/recovery/narrow-reset-pattern.md) — Only when ordinary window/relaunch recovery fails and a scoped state reset is needed; backup and rollback rules.
- [Evidence collection](../../references/recovery/evidence-to-collect.md) — When diagnosing an unclear failure or handing it off; the observations needed to distinguish causes.

## Workflow

1. Confirm app/window/process evidence and identify main app, helper and headless processes.
2. Follow the full least-destructive recovery sequence; preserve unrelated sessions.
3. If a narrow state reset is necessary, back up exactly the affected files and verify the reopened app.

## Deliver and verify

Report usable window and interaction evidence separately from a merely running process, with backup location for touched state.

## Example boundary

Good: request a normal new window before resetting support files. Bad: delete the whole app profile to fix window placement.

Use current host facts rather than assuming historical absolute paths apply elsewhere. Work Management owns task coordination; Master Security owns software/permission threat review. Existing authorization carries through routine reversible steps.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports IT Operations Specialist. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
