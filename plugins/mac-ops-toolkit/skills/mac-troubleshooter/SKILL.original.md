---
name: mac-troubleshooter
description: Use when troubleshooting application, process, window, login item, cache, or launch problems on this Mac; trigger for issues like an app shows open but no window appears, an app is stuck in the Dock, a process will not quit, a Mac app will not relaunch cleanly, or a safe backup-before-reset workflow is needed for Application Support data.
---

# Mac Troubleshooter

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
- Use `../storage-memory-manager/SKILL.md` when the symptom is really disk pressure, swap growth, or runaway cache behavior.
- Use `../local-mcp-debugging/SKILL.md` when the failing process is a local MCP server rather than a normal Mac app.
- Use `../native-macos-app-builder/SKILL.md` when the task becomes app architecture or native code repair.
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
