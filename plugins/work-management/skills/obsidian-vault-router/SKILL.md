---
name: obsidian-vault-router
description: Use when working with the local Obsidian setup and you need to decide which vault should hold a note or task, how to search or edit safely, whether to use MCPs or direct file edits, or how to preserve existing graph, metadata, link, and vault conventions across the local storage, memory, shareable, and knowledge vaults. Trigger for Obsidian notes, vault routing, wikilinks, frontmatter or properties, graph view, Bases, templates, backlinks, aliases, unresolved links, vault maintenance, or any request that names one of the local vaults or paths.
---

# Obsidian Vault Router

## Overview

Use this skill to route Obsidian work to the right vault and the safest interface on this Mac. Preserve existing vault conventions, keep large durable collections browsable through meaningful category folders, prefer links and metadata over unnecessary hierarchy for small working areas, and treat generated or config-heavy areas as protected unless the task explicitly targets them.

## Workflow

1. Identify the vault first.
   - If the request names a vault, use that vault.
   - If not, route by purpose:
     - working memory and personal recall -> Working Memory Vault
     - storage map and file-library navigation -> Storage Map Vault
     - public outputs and publishing surfaces -> Publishing Vault
     - glossary or curated knowledge graph work -> Knowledge Vault
   - Read [vault routing](references/vault-routing.md) when ownership is
     ambiguous, the work crosses vaults, or a protected zone may be involved.
   - When the choice affects the result, tell the recipient the chosen vault and why in
     one sentence before acting. Skip a general tour of the vaults.

2. Open the vault-specific reference before acting.
   - Working Memory Vault -> `references/kyle-second-brain.md`
   - Storage Map Vault -> `references/kyle-storage-hub.md`
   - Publishing Vault -> `references/kyle-shareables.md`
   - Knowledge Vault -> `references/knowledge-atlas.md`

3. Choose the safest interface.
   - Read [tool selection and safety](references/tool-selection-and-safety.md)
     when the interface is unclear or the task changes notes, links, or vault
     configuration.
   - Default order:
     1. relevant MCP when it is the cleanest high-level interface
     2. direct file edits for note content, frontmatter, `.base` files, and targeted `.obsidian` work
     3. Obsidian URI for open or create handoffs
     4. UI automation only when the visible app is required

4. Inspect before editing.
   - Search before creating.
   - Read the relevant start note and nearby notes first.
   - Check for aliases, duplicate titles, and protected or generated paths before changing structure.

5. Check browse density for large collection work.
   - Read `references/browse-density-and-frontmatter-hygiene.md` before imports, archive builds, generated note sets, taxonomy cleanup, or bulk moves.
   - Treat folders over about 50 notes as split candidates.
   - Prefer 10-40 notes per leaf folder when category metadata supports a useful split.
   - Preserve or add `browse_group`, `browse_path`, and `canonical_path` for generated or curated collection notes.

6. Preserve vault shape.
   - Prefer links, headings, block references, tags, properties, and Bases views over new folders for small or fluid working areas.
   - For durable collections that would become a wall of notes, use category-first browse folders as part of the initial implementation.
   - Prefer existing dashboards, start notes, and system notes over inventing parallel navigation layers.
   - Use existing `related` fields and graph-visible wikilinks for cross-note relationships unless the vault has a stronger local convention.

## Reference Map

- Core Obsidian operating rules:
  `references/obsidian-core-practices.md`
- Tool choice and safety rules:
  `references/tool-selection-and-safety.md`
- Cross-vault routing and protected zones:
  `references/vault-routing.md`
- Browse density, frontmatter hygiene, and bulk collection maintenance:
  `references/browse-density-and-frontmatter-hygiene.md`
- Working Memory Vault details:
  `references/kyle-second-brain.md`
- Storage Map Vault details:
  `references/kyle-storage-hub.md`
- Publishing Vault details:
  `references/kyle-shareables.md`
- Knowledge Vault details:
  `references/knowledge-atlas.md`

## Rules

- Search before creating a note.
- Treat `.obsidian/` as read-only unless the task explicitly asks for config changes.
- Require explicit user permission for bulk rename, bulk move, or delete operations.
- Do not assume community plugins are installed unless the vault proves it.
- Do not assume nested vaults are intentional or safe.
- Prefer aliases and precise heading or block links over duplicate notes.
- Prefer Obsidian-aware rename or move logic conceptually even when editing files directly.
- Validate YAML/frontmatter after touching notes, especially when Obsidian Properties render as red/plain text.
- Do not count AppleDouble `._*` sidecars as real notes; clean generated sidecars outside protected areas when a bulk operation creates them.
- Call out when a request touches generated, archived, or protected areas before changing them.

## MCP and Cross-Skill Routing

- Prefer `kyle_second_brain` MCP for memory search, capture, duplicate checks, context packs, and rebuild flows inside Working Memory Vault.
- Prefer `shareables` MCP for public-output shipping flows when the task is really about Publishing Vault and the MCP is available.
- Stay file-first for Storage Map Vault and Knowledge Vault.
- Use `$work-management:focus-work` when the user is really asking for prioritization, focus, or sequencing rather than vault operations.
- Use `$mac-ops-toolkit:mac-environment-conventions` or `../storage-memory-manager/SKILL.md` when the task is really about drive placement, generated backends, storage pressure, or external-disk behavior.
- Use `../local-storage-mcp/SKILL.md` when local file evidence across drives matters more than note editing.

## Receiving Machine Checks

- Verify whether `Obsidian.app` is installed on the receiving Mac.
- Verify whether the official Obsidian CLI is installed; treat unverified CLI commands as reference knowledge only.
- Do not assume community plugins; inspect the receiving vault plugin manifests.
- Shared reliable primitives across the vault set are core plugins and plain Markdown files, not community-plugin assumptions.

Recipient binding: these paths and folder maps are explicit templates. Configure the role root, start notes, allowed write areas, protected areas, attachments and available provider before use. If unconfigured, ask for the exact target vault and do not search or edit an assumed private location.
