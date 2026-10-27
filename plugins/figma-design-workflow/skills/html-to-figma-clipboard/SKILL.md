---
name: html-to-figma-clipboard
description: Render a local HTML file or localhost app into editable Figma clipboard data and copy rich HTML to the macOS clipboard, ready for Cmd+V. Use for local HTML-to-Figma capture, offline assets, viewport or selected-element export; no Figma connection is needed for conversion.
---

# HTML to Figma Clipboard

Use the bundled, pinned `@figit/dom-to-figma` engine through the executable wrapper. Conversion runs locally, without a Figma account connection, API key, destination file, or Figma plugin. The normal handoff ends with rich clipboard writing, then the user switches to Figma and presses Cmd+V.

## Run

Resolve this skill's actual directory; do not assume a developer's machine path. Node 22+ is required. First-use setup installs locked dependencies and a headless Chromium into a user-selected runtime directory. Prefer the host's configured bulk-storage destination. Verify the mount before a large install.

```sh
node scripts/setup.mjs /absolute/path/to/runtime
node scripts/capture.mjs /absolute/path/design.html --offline --out /absolute/path/output
node scripts/capture.mjs http://localhost:3000 --width 1440 --height 1000 --selector '#app' --out /absolute/path/output
```

Run these commands from this skill directory or use absolute script paths. Setup saves only the runtime binding in `~/.config/html-to-figma-clipboard/runtime.json`. Pass `--runtime` to override it. Dependencies and browser are installed once; conversion works offline afterward.

- Default `--layout auto` infers native Auto Layout with the converter's per-container geometry fallback. Use `--layout absolute` for a fully absolute capture.
- Offline is the default. It blocks external page HTTP(S), websocket, font and image requests and reports unresolved resources. `--allow-external` explicitly permits source assets while conversion still stays local. It never selects a hosted converter.
- Wait for fonts and images, plus the configured settling interval. For apps, use `--ready-selector '[data-ready]'` and `--settle-ms 1000` when needed. There is a 60-second overall timeout, configurable with `--timeout` in milliseconds.
- For fonts unavailable as local single-file fonts, supply `--font-map /absolute/fonts.json`. Read [usage and limitations](references/usage.md) for the manifest, CSS font support, asset root and fidelity boundaries.
- Use `--strict` to reject warnings before clipboard writing. Otherwise a degraded capture is copied with its report. `--no-copy` prepares files only; `--no-cache` forces conversion.

Never replace this route with text-only `pbcopy`. The native helper writes `public.html` and checks exact UTF-8 readback. If it fails, run the returned `copy` command and open its localhost URL for the **Copy for Figma** button. It uses `ClipboardItem(text/html)` with a rich copy-event fallback, and closes after successful copy or five minutes. Stop it with Ctrl+C when finished.

## Verify and hand off

Read `report.json`: converter/browser versions, resources, warnings, font diagnostics, omitted-node candidates, cache reuse, payload structure and clipboard receipt. Keep conversion, rich clipboard writing, actual Figma paste, visual fidelity and editability as separate states. Every capture starts the last three as unverified. A valid `fig-kiwi` envelope or native readback cannot verify Figma acceptance.

When actual paste checking is requested and Figma is available, use the existing operator and visual-QA skills: use a suitable test destination, paste, inspect native text/vector/layer properties, edit and restore one text sample, compare rendered anchors, and report the observed gaps. Otherwise leave the payload copied and provide the fixture and manual checks. Do not create or alter a destination merely to run an ordinary conversion.

The helper serializes capture browsers with a host-wide lock, closes browser/server on success, error, SIGINT and SIGTERM, and bounds reusable payloads to ten entries, 256 MiB and seven days. It freshly renders and hashes observed resources, DOM/computed geometry, resolved font bytes, viewport/settings, wrapper, browser and dependency lock before reuse. No persistent capture browser or service is installed. Hard-kill and OS crash cannot run cleanup handlers; a dead PID lock is reclaimed on the next run.

Hosted conversion has a separate, explicit adapter in `scripts/hosted.mjs`; read [hosted mode](references/hosted.md) only when the user selects divRIOTS code.to.design. Never activate it after a local failure. Actual `.fig` export is a separate future feature; clipboard bytes must not be renamed to `.fig`.

## Smoke test

```sh
node scripts/capture.mjs fixtures/diagnostic.html --selector '#diagnostic' --offline --strict --out /absolute/path/example
node tests/integration.mjs /absolute/path/test-output
```

The fixture is a technical diagnostic, not a brand template. Check the current execution report for checks actually performed; the package's dated [validation record](../../docs/html-to-figma-validation.md) does not certify a new source or host.
