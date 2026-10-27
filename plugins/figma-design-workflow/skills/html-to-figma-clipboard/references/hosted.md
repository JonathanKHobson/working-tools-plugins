# Explicit hosted adapter

The default capture executable never imports or calls this adapter. Select hosted mode only on a current user request. It sends the chosen HTML to divRIOTS code.to.design, so it has a different data and credit boundary.

```sh
CODE_TO_DESIGN_API_KEY='set locally, never paste a real key into chat'
export CODE_TO_DESIGN_API_KEY
node scripts/hosted.mjs --provider hosted --confirm-one-credit --input /absolute/self-contained.html --out /absolute/hosted-output
```

Prefer a local secret manager/environment over command history. The key is used only by the Node helper and never embedded in copy.html, browser code, reports or cache. Successful results are cached separately; a cache hit uses zero credits. A new `/html` request is documented as one credit as of 2026-10-19. The helper prints the expected use before any request and requires the explicit credit flag. No hosted request was made during local validation.

Only complete HTML documents with self-contained images/styles/scripts are accepted. Relative and HTTP(S) resource URLs are rejected because the hosted service cannot resolve local project assets and mutable remote assets invalidate content-only caching. Supply inline/data resources. The provider's clipboard documentation requires Google Fonts and discourages system fonts. Validate the actual provider response and Figma result separately. The adapter does not invent local-app state or serialize an authenticated browser.

References: [clipboard mode](https://docs-code.to.design/clipboard-mode), [API cost and schema](https://docs-code.to.design/api/~endpoints), [credit pricing](https://docs-code.to.design/pricing). This is an optional, untested-live integration; local capture requires none of its credentials.
