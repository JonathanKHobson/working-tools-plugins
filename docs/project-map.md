# Project map

Working Tools is a public collection of separately installable AI workflows and local runtimes.

- `plugins/<id>/`: reviewed public package source, notices and provenance.
- `catalog/packages.json`: public package identity, version, requirements and release state.
- `scripts/packages.py`: reference/privacy validation, marketplace generation and deterministic ZIP building.
- `.agents/plugins/marketplace.json` and `.claude-plugin/marketplace.json`: generated host catalogs.
- `docs/`: installation, compatibility, architecture and recovery guidance.
- `.github/`: validation and contributor entry paths.
- `dist/`: ignored generated packages; release downloads live in GitHub Releases.

Flow: reviewed source and registry -> validation -> deterministic archives -> native install/sample tasks -> versioned release -> reviewed Working Tools Site catalog projection. GitHub is authoritative for these public editions; the Site is a separately saved publication. Private source lineage is retained by the maintainer, with sanitized source hashes in package provenance.

Start a package change in its folder, then update its version and registry together. Run `python3 scripts/packages.py catalog`, `python3 scripts/packages.py validate`, the package tests, and `python3 scripts/packages.py build`. A package's upstream source need not be a Git checkout; never invent a source commit in place of its recorded hashes.
