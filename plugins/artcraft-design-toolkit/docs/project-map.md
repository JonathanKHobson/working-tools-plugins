# Project map

Purpose: one discoverable skill and one on-demand MCP gateway for the ten ArtCraft apps, with no always-on native servers or bundled upstream executables.

- `plugin.json`, `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json`: portable and host compatibility discovery.
- `mcp.json` and `.mcp.json`: portable and Codex compatibility registrations of the same on-demand gateway with plugin-relative paths.
- `scripts/artcraft_gateway.py`: host binding, allowlisted CLI execution, and one native MCP child session.
- `tests/test_gateway.py`: protocol, image pass-through, and EOF child cleanup checks with a fake native server.
- `skills/artcraft-apps/SKILL.md`: selection and operating boundaries.
- `skills/artcraft-apps/references/app-interfaces.md`: app-specific CLI, MCP, storage, and primary-source links.
- `README.md`: recipient setup and source validation.

Flow: a task activates the skill, resolves the host's installed CLI, reads the relevant app row, then uses `cli_run` or `open_session` plus native tool discovery and calls. The gateway spawns only the selected CLI and closes it after the session. The next command or version correction belongs in `references/app-interfaces.md`; gateway behavior belongs in `scripts/artcraft_gateway.py`; routing and shared safeguards belong in `SKILL.md`. Installed binaries, downloaded assets, projects, and rendered outputs live outside this source tree.
