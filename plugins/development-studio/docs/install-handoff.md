# Serialized installation handoff

Prepared package: `development-studio`, version `0.1.0`, visible name Development Studio. Canonical source is the enclosing directory. Parent ecosystem owner is the only marketplace/install writer; this task does not mutate shared registration or existing plugin manifests.

1. Register this canonical directory through the existing Personal local marketplace convention. Use the new package ID and preserve unrelated marketplace entries. Resolve the directory from the actual host rather than copying a personal absolute path into public source.
2. Install through the native plugin manager using `development-studio@working-tools`. Inspect the manager’s current command/help before acting. No MCP/config/provider declarations should be added by this method package.
3. Compare every source file and installed file in both directions, excluding only documented platform-generated metadata. Version equality alone is insufficient. Run the read-only package validator on source and installed roots; validate top-level skills with the host’s native skill validator.
4. Open a fresh chat/discovery context and confirm all 11 focused skills appear and libraries are support assets rather than extra global discovery. Exercise a direct help prompt, existing feature request, bug request, MCP task and missing-provider case from `tests/scenarios.json`. The scenario file is a test contract; its presence is not trial evidence.
5. Verify official provider discovery and the actual required connection separately. Check the provider map’s method locations against the installed versions. Keep OpenAI providers and necessary external services.
6. Only then evaluate predecessor retirement using `legacy-disposition.md`. Full helper/native-host functional equivalence is still a separate gate. Do not uninstall the disabled legacy bundles with unresolved useful coverage.

Current evidence: source and imports prepared, package structure/routing/portability checks and admission recorded in the companion validation report. Pending: native registration/install, source/cache parity, fresh discovery, representative actual-host task acceptance and any provider-specific runtime test. These are parent-owned installation gates, not claims of source incompleteness.

Public source distribution is covered by the path-specific grants in LICENSE.md. Installation and actual-host acceptance remain separate. Game Creation Studio has its own source and handoff.
