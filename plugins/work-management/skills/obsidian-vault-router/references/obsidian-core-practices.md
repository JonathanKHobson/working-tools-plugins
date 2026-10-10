# Obsidian Core Practices

Use this reference for the non-personal operating rules that apply to the recipient's vault work in general.

## Core Model

- An Obsidian vault is a local folder of Markdown notes plus a hidden `.obsidian/` config folder.
- Notes are plain text and can be edited directly, but rename and move operations still need extra care because link integrity matters.
- Do not create vaults inside other vaults.
- Treat `.obsidian/` as read-only unless the task explicitly targets settings, graph config, Bases, templates, or another known config file.

## Properties and Frontmatter

- Keep properties small and atomic.
- Use consistent property names across a vault.
- Prefer supported plural keys: `tags`, `aliases`, `cssclasses`.
- Quote internal links when they appear inside YAML text or list values.
- Do not put long Markdown content into frontmatter.
- If Obsidian shows Properties as red/plain Markdown instead of interactive properties, inspect the source frontmatter and parse it as YAML.
- Watch for invalid top-level list items after valid keys, such as `canonical_path` followed by `- class: cognitive`; normalize these into keyed fields such as `categories`.
- Validate all touched notes after bulk generation, import, or frontmatter repair.

## Links, Search, and Retrieval

- Search before creating a new note.
- Search the natural-language phrase first, then aliases, then tags and properties.
- Prefer heading and block links when the reference is specific.
- Prefer aliases over duplicate synonym notes.
- Use `file:` and `path:` style thinking when filename or location matters more than note body text.
- Treat unlinked mentions as a maintenance opportunity, not automatic proof that a link should be added.

## Graph and Bases

- Graph reflects internal links, not every visual relationship.
- Prefer meaningful links over decorative link density.
- Global graph is for pattern sensing; local graph is for working context.
- Use graph groups that map to note roles, states, or meaningful paths.
- Use Bases for structured browsing and dashboards before creating extra folders.
- Mermaid relationships do not count as graph connectivity.

## Refactoring Discipline

- Prefer Obsidian-aware rename or move logic conceptually whenever a note is already part of the link graph.
- Direct file edits are fine for content and frontmatter changes.
- Be cautious with bulk structure changes.
- Recommend splitting notes when they mix unrelated topics or become hard to navigate.
- Recommend merging notes when aliases or duplicate concepts are fighting each other.
- For large durable collections, run a browse-density check before accepting a flat folder of notes as done.
- Treat folders over about 50 notes as split candidates, aiming for 10-40 notes per leaf folder when categories support it.
- Preserve stable filenames, IDs, aliases, provenance, and source fields when reorganizing folders.

## Safe Defaults

- Operate inside the target vault only.
- Do not install, remove, enable, or update plugins without explicit permission.
- Do not assume sync is backup.
- Before destructive or broad changes, make a recoverable checkpoint when appropriate.
- Ask before bulk delete, archive, rename, or move operations.

## Maintenance Norms

### Daily

- Capture into the right inbox or working note.
- Add minimal metadata if the note should survive beyond the current moment.
- Add at least one meaningful link when context is fresh.

### Weekly

- Process inboxes.
- Review unresolved links, orphan notes, dead-end notes, and metadata drift.
- Normalize near-duplicate property names and tags.

### Monthly

- Verify backups.
- Review noisy folders and stale note types.
- Check whether the graph is still legible.

### Quarterly

- Merge duplicates.
- Split bloated notes.
- Revisit schema and folder assumptions.
- Remove unused or misleading structure.

## Troubleshooting

### Links did not update after rename or move

- Suspect raw filesystem rename or ambiguous names first.
- Re-run the operation through the safer vault-aware path when possible.
- Check for unresolved links and duplicate names.

### Search, graph, or backlinks feel stale

- Suspect metadata cache drift.
- Treat cache rebuild as normal maintenance, not automatic corruption.

### YAML behaves strangely

- Inspect frontmatter in source form.
- Check quoting, property types, and deprecated singular keys.
- Check for stray top-level YAML lists after ordinary scalar fields.
- Run a parser-based YAML scan across touched notes before signoff.
- Compare broken notes to a known-good note from the same collection before doing a broad repair.

### A folder becomes a wall of notes

- Count notes per folder, excluding `._*` sidecars.
- Split durable collections by meaningful category or browse group.
- Preserve `browse_group`, `browse_path`, and `canonical_path` when those fields exist or when the collection is generated.
- Update path-aware wikilinks and generated indexes after moves.

### Search missed an obvious target

- Check whether the target is really a file-path or filename problem.
- Check excluded files.
- Check whether the content lives in an attachment rather than a note.

### Counts look doubled or strange on macOS

- Suspect AppleDouble `._*` sidecars.
- Exclude sidecars from note counts, YAML scans, and import validation.
- Clean generated sidecars outside `.obsidian`, `_Meta`, archives, and other protected areas when safe.

## CLI Note

The official Obsidian CLI is not currently installed on this Mac. Keep CLI knowledge as reference-only for future use. Do not plan work around the CLI unless the environment changes and the tool is installed explicitly.

Recipient binding: these paths and folder maps are explicit templates. Configure the role root, start notes, allowed write areas, protected areas, attachments and available provider before use. If unconfigured, ask for the exact target vault and do not search or edit an assumed private location.
