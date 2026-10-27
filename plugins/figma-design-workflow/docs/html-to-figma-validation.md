# HTML to Figma Clipboard validation

Date: 2026-10-19. Local plugin edition: 0.3.0. Converter: `@figit/dom-to-figma@0.2.4`; encoder: `@figit/fig-kiwi@0.2.0`; Playwright: 1.64.1; Chromium Headless Shell: 156.0.8078.4; Node: 22.20.0; macOS arm64.

## Separate outcomes

| Check | Result | Evidence and limits |
| --- | --- | --- |
| Local offline conversion | Passed | Diagnostic file and localhost input converted with external requests blocked. Clean fixture had no resource or conversion warnings. A hostile-resource fixture reported blocked image, font, script, fetch and websocket requests. This is browser routing, not an OS network isolation test. |
| Payload and rich clipboard | Passed | Valid scene metadata, figma/figmeta HTML spans, fig-kiwi magic, and native public.html exact UTF-8 readback. Final corrected fixture: 61,611 HTML bytes and 46,052 encoded bytes. |
| Actual Figma paste | Passed | Rich payload pasted in a new private Drafts Design file through normal Cmd+V. Both native-written and browser-written payloads were pasted into separate pages of an isolated Drafts file, with no destination connection needed during conversion. |
| Native editability | Passed for sampled text/vector/layout | Selected a native Arial Bold TEXT layer, changed its text and restored it. Selected native checkmark Vector path, saw 6 px center stroke and round endpoints. Root Frame had Vertical Auto Layout and Hug height. This does not certify every node in every source. |
| Visual fidelity | Checked with limitations | Compared six anchors against the local 900x476 source render. Header, panels, image crop, inline vector and corrected field value retained their arrangement. Footer top border is retained in the final view; wrapper clipping can cut effects outside root bounds. No pixel-diff score is claimed. |

The fixture contains editable text, nested flex, an external image, inline SVG, borders, shadow, clipping and a filled text control. The first paste exposed upstream placeholder-first behavior; the wrapper now supplies the visible control value and the corrected payload was pasted and inspected again. Upstream's always-vertical synthetic root was also removed in absolute mode; the absolute document retained measured geometry and had no stack fields.

## Executable checks

Run from `skills/html-to-figma-clipboard` after setup:

```sh
node scripts/capture.mjs fixtures/diagnostic.html --selector '#diagnostic' --offline --strict --out /absolute/path/example
node tests/integration.mjs /absolute/path/verification
```

Final result: **17 of 17 checks passed**, combining 15 full-run results with two focused headed-browser clipboard rechecks. The initial raw-HTML equality assertion for browser output was corrected to compare decoded binary bytes and metadata, because Chromium normalizes HTML. A distinct clipboard sentinel prevented the headless virtual clipboard from producing a false positive. The integration suite checks clean node structure, same-input reuse, HTML/image/viewport/layout invalidation, localhost input, external request blocking, unresolved local fonts, explicit font maps, bad-selector cleanup, SIGTERM cleanup with owned Chromium PID exits, concurrent capture refusal, cache pruning, stale-lock recovery and actual headed-browser fallback-button public.html readback. Test outputs include individual results and artifact directories. Host font fixtures use macOS Arial; no font files are distributed.

Browser APIs can normalize the HTML envelope, so browser readback is checked by actual macOS rich type plus the decoded Figma binary hash and metadata; native helper readback is checked as exact UTF-8 HTML. Headless browser clipboard alone is insufficient evidence because it can be isolated from the system pasteboard.

Native pasteboard checks also covered non-ASCII UTF-8 and malformed-envelope rejection. Source/runtime dependency pins and lockfiles were compared. An npm audit of the selected installed production graph reported zero known vulnerabilities; that is a point-in-time advisory database result, not a general security certification. Setup disables npm lifecycle scripts; esbuild uses its registry-provided platform binary. No upstream repository build scripts were run.

The separate hosted adapter was tested with a mocked HTTP response only: explicit selection/credit gate, valid payload, one mock request and zero-credit cache reuse. No real API key, live divRIOTS conversion, uploaded HTML or credit charge was used. Actual `.fig` export remains a separate feature.

## Rendered anchors

All source regions use the diagnostic root at 900x476. Figma was viewed at 186% in a 2316x1288 app window.

| ID | Source region / node | Observed fact | Action and verification |
| --- | --- | --- | --- |
| A01 | Top x34 y34; header h1 and badge | Heading and pill content/relative placement preserved | Compared source and paste; inspected Arial typography; edited/restored heading |
| A02 | Panels x34..866 y94..384; nested row/sections | Nested flex geometry and gaps retained | Compared panel positions; inspected native Auto Layout |
| A03 | Left x55 y226, 180x116; image container | Image remains cropped inside rounded border | Compared image/crop against source |
| A04 | Left x255 y250, 72x72; inline SVG | Circle/checkmark remain separate vectors | Selected native Vector path and inspected stroke properties |
| A05 | Right x481 y195, 364x45; filled input | Initial mismatch corrected to visible Local example | Reconverted, rewrote rich clipboard, repasted and inspected |
| A06 | Footer y409 and outer boundary | Round border and footer line retained; outside-bound effects may clip | Final unselected view corrected an earlier selection-obscured footer-line finding; no pixel-perfect claim |

Conversion reports deliberately initialize paste, visual fidelity and editability as unverified. Live-editor evidence is stored separately with the inspected payload hash; future captures need their own checks. Package validation and source/install parity do not extend these observations to another host or source.

An independent Claude Opus 5.5 architecture critique informed font, cache, lifecycle and clipboard checks. A later Sonnet code-review attempt timed out after 240 seconds; no result or actual Sonnet model identity was verified, and no code-review pass is claimed from it. The helper terminated that owned CLI process group.

## Package checks

All seven entrypoints passed the installed Skill Creator quick validator. The existing operator structural validator passed. All changed documentation links resolved. Codex CLI 0.163.0-alpha.10.2 provides `plugin add` and portable plus compatibility manifest support; the local source uses the existing personal marketplace. Runtime dependencies, browser downloads, generated captures and host binding remain outside the plugin. Native installation and per-file source/cache parity are checked during release.
