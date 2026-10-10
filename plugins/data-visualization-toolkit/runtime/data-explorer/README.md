# Data Explorer MCP App

A local saved-table explorer for explicitly supplied immutable datasets. Includes source columns/units, missingness and zero preservation, semantic table and row bars, draft filters, selection, revisions, CAS saves, idempotent operation IDs and explicit discussion handoff. The model reads saved aggregates without raw rows; opening the app supplies rows to the UI. No file import, remote query, inference or data-cleaning service is included.

See [plugin installation](../../docs/installation.md). Node rebuild uses package-local pinned dependencies. The Python requirements are explicit. Private runtime bindings, Draw and Think sibling node_modules, datasets and caches are excluded from this public edition.

A local view change, successful save, context staging, delivered host message and actual assistant understanding are different states. The bridge feature-detects host capabilities and retains a copyable discussion summary when delivery is unavailable. A loopback preview is a QA surface and never native host acceptance.

Public rendered QA corrected the loading container live-region scope, explicit accessible select labels, primary control/table text size and narrow control/header wrapping. Light/dark synthetic loopback previews and relevant saved-view interactions were checked. This is separate from native MCP host acceptance or a complete accessibility certification.
