# Design Library

Use for requests to browse, compare or select reusable Site templates. Design Templates owns the gallery and retained editable template collection; Sites owns adapting/building a selected application. UX keeps this compatible route. The separately installed owner exposes only the catalog and sources authorized on the recipient host.

1. For independent AI retrieval or selection, call `search_design_library`; structured results never open a widget. Call `browse_design_library` only when intentionally presenting options for a human to choose, browse or inspect. The MCP Apps gallery shows actual desktop/mobile preview evidence, best uses, limitations and comparison controls. Search and comparison remain local UI state.
2. The user can inspect a template and select **Use this template**, optionally adding a brief. The app calls `prepare_design_handoff` and sends a selection message to the conversation only when the host supports it. A selection is not a created or deployed Site.
3. Before beginning a build, call `prepare_design_handoff` with the selected ID and brief to verify the current verified source. Read the returned template skill, preserve its reference, and use Sites to adapt a new working copy. Missing, changed or unsafe sources require repair/review, not a silent substitute.
4. Preserve the supplied brief's boundaries. The gallery never grants permission to publish or supplies real content from fictional examples. Source widgets retain their limits: e.g. Readiness Workbench is session-only, not persistent task management.

Search the receiving host's current authorized catalog by task or functional tag; do not promise a named template before confirming it is available. Native Office templates stay in their own galleries, and PDF export remains with its document owner.

If UI is unsupported, tools still return concise metadata and a verified handoff. Design Templates documents its own local gallery export when that runtime and an authorized collection are installed. Its standalone selection provides a copyable request for the assistant to verify; it must not be described as already sent to the assistant. No account, telemetry or external web service is needed.

For palettes, typography or unresolved component decisions without a template request, use the existing offline reference lookup. Native Office templates remain in their existing galleries; PDF outputs remain the Documents export workflow. Shareables remains an optional independent authoring system; its catalog-only entries are not yet included in this v1 gallery.

For unsuccessful or poor-fit AI library searches, follow [private search-miss recording](../../../references/atlas-library.md#ai-search-misses). Writing Voice Library records use `library="writing"`; Design Library uses `library="design"`; Atlas searches use `library="activity-atlas"`. MCP tools fix the library automatically; the CLI requires it explicitly. Preserve the actual route.
