# Vault Routing

Use this reference to decide which vault should hold the work and which areas are safe by default.

## Quick Routing

- Personal working memory, durable recall, session context, decisions, prompts, source notes, and raw logs -> Working Memory Vault
- Storage map, external-drive navigation, file-library orientation, and index notes -> Storage Map Vault
- Public-facing outputs, shipping queues, source-to-shareable flow, and review dashboards -> Publishing Vault
- Curated glossary or knowledge-map work -> Knowledge Vault

## Routing Table

| Vault | Purpose | Path | Main entry note | Safe default write zones | Protected zones | Attachment path | Plugin assumptions | Preferred interface | Common tasks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Working Memory Vault | Clean working memory and semantic recall | `${MEMORY_VAULT}` | `00 Start Here.md` | `01 Inbox` to `08 Raw Logs`, targeted `_System` notes | `.obsidian/`, broad `_System` work, `90 Archive` | `_System/Attachments` | Core plugins only; Bases and Graph are live | `kyle_second_brain` MCP first, files second | capture notes, search memory, update graph or Bases, maintain Memory Palace |
| Storage Map Vault | Human-facing storage index and drive map | `${STORAGE_VAULT}` | `00 Start Here.md`, `00 Dashboard.md`, `How This Vault Works.md` | dashboards, library notes, human-facing maps, Inbox-style notes | `.obsidian/`, `98 Vault Tools/`, `99 Search Backend - Do Not Browse/`, generated/meta areas | `Inbox/Attachments` | Core plugins only; daily notes enabled | files first | update storage maps, add human-facing indexes, inspect drive-oriented note surfaces |
| Publishing Vault | Public-output and publishing control surface | `${PUBLISHING_VAULT}` | `00 Start Here.md` | `01 Dashboards`, `02 Projects`, `03 Cuts`, `04 Frames`, `05 Shareables`, `06 Sources`, `07 People`, `08 Reviews`, `09 Assets` | `.obsidian/`, `_System`, `90 Archive` | `_System/Attachments` | Core plugins only | `shareables` MCP when applicable, files otherwise | update dashboards, route shipping work, organize share-safe artifacts |
| Knowledge Vault | Curated patterns, terms, collections, and graph view | `${KNOWLEDGE_VAULT}` | `00 Start Here.md` | `01 Patterns`, `02 Terms`, `03 Collections`, targeted `_System` notes | `.obsidian/`, `_Meta` unless explicitly targeted | `_System/Attachments` | Core plugins only; graph, templates, Bases, bookmarks available | files first | refine Atlas entries, maintain category browse folders, update relationship and graph notes |

## Safe Routing Defaults

- If the task is about memory or personal context, start in Working Memory Vault.
- If the task is about files on drives or catalogs, start in Storage Map Vault.
- If the task is about output that other people will consume, start in Publishing Vault.
- If the task is about AI glossary or curated knowledge mapping, start in Knowledge Vault.
- If the task creates or reorganizes many durable notes, apply the browse-density and frontmatter-hygiene reference after routing.

## Notes

- No community plugins should be assumed in any receiving vault.
- Verify daily-note settings independently for each receiving vault.
- Verify `alwaysUpdateLinks` in each receiving vault; rename or move operations should still be treated as link-sensitive.
- Live-vault verification matters: for Knowledge Vault and archive imports, confirm notes exist in the expected Obsidian vault path, not only in a project-local export folder.

Recipient binding: these paths and folder maps are explicit templates. Configure the role root, start notes, allowed write areas, protected areas, attachments and available provider before use. If unconfigured, ask for the exact target vault and do not search or edit an assumed private location.
