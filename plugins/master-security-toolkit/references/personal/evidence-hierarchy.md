## Evidence Hierarchy

When evidence conflicts, prefer stronger evidence in this order:

1. Official publisher documentation, official download page, official registry
   page, official GitHub organization, and official security advisory.
2. Cryptographic verification: detached signatures, signed checksums,
   notarization, code signing, Sigstore/GitHub/PyPI attestations, and SLSA
   provenance.
3. Source-to-artifact traceability: reproducible build notes, release workflow,
   artifact attestation, matching tags/commits, and transparent release history.
4. Manifest and code inspection: install scripts, entrypoints, MCP schemas,
   permissions, dependency graph, and lockfile diff.
5. Independent reputation: security research, maintainer history, issue
   reports, vulnerability databases, and malware reports.
6. Weak signals only: stars, forks, social buzz, attractive README,
   screenshots, AI recommendations, or "popular on Reddit."

A signed or notarized app is not automatically safe. It is useful evidence, not
a safety guarantee.
