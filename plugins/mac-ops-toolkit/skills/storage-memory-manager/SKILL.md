---
name: storage-memory-manager
description: Use when checking, reclaiming, or reorganizing storage and memory on this Mac; trigger for low disk space, large cache growth, memory pressure, swap usage, deciding what can be safely deleted, or deciding what should stay on the internal disk versus ${RUNTIME_VOLUME} or ${ARCHIVE_VOLUME}.
---

# Storage Memory Manager

## Overview

Use this skill when the goal is to speed up future troubleshooting by quickly
finding large storage consumers, spotting memory pressure, and choosing the right
place for apps, caches, backups, and user-library data on this Mac.

This skill combines diagnosis with local placement rules so cleanup
work does not accidentally fight the existing external-drive strategy.

## Workflow

0. Narrow broad cleanup requests.
   If the user is overwhelmed or the request is sprawling, use Focus Start from
   `work-management:focus-work and its maintained operating protocols` to lock one
   concrete cleanup or measurement deliverable.
1. Measure before changing anything.
   Capture disk usage, memory pressure, swap, and the biggest directories in the
   likely hot zones.
2. Classify the payload.
   Decide whether each large item is runtime-oriented, archive-oriented, cache,
   backup, project data, or system-managed data.
3. Follow local drive conventions.
   Runtime/app-support material generally belongs with `${RUNTIME_VOLUME}`;
   archive-style files generally belong with `${ARCHIVE_VOLUME}`.
   MCP source/project folders are a special case: future MCP project homes
   should default to `${MCP_PROJECT_ROOT}`, while
   heavy runtimes, caches, generated DBs, venvs, and app-support payloads may
   remain on SSD II or under `~/.local/share`.
4. Prefer safe reclaim steps first.
   Clear obviously rebuildable caches and stale support files before moving
   active projects or app state.
5. Ask before deleting and back up first.
   Get user confirmation before deleting anything. Back up anything slated for
   deletion unless it is clearly disposable cache or temp data and the user has
   approved removing it.
6. Verify the effect.
   Re-check available disk space, memory pressure, and whether the relevant app
   still launches or performs normally.
7. Close the loop.
   Use Ship Log from `work-management:focus-work and its maintained operating protocols`
   after cleanup triage, measurement, or safe reclaim work.

## Common Triggers

- "What is eating space on my Mac?"
- "Can you help clean up storage safely?"
- "My Mac is slow and memory feels maxed out."
- "What can I delete without breaking apps?"
- "Should this live on the internal disk or the SSD?"
- "Find the biggest caches and backups."

## Quick Checks

- Use `scripts/storage_hotspots.sh` for a fast high-level disk usage scan.
- Use `scripts/memory_pressure_snapshot.sh` for memory pressure, swap, and top
  memory consumers.
- Read `references/cleanup-playbook.md` before deleting or relocating anything
  broad.

## Coordination and MCP Awareness

- Start with this skill for storage pressure, memory pressure, cleanup triage, and safe reclamation work.
- Use `../local-storage-mcp/SKILL.md` first when the question is mostly "where does this live?", "what already exists?", or "which report has the evidence?" across `${ARCHIVE_VOLUME}` and `${RUNTIME_VOLUME}`.
- Use `$mac-ops-toolkit:mac-environment-conventions` when the cleanup decision depends on local drive-role and external-storage rules.
- Use `$mac-ops-toolkit:mac-troubleshooter` when a specific app is malfunctioning and storage is only one part of the diagnosis.
- Use `development-studio:local-app-pipeline` when Docker, PocketBase, or pipeline storage layout on this Mac is part of the problem.
- Use `build-mcp-apps:build-mcp-apps` when storage/runtime issues are breaking a local MCP launcher or Python environment.
- For MCP fleet physical organization, use
  `${MCP_PLANNING_ROOT}`
  as the planning source of truth before recommending moves. Check the
  candidate inventory, physical taxonomy, and migration runbook before touching
  MCP project folders.
- Use `local_storage` or `kyle_second_brain` only when indexed storage evidence, prior notes, durable memory, or prior cleanups materially help the current diagnosis.
- Use `work-management:focus-work and its maintained operating protocols` for Focus Start
  on broad cleanup asks, MCP Use Check when an MCP is enabled, and Ship Log when
  a diagnosis or cleanup loop closes.

## Reference Map

- For safe cleanup order and what to delete first:
  `references/cleanup-playbook.md`
- For drive choice and storage-role boundaries:
  `$mac-ops-toolkit:mac-environment-conventions`
- For exact layout rules:
  `../mac-environment-conventions/references/storage-layout.md`
- For safe Codex/ChatGPT crash-report cleanup, session offloads, and updater
  `ENOSPC` verification:
  `../mac-environment-conventions/references/codex-storage-and-updates.md`
- For existing redirect patterns:
  `../mac-environment-conventions/references/install-targets.md`
- For indexed drive/report lookup before scanning raw folders:
  `../local-storage-mcp/SKILL.md`
- For Focus Start, MCP Use Check, Browser Handoff, and Ship Log:
  `work-management:focus-work and its maintained operating protocols`

## Rules

- Measure first, clean second.
- Ask before deleting anything.
- Back up anything before deleting it unless it is clearly rebuildable cache or
  temp data and the user has explicitly approved that cleanup.
- Prefer reversible cleanup over irreversible deletion.
- Do not move system-managed macOS components unless there is an existing redirect
  pattern.
- Do not treat `${RUNTIME_VOLUME}/Applications` as the default home
  for new MCP source projects. It should trend toward `.app` bundles and
  runtime/app-support payloads.
- Do not move MCP folders, create symlinks, or edit Claude/Codex config as part
  of storage cleanup unless a specific MCP migration runbook authorizes it.
- When in doubt, classify data as archive-oriented or runtime-oriented before
  deciding which external drive should hold it.
- Call out what was measured, what was removed, and what remains risky.

## Explicit receiving setup

Configure `RUNTIME_VOLUME`, `ARCHIVE_VOLUME`, `MCP_PROJECT_ROOT` and `MCP_PLANNING_ROOT` only when that placement question is in scope. They are placeholders requiring recipient verification, not installed paths. `local_storage` and any memory provider are external capabilities: report missing or unconfigured access and use an exact authorized project path when it already answers the question. Do not invent catalog results or infer authorization to move files.

The full disk helper accepts optional explicit volume paths as positional arguments and `STORAGE_SCAN_HOME` as an optional bounded home-like scan root. The memory helper requires macOS `memory_pressure`, `vm_stat` and `top`; it does not terminate processes. Scripts are read-only and never auto-run on installation.
