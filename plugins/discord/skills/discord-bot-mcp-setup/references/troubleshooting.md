# Troubleshooting

## Startup failures

### `mcp.server.fastmcp` missing

- This usually means the launcher is picking up a broken or partial `mcp` package.
- Fix the Python path before changing the MCP protocol code.
- Prefer a known-good interpreter plus the correct site-packages path.
- Clear stale `mcp` modules from `sys.modules` if the launcher preloads them.

### Claude says "Could not attach to MCP server"

- Read `~/Library/Logs/Claude/mcp-server-<name>.log`.
- Confirm the command exists.
- Confirm the config entry still exists in the active client config.
- Reproduce the exact command in Terminal.

### `Operation not permitted` from Claude on a shell wrapper

- Treat this as a launcher issue.
- For a receiving host with Claude Desktop, verify this direct-interpreter example against its actual installed runtime:
  - `command`: `/usr/local/bin/python3.10`
  - `args`: an external script path
- If Claude Desktop blocks a shell wrapper on external storage, verify the direct interpreter and explicit script path instead.

## Empty exports

### Channel or thread exports as zero messages

- Check bot permissions.
- Check whether the bot can actually see that channel or thread.
- Check whether the content lives in threads that were not synced.
- Check the sync report for a dead-zone reason.
- Check index health before rewriting export code.

### Claude says a file path is not visible

- Keep exports on a stable host folder.
- Add a read-back tool instead of assuming Claude can open the file directly.
- Do not assume `/tmp` means the same thing in every runtime.

## Config mistakes

### New MCP removed old MCPs

- Restore the backup.
- Re-edit the live config by merging into `mcpServers`.
- Never replace the whole config object by default.

### Bot token problem

- Store the token locally in an env var or file.
- Protect the file with `chmod 600`.
- Never commit the token or paste it into a prompt.
