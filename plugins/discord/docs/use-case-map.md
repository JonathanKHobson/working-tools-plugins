# Discord: choose a workflow

For capabilities, first requests and setup, read [Start here](../README.md). For a known task use the matching skill directly. Read its complete procedure and only the conditional support it calls for. A listed MCP or provider still needs current runtime verification.

| Skill | Outcome and selection trigger |
| --- | --- |
| [discord](../skills/discord/SKILL.md) | Explain Discord capabilities and getting started, or use a Discord bot MCP for guild channels, threads, search, exports, and bot-identity messages. Route personal DMs or explicit UI requests to discord-computer-use only when suitable authorized API access is unavailable. |
| [discord-computer-use](../skills/discord-computer-use/SKILL.md) | Use observed Discord UI state as a narrow fallback for the user's personal DMs or an explicit UI request when suitable authorized API access is unavailable. Do not use for ordinary bot-visible guild work. |
