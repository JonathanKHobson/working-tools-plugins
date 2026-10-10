# Storage Map Vault

Use this reference when the task targets the recipient's storage-map vault.

## Identity

- Path: `${STORAGE_VAULT}`
- Main entry notes:
  - `00 Start Here.md`
  - `00 Dashboard.md`
  - `How This Vault Works.md`
- Purpose: human-facing index of files, folders, projects, downloads, and drive-backed materials
- Preferred interface: direct file edits and local inspection, not MCP-first

## Character

- This vault is an index, not a duplicate hard drive.
- Human-facing maps and navigation notes belong here.
- Generated backend material is intentionally constrained so the live vault stays usable.

## Key Areas

- `01 Project Library`
- `Areas`
- `Projects`
- `Inbox`
- `Documents`
- `Downloads`
- `Drives`
- `Websites`
- `MCPs`
- `_Meta`

## Generated Backend Warning

- `99 Search Backend - Do Not Browse/` is protected and generated.
- Do not regenerate a full file-card backend inside the live vault.
- Archived backend location:
  `${GENERATED_BACKEND_ARCHIVE}`

## Safe Default Writes

- dashboard notes
- project-library notes
- human-facing maps
- Inbox-style operational notes
- explanatory start notes

## Protected By Default

- `.obsidian/`
- `98 Vault Tools/`
- `99 Search Backend - Do Not Browse/`
- generated or manifest-heavy `_Meta` areas unless the task explicitly targets them
- `_Archive`

## Attachment Path

- `Inbox/Attachments`

## Receiving Machine Checks

- Verify enabled core plugins.
- Check whether `daily-notes` is enabled here.
- Verify `alwaysUpdateLinks`; rename and move work should still be treated as link-sensitive.

## Starting Points

- `00 Start Here.md`
- `00 Dashboard.md`
- `How This Vault Works.md`
- `99 Search Backend - Do Not Browse/README.md` when the task risks touching generated backend areas

Recipient binding: these paths and folder maps are explicit templates. Configure the role root, start notes, allowed write areas, protected areas, attachments and available provider before use. If unconfigured, ask for the exact target vault and do not search or edit an assumed private location.
