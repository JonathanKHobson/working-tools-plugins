> Historical source evidence with receiving-host-neutral locators. Listed configuration, availability, old observations and changes are not current facts or instructions for the recipient. Inspect actual callable capabilities and preserve active jobs before acting. No private config or corpus is supplied.

# MCP Registry

Use this as the canonical inventory for Codex and Claude MCPs on this Mac.

## Source Of Truth

- Codex active config: `~/.codex/config.toml`
- Codex preserved full inventory: `~/.codex/config.mcp-disabled.backup.toml`
- Codex per-server snippets: `~/.codex/mcp-profiles/`
- Claude Desktop config: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Claude Desktop profile files:
  - `~/Library/Application Support/Claude/claude_desktop_config.full-consolidated.json`
  - `~/Library/Application Support/Claude/claude_desktop_config.research-suite-package.json`
  - `~/Library/Application Support/Claude/claude_desktop_config.generic-ttrpg-suite-package.json`
  - `~/Library/Application Support/Claude/claude_desktop_config.storage-transition-package.json`
  - `~/Library/Application Support/Claude/claude_desktop_config.social-intake-package.json`
  - `~/Library/Application Support/Claude/claude_desktop_config.dev-utility-package.json`
  - `~/Library/Application Support/Claude/claude_desktop_config.workbench-core.json`
  - `~/Library/Application Support/Claude/claude_desktop_config.research-pack.json`
  - `~/Library/Application Support/Claude/claude_desktop_config.rpg-pack.json`
  - `~/Library/Application Support/Claude/claude_desktop_config.study-or-quarantine.json`
  - `~/Library/Application Support/Claude/claude_desktop_config.full-fleet.json`
- Fleet report: `~/.codex/skills/focus-ops-manager/references/claude-mcp-fleet-report.md`

## Activation Rule

- Codex keeps an automation-safe active MCP footprint, with Kyle Second Brain as the permanent fail-soft baseline MCP. The logical baseline is `arxiv-scout`, `critical-compass`, `discord_digest`, `knowledge_atlas`, `shareables`, and `kyle_second_brain`. Critical Compass is supplied by the enabled `research-methodology-local@personal` plugin when its current installed manifest packages the `critical-compass` MCP; otherwise the global `[mcp_servers.critical-compass]` block is the fallback. Knowledge Atlas is supplied by the enabled `prompt-playbook-studio@personal` plugin when its current installed manifest packages `knowledge_atlas`; otherwise the global `[mcp_servers.knowledge_atlas]` block is the fallback. `codex_mcp_manage.py baseline` chooses each provider from installed metadata and preserves the other baseline MCPs. If KSB is missing from Codex config, repair it with `python3 ~/.codex/scripts/codex_ksb_mode.py enable`. A manifest declaration does not prove runtime health; verify initialize, tool listing, and a representative overview before relying on a newly installed provider or retiring the global block.
- Kyle Second Brain's Codex profile stays preserved at `~/.codex/mcp-profiles/kyle_second_brain.toml` with `required = false`, the exact 12-tool `codex-core` allowlist, `KSB_TOOL_PROFILE=codex-core`, the arm64 runtime `~/.local/share/kyle-second-brain/venv-arm64/bin/python`, and local Chroma sidecar `KSB_CHROMA_PATH=~/.local/share/kyle-second-brain/chroma-local`; full/admin KSB access is for Claude, direct smoke tests, or deliberate admin use. KSB is permanent but nonfatal in Codex because `required = true` can turn a host-side handshake glitch into a failed chat resume.
- Do not claim Kyle Second Brain is available in a Codex session until `tool_search` finds `memory_context_pack`, `memory_search`, and `memory_capture_working_note`.
- Run `python3 ~/.codex/scripts/codex_ksb_mode.py expose-all-chats` for the standard KSB every-chat gate. It enforces the KSB baseline, checks project config shadows, runs exact direct smoke, attempts app-server MCP reload/status when a control socket exists, and writes `~/.codex/state/ksb-exposure.json`.
- KSB-specific May 2026 root cause: duplicate Codex stdio starts for the fixed
  `KSB_CLIENT_PROFILE=codex-global` were blocked by KSB's server-instance
  runtime lock, closing MCP `initialize` before Codex could index tools. The
  fixed state is `python3 ~/.codex/scripts/codex_ksb_mode.py lock-diagnostic`
  returning `codex_global_lock_nonfatal`; exact `codex-global` and unique
  Codex profiles should both list the exact 12 `codex-core` tools. Writer
  locks remain separate and must stay enforced for `memory_capture_*`.
