# ChatGPT History Example

This skill’s main example is the ChatGPT History MCP already built on some macOS hosts.

## Current implementation

Project root:

```text
<external-ssd>/ChatGPT History
```

Key files:

- `build_history_mcp_index.py`
- `history_mcp_server.py`
- `history_mcp_common.py`
- `all-history-viewer-data/history-mcp.db`

## Architecture

- Reuse merged viewer artifacts as the metadata source of truth.
- Build a companion SQLite database instead of reparsing giant `chat.html` files on every request.
- Use SQLite FTS5 for message-body search.
- Canonicalize duplicate archive snapshots into one public `conversation_id`.
- Preserve source archive membership separately.

## Observed state

The current DB was validated at:

- 7 archives
- 7,441 canonical conversations
- 126,266 normalized message rows
- 122,949 searchable message rows

The malformed recovered archive remains excluded.

## Config wiring

The same server command was wired into:

- `~/.codex/config.toml`
- `~/Library/Application Support/Claude/claude_desktop_config.json`
- `<external-ssd>/ChatGPT History/.mcp.json`

## Important lesson

The ChatGPT History MCP is already implemented and configured. If it does not appear in Codex or Claude, treat that as a client reload or workspace pickup issue before assuming the MCP is missing.

Another lesson from the same setup: one client can be configured correctly while another is missing the same server entirely. Compare Codex and Claude config files directly instead of assuming they stayed in sync.

## Storage lesson

- Keep the large index on `<external-ssd>`.
- Keep the Python runtime in the home directory if the external drive produces broken `._*` Python sidecar files.
