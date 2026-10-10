# Publishing Vault

Use this reference when the task targets the recipient's public-output vault.

## Identity

- Path: `${PUBLISHING_VAULT}`
- Main entry note: `00 Start Here.md`
- Purpose: public-output and publishing control surface
- Preferred interface: `shareables` MCP when the task is really a shareables workflow; otherwise direct file edits are fine

## Rule

- Pointers first.
- Snapshot only finalized or intentionally share-safe artifacts.
- Do not mirror whole projects unless the task explicitly calls for it.

## Key Areas

- `01 Dashboards`
- `02 Projects`
- `03 Cuts`
- `04 Frames`
- `05 Shareables`
- `06 Sources`
- `07 People`
- `08 Reviews`
- `09 Assets`
- `90 Archive`
- `_System`

## Safe Default Writes

- dashboards
- projects
- cuts
- frames
- shareables
- sources
- people
- reviews
- assets

## Protected By Default

- `.obsidian/`
- `_System` unless the task explicitly targets system metadata or routing
- `90 Archive`

## Attachment Path

- `_System/Attachments`

## Starting Points

- `00 Start Here.md`
- `01 Dashboards/Shipping Dashboard.md`
- `01 Dashboards/Review Queue.md`
- `01 Dashboards/Published Shareables.md`
- `01 Dashboards/Source Projects.md`

## MCP Note

If the real task is public-output shipping or shareable artifact workflow, prefer the `shareables` MCP. If the task is just note editing, metadata cleanup, or dashboard maintenance, file edits are fine.

Recipient binding: these paths and folder maps are explicit templates. Configure the role root, start notes, allowed write areas, protected areas, attachments and available provider before use. If unconfigured, ask for the exact target vault and do not search or edit an assumed private location.
