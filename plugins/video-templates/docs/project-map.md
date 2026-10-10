# Project map

Video Templates owns the reusable public catalog, family/example selection, seven pinned staged methods and revisioned storyboard MCP runtime. Video Production Studio owns film production; Graphic Design owns art direction.

- `plugin.json`/`mcp.json` plus `.codex-plugin/plugin.json`/`.mcp.json`: one discovery head and stable `video-style-library` registration.
- `skills/video-templates/SKILL.md`: sole discoverable workflow entry.
- `data/catalog.json`: public Activity Atlas catalog snapshot, 30 families / 38 examples; no project media.
- `runtime/video-style-library/`: catalog projection, adapters, storyboard store and server.
- `runtime/library-chooser/`: pinned portable projection of the Design Templates chooser. Refresh from its canonical owner, never fork the shared implementation silently.
- `libraries/animate-methods/`: intact pinned third-party reference closure and source inventory; inactive upstream SKILL.md is not a discovery head.
- `scripts/video_style_library_mcp.py`: portable launcher and external binding adapter.
- `docs/source-provenance.json`, `docs/rights.md`, `DESIGN.md`: source identities, dependency/rights classification and observed design contract.
- `tests/`: cold-start and MCP stdio behavior checks. Host fixtures and render evidence stay in the consolidation workspace.

Verify with `python3 scripts/validate.py`, then an MCP-equipped interpreter running `tests/test_stdio.py`. Export review HTML with `python3 scripts/video_style_library_mcp.py --export-html /absolute/review/video-library.html`. Private state defaults to the existing external user data directory; never include it in a package.
