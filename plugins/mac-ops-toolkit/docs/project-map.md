# Project map: mac-ops-toolkit

- `.codex-plugin/plugin.json`: identity and native discovery.
- `skills/`: independently selected runtime entrypoints and their narrow supporting material.
- `references/` or `libraries/` where present: conditional shared/deep resources; never load everything by default.
- `README.md`: ownership, private-source boundaries and install workflow.
- `docs/`: source-to-target and maintenance notes. Work Management owns the shared `skill-plugin-map.md`.

Maintain the canonical owner and mirror distributable files byte-for-byte to the public package. Validate changed entrypoints and manifests, exercise affected helpers and task routes, then install the selected version through the host's plugin manager. Start a new task to use refreshed discovery. Recipient volume roles and provider bindings remain outside the package.

## Reconciled standalone methods

- `skills/local-storage-mcp/` and `skills/storage-memory-manager/`: complete source-first storage routing, diagnosis and read-only helpers. Recipient volume paths and provider access are supplied at use time. File-level disposition is in `docs/standalone-additions-provenance.json`.
