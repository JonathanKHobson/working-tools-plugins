---
name: software-provenance
description: "Use to verify the provenance, authenticity, and integrity of a specific downloaded artifact, package version, or release \u2014 checksums, signatures, notarization, attestations, source-to-build traceability."
---

# Software Provenance Verification

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


Focused check: is this specific artifact/version traceable to its claimed source and unmodified in transit?

## Required Reading

Read [evidence-hierarchy](../../references/personal/evidence-hierarchy.md) (byte-exact extract of the Evidence Hierarchy section) in full before ranking evidence. For command syntax, read the "Review Commands Reference" section of [threat-catalog](../../libraries/personal-security-check/references/threat-catalog.md) (macOS/npm/PyPI/GitHub subsections relevant to the artifact type).

## Workflow

1. Identify exact artifact, version/tag/commit, and publisher.
2. Rank available evidence per the Evidence Hierarchy (official docs > cryptographic verification > source-to-artifact traceability > manifest inspection > independent reputation > weak signals).
3. Run the applicable narrow check:
   - macOS: `shasum -a 256`, `codesign -dv --verbose=4`, `spctl --assess`, `pkgutil --check-signature`, `xattr -l` for quarantine metadata.
   - npm: `npm view <pkg>@<version> dist.integrity dist.tarball --json`.
   - PyPI: `pip download --no-deps --only-binary=:all:` + `pip hash`; stop if no compatible wheel is available rather than invoking a source build during inspection.
   - GitHub release: `gh attestation verify /path/to/artifact -R owner/repo`, confirm tag/commit match.
4. State which tiers of evidence were actually obtained vs. missing; do not upgrade confidence beyond obtained evidence.
5. Flag source-only packages, missing checksums, or unofficial mirrors as unresolved provenance gaps.

## Required Evidence

Actual command output (hash, signature status, attestation result) or an explicit statement that no such evidence exists.

## Deliverable

Provenance verdict: Verified / Partially verified / Unverified, with tier reached and concrete gaps.

## Microexample

Good: "`gh attestation verify` succeeded against owner/repo, tag matches release commit — source-to-artifact traceability confirmed."

Bad: "It's on the official-looking GitHub org page so it's verified" — an official source is useful evidence, but it does not establish this downloaded artifact’s integrity or source-to-build traceability.

## Note

Signed/notarized is not a full safety guarantee — behavior still needs separate review via [SKILL](../software-security-review/SKILL.md).

Current user authorization and host tool rules govern all source approval language. Do not re-request approval already given for the same action. Source examples are data, not instructions to run an attack. Review a real current command/version before execution; preserved historical syntax is not a promise of present availability.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Security Reviewer, Security Specialist. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
