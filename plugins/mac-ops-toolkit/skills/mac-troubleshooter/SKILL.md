---
name: mac-troubleshooter
description: "Diagnose Mac app launch, window and process failures, then apply the smallest reversible fix; use for unexplained failures or toolkit first-use help."
---

# Mac Troubleshooter

For “what can Mac Operations Toolkit do?”, setup or getting-started help, read the capability, first-task and setup sections of the [plugin introduction](../../README.md) and recommend one relevant first task; skip maintainer notes unless updating the package. Help alone does not start a diagnosis, scan, audit or external action. For a concrete request, use the matching procedure below without loading the whole plugin.


## Overview

Use this skill for Mac-specific troubleshooting on this machine when
the goal is to diagnose first, preserve user state where possible, and apply the
smallest safe fix before escalating.

This skill is especially useful for GUI apps that appear open without a visible
window, stale background or headless processes, stuck launch state, login item
conflicts, and narrow resets of app support data.

## Workflow

1. Confirm the symptom with local evidence.
   Check whether the app is running, whether macOS sees it as visible/frontmost,
   whether it has windows, and whether the active process is actually the GUI app
   or a stale helper/headless process.
2. Prefer the least-destructive recovery first.
   Try normal activation, explicit new-window creation, and a clean relaunch
   before touching user state.
3. Back up before resets.
   If app support files, preferences, or session state might be changed, create a
   timestamped backup first.
4. Reset only the narrowest state that matches the symptom.
   Prefer session or window-placement cleanup over wiping full profiles or caches.
5. Separate app binary problems from user-data problems.
   If needed, test a fresh profile or temporary data directory before suggesting
   reinstall or large migrations.
6. Escalate deliberately.
   Only move to broader cleanup, new profiles, or reinstall after the narrow
   fixes fail.

## Common Triggers

- "Chrome says it opened but I do not see a window."
- "This app is stuck in the Dock."
- "The app opens in the background only."
- "The process will not quit."
- "A Mac app keeps reopening broken."
- "Back up the app state before resetting it."

## Quick Checks

- Use `scripts/app_window_state.sh "App Name"` to inspect process, visibility,
  frontmost state, and window count.
- Use `ps`, `pgrep`, and `osascript` together before assuming the main app is
  healthy.
- Look for stale `--headless`, helper, renderer, updater, or login-item
  processes that can impersonate the real app.
- When app data may need to be touched, use
  `scripts/support_state_backup.sh <target-path> [more-paths...]`.

## Coordination and MCP Awareness

- Start with this skill for Mac app/process/window/login-item troubleshooting.
- Use `../mac-environment-conventions/SKILL.md` when drive choice, Application Support placement, or external-SSD storage rules affect the fix.
- Use the installed `storage-memory-manager` skill when the symptom is really disk pressure, swap growth, or runaway cache behavior.
- Use the installed `local-mcp-debugging` skill when the failing process is a local MCP server rather than a normal Mac app.
- Use the installed `native-macos-app-builder` skill when the task becomes app architecture or native code repair.
- Use the `playwright` MCP only when browser behavior is part of reproducing the problem.

## Reference Map

- For symptom-specific recovery patterns:
  `references/recovery-playbook.md`
- For where app support data and backups should live on this Mac:
  `../mac-environment-conventions/SKILL.md`
- For exact drive-role boundaries:
  `../mac-environment-conventions/references/storage-layout.md`
- For existing symlink rules before moving app data:
  `../mac-environment-conventions/references/symlink-rules.md`
- For Codex/ChatGPT updater errors caused by local storage or runaway crash
  reports:
  `../mac-environment-conventions/references/codex-storage-and-updates.md`

## Rules

- Preserve user state by default: tabs, profiles, bookmarks, history, sign-in,
  and extensions stay intact unless the user asks for a broader reset.
- Treat `~/Library/Application Support/...` as sensitive. Back up before edits.
- Do not assume the visible macOS app record points to the real GUI process.
- Prefer exact, testable observations over generic Mac troubleshooting advice.
- Keep fixes reversible and document backup locations in the response.

For a requested check that a backup can recover the state being protected, read [bounded backup restore drill](../../references/recovery/backup-restore-drill.md). Keep the drill separate from live app-state replacement; a created backup is not a verified restore.

## Adjacent owners

Use `master-security-toolkit:software-security-review` for suspicious installers, permissions or data-flow behavior; ordinary launch recovery stays here. Use `work-management:focus-work` only for competing priorities, bounded delegation or plugin-maintenance coordination. Do not merge machine recovery with artifact security review or require either as an automatic preflight for the other.

For a detailed recovery or storage-convention task, read the [complete original procedure](SKILL.original.md) and its task-specific references as well as the current routing above. This preserves the original checks, examples and constraints in full. Current host and user instructions govern stale names, paths or historical approval wording; verify live state before changing it.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports IT Operations Specialist. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
