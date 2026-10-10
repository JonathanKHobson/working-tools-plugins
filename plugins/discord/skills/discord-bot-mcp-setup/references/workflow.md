# Workflow

## 1. Define the scope

- Server-scoped bot first.
- DMs stay out of MVP unless the user explicitly asks.
- Decide whether the bot needs only read access or also thread visibility, sync reporting, and export helpers.

## 2. Create the Discord app and bot

- Make the app in the Discord Developer Portal.
- Add the bot user.
- Enable only the intents you actually need.
  - `Message Content` is required for message text.
  - `Server Members` and `Presence` are optional and should only be enabled if the project truly needs them.
- Generate the OAuth invite from the application ID plus a permissions integer.

## 3. Invite the bot

- Invite it to the target server.
- Start with the smallest permission set that can read the channels and threads you want.
- If the user already wants admin, do not fight that choice; just avoid adding extra permissions that are not needed.

## 4. Store the token safely

- Use an env var or a local file.
- Preferred pattern: `~/.local/share/<project>/<token-file>.txt`
- Protect the file: `chmod 600 <file>`
- Never put the token into Claude prompts, MCP config, or exported docs.

## 5. Wire the MCP

- Prefer a direct interpreter command, not a shell wrapper.
- For a receiving host with Claude Desktop, verify this direct-interpreter example against its actual installed runtime:
  - `command`: `/usr/local/bin/python3.10`
  - `args`: the external Python launcher or server script path plus flags
- If the server lives on external storage, keep its script path explicit and verify the selected interpreter.
- Load the live client config first and merge into `mcpServers`.
- Never replace the whole config file unless the user explicitly asks for a reset.
- Preserve unrelated MCPs and settings.

## 6. Expose the right tools

For a Discord digest MCP, the useful read-only tools are:

- health: `get_index_health`
- sync status: `get_sync_report`
- scope lookup: `resolve_scope_by_name`
- search: `search_messages`
- export discovery: `list_export_files`
- file read-back: `read_export`

If the export layer writes files, prefer a stable host folder and mirror temp outputs there so Claude can find them later.

## 7. Validate

- Restart the client after config changes.
- Confirm the server appears in `tools/list`.
- Confirm the logs reach `initialize`.
- Run a small sync first.
- Export one known channel or thread.
- Read the export back through the MCP if path visibility is uncertain.

## 8. If results look empty

Check in this order:

- Token present and valid.
- Bot is in the server.
- Required intents are enabled.
- Bot can see the channel or thread.
- Sync report shows messages or a dead-zone reason.
- Index health shows the DB and FTS tables you expect.
