---
name: design-templates
description: Browse, compare and select reusable visual templates; find a retained Site, document, presentation or spreadsheet from the Studio collection and hand it to its authoring provider.
---

# Design Templates

Use this owner for reusable visual templates. UX Design Studio owns interface critique and implementation methods; Brand Templates owns brand guides; native providers own adaptation and export.

For assistant-only Site retrieval, call `search_design_library`. Call `browse_design_library` only to intentionally present the existing visual chooser. Call `prepare_design_handoff` before adapting a selection: it validates the exact explicitly supplied source hash and returns a source path. Copy the verified source into a new working directory, read the package's `DESIGN.md` and `WORKFLOW.md`, then use Sites. Preserve the retained template.

For a first result, provide the audience, the task they should complete and the known content. Select one fitting source and read only its handoff references. Ask for missing facts only when they change the result; leave other unknowns explicit. The user's brief controls authorized changes and publication.

For a small onboarding, dated practice or evaluation-history adaptation, run `python3 scripts/template_catalog.py --recipes`, then `--recipe <id>`. The three original first-party recipes remain conditional on matching user-supplied sources. Supplied recipes map inputs to existing source fields or document regions; they do not create additional templates or imply completed runtime features.

Preserve each source's own token names and literal-value conventions. `design/foundations.json` already records observed values and scopes; do not add a duplicate token document or invent one shared palette. For a Site copy, use `scripts/check_template_tokens.py --help` for the source token check and comparison against the retained source. A static check does not replace rendered review.

The original private owner retains 16 Site selections and a 112-template collection; they are excluded from this public edition. For your explicitly supplied full-format inventory, run `python3 scripts/template_catalog.py --query "<need>" --kind <kind>` from this plugin root, or read [the catalog](../../templates/catalog.json). Resolve each relative reference within DESIGN_TEMPLATES_DATA_ROOT. The public default inventory is empty. Read only the selected `DESIGN.md` and `WORKFLOW.md`, verify the supplied provenance/template-assets.json, and hand the editable reference to the host's Documents, Presentations or Spreadsheets provider. These Office entries are retained source data, not newly executed native provider templates.

When building, extending or delivering a reusable template, read [template authoring acceptance](references/template-authoring-acceptance.md). Distinguish the editable source, clean starter and populated example; test real author edits and target-format behavior before claiming reuse.

Keep fictional examples fictional until verified content is supplied. Selection and preparation do not grant publication permission. Missing sources, unknown rights or unavailable providers require an honest limitation, not a replacement presented as equivalent. Official provider materials remain with their providers and are not bundled.

For a fresh host, follow [setup](../../docs/setup.md). Use the text tools and local HTML export when MCP Apps rendering is unavailable. Standalone selection is a copyable request until a host delivery is observed.
