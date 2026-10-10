# Codex MCP Test Plan

Use this plan to verify that Codex can enable one MCP at a time, use it, disable it again, and return to a clean MCP-free baseline.

## Rules

- Codex is the only test target.
- Claude Desktop is read-only reference material only. Do not edit it as part of this plan.
- Start from `~/.codex/config.toml` in its MCP-free state.
- Use `~/.codex/config.mcp-disabled.backup.toml` and `~/.codex/mcp-profiles/` as the source for re-enabling one MCP at a time.
- Keep `playwright` as the primary recurring canary.
- After each Codex MCP test, restore the MCP-free baseline before moving to the next item unless a failure needs deeper debugging.

## Standard Lifecycle

For each MCP:

1. Enable exactly one MCP with `python3 ~/.codex/scripts/codex_mcp_manage.py enable <name>`.
2. Restart Codex.
3. Confirm the MCP appears in Codex and is usable.
4. Run one minimal smoke action.
5. Return to the MCP-free baseline with `python3 ~/.codex/scripts/codex_mcp_manage.py baseline`.
6. Restart Codex.
7. Confirm the MCP is gone and no helper process lingers.

## Text Pass

Before any live test:

- Confirm the registry row exists in `mcp-registry.md`.
- Confirm there is a matching snippet in `~/.codex/mcp-profiles/` or a matching block in the Codex backup config.
- Confirm the enable path is obvious and reversible.
- If there is a Claude alias, treat it as a read-only cross-check only.

## Helper Commands

- `python3 ~/.codex/scripts/codex_mcp_manage.py list`
  - show the Codex MCP inventory and current enable state
- `python3 ~/.codex/scripts/codex_mcp_manage.py status`
  - show currently enabled Codex MCPs
- `python3 ~/.codex/scripts/codex_mcp_manage.py enable playwright`
  - enable one MCP for a live smoke test
- `python3 ~/.codex/scripts/codex_mcp_manage.py baseline`
  - restore the MCP-free baseline after the test
- `python3 ~/.codex/scripts/codex_mcp_manage.py log-template`
  - create the run log template at `~/.codex/mcp-test-log.md`

## Run Log Template

Use one block per MCP:

- Date:
- Canonical name:
- Codex key:
- Enable path used:
- Disable path used:
- Launch time:
- Codex PID:
- Child process count at launch:
- RSS at 0 min:
- RSS at 2 min:
- RSS at 5 min:
- RSS at 10 min:
- RSS after close:
- Smoke action:
- Smoke result:
- Lingering child processes:
- Notes:

## Live Smoke Rows

| Canonical name | Codex key | Default state | Enable step | Disable step | Minimal smoke action |
| --- | --- | --- | --- | --- | --- |
| Playwright | `playwright` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable playwright` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Open a page or run a tiny browser validation |
| Figma | `figma` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable figma` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Confirm the MCP appears and can fetch design context |
| Pinboard network local | `pinboard_network_local` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable pinboard_network_local` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Confirm the local launcher starts and returns a small read |
| ChatGPT History | `chatgpt_history` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable chatgpt_history` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Confirm a history lookup or metadata read works |
| Dialog MCP | `dialog_mcp` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable dialog_mcp` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Confirm the server appears and responds to one lookup |
| AI Glossary Library | `aiglossary_library` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable aiglossary_library` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Run one terminology or framework lookup |
| Local Storage | `local_storage` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable local_storage` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Run one local evidence or path lookup |
| Kyle Second Brain | `kyle_second_brain` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable kyle_second_brain` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Confirm the knowledge-base server opens and returns one record |
| P2P GM MCP | `p2p-gm-mcp` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable p2p-gm-mcp` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Run one RPG knowledge query |
| Source Library | `source-library` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable source-library` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Confirm a source lookup or list request works |
| Idea Reality | `idea-reality` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable idea-reality` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Confirm the server starts and answers one prompt |
| MCP Open Library | `mcp-open-library` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable mcp-open-library` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Confirm a book lookup or catalog query works |
| MTG Oracle | `mtg-oracle` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable mtg-oracle` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Run one card lookup or rules query |
| Meigen | `meigen` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable meigen` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Confirm the server starts and responds to one simple call |
| TRPG MCP | `trpg-mcp` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable trpg-mcp` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Run one tabletop-oriented query |
| Arxiv Scout | `arxiv-scout` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable arxiv-scout` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Run one paper search or paper-detail request |
| Role-playing MCP Server | `role-playing-mcp-server` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable role-playing-mcp-server` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Confirm a story or role-play response works |
| Mnehmos RPG MCP | `mnehmos-rpg-mcp` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable mnehmos-rpg-mcp` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Run one RPG state or world query |
| Research Orchestrator | `research_orchestrator` | Disabled by default | `python3 ~/.codex/scripts/codex_mcp_manage.py enable research_orchestrator` | `python3 ~/.codex/scripts/codex_mcp_manage.py baseline` | Run one research orchestration lookup |

## Cleanup Criteria

After each disable step:

- Codex should return to the MCP-free baseline.
- No unexpected MCP helper process should remain.
- Idle memory should not keep climbing after the disable/restart cycle.
- If cleanup fails, stop and debug that MCP before moving on.

## Recommended Order

1. Playwright
2. Local Storage
3. Research Orchestrator
4. Arxiv Scout
5. One RPG MCP
6. One external-drive-backed MCP
7. The rest in whatever order matters most to the current work
