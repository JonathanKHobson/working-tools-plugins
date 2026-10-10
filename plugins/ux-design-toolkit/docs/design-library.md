# Design Library app

Design Templates is the canonical owner of the Design Library MCP app, its catalog, gallery, previews, source checks and handoff. UX retains a compatible launcher and selection method. The recipient must install Design Templates and provide an authorized template collection. Sites remains responsible for adapting and delivering a selected application. Selection does not create or publish a Site.

## Use

Ask: “Open Design Library,” “Show me a Site template for research evidence,” or “Compare our Site templates.” The existing `design-reference-lookup` skill routes these requests to `browse_design_library`. Preview desktop/mobile examples, inspect use cases and limits, and use the selection handoff to start a new working copy. Selection never deploys or publishes.

If a host does not render MCP Apps, the tools still provide text metadata and verified handoffs. For a local visual fallback, export the exact same gallery:

```sh
python3 /absolute/path/to/design-templates/runtime/design-library/server.py --export-html /absolute/path/design-library.html
```

This fallback's selected template becomes a copyable request for the AI to verify; it cannot claim to send a message to a host it is not connected to. Open the exported HTML in a browser. Use a local HTTP server for browser automation where the host requires HTTP(S).

## Runtime and data

Run the separately installed `design-templates` package and verify its `design-library` MCP server in the receiving host. The UX compatibility launcher `scripts/design_library_mcp.py` routes to an adjacent `design-templates` package or `DESIGN_TEMPLATES_ROOT`. It fails clearly when that owner is absent. This package does not include a private gallery, template previews, a fallback catalog or an Atlas data binding.

The owner verifies a selected template's editable source before handoff. Browse results and a local exported gallery may help comparison, but a standalone selection is a copyable request until the host confirms message delivery. Missing, changed or unauthorized source must remain unavailable for a verified handoff. For catalog additions, source integrity, MCP Apps behavior and native testing, follow Design Templates' current documentation and tests.

## Verification boundaries

An installed Design Templates package, its authorized source collection, MCP tool discovery and one source-verified handoff are distinct checks. A local export does not establish native host rendering or conversation delivery. Keep recipient configuration and source rights with that owner.

## References

- https://developers.openai.com/plugins/build/chatgpt-ui
- https://apps.extensions.modelcontextprotocol.io/api/documents/Quickstart.html
- https://github.com/modelcontextprotocol/ext-apps/tree/main/specification
- Shareables `design-system/registry/README.md`: source references, readiness and preview evidence conventions; inspected 2026-09-30.
