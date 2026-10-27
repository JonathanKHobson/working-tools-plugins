# Figma Design Toolkit

## One focused workflow

- `skills/figma-ui-operator`: direct Figma operations and shared detailed guides.
- `skills/figma-ui-operator/references/figjam-workshops.md`: conditional native FigJam authoring, preservation, reveal/lock/role checks, and review/reset handoff. Design UI guides do not establish FigJam API support.
- `skills/html-to-figma-clipboard`: Node CLI, serialized browser capture, local font/image resolution, rich clipboard helper, diagnostic fixture, bounded payload cache and explicit hosted boundary. `runtime/` contains only pinned npm manifests; dependencies/browser/outputs stay in the configured external runtime.
- `skills/stitch-figma-handoff`: convert/copy/paste, batch inventory, editable import QA.
- `skills/design-reference-prep`: optional Claude Desktop/Claude Design and imagegen references before Stitch.
- `skills/design-visual-qa`: visible usability, fidelity, structure, and Design Taste Gate.
- `.codex-plugin/plugin.json`: discovery and app metadata.
- `plugin.json` and `.claude-plugin/plugin.json`: portable and Claude-compatible discovery for the same maintained implementation.
- `LICENSE-SCOPE.json`, `PROVENANCE.json`, and `PUBLIC_FILE_MANIFEST.json`: scoped rights and per-file distribution evidence.
- `docs/validation.md`: exact check results and live-test limits.

Start at the relevant skill; load only the supporting guide needed for that step. Shared mechanics live in the operator references so fixes stay in one place. External tools remain supplied by the host: Computer Use for app interaction, optional built-in imagegen, optional Figma connector, and the user's accessible Claude/Stitch sessions. Claude Design availability is verified at execution time. There are no bundled MCP servers, hooks, credentials, or persistent background processes. HTML capture starts a short-lived headless browser; the optional Copy button server expires after five minutes.

## Provenance and updates

The operator is adapted from the user's supplied Figma UI Operator ZIP. Dated user-authorized task/history evidence informed import and recovery guidance; private source content is excluded. The focused QA guide adapts local design-taste-gate and UX heuristic principles without depending on their full tool stacks. Built-in imagegen remains a separate installed skill/runtime, not copied into this plugin.

Edit the owning skill or shared reference, validate every skill plus the plugin, check internal links, then use the plugin-creator cachebuster/reinstall flow for an installed update. Keep unrelated project work and raw design exports outside this plugin.

## Reconciled standalone methods

- `skills/figma-to-stitch-design-iteration/` and `skills/kyle-mac-design-partners/`: complete source-first standalone design iteration and local-partner consultation methods. Their examples and host context are recipient-ready; private original evidence remains in the author archive. File-level disposition is in `docs/standalone-additions-provenance.json`.
