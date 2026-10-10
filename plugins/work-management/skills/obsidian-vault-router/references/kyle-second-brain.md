# Working Memory Vault

Use this reference when the task targets the recipient's structured working-memory vault.

## Identity

- Path: `${MEMORY_VAULT}`
- Main entry note: `00 Start Here.md`
- Purpose: clean AI working memory for structured notes, decisions, concepts, prompts, source notes, and raw logs
- Preferred interface: `kyle_second_brain` MCP first, direct file edits second

## Folder Map

- `01 Inbox`
- `02 Sessions`
- `03 Projects`
- `04 Decisions`
- `05 Concepts`
- `06 Prompts and Patterns`
- `07 Sources`
- `08 Raw Logs`
- `90 Archive`
- `_System`

## Memory Layer

- Memory Palace home: `_System/Memory Palace/README.md`
- Graph legend lives in `_System/Memory Palace/Graph Legend.md`
- Bank hubs live under `_System/Memory Palace/Banks/`
- History import review and `.base` browsing live under `_System/Memory Palace/History Import/`
- Raw memory imports live under `08 Raw Logs/YYYY-MM-DD/`

## Optional UX Conventions To Verify

- Verify role-colored graph groups before relying on them.
- Verify whether Bases is used for imported-memory review surfaces.
- The listed memory-bank, hub-note, curated-draft and raw-log layout is a template; compare it with recipient conventions.
- If `_System/Tag Taxonomy.md` exists, preserve it when editing taxonomy-related behavior.

## Safe Default Writes

- `01 Inbox` through `08 Raw Logs`
- Targeted `_System` notes when the task explicitly concerns system navigation, graph, taxonomy, Bases, or Memory Palace UX

## Protected By Default

- `.obsidian/` unless the task explicitly asks for config changes
- broad `_System` edits when the task is not specifically about that surface
- `90 Archive`

## When To Prefer MCP

Prefer `kyle_second_brain` MCP for:
- `memory_search`
- `memory_context_pack`
- note capture or update flows through the supported tools
- semantic-memory rebuild or audit work
- duplicate checking
- memory taxonomy inspection

## When Files Are Fine

Prefer direct file edits for:
- note content revisions
- graph config
- `.base` files
- vault UX notes
- cross-link or tag backfills that are explicitly file-centric

## Starting Points

- `00 Start Here.md`
- `_System/Vault Guide` when present in the task context
- `_System/Memory Palace/README.md` for memory-specific work

Recipient binding: these paths and folder maps are explicit templates. Configure the role root, start notes, allowed write areas, protected areas, attachments and available provider before use. If unconfigured, ask for the exact target vault and do not search or edit an assumed private location.
