# Design Library app

Owner: UX Design Studio (`ux-design-toolkit`). Approved scope: browse, compare and select the three existing personal Site templates. Local-first, no accounts, paid APIs, publishing, source duplication, or new external dependencies.

## User flow

Ask for Site template options → search/filter a visual gallery → inspect desktop/mobile previews and use cases → compare up to three → select a template and optional brief → return an exact, version-bound handoff to the conversation. Selection is not creation or deployment. A standalone HTML fallback offers the same gallery with a copyable handoff.

The AI interprets the brief and adapts the selected retained source using Sites. The interface supports visual comparison and communicates the stable selection to the model. Existing template packages remain authoritative. Shareables supplies registry conventions (best-for, avoid-when, readiness, evidence provenance), not a mandatory live service or a replacement renderer.

## Implementation boundaries

- `catalog.json`: three portable records, IDs, descriptive/use-case metadata, source skill names and expected source hashes. No private absolute paths. Future additions are explicit catalog records.
- `assets/`: derived, original fictional-content desktop/mobile preview images, with provenance and hashes. No retained app source duplication.
- `catalog.py`: validate/query registered records; resolve installed personal template packages; reject missing, changed, malformed, escaping or symlinked sources for handoff. Read only.
- `server.py`: MCP through the already installed Python MCP SDK, stdio; UI resource `ui://design-library/gallery.html`; optional standalone export command.
- `ui/`: dependency-free HTML/CSS/JS gallery and standards-based MCP Apps bridge. No remote scripts/fonts or analytics. DOM text insertion for catalog data.
- `tests/`: meaningful catalog safety, MCP protocol, source integrity, handoff and UI-state checks.

## Tool and view contract

`browse_design_library(query="", category="all")`: read-only, returns `{schemaVersion:1, items:[...], query, category, owner:"UX Design Studio"}` in structuredContent, compact text summary. Tool metadata links the gallery UI. Images stay in resource HTML bootstrap, not model-visible tool text.

`prepare_design_handoff(template_id, brief="")`: read-only, validates source freshness and returns `{templateId, name, skillName, sourcePath, sourceHash, mode:"complete-template", brief, instructions, handoffText}`. Never accepts arbitrary filesystem paths, executes source, edits it or deploys. The UI sends this confirmed selection through the host bridge; if unavailable, shows a copyable handoff without pretending it reached the model.

UI bootstrap `window.DESIGN_LIBRARY_DATA`: `{schemaVersion:1, owner, items:[{id,name,summary,category,tags,bestFor,avoidWhen,interactions,limitations,skillName,sourceHash,availability,desktopPreview,mobilePreview}]}`. Image fields are self-contained data URLs; availability is `ready`, `missing` or `changed`. UI input escaping and textContent required. Detail/compare/search state is local; no per-click backend calls except handoff.

### Compact chooser presentation

The hosted and standalone gallery opens as a compact chooser headed `Design Templates`. The initial state is one horizontal, scroll-snap row of preview cards with previous/next controls, concise search and category filtering, and a `More filters` disclosure for tags. Cards retain the supplied desktop preview evidence and expose a keyboard- and touch-accessible three-dot menu with `View` and `Use`; unavailable sources keep `Use` disabled. `View` opens a fuller detail surface with an explicit `Back to templates` action, desktop/mobile preview tabs and the existing validated handoff flow. The widget does not add a redundant outer close control for the detail surface. Layouts must remain usable inline, in a side panel and at narrow widths without horizontal page overflow; theme values follow the host light/dark context. Loading, empty and unavailable preview states remain explicit. If the host cannot accept a user-initiated message, `Use` labels the result as a copyable handoff and never claims that it was sent.

## Acceptance

All three installed templates appear with actual preview evidence. Search/empty/reset, details, compare, selection and fallback work; keyboard/focus and narrow-screen layout checked. MCP initialize/list/read/call verified using SDK client; UI metadata, no-image model results and missing/stale-template refusal checked. Install through the supported personal plugin route, then verify installed bytes and discovery. Native host UI display/selection must be reported separately from local/browser/bridge-harness evidence.

## Sources

- MCP Apps specification and OpenAI plugin UI documentation; use supported `ui://`, `text/html;profile=mcp-app`, `_meta.ui.resourceUri`, `ui/initialize`, tool-result notifications, tools/call and model-visible selection message.
- Existing Shareables registry contracts and the verified September 29 Studio template import. Do not relabel inspiration-only records as functional templates.

Future work: cross-format visual directions, DTCG token extraction and vetted Shareables/widget adapters. PDFs remain Documents exports. These are not included in v1.
