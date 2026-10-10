# Discord account access

Checked 2026-10-01. Use the smallest suitable authorized route. The computer-use skill is an optional last fallback, not a background inbox mirror.

| Route | Actual scope | Current use |
| --- | --- | --- |
| Bot REST / Digest Helper | Servers and conversations visible to the bot; sends as bot | Primary MCP route |
| Social SDK | Linked-user messaging for approved game integrations; history limited to 200 messages / 72 hours; history fails if either participant has not played the game | No documented general personal-assistant integration; not configured |
| OAuth / local RPC | Restricted scopes and approval; documented local message reading, no documented ordinary DM-send command | Not configured; not a complete inbox/send replacement |
| Signed-in Discord UI | Conversations the user can view; UI composition under that account | Optional focused fallback after API suitability check |
| Discord data package | The user's own sent messages, rather than complete incoming conversations | Prefer for authorized bulk writing-style analysis; user selects/requests export |

The SDK requires sends to follow user action. Do not mistake user installation of a bot for permission to read the user's inbox. No personal-account API tokens are needed by the UI fallback. Live UI receipt verification is required before reporting a send as verified.

Official sources:

- [OAuth scopes](https://docs.discord.com/developers/topics/oauth2)
- [RPC commands and approval](https://docs.discord.com/developers/topics/rpc)
- [Social SDK client and history limits](https://discord.com/developers/docs/social-sdk/classdiscordpp_1_1Client.html)
- [Message content and sending restrictions](https://discord.com/developers/docs/social-sdk/classdiscordpp_1_1MessageHandle.html)
- [Game communication approval](https://discord.com/blog/discords-powerful-cross-platform-chat-ready-for-your-game)
- [Discord data package](https://support.discord.com/hc/en-us/articles/360004957991-Your-Discord-Data-Package)

Recheck these sources when an approved account integration becomes available. Do not repeat this investigation for every ordinary DM request.