- If a stale Codex conversation cannot expose KSB through `tool_search` but
  config and direct smoke are healthy, use the standard direct fallback
  `~/.codex/scripts/ksb_direct_tool.py` for immediate KSB
  retrieval/capture. Keep reporting that native exposure failed in that
  conversation; the fallback is continuity, not proof of native tool exposure.
- Public Codex Desktop bug evidence exists for this same failure shape: MCPs
  can appear in Settings or `codex mcp list` while Desktop chat cannot use
  them, or resume with confusing/missing MCP tool behavior. See OpenAI Codex
  issues #10499 and #18233 before rebuilding KSB or its indexes.
- To use a Codex MCP, copy one block back into `~/.codex/config.toml` or uncomment the matching block.
- Claude uses its own config file and does not depend on the Codex MCP state.
- Claude Desktop active config is now the `full-consolidated` posture: `research_orchestrator`, `aiglossary_library`, and `oppia_markdown_search` are merged into `research_suite_package`.
- Full-fleet boot is preserved for inspection only and should not be the normal daily posture.
- When several Claude MCPs fail together, switch profiles and run the fleet checker before debugging individual repos.
- When talking to the assistant, use the Codex key below unless the Claude alias is the one you actually need.
- After a Codex task uses an extra MCP, restore the automation-safe baseline before signoff
  unless the user explicitly asked to keep that MCP enabled.

## Inventory

Important:
- The `Claude key` column below is the key to use when a server is present in a Claude Desktop profile. It is no longer a promise that the server is in the current active profile.
- Local stdio servers listed here are available through Claude Desktop on this Mac. They are not the same thing as Claude.ai cloud MCP connectors.
- Per Anthropic's MCP connector docs, Claude.ai cloud/API connectors require publicly reachable HTTPS MCP servers. Local stdio servers cannot be attached to Claude.ai cloud directly.
- Every live Claude MCP either exists in the preserved `full-fleet` profile or is represented by `research_suite_package`.

