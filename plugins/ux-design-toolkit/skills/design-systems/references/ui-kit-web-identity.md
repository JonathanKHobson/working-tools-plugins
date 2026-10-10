# Website identity and discovery handoff

Use when the kit will supply a website or public web experience. Native icons and store listings need their platform's separate delivery contract. A UI kit can prepare identity and metadata patterns; production discovery also depends on actual content, routes and hosting.

## Identity assets

Specify a recognizable small mark, not simply a miniature hero. Review at actual browser-tab sizes and on light/dark surroundings. Provide formats and sizes required by the supported browsers and installation surfaces, with a stable source master and derivative records. Typical web exports include an SVG or PNG favicon, ICO fallback where needed, an Apple touch icon, and manifest icons when installation is in scope. These are a compatibility plan, not a universal mandatory file count.

Verify manifest entries, purpose, dimensions and safe areas. Declare `maskable` only for artwork composed and inspected for masking. A manifest and icons do not establish offline operation, a service worker or full PWA capability. Search engines have their own eligibility and caching behavior; follow [Google's favicon guidance](https://developers.google.com/search/docs/appearance/favicon-in-search) for that destination without promising appearance.

Create a social preview with readable title/identity and intentional crop-safe composition. A 1200 × 630 export is a common landscape option, not a universal platform requirement. Define alternate crops when the intended destination needs them. Record image alternative text and inspect real-size previews. Keep visual type in this promotional image distinct from live page headings.

## Page content and metadata contract

Each eligible public page needs a truthful, distinct title and description, meaningful heading hierarchy, actual content, useful link names and image alternatives. Decorative art has a different alternative-text treatment from informative art. Make essential page meaning and navigation available in the initial rendering strategy; metadata cannot compensate for missing content.

For the selected sharing destinations provide accurate title, description, image and page URL using their documented fields. The [Open Graph protocol](https://ogp.me/) defines its core properties. Do not invent a social account, author credential, search endpoint, organization address or structured-data feature to fill a template.

Canonical URLs, absolute social URLs, sitemap entries and structured-data identifiers depend on the real production origin and routes. Keep these explicit configuration inputs; fail or clearly withhold production export when missing. Emit only truthful, applicable structured data consistent with visible content. A sitemap should list eligible canonical pages, not private fixtures and redirects. A local `.test` fixture is verification data, not a public domain.

## Review versus launch

Keep review-only pages appropriately non-indexable. `noindex` is not access control: private material needs authentication or removal from the public build. For Google to observe a page's `noindex`, crawling must be possible; robots.txt disallow is not a substitute and may prevent that observation. See [block indexing](https://developers.google.com/search/docs/crawling-indexing/block-indexing) and [robots.txt limits](https://developers.google.com/search/docs/crawling-indexing/robots/intro).

At launch, verify the actual served pages, redirects/status codes, canonical origin, metadata, accessible images, sitemap/robots behavior and public/private boundaries. Check sharing previews and installed icons on the claimed destinations; local HTML inspection proves only local output. Search appearance, indexing and ranking remain external outcomes. Never claim SEO is complete simply because meta tags or a favicon exist.
