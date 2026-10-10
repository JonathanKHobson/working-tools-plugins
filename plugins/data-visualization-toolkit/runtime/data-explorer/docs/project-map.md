# Data Explorer map

- `server.py`:stdio FastMCP tools and self-contained MCP App resource.
- `store.py`:bounded immutable source schema, SQLite storage, compare-and-swap/idempotent saves and authoritative calculation.
- `web/`:controls, semantic table, source-preserving preview computation and official SDK bridge.
- `build.mjs`, `package.json`, `package-lock.json`:package-local pinned app build; generated `dist/widget.html` retains bundled SDK/esbuild license notices.
- `preview.py`:loopback QA harness with origin/host/token checks.
- `tests/test_explorer.py`:storage, conflict, protocol and JavaScript/Python parity checks.

Use [installation](../../../docs/installation.md) for portable setup. Native rendered acceptance and conversation transport are separate from tests.
