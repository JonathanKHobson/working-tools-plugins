# Commands and fidelity boundaries

`node scripts/capture.mjs --help` lists all options. Paths may contain spaces when quoted. Local files are served only from the file's real parent directory, on an ephemeral loopback port; parent escapes and outside-root symlinks are refused. Use a localhost development server for projects with a wider asset root, build tooling or routing. Only localhost, 127.0.0.1 and ::1 are accepted as URL inputs. No external conversion service is used.

The output directory receives `clipboard.html` (the actual rich envelope), `document.json` (native layer-change structure), `trace.json` (source-node mapping), `source.png`, `copy.html`, and `report.json`. Use a different `--out` for durable versions. Source data and images may be private; outputs and payload caches stay local with restricted file permissions. A default `outputs/latest` directory is reused inside the configured runtime. Payload caches are bounded; manually selected output directories are user artifacts and are not automatically deleted.

## Local fonts

CSS `@font-face` URL sources are fetched through the same local/offline request policy. Installed single-file TTF/OTF/WOFF/WOFF2 fonts are matched by family, weight and italic state. An explicit manifest overrides installed lookup:

```json
[
  {"family":"Inter","weight":400,"italic":false,"path":"./fonts/Inter-Regular.ttf"},
  {"family":"Inter","weight":700,"italic":false,"path":"./fonts/Inter-Bold.ttf"}
]
```

Paths are relative to the manifest or absolute. Use the actual font used by the browser; a mapping alias does not change the page's CSS. No Fontsource/CDN fallback or unrelated metric substitution is performed. Missing font metrics can cause the upstream converter to omit text, so inspect warnings and use `--strict` for release captures. Fonts still need to be available in Figma to edit/render correctly. Generic families, TTC collections, local()-only CSS faces, variable-font axes and multi-file Unicode subsets require special care; collections are unsupported, subset ambiguity is reported. Use explicit single-file faces when possible. Font files are not packaged with the skill.

## Rendering and caching

The context uses DPR 1, light color scheme, en-US, UTC, reduced motion, fresh storage and blocked service workers. It has no user browser cookies, logins or extension state. Lazy images are eagerly requested; failed loads are recorded. Responsive `<picture>`/srcset images are pinned to the browser's selected currentSrc for conversion. Filled text input/textarea values replace upstream placeholder content for conversion. Passwords, selects and native controls are flagged as appearance risks.

Browser resource responses, computed CSS/geometry, DOM, visible control state, local font hashes, converter dependency lock, wrapper source and browser build contribute to cache identity. Live pages still render before a cache hit, which avoids trusting old localhost output. Incomplete/unstable captures are not cached as clean. A websocket/animation app may require a meaningful ready selector; no finite settling heuristic proves the app has no future content. Offline enforces browser resource routing, not an OS-wide air gap or control over a localhost server's own outbound requests.

## Known fidelity limits

The engine preserves supported editable text, frames, SVG vectors, images, borders, shadows and clipping. Browser-native controls become design layers rather than working controls. Canvas/WebGL, video/iframes, filters/masks, complex CSS, unsupported fonts/glyphs and pseudo-elements may be approximated or omitted. Warnings and trace-based visible-leaf candidates help find loss; they are not an exhaustive proof that every visible pixel maps to a layer.

For the diagnostic fixture, actual Figma paste and native text editing were checked. Layout, image clipping, inline vector shape and visible field value were inspected. The one-sided footer border is retained. The selected-root wrapper clips content at its bounds, so outside shadows/effects may need adjustment; longer edited text may need resizing because text boxes use captured fixed dimensions. This is a useful editable starting point, not pixel-perfect fidelity. `--layout absolute` can help geometry but cannot repair unsupported styles.

For manual validation, compare the heading and badge, two panel positions, clipped image, vector/checkmark, field value, footer line and outer shadow with `source.png`. Select a sentence in Figma, inspect its TEXT typography and edit one word. Select the SVG child and confirm Vector path properties. Inspect parent Auto Layout or absolute positions. Record each result separately.

`.fig` export is deliberately absent. Evaluate [OpenPencil's documented CLI import](https://openpencil.dev/reference/cli) in a separate task if a real file is later required.
