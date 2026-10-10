# Tool Selection and Safety

Use this reference to choose the execution path for Obsidian work on the recipient's machine.

## Execution Ladder

1. Relevant MCP when it is the safest high-level interface.
2. Direct file edits for note content, frontmatter, `.base` files, and targeted config files.
3. Obsidian URI for open, search, or create handoffs.
4. UI automation only for visible app-only work.

## MCP-First Cases

### `kyle_second_brain`

Prefer this MCP when the task is really about:
- memory search or semantic recall
- context pack retrieval
- durable note capture into Working Memory Vault
- duplicate checking
- taxonomy or audit views
- rebuild or semantic-memory maintenance

### `shareables`

Prefer this MCP when the task is really about:
- public-output shipping flows
- shareable artifact routing
- work that belongs in Publishing Vault as a publication or publishing workflow

## File-First Cases

Prefer direct file edits when the task is really about:
- note drafting or rewriting
- frontmatter cleanup
- inserting links or navigation sections
- editing `.base` files
- editing graph settings, app settings, templates, or other explicit vault config
- inspecting start notes, dashboards, or system notes
- Storage Map Vault or Knowledge Vault work, which use file-first routing unless the recipient deliberately configures a different interface

## Bulk Collection Maintenance Sequence

Use this sequence before large imports, generated note sets, browse-folder reorganizations, taxonomy cleanup, or bulk moves:

1. Verify the live vault path, not only project-local output.
2. Exclude `.obsidian`, `_Meta`, attachments, generated backends, archives, and AppleDouble `._*` sidecars unless explicitly targeted.
3. Run or produce a folder-density report.
4. Dry-run the path map when possible.
5. Make a recoverable backup of touched notes and indexes.
6. Apply deterministic moves or edits.
7. Update path-aware wikilinks, `canonical_path`, and browse metadata.
8. Validate counts, YAML parsing, and link targets.
9. Clean generated sidecars outside protected areas.

Treat `alwaysUpdateLinks` as helpful but not sufficient; direct filesystem moves still require explicit link validation.

## URI Use

Use Obsidian URI when you need to:
- open a note in the app
- open a prepared search
- create a note through a handoff rather than local file writing

Treat URI as optional convenience, not the default working path.

## UI Automation Use

Use UI automation only when the visible app must be touched, such as:
- changing a visual setting that lives only in the interface
- capturing a screenshot of graph, canvas, or rendered note state
- interacting with a plugin or settings pane that has no clean file or MCP equivalent

## Hard Rules

- Search before creating.
- Prefer aliases and heading or block links over duplicate notes.
- Treat `.obsidian/` as read-only unless the task explicitly asks for config changes.
- Require explicit permission for bulk rename, bulk move, or delete actions.
- When bulk move permission is already explicit, still make a backup and validate links.
- Never assume community plugins.
- Never assume nested vaults are safe.
- Never install, enable, disable, update, or remove plugins without explicit permission.
- Prefer safe, specific edits over broad refactors.

## Shared Machine Facts

- `Obsidian.app` is installed.
- Verify whether the official Obsidian CLI is installed on the receiving host.
- No community plugin manifest files are present in the four target vaults.
- Reliable shared primitives are core plugins, Markdown notes, `.obsidian` JSON files, and MCPs that are already part of the recipient's setup.

Recipient binding: these paths and folder maps are explicit templates. Configure the role root, start notes, allowed write areas, protected areas, attachments and available provider before use. If unconfigured, ask for the exact target vault and do not search or edit an assumed private location.
