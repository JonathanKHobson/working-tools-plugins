# Master Security Toolkit

Version **0.2.3** adds portable MCP discovery through root [`mcp.json`](mcp.json) for the existing optional launchers. Their server identities, runtime bindings and compatibility declarations are preserved; backend availability remains a separate check.

Inspect software, plugins, permissions and AI instruction boundaries, then explain evidence-backed risks and verify targeted fixes. Bring a local artifact or exact source revision, the intended use, and the decision you need. Begin with one of the [nine complete skills](docs/use-case-map.md), or ask what this toolkit can do.

- `software-security-review` and `software-provenance` assess an external package or release before admission.
- `agent-artifact-scanning` runs a pinned local, read-only scanner on an authorized target and reports exact evidence and noncoverage.
- `instruction-security-review`, `indirect-injection-review` and `security-regression-tests` assess AI instruction boundaries and test mitigations.
- `application-security-testing`, `mcp-security-review` and `permission-and-data-review` cover authorized app, MCP and permission surfaces.

The full first-party skill heads, support references, role contracts, local scripts and licensed retained upstream methods are included. [Procedure selection](docs/full-procedures.md) identifies one external dependency: the four complete Injection Checker depth methods come from the official separately installed `injection-checker@openai-curated-remote` plugin. In Codex, install it through the native plugin manager and start a fresh task; use `injection-checker:injection-checker`, `injection-checker:indirect-injection-review`, `injection-checker:agent-tool-boundaries` or `injection-checker:mitigation-regression-tests` as the review requires. This exact installed-provider route is verified in Codex; equivalent Claude discovery has not yet been verified. If unavailable on a host, the Toolkit's complete first-party review methods still operate, but report the missing external depth route. No copied provider body is distributed here.

## Optional security Atlas

The [security Atlas route](references/atlas-library.md) selects external reference material; it is not a scanner or vulnerability test. The fixed-domain launcher in `scripts/atlas_library_mcp.py` is declared in portable `mcp.json` and compatibility `.mcp.json`, and uses `python3` on PATH. Portable Codex discovery uses root `mcp.json` with `${PLUGIN_ROOT}` paths. Claude uses the corresponding `${CLAUDE_PLUGIN_ROOT}` path in `.claude-plugin/plugin.json`. Copy the [inert binding example](examples/runtime-bindings/atlas-library.json) only if no existing binding should be preserved, then replace placeholders with your separately installed Activities Templates runtime and approved recipient-owned catalog. Keep actual binding paths private. The launcher makes no download or repair attempt and reports missing access. Installation does not prove a host exposes the tool.

Optional cross-Studio routes, including Activities Templates, Work Management and Mac Ops, require those owners to be installed. If an owner is missing, continue this Toolkit's bounded review with available evidence, identify the unavailable handoff and do not claim its specialized check ran. Historical personal source references describe prior behavior and do not set a recipient's privacy or approval preferences.

A clean static scan is not a safety certificate. Source review, target-controlled testing, live tool access and installation are separate outcomes. No hook, background service or automatic gate starts with this package. Run the pinned scanner only on a task-authorized local target; it does not execute the target or write a report.

## Source and licensing

The stable package ID is `master-security-toolkit`, and the display name is Master Security Toolkit. The canonical local owner and public package carry the same distributable files. Maintainers change canonical source first and export exact bytes; installed caches are generated snapshots.

First-party code uses AGPL-3.0-only. First-party documentation, skills, methods, roles and original templates use CC BY-SA 4.0. Retained SkillGuard and Cloudflare MIT material, Strix Apache-2.0 material, and other recorded upstream grants remain under their own terms. See [licensing](LICENSING.md), [notices](THIRD_PARTY_NOTICES.md), [scope inventory](LICENSE-SCOPE.json), and [source attribution](SOURCE-ATTRIBUTIONS.md). The provider's independently installed method, Atlas corpus, private bindings, account data and target files are not included.

[Project map](docs/project-map.md) and [use-case map](docs/use-case-map.md) locate the maintained entrypoints.
