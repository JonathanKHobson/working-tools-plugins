# Discord

Find and summarize Discord channel conversations, prepare replies, and send authorized messages with the correct identity.

## What you can do

- Search indexed guild conversations or read a focused current channel/thread.
- Draft a reply from the relevant conversation context.
- Send an explicitly authorized bot message, or use the narrow personal-account UI route when appropriate.

## How to start

1. Select this plugin in a supported host, or name the workflow in your request. Describe the result you want and provide the inputs listed below.
2. Start with one useful task. The assistant should explain the relevant capability, required input/access and expected result briefly when that helps; an explicit task can begin immediately.
3. Check the result and its reported state. A draft, local file, sent message and published result are different outcomes. Ask “what else can this plugin do?” or “help me get started” whenever you need the wider menu.

## Try a first task

| Ask | Bring | Expect |
| --- | --- | --- |
| “Summarize the recent decisions in this server channel.” | Server/channel and time window; bot access to that scope. | A source-backed summary that says whether messages came from the index or a live read. |
| “Draft a reply to this Discord thread.” | Thread and intended message. | An unsent draft; sending requires an explicit request. |

## Choose a skill

The table is a selection guide. Once a task matches, read that complete skill; follow only its applicable support-file routes.

| Skill | Use it for |
| --- | --- |
| [discord-bot-mcp-setup](skills/discord-bot-mcp-setup/SKILL.md) | Complete Developer Portal, invite/intents, token, MCP merge and troubleshooting workflow. |
| [discord](skills/discord/SKILL.md) | Use a Discord bot MCP for guild channels, threads, search, exports, and bot-identity messages. |
| [discord-computer-use](skills/discord-computer-use/SKILL.md) | Use observed Discord UI state as a narrow fallback for the user's personal DMs or an explicit UI request when suitable authorized API access is unavailable. |

## Tools, setup and access

`discord_digest` connects to the separately installed Discord Digest server. For cached history use overview/scope resolution and focused search; for current state use the live connection/read tools. Setup paths and verification are below. Test one permitted channel read before relying on access. If startup fails, inspect the configured interpreter/server/database paths; if a channel is invisible, check the bot’s actual scope. Do not substitute a selfbot or copied browser credentials.

The MCP speaks as a bot. It does not inherit your personal account or all your DMs. Indexed history can be stale; a plugin installation does not prove bot access.

Installation makes a package available; it does not establish a working server or permission for every action. The complete optional launcher uses receiving-host configuration. This public package installs no automatic MCP registration; select your own supported provider and inspect its configured runtime/database paths. Verify tool discovery and one harmless scoped read/overview. Keep credentials in the provider’s supported setup, never in a chat or this README. Report missing configuration, unreachable service, insufficient permission and an empty search as different conditions. Preserve the original task through setup; verify uncertain writes before retrying. Any historical verification notes are dated evidence, not current readiness.

## Reading routes for the assistant

- For a concrete task, go directly to the selected `SKILL.md`; this README is not required reading for every run.
- For a capability/help question, use the introduction, first-task examples, skill table and relevant setup section, then recommend one first request. Skip maintainer notes unless the question concerns an update. On first relevant use, give a brief task-specific orientation; do not replay a tour on every invocation or claim the user has been permanently onboarded.
- Load the full selected procedure and its required support. References explain methods; scripts execute only the authorized operation; templates/assets are output material. Preserved libraries are conditional depth, not a bulk context load.
- Check actual callable tools and action/resource scope before promising access or completion.

## Maintainer and existing integration notes

This local Codex plugin uses a separately installed Discord Digest MCP server for bot-visible guild work. It does not copy the server, database, token, or other runtime data into the plugin. The `discord-computer-use` skill covers the user's personal DMs or an explicit UI request only when a suitable authorized API is unavailable.

Optionally configure the launcher in `~/.config/discord-connector/config.json`, or set `DISCORD_CONNECTOR_CONFIG` to another JSON file. Example:

```json
{
  "python": "/usr/local/bin/python3",
  "server_path": "~/tools/discord-digest-mcp/discord_digest_mcp.py",
  "db_path": "~/.local/share/discord-digest/discord-digest.sqlite"
}
```

Each value can instead be overridden with `DISCORD_CONNECTOR_PYTHON`, `DISCORD_CONNECTOR_SERVER`, or `DISCORD_CONNECTOR_DB`. Paths may use `~` and environment variables; relative paths resolve from the config file's directory. Keep credentials in the existing MCP's private storage, never in this package.

Install from the desired local marketplace, then verify the MCP's tool listing and a focused read. If a global `discord_digest` MCP is enabled, an explicitly configured launcher may create a second provider; migrate to one provider only after validating the explicitly configured optional MCP. Plugin discovery and `@Discord` availability depend on the product surface and must be checked there. The intended installed skill route in Codex is `$discord:discord` or explicit plugin selection when available.

Verify locally with `python3 -m unittest discover -s tests` and the Codex skill validator for all three skill folders. Installation and host configuration are handled separately.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional agents

[Studio roles and assignments](references/professional-agents/README.md) connect these skills to named jobs. Work Management maintains cross-studio coverage and handoffs; native registrations are installed separately for each host.
<!-- END PROFESSIONAL-AGENTS -->

## Public edition prerequisites and missing-provider example

Three complete skills retain bot identity, indexed/live evidence, draft/send authorization and the focused personal-account UI fallback. One automatic `.mcp.json` registration is omitted. The complete original `scripts/launch.py` and all launcher tests remain. Python 3 is needed for that optional helper; a separately installed Discord Digest implementation, its reviewed interpreter and an authorized local database are needed only for the bot route. Configure its existing JSON settings or documented environment variables explicitly. No token or database is supplied. Computer Use requires an available signed-in Discord UI and current host capability.

For “summarize recent decisions in channel 123” with no provider or UI access, report “Discord access is not configured for this channel; bring the channel/thread content or configure an authorized provider,” then preserve the requested scope. Do not invent a live read, convert an empty index into absence of messages, start a selfbot or send a reply. Synthetic launcher tests establish settings/argv and missing-settings behavior, not Discord access or a sent-message receipt.

## Version 0.2.0 bot setup integration

The complete original four-file Bot MCP Setup method is included, with receiving-host interpreter/storage examples. It preserves minimal intents/permissions, safe local token handling, unrelated MCP settings, actual tools/sync/export/readback verification and focused troubleshooting. No bot account, token, database, Discord runtime or automatic MCP registration is supplied. Setup/source review is distinct from an invited bot, live channel read or sent message.
