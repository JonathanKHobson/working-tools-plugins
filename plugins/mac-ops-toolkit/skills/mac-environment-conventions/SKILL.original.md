---
name: mac-environment-conventions
description: Use when working on this Mac and you need to decide where apps, libraries, caches, backups, projects, or assets should live across the internal disk, $RUNTIME_VOLUME, and $ARCHIVE_VOLUME; when setting up or extending symlink-based storage redirects; or when a task involves external-first app installs, Application Support placement, or deciding which drive should hold a file or runtime dependency.
---

# Mac Environment Conventions

## Overview

This skill captures the observed storage and placement conventions on this Mac
so agents can put things in the right place, preserve existing
patterns, and avoid inventing new storage rules mid-task.

## Workflow

1. Identify the payload class.
   App bundle, Application Support, caches, backup data, creator assets,
   projects, archive files, or mixed workspace.
2. Read the right references before acting.
   Use `references/storage-layout.md` for drive selection,
   `references/symlink-rules.md` for redirects, and
   `references/install-targets.md` for concrete placement targets.
3. Inspect current machine state before changing anything.
   Check the `local_storage` MCP first for path evidence, report rows, and
   current placement signals, then confirm against existing symlinks, current
   install roots, and any `_Catalog/reports` outputs on the relevant drive.
4. Prefer extending an established pattern.
   If an app family or storage class already lives on `$RUNTIME_VOLUME`,
   keep using that structure unless the task explicitly requires something else.
5. Avoid broad relocations.
   Do not mass-move internal data or rewrite symlinks unless the user asked for
   that specific migration.
6. Keep Claude Desktop manual-launch when its MCP set depends on external-drive
   runtimes.
   Do not leave Claude in Login Items if it needs `$ARCHIVE_VOLUME` or
   `$RUNTIME_VOLUME` to be mounted before startup.
   Keep the active Claude profile small; default daily posture is the
   `<selected-daily-profile>` profile, not full-fleet boot.

7. Orchestrate adjacent skills when storage is not the only issue.
   - Use `../local-storage-mcp/SKILL.md` first when the task is mainly about finding local files, checking report evidence, or deciding which drive should hold something.
   - Use `../mac-troubleshooter/SKILL.md` when the main problem is app/process/window state or launch behavior.
   - Use `../storage-memory-manager/SKILL.md` when the main problem is disk pressure, cleanup, or memory pressure.
   - Use `../local-data-mcp-builder/SKILL.md` when the task is really about local data MCP design or SQLite-backed retrieval.
   - Use `../local-mcp-debugging/SKILL.md` when a local MCP fails to start or attach.
   - Use `../personal-security-check/SKILL.md` before downloading, installing, or granting permissions to unfamiliar apps, CLIs, launchers, runtimes, scripts, or external MCP packages.
   - Use `../native-macos-app-builder/SKILL.md` when the task becomes native macOS app architecture or Xcode work.
   - Use `../focus-ops-manager/SKILL.md` when the user is not blocked by storage rules but by priorities, sequencing, or work focus.
   - Use `knowledge_atlas`, `kyle_second_brain`, and `playwright` MCPs when stronger local evidence, durable context, or browser validation would improve the decision.

## Local Design Consulting

When the task is using Claude Desktop, Claude Code, Claude Design, Stitch, or
Figma for a concrete design decision, use `kyle-mac-design-partners` if installed.
That personal companion covers current app discovery, shared plan capacity,
separate mockup workspaces, export verification, and browser handoff. Keep the
core computer-use tool instructions authoritative. Verify current mounts and
host access; an SMB file share does not imply remote app control.

## Trigger Examples

- "Install this app and keep it off the internal disk."
- "Move this Application Support folder to the external drive."
- "Where should this project live?"
- "Set up symlinks for this app."
- "Which SSD should hold these assets?"
- "Why is this app storing too much on the internal disk?"

## Reference Map

- For drive choice and role boundaries:
  `references/storage-layout.md`
- For how native paths point into `$RUNTIME_VOLUME`:
  `references/symlink-rules.md`
- For concrete target roots by storage class:
  `references/install-targets.md`
- For Codex/ChatGPT updater failures, Crashpad growth, and session offloads:
  `references/codex-storage-and-updates.md`
- For GitHub account, repo, branch, and upload conventions:
  `../github-conventions/SKILL.md`
- For cross-skill and MCP routing:
  `../focus-ops-manager/references/skill-mcp-orchestration.md`
- For the Codex MCP idle-memory investigation record:
  `../focus-ops-manager/references/codex-mcp-investigation-report.md`

## Rules

- `$ARCHIVE_VOLUME` is the archive/file library drive.
- `$RUNTIME_VOLUME` is the apps/runtime/backups drive.
- Never externalize `~/Downloads`. It must remain a real
  local folder, not a symlink, alias, moved folder, or external redirect.
  Archive its contents by moving them into a dated folder under
  `$ARCHIVE_VOLUME/Downloads/`, then leave the local Downloads folder in place.
- Prefer native-path symlinks into `$RUNTIME_VOLUME/UserMirror/Library/...`
  when that pattern already exists for an app family.
- Prefer `$RUNTIME_VOLUME/ExternalApplications` for relocatable
  user-installed app bundles that already follow the externalized app pattern.
- Current MCP runtime installs that should be treated as part of this
  external-apps posture:
  - `mnehmos.rpg.mcp`
  - `role-playing-mcp-server`
  - `research-orchestrator`
- For critical daily Claude MCPs, prefer a home-directory runtime even when the
  project code or data lives on an external drive.
- Keep system-managed or obviously internal-only macOS components local unless
  there is clear evidence they already follow an external redirect pattern.
- Do not invent GitHub repo placement rules inside this skill. Use
  `github-conventions` for GitHub account orientation and uploads.
- Treat this skill as the machine/storage orchestrator on this Mac when several other skills depend on drive choice, runtime placement, or external-SSD constraints.
