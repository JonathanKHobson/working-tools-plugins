# Project map

Working Tools is a public collection of separately installable AI workflows and local runtimes.

- `plugins/<id>/`: reviewed public package source, notices and provenance.
- `catalog/packages.json`: public package identity, version, requirements and release state.
- `catalog/source-inventory.json` and `catalog/coverage-baseline.json`: reviewed canonical file locks and audit dispositions.
- `scripts/skill_bundles.py` and `scripts/release_manager/skill_downloads.py`: generated individual-skill archives and immutable companion releases; `catalog/skill-downloads.json` feeds Site downloads automatically during normal publication. See [individual skill downloads](individual-skill-downloads.md).
- `scripts/packages.py`: reference/privacy validation, marketplace generation, development builds and the strict release command.
- `scripts/source_inventory.py` and `scripts/release_archive.py`: source completeness and archive-byte verification.
- `scripts/license_checks.py`: exact license-scope and manifest checks used by releases and individual skill bundles, plus registry-owned source-rights holds checked at release; packaging consistency does not establish rights clearance.
- `.agents/plugins/marketplace.json` and `.claude-plugin/marketplace.json`: generated host catalogs.
- `docs/`: installation, compatibility, architecture, system-context transparency and recovery guidance.
- `examples/AGENTS.starter.md`: illustrative public instructions; not automatically active.
- `integrations/codex-host-hooks/`: optional portable lifecycle hooks, explicit setup and isolated tests. This is a host integration, outside the plugin registry.
- `.github/`: validation and contributor entry paths.
- `dist/`: ignored generated packages; release downloads live in GitHub Releases.

Flow: reviewed source and registry -> validation -> deterministic archives -> native install/sample tasks -> versioned release -> reviewed Working Tools Site catalog projection. GitHub is authoritative for these public editions; the Site is a separately saved publication. Private source lineage is retained by the maintainer, with sanitized source hashes in package provenance.

Start a package change in its folder, validate the local change, then record it in the pending queue. Allocate its public version only when publishing the accumulated batch. Run `python3 scripts/packages.py catalog`, `python3 scripts/packages.py validate`, the package tests, and `python3 scripts/packages.py build`. A package's upstream source need not be a Git checkout; never invent a source commit in place of its recorded hashes.

Publication uses `python3 scripts/packages.py release`; ordinary `build` output is a development artifact. See [the release coverage gate](architecture.md#release-coverage-gate) for local source checks and current unresolved inventory boundaries.

Local completion and explicit batch publication are implemented by `scripts/complete_update.py` and `scripts/release_manager/`. The default command refreshes ignored private `dist/release-manager/pending.json`; `--publish` enters the release pipeline. `catalog/releases/` owns specific version entries; `catalog/release-history.json` is the verified GitHub projection; `catalog/external-products.json` maps independently hosted and legacy downloads. `scripts/release_site_bridge.py` invokes the authenticated native Sites adapter after publication. Its explicit `static-dist-v1` contract protects the current redesigned Site, stamps its static payload, checks both release and skill catalogs, and revalidates native source before a no-op. `tests/test_static_site_adapter.py` covers this boundary without public releases. See [release management](release-management.md) for the completion event and recovery command.
