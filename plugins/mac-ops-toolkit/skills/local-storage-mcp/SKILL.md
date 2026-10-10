---
name: local-storage-mcp
description: Find files across verified recipient volumes, review storage catalogs, or choose placement for apps, backups, assets, and runtimes. Use for uncertain location or storage policy; exact project paths with sufficient local evidence need no storage-catalog lookup.
---

# Local Storage MCP

## Overview

This skill routes storage discovery and placement questions through the
`local_storage` MCP instead of broad filesystem exploration. Use it when the
question is about what already exists, where something lives, which drive should
hold a new item, or which report contains the relevant evidence.

When the answer depends on a catalog rather than a known project path, briefly
explain which source you checked and why. Skip that orientation when the user
already gave an exact path and the project evidence answers the question.

For MCP project placement questions, the current planning source of truth is
`${MCP_PLANNING_ROOT}`.
The canonical future MCP project home is
`${MCP_PROJECT_ROOT}`, but live MCP folders, configs,
symlinks, DBs, and runtimes should not be changed unless a migration runbook
explicitly authorizes that work.

## Workflow

1. Start with the exact task path or native Codex project when one is known.
   Resolve symlinks/aliases, identify the owning checkout, and read its existing
   `docs/project-map.md` (if present) before requesting a new MCP discovery.
   If that evidence answers the lookup, stop there.
2. If project evidence is absent or insufficient, use the MCP, not a raw drive
   scan. Use `search_storage`, `lookup_path`, `get_report`, and
   `suggest_storage_location` first.
3. Pick the smallest tool that answers the question.
   - Use `lookup_path` for an exact path.
   - Use `search_storage` for a topic, app, project, or asset query.
   - Use `get_report` when the user wants candidate lists or policy rows.
   - Use `get_storage_conventions` or `suggest_storage_location` for placement.
4. Escalate only when the MCP is missing evidence.
   If a path or report is missing, check whether the relevant `_Catalog` index is
   stale before scanning raw directories.
5. Keep the boundary clear.
   This MCP is metadata-first and read-only. Do not treat it as permission to
   move files, rewrite symlinks, or read arbitrary local file contents.
6. For native project metadata, deduplicate labels that resolve to the same
   realpath, preserve each worktree identity, and treat an alias absent from
   native metadata as an alias condition rather than a missing repository.
7. For new MCP placement or MCP reorganization, classify before recommending a
   path.
   - Check the MCP Fleet Consolidation planning workspace first.
   - Choose ownership, lifecycle, dependency risk, and move policy.
   - Default source/docs/project roots to
     `${MCP_PROJECT_ROOT}`.
   - Keep runtime-only payloads, venvs, caches, generated DBs, and app-support
     state in their existing safe runtime homes unless a per-MCP runbook says
     otherwise.
8. Close the loop.
   Use the MCP Use Check in `work-management:focus-work and its maintained operating protocols`
   when `local_storage` is enabled, and use Ship Log when a lookup produces a
   decision or recommendation.

## Trigger Examples

- "Where does BBEdit live?"
- "What TTRPG material do I already have?"
- "Which local Application Support folders are candidates to externalize?"
- "Where should a new stream asset pack go?"
- "Where should this archive of PDFs live?"
- "Show me the symlink policy rows for this app."

## Tool Map

- `search_storage`
  Best first query for topics, apps, assets, and fuzzy retrieval
- `lookup_path`
  Best for exact path confirmation plus related report hits
- `get_report`
  Best for structured lists such as `library_redirect_candidates`,
  `install_roots_summary`, `topic_clusters`, and `app_runtime_clusters`
- `get_storage_conventions`
  Best for policy text grounded in Jonathan's machine conventions
- `suggest_storage_location`
  Best for deciding internal disk vs `${ARCHIVE_VOLUME}` vs
  `${RUNTIME_VOLUME}`

## Rules

- Prefer the MCP over broad `find` or `rg` scans when the answer should come
  from the storage catalogs.
- Use `work-management:focus-work and its maintained operating protocols` for MCP Use
  Check and Ship Log when this skill creates tool-use or decision-closeout work.
- Treat `._*` AppleDouble files and singleton/socket symlink noise as non-signal
  unless the task explicitly concerns filesystem artifacts.
- If the MCP and the current disk state disagree, refresh the relevant `_Catalog`
  before making a placement or cleanup recommendation.
- Do not place global MCP fleet plans inside the `local-storage-mcp` project.
  Point future planning to
  `${MCP_PLANNING_ROOT}`
  instead.
- For MCP project homes, prefer
  `${MCP_PROJECT_ROOT}` over
  `${RUNTIME_VOLUME}/Applications`; keep SSD II for app bundles,
  runtime support, caches, and heavy generated state when appropriate.
- For actions that change storage layout, pair this skill with
  `$mac-ops-toolkit:mac-environment-conventions`.

## Explicit receiving setup

Configure `RUNTIME_VOLUME`, `ARCHIVE_VOLUME`, `MCP_PROJECT_ROOT` and `MCP_PLANNING_ROOT` only when that placement question is in scope. They are placeholders requiring recipient verification, not installed paths. `local_storage` and any memory provider are external capabilities: report missing or unconfigured access and use an exact authorized project path when it already answers the question. Do not invent catalog results or infer authorization to move files.
