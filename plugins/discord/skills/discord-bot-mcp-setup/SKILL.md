---
name: discord-bot-mcp-setup
description: Create Discord bots and connect them to local MCP servers for Claude Desktop, Claude Code, or Codex. Use when setting up a Discord application/bot, generating invite URLs and permissions, storing tokens safely, wiring a bot-backed MCP, preserving existing mcpServers config, or debugging launch/import failures, empty syncs, or missing MCPs.
---

# Discord Bot MCP Setup

Use this skill to create or update Discord bot-backed MCPs. It covers Discord app setup, token handling, invite permissions, local MCP wiring, and the failure modes we hit in practice.

## Receiving-host requirements

The Discord Developer Portal, administrator invite authority, reviewed bot MCP implementation, supported client, interpreter/dependencies and explicitly authorized channel scope are external requirements. No token, bot account, server, database or MCP registration is supplied by this skill. Inspect current official provider documentation before setup. Read-only source review or a synthetic config check does not establish a live invite, bot access, sync or export.

## Use when

- Creating a new Discord bot for ingestion or export.
- Inviting a bot to a server and choosing permissions or intents.
- Wiring a bot into Claude Desktop, Claude Code, or Codex MCP config.
- Fixing "MCP missing", bad launch commands, import errors, empty syncs, or file-visibility problems.
- Adding read-back or export support so Claude can consume generated files reliably.

## Core rules

- Prefer a bot over a user token or selfbot.
- Decide scope first: server, channels, threads, DMs out of MVP unless explicitly required.
- Keep permissions minimal unless the user already wants admin.
- Store the token locally or in an env var; never paste it into config, prompts, or logs.
- When editing MCP config, load the live file first and merge into `mcpServers`; never replace the whole object.
- Preserve unrelated MCPs, preferences, and transport settings.
- On the receiving host, verify a direct Python interpreter plus the actual external script path. If the client blocks a shell wrapper on external storage, use the direct interpreter route.
- If a task needs persistent exports, write to a stable host folder and optionally mirror temp outputs there.
- Validate with a real client and logs; do not stop at "the server launches."

## Workflow

1. Read [the setup workflow](references/workflow.md) when creating a bot,
   inviting it, or wiring a new MCP. For a focused failure in an existing
   setup, start with the matching [troubleshooting guide](references/troubleshooting.md)
   and current client logs.
2. Create the Discord application and bot.
   - Add only the intents the server actually needs.
   - Generate the invite URL from the application ID and permissions.
3. Invite the bot to the target server.
4. Save the bot token locally.
   - Prefer `~/.local/share/<project>/...` with `chmod 600`.
5. Wire the MCP.
   - Use a direct Python command and an external script path.
   - Add token, db, and export flags as needed.
   - Merge the config entry into existing `mcpServers`.
6. Validate.
   - Restart the client.
   - Confirm `tools/list`.
   - Run one sync.
   - Export one channel or thread and read it back.
7. If the export is empty, check permissions, thread visibility, sync reports, and index health before changing code.

## Recommended MCP tools

For bot-backed Discord digest MCPs, expose read-only helpers that answer these questions:

- Is the index healthy?
- Did the last sync hit zero-message channels?
- What guild/channel/thread name maps to which ID?
- What export files exist?
- Can Claude read the export back without guessing the filesystem path?

The minimum useful tool set is usually:

- `get_index_health`
- `get_sync_report`
- `resolve_scope_by_name`
- `list_export_files`
- `read_export`
- `search_messages`
- `export_*`

## Debug first

Read [references/troubleshooting.md](references/troubleshooting.md) when:

- Claude says the MCP is missing.
- The server crashes on startup.
- `mcp.server.fastmcp` cannot be imported.
- Claude cannot see exported files.
- A channel or thread exports as zero messages unexpectedly.

## Keep it clean

- Back up configs before edits.
- If the user already has a working Codex on-demand pattern, leave it in place unless they ask to change it.
- Remove only the server you are changing; do not touch unrelated MCPs.

## Project organization guardrail

Before creating or expanding app, plugin, MCP, or service project files, consult the `work-management:project-structure` skill. Do not store all behavior in one monolithic file unless the user explicitly requests a tiny one-off proof of concept or self-contained artifact.

Separate entry points, commands/actions, UI, services, configuration, persistence, docs, tests, and assets before implementation when the project is expected to grow.
