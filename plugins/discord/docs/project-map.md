# Project map

The plugin routes Discord work through an external bot MCP and a narrow personal-account UI fallback.

- The three outer manifests: package identity and complete two-skill discovery; no automatic MCP registration.
- `skills/discord/SKILL.md`: bot-first guild workflow and send boundaries.
- `skills/discord-computer-use/SKILL.md`: personal DM and explicit UI fallback.
- `scripts/launch.py`: reads local connector paths and replaces itself with the existing server process.
- `tests/test_launch.py`: launcher behavior checks.

Flow: An operator explicitly selects the optional provider → launches `scripts/launch.py` → launcher reads user config and `execv`s the separately installed Discord MCP. Update skill routing in `skills/`; update path resolution in `scripts/launch.py`. Run `python3 -m unittest discover -s tests` for launcher changes.