| Canonical name | Codex key | Claude key | Focused profiles | Risk class | Runtime note | Safe for daily | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Figma | `figma` | not in Claude profiles | none | pack-only | remote connector | no | Codex-only design lane today. |
| Playwright | `playwright` | `playwright` | `study-or-quarantine` | study | `npx` launcher | no | Useful on demand, not part of the daily Claude profile. |
| Pinboard network local | `pinboard_network_local` | `pinboard_network_local` | none | retired | system Python -> external script | no | Failed experiment. Removed from active Claude profiles; preserved only in older backups if ever needed for archaeology. |
| ChatGPT History | `chatgpt_history` | `chatgpt_history` | `research-pack` | pack-only | home runtime -> external script/data | no | Research recall MCP. |
| Dialog MCP | `dialog_mcp` | `dialog_mcp` | `research-pack` | pack-only | `npx` launcher | no | Research/discussion bridge. |
| Research Suite Package | not configured | `research_suite_package` | active config, `research-pack`, `research-suite-package` | daily-default | home runtime -> `$PROJECT_VOLUME/Documents/My Projects/MCPs/archive-review/research/research-suite-package/research_suite_mcp_server.py` | yes | Active consolidated replacement for `research_orchestrator`, `aiglossary_library`, and `oppia_markdown_search`. |
| AI Glossary Library | `aiglossary_library` | `aiglossary_library` | preserved legacy/full-fleet profiles | merged | home runtime -> external script | no | Merged into active `research_suite_package`; standalone entry preserved for rollback/legacy profiles. |
| Knowledge Atlas | `prompt-playbook-studio@personal` packaged MCP `knowledge_atlas`; global `knowledge_atlas` fallback | `knowledge_atlas` | `workbench-core` | daily-default | installed Prompt Playbook Studio `.mcp.json` or preserved global profile | yes | Keep one Codex provider. The baseline helper omits the global block only when the enabled installed plugin version declares this MCP; otherwise it restores the global fallback. Verify live tool exposure separately. Full active Knowledge Atlas AI-facing sidecar: SQLite/FTS plus Chroma, read-only MCP over `$PROJECT_VOLUME/Documents/My Projects/MCPs/Knowledge Atlas/data`; also merged into active Claude config plus preserved `full-consolidated` and `full-fleet` profiles on 2026-05-02. |
| Local Storage | `local_storage` | `local_storage` | `workbench-core`, `research-pack` | daily-default | home runtime -> external script/data | yes | Machine evidence and storage conventions. |
| Kyle Second Brain | `kyle_second_brain` | `kyle_second_brain` | `research-pack` | daily-default | arm64 home runtime -> canonical MCP app/data + local Chroma sidecar | yes | Permanent Codex baseline. Codex must use compact `KSB_TOOL_PROFILE=codex-core`; full/admin surface remains available to Claude, direct smoke tests, or deliberate admin use. If direct MCP health passes but `tool_search` does not expose KSB, run `codex_ksb_mode.py lock-diagnostic` before blaming Codex generally; exact `codex-global` failing while a unique profile passes means the KSB runtime lock regressed. Semantic backend uses `KSB_CHROMA_PATH=~/.local/share/kyle-second-brain/chroma-local`; do not point live Codex/Claude at the external-drive Chroma store unless a fresh health check proves it no longer segfaults. |
| Kyle Second Brain Canary | `kyle_second_brain_canary` | not configured | none | temporary diagnostic | home runtime -> same KSB script/data, `KSB_CLIENT_PROFILE=codex-canary` | temporary | Temporary Codex comparison MCP exposing only `stats`, `memory_context_pack`, and `memory_search`. Keep only through several restart/new-chat cycles after the 2026-05-02 lock fix; do not treat it as the permanent memory namespace. |
| P2K GM MCP | `p2k-gm-mcp` | `p2k-gm-mcp` | `rpg-pack` | pack-only | home runtime -> external script/data | no | RPG/game knowledge lane. |
| P2P GM MCP | `p2p-gm-mcp` | `p2p-gm-mcp` | `rpg-pack` | pack-only | home runtime -> external script/data | no | RPG/campaign knowledge lane. |
| Source Library | `source-library` | `source-library` | `research-pack` | pack-only | `npx` launcher | no | Source retrieval and library lookup. |
| Idea Reality | `idea-reality` | `idea-reality` | `research-pack` | pack-only | system Python launcher | no | Grounding / idea-vs-reality support. |
| MCP Open Library | `mcp-open-library` | `mcp-open-library` | `study-or-quarantine` | study | system Node launcher | no | Useful but not daily-critical. |
| MTG Oracle | `mtg-oracle` | `mtg-oracle` | `rpg-pack` | pack-only | `arch` wrapper -> system runtime | no | MTG-specific lookup. |
| Meigen | `meigen` | `meigen` | `study-or-quarantine` | study | `arch -arm64` wrapper -> system `npx` | no | Utility MCP; force arm64 because the `sharp` runtime failed when inherited as x64. |
| TRPG MCP | `trpg-mcp` | `trpg-mcp` | `rpg-pack` | pack-only | system `dotnet` -> external DLL | no | Tabletop RPG support lane. |
| Critical Compass | `research-methodology-local@personal` packaged MCP `critical-compass`; global `critical-compass` fallback | `critical_compass` | `workbench-core`, `research-pack` | daily-default | installed Research Studio `.mcp.json` or preserved global profile | yes | Keep one Codex provider. The baseline helper omits the global block only when the enabled installed plugin version actually declares this MCP; otherwise it restores the global fallback. Verify live tool exposure separately. |
| Prompt Compass | not configured | `prompt_compass` | `workbench-core` | daily-default | home runtime -> external script/data | yes | Core daily prompt-engineering MCP. |
| Arxiv Scout | `arxiv-scout` | `arxiv-scout` | `research-pack` | pack-only | `npx` launcher | no | Academic search lane. |
| Shareables | `shareables` | `shareables` | `workbench-core` | daily-default | home runtime -> external script/data | yes | Public-output shipping lane. |
| Role-playing MCP Server | `role-playing-mcp-server` | `role-playing-mcp-server` | `rpg-pack` | pack-only | `npx` launcher | no | Lighter RPG/story lane. |
| Mnehmos RPG MCP | `mnehmos-rpg-mcp` | `mnehmos-rpg-mcp` | `rpg-pack` | pack-only | `arch -arm64` wrapper -> canonical dist/data | no | Canonical runtime under MCP home; force arm64 because `better-sqlite3` is arm64. |
| Research Orchestrator | `research_orchestrator` | `research_orchestrator` | preserved legacy/full-fleet profiles | merged | home runtime -> external script/data | no | Merged into active `research_suite_package`; standalone entry preserved for rollback/legacy profiles. |
| GitHub | `github` | `github` | `study-or-quarantine` | study | local binary wrapper | no | Keep out of daily Claude until explicitly needed. |
| Discord Digest | `discord_digest` | `discord_digest` | `study-or-quarantine` | study | system Python launcher | no | Not part of the default daily workbench. |
| Oppia Markdown Search | not configured | `oppia_markdown_search` | preserved legacy/full-fleet profiles | merged | home runtime -> external script/data | no | Merged into active `research_suite_package`; standalone entry preserved for rollback/legacy profiles. |
| Stargate Playtest MCP | `stargate_playtest_mcp` | `stargate_playtest_mcp` | `rpg-pack` | pack-only | home runtime -> external script/data | no | Game playtest lane. |
| Think MCP | `think-mcp` | `think-mcp` | `study-or-quarantine` | quarantine | `npx` launcher | no | Keep quarantined until it stops emitting invalid JSON. |
| Sequential Thinking | `sequential-thinking` | `sequential-thinking` | `study-or-quarantine` | study | `npx` launcher | no | Study-only in Claude for now. |
| ThoughtProof | `thoughtproof` | `thoughtproof` | `study-or-quarantine` | study | `npx` launcher | no | Verify account/API needs before active use. |
| Ethics Vibe Check | not configured | not in Claude profiles | none | study | source mirror only | no | Needs `GEMINI_API_KEY`; not a live installed profile. |
| Claude Prompts | not configured | not in Claude profiles | none | study | study library only | no | `mcp-shield` flagged path traversal risk; do not install live. |

