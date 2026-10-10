## Runtime Adoption Gates

Credentialed tools can be useful, but they are not silently adopted. Treat
these as separate lanes:

- Google Search Console, GA4, Matomo, Clarity, or analytics MCPs
- Reddit/Substack research MCPs
- Firecrawl/browser scraping
- BrandSystem or OSP content MCPs
- Playwright MCP or browser automation
- Ad platform APIs, CRMs, schedulers, email senders, social APIs

Before runtime use:

1. Identify exact repo/package/version and license.
2. Review scripts, package manifests, Dockerfiles, server cards, env vars,
   OAuth scopes, browser/session behavior, network writes, storage, and logs.
3. Confirm cost and credentials.
4. Run only a bounded, reversible, read-only first test when possible.
5. Keep public output behind Shareables/public-safety review.
