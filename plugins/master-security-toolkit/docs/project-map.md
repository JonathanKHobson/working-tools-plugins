# Master Security Toolkit

Nine focused skills provide conditional software, application and instruction review methods. The plugin includes a pinned, local, read-only scanner wrapper. Its scanner has no hook, network service, or automatic gate. An optional read-only Atlas MCP supplies scoped instruction-security reference material.

| Path | Role |
|---|---|
| `skills/software-security-review/SKILL.md` | External software, package, installer, repository, and MCP provenance/capability review |
| `skills/software-security-review/references/threat-catalog.md` | Conditional surface-specific threat matrix and inspection commands |
| `skills/software-security-review/references/agent-artifact-scanning.md` | Agent skill/plugin scan interpretation, exact evidence, suppressions, noncoverage, optional verified upstream scanner |
| `skills/instruction-security-review/SKILL.md` | Prompt-injection and tool-boundary review entrypoint |
| `skills/instruction-security-review/references/injection-review-patterns.md` | Direct/indirect entry, tool authority, synthetic regression, finding contract |
| `scripts/skillguard_scan.py` and `vendor/agent-skillguard/` | Fixed-path, stdout-only wrapper for MIT-licensed upstream v0.1.5 scanner, rules, noncoverage registry, synthetic fixtures, and rule-corpus verifier |
| `scripts/publication_preflight.py`, `tests/test_publication_preflight.py`, `skills/software-security-review/references/publication-privacy-preflight.md` | Original bounded, read-only local publication secret/privacy check; conditional owner reference, masked artifact evidence and synthetic tests |

The scanner is invoked only for a task-authorized local target and its deterministic output remains one input to a human-readable assessment. The wrapper does not execute target files or write reports. The original upstream CLI also supports report/suppression file creation; those write paths are intentionally absent from this integration.

The upstream tag `v0.1.5` resolves to commit `affd36ef237d1fb7ebd830cde630a7b4cc27aaba`. The vendored scanner module matches upstream byte-for-byte at SHA-256 `e958c180cb6859f64f66c452e218f566943734797a09f2a00ca6d5038ca3f967`; the rule pack is `7b77ea3817aa4e66992a09cacdd8ca8b672b315524d4c26b8b49165702ef9ebf` and the noncoverage registry is `f2cd5c69eb28a09b983d9ce72d7f997b5b228df97aea50c8456ae72bd95918e6`. The only upstream source adaptation is the rule-corpus verifier's local paths and removal of its optional file-output flag. The wrapper itself is an original integration layer.

Upstream public metadata and source inspection cannot establish that a future release is safe or that a scan detects all malicious behavior. The vendored static scanner does not run target code, inspect binaries, observe runtime networking, or prove sandbox containment. `v0.1.5` has eight deterministic rules; the bundled verifier passed twelve positive/negative fixtures covering all eight rules. Changes require pinned-source diff review and a fresh verifier run.

## Source coverage

The four Injection Checker depth methods are supplied by the official receiver-installed `injection-checker@openai-curated-remote` plugin (v0.1.0 verified on the maintainer host), not copied into this package. `instruction-security-review`, `indirect-injection-review` and `security-regression-tests` retain their complete first-party review contracts and route to the exact installed namespaces. Missing provider discovery is reported as a capability-access gap.

The complete original Personal Security Check, pinned MIT SkillGuard source and wrapper, Apache-2.0 Strix adaptations, and MIT Cloudflare coverage audit remain in their existing library locations. See `docs/full-procedures.md` for conditional method selection.

## Application security

`skills/application-security-testing/SKILL.md` routes to the complete `references/application-security-testing.md` for source, API, staging, finding triage and fix verification. Selected methods from Strix are adapted with an Apache-2.0 notice in `libraries/strix-methods/`. The Strix executable and its cloud/CI/install machinery are not bundled or enabled. Existing reviewed host tools perform bounded tests; tool-specific runtime admission remains separate.

`skills/agent-artifact-scanning/references/candidate-depth-review.md` adds a conditional manual trace for retained/re-injected context and delayed triggers. It complements the existing static scanner without installing SkillSpector, adding detection rules or enabling external semantic analysis.

For broad source audits, `references/coverage-led-security-audit.md` conditionally routes to the complete MIT-licensed Cloudflare method in `libraries/cloudflare-security-audit-original/`. It adds coverage and finding records, independent verification, and reviewed local JSON validators. Target-controlled dynamic validation requires verified OS isolation; the unrestricted host shell does not supply it.

- `references/atlas-library.md`: scoped security Atlas retrieval and private human library. `scripts/atlas_library_mcp.py` and `.mcp.json` launch the fixed domain against a shared external index; no corpus is packaged.
