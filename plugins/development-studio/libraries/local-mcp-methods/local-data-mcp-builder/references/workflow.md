# Local Data MCP Workflow

## Recommended architecture

Use a two-part design:

1. A builder that reads local source artifacts and writes a normalized SQLite database.
2. A stdio MCP server that reads that database in query-only mode.

This avoids reparsing giant exports on every tool call and keeps the tool layer simple.

## Decision order

1. Inspect existing artifacts first.
2. Decide whether metadata already exists.
3. Decide whether full-text search is required.
4. Decide where the index should live.
5. Build the index.
6. Implement the MCP on top of the normalized store.
7. Wire clients.
8. Validate with a real MCP client.

## Data shape guidance

- Prefer stable public IDs.
- If snapshot archives duplicate the same conversation, canonicalize them into one record and preserve source membership separately.
- Keep large raw payloads out of routine list responses.
- Use pagination for lists and searches.
- Keep the server read-only unless the user explicitly needs mutation.

## SQLite guidance

- Prefer SQLite FTS5 for local full-text search.
- Keep metadata tables separate from the FTS table.
- Open the finished DB read-only in the MCP server.
- Rebuild only when source artifacts are missing or stale.

## Tool surface guidance

For local-data MCPs, a strong default surface is:

- `get_overview`
- `list_sources`
- `list_records`
- `search_evidence`
- `get_record`
- `get_evidence_by_id`

Rename for the user’s domain, but keep the shape simple.
