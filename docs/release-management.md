# Release management

The public distribution has independently versioned plugins. The version authority is `catalog/packages.json`; its value is synchronized into all three supported plugin manifests. `catalog/source-inventory.json` fixes the reviewed distribution paths and exclusions. Historical source packages and downloads are not replaced. Separate guide/legacy downloads are registered in `catalog/external-products.json` with observed version schemes and provenance; a page-only guide is not an installation package. There is no distributed whole-ecosystem bundle to version.

## Completion event

Maintainer setup: create an isolated Python environment with `python3 -m venv .venv`, then `.venv/bin/python -m pip install -r requirements-release.txt`. Git, the authenticated GitHub CLI, and the existing Codex Sites connection are also required. The catalog runs both the checked-in JSON Schema and its semantic selection checks.

The authoring agent runs the following once the requested public update and focused checks are complete:

```sh
.venv/bin/python scripts/complete_update.py --config "$RELEASE_CONFIG"
```

This explicit completed-update command, not a file save, interim commit, schedule or generic stop hook, starts publication. Codex maintenance routes to it. Changes made outside Codex use this same command after their public update is complete. The authoring agent prepares a specific `catalog/changes/<product-id>.json` record from the diff with `level`, `summary`, `why`, `notes`, `compatibility`, `upgrade_guidance` and `validation`; the human does not separately compose notes, upload assets or edit links. An absent record stops before changing versions so unsupported semantic claims cannot become public release notes.

The private maintainer config contains `canonical_root`, `public_source`, `site_source`, `site_receipt`, `site_adapter` (an argv array), and optional `codex_command`. `external_checkouts` maps the active `shareables` and `what-is-an-mcp` owners to their public source checkouts. If a reviewed canonical product root is a symlink, `canonical_sources` must map its product ID to the exact absolute, resolved target directory, for example `{"product-id": "/absolute/reviewed/source"}`. A missing or changed target stops completion; symlinks inside a product remain disallowed. The maintained adapter is `["python3", "scripts/release_site_bridge.py"]`. It uses the authenticated Codex CLI Sites connector and requires that existing connection. Credentials are refreshed through the connector, not stored in this configuration. Recipient publishers configure their own source roots and hosting; no author paths are shipped.

The command reconciles changes to already reviewed public paths, checks conflicts and exclusions, synchronizes manifests, creates a durable version record and package changelog, commits the intended files, validates the exact release commit, then pushes. Source-inventory validation always checks every public package and the complete reviewed baseline. During an independent release, live canonical included and excluded bytes are checked for the named releasing products; unrelated private work does not block them. A no-change completion checks the full public snapshot without claiming that other private source trees were audited. Standalone `scripts/source_inventory.py --canonical-root ...` still audits every canonical product and the canonical namespace. It builds deterministic ZIPs from the exact release commit and verifies their inventory. Publication uses draft, complete assets, downloaded-byte verification, then publish. A collision preserves the original release and stops with the exact discrepancy. There is no moving `latest/download` URL in the catalog.

A new public file or removed source must receive an explicit review in the existing source inventory/provenance/coverage records. That review can be completed by the authorized authoring agent. The command never imports unreviewed private files or runs historical one-off exporters. For public contributions, reconcile the reviewed public edition with the local authoring source before export, preserving conflicts for resolution.

## Versions and compatibility

Compatible corrections, including instruction/reference changes, normally increment patch. Compatible optional capabilities increment minor. Removing invocation IDs, required installation/configuration contracts or supported inputs/outputs needs a major change. Review behavioral instruction changes explicitly; a file extension alone cannot determine compatibility. Build metadata retains historical identity but does not control SemVer ordering. Independent plugins keep independent versions; the highest eligible stable version is selected per product, not by repository-wide Latest or publication date. Prereleases, drafts, withdrawn records and unavailable packages do not automatically advance current downloads. A maintenance backport remains in history without replacing a higher stable line.

Every shipped file contributes to change detection. The private `shared_shipped_paths` map assigns a repository-relative shared source to its already-reviewed installation destinations, for example `{"shared/template.md": ["plugins/a/references/template.md", "plugins/b/references/template.md"]}`. The completion command reconciles those bytes and releases every affected product; a conflict with separate edits stops before publication. Website-only edits, version records outside packages and unchanged reruns do not cause package versions. Changes to a shipped changelog or instructions require a new package; corrections to external notes/catalog metadata can reconcile without changing package bytes.

## History and deployment

`python3 scripts/sync_release_catalog.py` imports every GitHub API page, resolves each tag, checks installation archives against the exact tagged source tree, and validates `catalog/release-history.json`. Verified evidence can be reused only when commit and GitHub asset name, URL, size and digest still agree. Failed history lookup cannot truncate the prior catalog. Separate external records retain original links, observed checksums and reconstruction limits.

The Site adapter copies the catalog into the maintained `working-tools-site` repository and generates static product/version pages. It builds from pinned source, pushes the existing managed Sites source, saves and deploys through the supported Sites connector, and reads back the live catalog. The release labels and URLs come from the same record. Product IDs, version records and `/plugins/<id>/releases/<version>/` addresses survive display-name or visual rebranding.

Local completion and Site promotion have separate locks. The Site adapter rechecks canonical release state immediately before promotion and refuses stale input. Source pushes are fast-forward only. A newer published package cannot be overwritten by an older catalog job. Publication does not rely on a `release` event launching another workflow with `GITHUB_TOKEN`.

## Recovery

```sh
.venv/bin/python scripts/complete_update.py --config "$RELEASE_CONFIG" --reconcile-only
```

Recovery resumes a draft or verifies identical published assets, then retries catalog synchronization without allocating another version. If GitHub succeeds and the Site fails, retain both the published packages and the prior live Site. The receipt stays `catalog_pending` until exact live catalog readback. `dist/release-manager/receipt.json` and the configured Site receipt distinguish preparation, publication and deployment; ignored build/cache files contain no canonical version authority.

Focused fixtures cover instruction/template detection, website/no-op isolation, semantic ordering, pagination failure, exact-byte collisions, incomplete drafts and recovery. They do not create artificial public test releases. Runtime installation, visual keyboard/mobile checks and publication readback remain separately recorded acceptance evidence.

Independent active guides use the integrated external completion step and [owning-repository recovery](external-release-management.md). Frozen legacy resources remain unchanged.

The independently installed optional host-hooks integration has its own version authority in `catalog/integrations.json`, outside the plugin marketplace. See [integration pack releases](integration-release-management.md).
