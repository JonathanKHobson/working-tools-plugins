# Serialized installation handoff

Prepared package: `development-studio`, version `0.3.0`, visible name Development Studio. The enclosing directory is the distributable package source. Installation requires the recipient’s configured plugin marketplace; this document does not change shared registration or provider setup.

1. Obtain this package from the Working Tools plugin repository and configure its `working-tools` marketplace according to the receiving host’s native plugin manager. Preserve unrelated marketplace entries and use the actual checkout or marketplace location on that host.
2. Install through the native plugin manager using `codex plugin add development-studio@working-tools` when that marketplace is configured. Inspect the manager’s current command/help before acting. The only MCP declaration is the reviewed plugin-owned REA launcher. Before enabling it, validate the private runtime binding and configure native per-server write approvals plus the explicit prompt set in `rea-tool-catalog.json`. Other providers remain external.
3. Compare every source file and installed file in both directions, excluding only documented platform-generated metadata. Version equality alone is insufficient. Run the read-only package validator on source and installed roots; validate top-level skills with the host’s native skill validator.
4. Open a fresh chat/discovery context and confirm all 22 focused skills appear and libraries are support assets rather than extra global discovery. Exercise a direct help prompt, existing feature request, bug request, MCP task and missing-provider case from `tests/scenarios.json`. The scenario file is a test contract; its presence is not trial evidence.
5. Verify official provider discovery and the actual required connection separately. Check the provider map’s method locations against the installed versions. Keep OpenAI providers and necessary external services.
6. Only then evaluate predecessor retirement using `legacy-disposition.md`. Full helper/native-host functional equivalence is still a separate gate. Do not uninstall the disabled legacy bundles with unresolved useful coverage.

Historical source-preparation evidence is recorded in the companion validation report. On each receiving host, verify native installation, source/cache parity, fresh discovery, representative task behavior and any required provider runtime separately. The author-host installation receipt does not establish recipient readiness.

Public source distribution is covered by the path-specific grants in LICENSE.md. Installation and actual-host acceptance remain separate. Game Creation Studio has its own source and handoff.
