# Application appearance and theme selection

Use for an explicit app appearance, theme, readability or font-choice task. This original UX method needs no theme catalog plugin. The receiving application's supported appearance controls own actual application and export; their capabilities must be inspected at use time. It does not reproduce a third-party theme collection or its proprietary codec/builder.

## Ground and choose

Identify the application, requested choice/export/apply stage, user's supplied colors/font or named visual reference, normal ambient/viewing context, content examples and current settings. Reuse an explicit choice; otherwise use the incumbent system and offer only the useful variants. Do not imply eye-health benefits from aesthetic labels. A familiar theme name does not grant rights to bundled font files or a catalog reproduction.

For a new original palette, define roles: background/surface, primary/muted text, border, focus, accent/selection and error/warning/success/info. Use semantic roles rather than a long color list. Distinguish feedback by label/icon as well as hue. Check contrast for actual text/control roles, comfortable content hierarchy and focus visibility at the relevant display size; measured contrast is distinct from broad accessibility acceptance. For type, specify UI and code roles separately when the application supports them. Check actual availability, rights, glyph coverage, small labels, numbers and distinction of similar characters. Keep source quotes/code intact.

## Preview

Use the app's actual supported preview when available, or create a clearly labeled portable sample with representative headings, body text, muted text, links, input/focus, selected item and status/error. A portable preview is design evidence, not application. Map source/viewport anchors and inspect light/dark variants only when requested or useful for the current choice. Compare the same content and viewport. Record unresolved native rendering, syntax highlighting and font availability limits.

## Export or apply

Inspect current app controls/tool documentation before claiming an import string or deterministic export. If the application exposes a supported export, produce it with that tool and verify its readback. Use the original role-palette exporter below for the documented observed JSON interchange. Do not reverse-engineer an unknown native variant or invent import compatibility beyond the checked contract. Named legacy catalog palettes/previews remain outside this package. A generated export is prepared output; actual receiving-app import needs its own check.

Apply an already authorized change through actual supported settings. Record the starting choice for rollback, change only requested fields, and inspect the resulting application with representative content. If no supported apply operation exists, provide precise manual handoff based on observed controls and label the result prepared. Do not edit hidden config/database/installation files as a substitute. An exported string, saved palette, rendered preview and applied setting are distinct states.

## Acceptance

Verify role contrast, meaning without color, focus and representative text in the tested preview. Verify font readiness independently. For apply, verify the real app state/readback and the changed rendered anchors. For export, verify the supported output and receiving import capability. Deliver choice/palette or actual app outcome, evidence, rollback when changed and unresolved limits. Do not add a restart requirement without current application evidence.

Historical Material Themes content belongs to Robin Li, not OpenAI. Its catalog, builder and previews have unresolved redistribution rights and remain outside UX. [The compatibility record](../../../libraries/codex-material-themes/PROVIDER.md) documents the omission; no method-pack install is a normal step in this workflow.

## Functional original palette, export and preview

Use [application_appearance.py](../../../scripts/application_appearance.py), a standard-library Python tool independently implemented here. It contains no third-party theme catalog, brand assets, preview images or builder code. Colors/fonts can be supplied by the user; `example` emits an original neutral demonstration to edit, not a named catalog match.

```sh
python3 <plugin-root>/scripts/application_appearance.py example --output <project>/palette.json
python3 <plugin-root>/scripts/application_appearance.py validate --spec <project>/palette.json
python3 <plugin-root>/scripts/application_appearance.py export --spec <project>/palette.json --output <project>/theme-import.txt
python3 <plugin-root>/scripts/application_appearance.py preview --spec <project>/palette.json --output <project>/theme-preview.html
```

The own input schema version 1 requires `surface`, `ink`, `accent` (six-digit hex), `contrast` (integer 0–100 native parameter), `ui_font`, `code_font` (plain font names), `opaque_windows` (boolean), `semantic_colors` (`diffAdded`, `diffRemoved`, `skill`, each six-digit hex) and `variant` (`dark`, the observed supported case), plus `schema_version: 1`. `contrast` is not a WCAG ratio. The validator separately reports the text/surface luminance ratio; actual UI combinations still need review. Font names do not install or bundle font files. Unsupported variants/fields, malformed colors, control/CSS syntax in names and bad types fail instead of producing a plausible export.

The export is one deterministic line: prefix `codex-theme-v1:` followed by ordinary JSON containing `codeThemeId: "codex"`, `theme` (the role colors, native contrast, separate `fonts.ui`/`fonts.code`, `opaqueWindows`, `semanticColors`) and `variant`. This field contract was observed in the legitimately installed 1.0.2 Material Themes exporter, not copied from its implementation or catalog. JSON property order is semantically irrelevant. The implementation maps user values independently and validates the declared subset. Exact native import acceptance is separate from field/serialization validation.

The generated HTML is a self-contained original sample of headings, body copy, links, focus, input, UI/code font roles, diff/skill colors and palette rows. It uses no hosted assets, network requests or vendor screenshot. Its Select/Reset controls affect only the preview and visibly acknowledge their state. Inspect it in a supported browser at normal and narrow widths; it is a role preview, not a native Codex screenshot. The output files are preserved by default; `--replace` intentionally regenerates an existing output, and symlink outputs are refused.

On 2026-10-11, a receiving-app import check was attempted but the current computer-use tool expressly prohibited controlling `com.openai.codex`; no supported native theme tool was exposed. No restriction was bypassed and no hidden settings were inspected. Native import/application remains **unverified**, while the custom export and local preview can still be prepared and checked. CLI receipts set `native_import_verified: false` because the tool itself never operates the application. On an allowed receiving host, inspect its current Import controls, test the complete generated line, read back the applied palette/font roles and restore the baseline after a QA import. Do not claim applied from the export file or portable preview.
