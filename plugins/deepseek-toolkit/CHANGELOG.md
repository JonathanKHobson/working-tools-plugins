# Changelog

## 0.1.0

Introduce a bounded DeepSeek text worker with fixed NVIDIA routing, explicit completion checks and optional metadata-only usage recording.

Why: Provide a recipient-configured alternative model route while keeping project access, provider accounts, credentials and external coding clients outside the package.

Compatibility: First public version 0.1.0, with one complete operative skill and no hooks, MCP servers or automatically installed provider runtime. The helper uses Python standard library and supplied stdin only. Recipient account terms and current allowance govern any later inference; a configuration check is not authentication.

Upgrade: Install the package, read the operative skill and configure only recipient-owned credentials when explicitly authorized. Use --check for configuration evidence; request a separate authorized inference before claiming working access. Do not infer a free entitlement, paid fallback or separate OpenCode launcher from package installation.

Validation: Fourteen mocked worker tests pass. Installed Claude Code 2.1.280 strict manifest validation passes with no warnings. Public package, privacy/reference, license/provenance and selected live canonical-source checks pass. The installed Codex CLI offers no read-only plugin-validation command; Codex metadata was checked by the package rules without installation. These checks do not establish live NVIDIA authentication, allowance, inference, hosted latency or recipient runtime readiness.
