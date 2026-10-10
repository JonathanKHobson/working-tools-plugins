# Knowledge Vault

Use this reference when the task targets the recipient's curated knowledge-graph vault.

## Identity

- Path: `${KNOWLEDGE_VAULT}`
- Main entry note: `00 Start Here.md`
- Purpose: curated graph view for patterns, terms, collections, File-O-Fun, and related knowledge-map material
- Preferred interface: direct file edits and local inspection, not MCP-first

## Current Boundary

- This vault is the human-facing Knowledge Vault, not just the old AI Glossary surface.
- Keep source/provenance clear when adding material from projects such as File-O-Fun or AI Glossary-derived data.
- Critical Thinking and other expansions should not be assumed to belong here unless the task says so.

## Key Areas

- `01 Patterns`
- `02 Terms`
- `03 Collections`
  - `03 Collections/Biases`
  - `03 Collections/Bias Mitigation`
  - `03 Collections/Ethical Dilemmas`
  - `03 Collections/File-O-Fun`
  - `03 Collections/Paradoxes & Puzzles`
  - `03 Collections/Personas`
  - `03 Collections/Task Templates`
- `_Meta`
- `_System`

## Safe Default Writes

- curated pattern, term, and collection notes
- mapped system notes
- targeted navigation notes, indexes, reports, and schemas that support the atlas directly

## Browse And Graph Norms

- Category browsing is a first-class requirement in this vault.
- Before large imports, generated note sets, taxonomy cleanup, or bulk moves, read `browse-density-and-frontmatter-hygiene.md`.
- Avoid leaving hundreds of notes flat in one `Entries` folder.
- Preserve or add `browse_group`, `browse_path`, and `canonical_path` on generated or curated collection notes.
- Use `related` plus wikilinks for cross-collection relationships so the graph has real edges.
- Do not remove or merge near-duplicates during browse cleanup; flag them for review.

## Protected By Default

- `.obsidian/`
- `_Meta` unless the task explicitly targets metadata or manifests

## Attachment Path

- `_System/Attachments`

## Core Plugin Checks

Check whether the receiving vault enables:
- Graph
- Templates
- Bases
- Bookmarks
- Search
- Backlinks
- Outgoing links
- Page Preview
- Properties

Do not assume community plugins.

## Starting Points

- `00 Start Here.md`
- `01 Patterns/Patterns Home.md`
- `01 Patterns/Indexes/All Patterns.md`
- `01 Patterns/Indexes/Patterns By Browse Folder.md`
- `02 Terms/Terms Home.md`
- `02 Terms/Indexes/All Terms.md`
- `02 Terms/Indexes/Terms By Browse Folder.md`
- `03 Collections/Collections Home.md`
- `03 Collections/File-O-Fun/File-O-Fun Collection Home.md`
- `_System/Folder Density Report.md`
- `_System/Relationship Index.md`
- `_System/Graph Legend.md`
- `_System/Metadata Schema.md`

## Known Failure Patterns

- Project-local output is not enough. Verify the live vault path, especially `03 Collections/File-O-Fun`, when the user expects to see notes in Obsidian.
- Obsidian Properties rendered as red/plain text usually means malformed YAML frontmatter. Scan imported notes with a YAML parser and check for stray top-level list items after keys such as `canonical_path`.
- AppleDouble `._*` sidecars can appear after generation or bulk moves. Exclude them from counts and clean them outside protected areas.

Recipient binding: these paths and folder maps are explicit templates. Configure the role root, start notes, allowed write areas, protected areas, attachments and available provider before use. If unconfigured, ask for the exact target vault and do not search or edit an assumed private location.
