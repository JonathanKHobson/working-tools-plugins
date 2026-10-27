# Source provenance and coverage

Reviewed 2026-10-08. [imports.json](imports.json) records source version, each source hash, destination hash and disposition. [provider-inventory.json](provider-inventory.json) records all files of retained official providers so final readback can detect unintended changes. These are local installed/source observations; no upstream signature or source-build attestation was obtained.

## Full preserved sources

- Superpowers 6.4.2, Jesse Vincent, repository `https://github.com/obra/superpowers`: all package files preserved byte-for-byte under `libraries/superpowers-6.4.2/`, including 15 methods, prompts, examples, scripts, adapter guidance, assets and MIT license. Source was the installed `openai-curated-remote` cache version. Focused top-level skills route all methods except the universal conversation hook, which is deliberately retained for framework migration/provenance and superseded by conditional discovery. Optional helpers remain source assets pending invocation-specific review.
- Personal Build MCP Apps `1.0.1-kyle.1+agents.20261007062618`: both active skills, their full references, professional-role guidance and all Alpic snapshot files carried into this owner. Predecessor package metadata/README/docs are replaced by current identity, setup and provenance. Professional role paths are relative; the personal theme preference is externalized into project configuration. Per-file hashes identify exact adaptations.
- Current-source reconciliation, 2026-10-17: canonical personal Build MCP Apps `1.0.5` retains the same two active skills and 42-file Alpic 1.0.1 snapshot. The historical import identity above remains an accurate record of the original intake. `imports.json.current_source_reconciliation` separately hashes all 54 historically considered source paths against current `1.0.5` and their Development outputs where carried: 45 byte-identical, three adapted for portable theme/role ownership, and six predecessor metadata files superseded by Development Studio records. The adapted role index was corrected to name Development Studio and route Work Management through the installed plugin. This is a source-file reconciliation, not fresh native discovery or a claim that the two plugin identities are the same release.
- Alpic 1.0.1: unchanged nested source from the maintained Build MCP Apps owner, repository `https://github.com/alpic-ai/alpic-plugin`; included Apache license acquired by that prior maintained source from upstream. Its historical version and current upstream version are not conflated.
- Local MCP methods: see [local-mcp provenance](local-mcp-provenance.json) and [admission](local-mcp-admission.md) for full preserved/adapted source, helpers and host portability changes.

## Retained execution/method owners

Build Web Apps 0.1.2, Build iOS Apps 0.1.2, Build macOS Apps 0.1.4, Test Android Apps 0.1.2, Plugin Eval 0.1.2 and Game Studio 0.1.2 identify OpenAI in their installed author/developer metadata. They are untouched. The directory name `openai-curated-remote` alone does not establish official authorship; Superpowers and Game Development Studio are third-party publishers. Game Creation Studio handles that game source separately.

All 33 development-provider methods and nine Game Studio methods are inventoried with their actual file routes. Full procedures and execution dependencies remain external, not imitated here. Retained provider file hashes are evidence of preservation, not live availability.

No claimed full replacement of disabled Builder Tools or MCP Workbench: [legacy disposition](legacy-disposition.md) identifies useful unmigrated methods and rights gaps. Their source remains retained. Public distribution status is explicit in [rights](../LICENSE.md).
