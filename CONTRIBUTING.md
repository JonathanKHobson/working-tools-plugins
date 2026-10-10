# Contribute

Start with a small reproducible issue or a focused pull request. Identify the package, version, host and expected outcome. Use synthetic fixtures and preserve source/asset rights. Do not attach credentials, personal data or proprietary project files.

Read AGENTS.md and docs/project-map.md. Run `python3 scripts/packages.py catalog`, `python3 scripts/packages.py validate`, `python3 -m unittest discover -s tests -v`, and the changed package's tests. Build with `python3 scripts/packages.py build`. Generated marketplace files come from the registry.

Changes to package behavior need a version change, changelog entry, affected reference checks and a representative task. Preserve notices and provenance. Releases are deliberate maintainer actions after installation and download verification. Support is best effort; there is no promised response time.
