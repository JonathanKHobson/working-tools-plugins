# External catalog setup

Required dependencies are an operator-supplied Python 3.10+ environment with `mcp` and `PyYAML`, a compatible `studio-library-v1` SQLite catalog, and its original source vault mounted at the catalog's recorded location. Obtain Python and the two packages through the target host's normal package manager/environment workflow. The plugin ships neither dependencies nor the private corpus. An operator with authorized source notes can build an index explicitly through this package's `server.py --build --vault <external-vault> --db <external-catalog.sqlite>`. Building never occurs during search/startup.

The stdlib bootstrap uses `python3` from the host PATH, then executes the configured interpreter. Supply the private JSON binding at `~/.config/studio-tools/atlas-library.json`, or set `ACTIVITIES_ATLAS_CONFIG` to a different external JSON file. Existing `server` keys are accepted by the host's old compatibility launchers; this package always runs its own `runtime/studio_library/server.py`.

```json
{
  "interpreter": "/absolute/path/to/environment/bin/python",
  "database": "/absolute/path/to/external/studio-library.sqlite",
  "search_misses_database": "/absolute/path/to/external/observability/library-search-misses.sqlite"
}
```

`search_misses_database` is optional; its default is the catalog's parent directory plus `observability/library-search-misses.sqlite`, preserving the original private feedback location. The launcher refuses a catalog or feedback path inside the plugin. A missing/malformed binding, interpreter or catalog produces a concise unavailable message, exits nonzero and makes no repair, download or substitute-corpus attempt. Missing original vault sources likewise leave the source provider unavailable. Do not mistake installation for access.

Harmless verification: with the configured interpreter, run `runtime/studio_library/server.py --db <external-catalog.sqlite> --domain facilitation --status`. Status reads the catalog and original source hashes, without modifying notes or rebuilding. Normal MCP startup is `python3 scripts/atlas_library_mcp.py facilitation`; the domain is fixed for that process and no extra launcher arguments are accepted.

For a private scoped HTML snapshot, use `server.py --db <external-catalog.sqlite> --domain facilitation --export-html <private-output.html>`. The export includes original source bodies and paths. Keep it private and outside the canonical vault/runtime. An export is a dated snapshot, not a live channel. Check the rendered output before visual signoff.

The existing whole-Atlas baseline is independent. Do not remove its global registration, move its source vault/database, or use installation as permission to publish its contents. Before cutover, compare each preserved tool/resource contract, install this owner, retire only duplicate plugin registrations, and keep a recoverable predecessor snapshot.