## Fast Enable Notes

- Preferred helper:
  - `python3 ~/.codex/scripts/codex_mcp_manage.py enable <name>`
  - `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` restores the automation-safe logical set: `arxiv-scout`, `discord_digest`, `knowledge_atlas`, `shareables`, `critical-compass`, and `kyle_second_brain`. Knowledge Atlas and Critical Compass use their enabled installed plugin MCPs when the exact installed manifests declare them; otherwise their global blocks are restored as fallbacks
  - `python3 ~/.codex/scripts/codex_mcp_manage.py ksb-only` is temporary diagnostic mode only
- Kyle Second Brain Codex mode helper:
  - `python3 ~/.codex/scripts/codex_ksb_mode.py status`
  - `python3 ~/.codex/scripts/codex_ksb_mode.py enable`
  - `python3 ~/.codex/scripts/codex_ksb_mode.py expose-all-chats`
  - `python3 ~/.codex/scripts/codex_ksb_mode.py lock-diagnostic`
  - `python3 ~/.codex/scripts/codex_ksb_mode.py disable --confirm-temporary-disable` only for deliberate temporary emergency removal
- Codex:
  - Copy one block from `~/.codex/config.mcp-disabled.backup.toml`
  - Or copy the matching snippet from `~/.codex/mcp-profiles/<name>.toml`
  - Restart Codex after the edit
  - For Kyle Second Brain, prefer `python3 ~/.codex/scripts/codex_ksb_mode.py expose-all-chats`; verify `KSB_TOOL_PROFILE = "codex-core"`, arm64 `venv-arm64` runtime, `KSB_CHROMA_PATH` points to the local sidecar, exact 12-tool direct smoke, `lock-diagnostic` is `codex_global_lock_nonfatal`, and then confirm `tool_search` finds `memory_context_pack`, `memory_search`, and `memory_capture_working_note`
- Claude:
  - Edit `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Keep the launcher paths stable, especially for external-drive runtimes
  - Prefer switching among named profile files over expanding the default daily profile

## Test Plan

- Use [mcp-test-plan.md](mcp-test-plan.md) for the Codex-only enable/disable smoke test sequence.
- For Claude Desktop health:
  - `python3 ~/.codex/skills/local-data-mcp-builder/scripts/check_claude_mcp_fleet.py`
  - `<mcp-enabled-python> ~/.codex/skills/local-data-mcp-builder/scripts/smoke_claude_profile.py --config ~/Library/Application\\ Support/Claude/claude_desktop_config.workbench-core.json`

## Most Common Codex MCPs

- `arxiv-scout`, `critical-compass`, and `discord_digest` for the Weekly AI Brief automation
- `knowledge_atlas` and `shareables` for daily project/output support
- `playwright`
- `local_storage`
- `kyle_second_brain` as the permanent baseline, repaired with `python3 ~/.codex/scripts/codex_ksb_mode.py enable` if missing
- `chatgpt_history`
- `research_orchestrator`
- `arxiv-scout`
- `figma` when design context is needed

## New MCP Intake Rule

Before a new MCP is allowed into Claude Desktop, declare:

- profile assignment
- runtime location
- command type
- expected startup SLA
- default enabled status

Then run the fleet checker and the target profile smoke test before making it part of the active daily Claude profile.
