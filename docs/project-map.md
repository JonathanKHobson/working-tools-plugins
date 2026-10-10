# Project map

Working Tools is a public collection of separately installable AI workflows and local runtimes.

- `plugins/<id>/`: reviewed public package source, notices and provenance.
- `catalog/packages.json`: public package identity, version, requirements and release state.
- `catalog/source-inventory.json` and `catalog/coverage-baseline.json`: reviewed canonical file locks and audit dispositions.
- `scripts/packages.py`: reference/privacy validation, marketplace generation, development builds and the strict release command.
- `scripts/source_inventory.py` and `scripts/release_archive.py`: source completeness and archive-byte verification.
- `.agents/plugins/marketplace.json` and `.claude-plugin/marketplace.json`: generated host catalogs.
- `docs/`: installation, compatibility, architecture and recovery guidance.
- `.github/`: validation and contributor entry paths.
- `dist/`: ignored generated packages; release downloads live in GitHub Releases.

Flow: reviewed source and registry -> validation -> deterministic archives -> native install/sample tasks -> versioned release -> reviewed Working Tools Site catalog projection. GitHub is authoritative for these public editions; the Site is a separately saved publication. Private source lineage is retained by the maintainer, with sanitized source hashes in package provenance.

Start a package change in its folder, then update its version and registry together. Run `python3 scripts/packages.py catalog`, `python3 scripts/packages.py validate`, the package tests, and `python3 scripts/packages.py build`. A package's upstream source need not be a Git checkout; never invent a source commit in place of its recorded hashes.

Publication uses `python3 scripts/packages.py release`; ordinary `build` output is a development artifact. See [the release coverage gate](architecture.md#release-coverage-gate) for local source checks and current unresolved inventory boundaries.
