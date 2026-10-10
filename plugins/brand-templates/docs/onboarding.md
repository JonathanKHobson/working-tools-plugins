# Run Brand Templates

Requires Python 3.10+ and `mcp==1.27.0` in an operator-selected environment. The standalone HTML exporter and catalog integrity checks use only the standard library. No fonts are required to browse raster previews; adapting/rendering selected kits requires their recorded font dependencies and a suitable output provider.

Use `BRAND_TEMPLATES_PYTHON` to select an existing Python executable with MCP installed. The launcher also honors an optional external `~/.config/studio-tools/design-library.json` object with an `interpreter` field. If neither is set, it uses the launcher's Python. Configuration, personal project data and credentials do not belong in this package. The launcher never installs dependencies.

Register the `brand-library` server from `.mcp.json` in the host through its native plugin manager. For a global MCP entry, use an absolute path to this package's `scripts/brand_library_mcp.py`, an appropriate interpreter and package cwd. Keep that host-specific entry outside the package. Register exactly one effective server with this ID per host; do not add a duplicate global entry if the plugin registration already exposes it.

`python3 scripts/brand_library_mcp.py --export-html /your/output/brand.html` exports the same UI. A standalone Use action provides a copyable fallback, without claiming source verification or a sent message. Actual MCP tools validate the registered source edition before returning the handoff.

This is a public-audience candidate, not a newly published release. Read per-asset notices, validate the target host and dependency environment, inspect privacy and packaging closure, and complete actual rendered and provider execution checks before any public distribution claim.


Collection-dependent history and commands describe the maintained source-owner collection. Its bodies and private integrity pins are excluded from public distribution. Bind your own authorized collection before running those commands; the fresh public runtime uses its documented fixture or included eligible kits.
