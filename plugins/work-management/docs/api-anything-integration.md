# API Anything integration

Source: [goodnight000/api-anything](https://github.com/goodnight000/api-anything/tree/20cb677039fcfe92d3d9c777aa9362e30ff1fdb8), version 0.1.0, commit `20cb677039fcfe92d3d9c777aa9362e30ff1fdb8`. Reviewed October 21, 2026. The complete 169-file working tree is preserved under `libraries/api-anything`; only Git administration and filesystem sidecars are excluded. [Per-file SHA-256 values](api-anything-source.json) bind the snapshot. The original [MIT license](../libraries/api-anything/LICENSE) remains in force. First-party helper, tests and routing text follow Work Management's own licensing.

The integration adds an on-demand setup/CLI/MCP runner under the existing tool-workflow-routing entrypoint. It preserves upstream code unchanged. Source, tests, site specs, examples, docs, benchmarks, media and upstream host metadata all remain as inactive library material; only the root Work Management metadata is installed. The upstream skill's unpinned install fallback and repeated approval step are overridden by the maintained integration reference. There is no new top-level skill or hook.

## Security review

Verdict: proceed with caution for authorized local operation. Confidence: medium. Source inspection and focused checks reduce specific risks; they are not a full audit or security guarantee.

Inspected: package manifest and lockfile, CLI/MCP entrypoints, request/redirect path, browser/profile selection, session/spec storage, registry pull and publish code, plus the complete teaching skill. All resolved lockfile packages point to npm's registry. Dependency lifecycle scripts are disabled; only the reviewed TypeScript build is invoked. The static skill scan returned zero active findings across eight rules. It does not cover all runtime behavior, dependencies or website content. No release signature or artifact attestation was established; Git commit and per-file hashes provide reproducible source identity, not publisher certification.

`npm audit` reported one moderate transitive Hono advisory, [GHSA-5r4p-p66f-jhc7](https://github.com/advisories/GHSA-5r4p-p66f-jhc7), affecting static HTTP serving in the locked dependency. This integration uses stdio MCP and the CLI, with no Hono static HTTP server or listening endpoint. The affected serveStatic path was not found in the reviewed entrypoints. Retain that limitation and re-evaluate before adding HTTP serving or changing dependencies; no claim of zero vulnerabilities is made.

Threats checked: source spoofing, unpinned execution, install-time hooks, persistent services, sensitive profile/session access, tool metadata injection, untrusted specs, redirect credential forwarding, arbitrary network destinations and public spec submission. Captured pages and spec notes remain untrusted. The helper is a reproducibility boundary, not a sandbox. Runtime dependencies are lockfile-installed, but are not rehashed at every call. User-authored specs and authorized account state can change independently of the pinned source.

Claude Sonnet 5 independently reviewed supplied source and proposed acceptance checks. Accepted findings: distinguish read-default from auth-free, document implicit session refresh, keep private state separate, pin updates and verify cold-start/tamper cases. The suggestion to put private state inside the runtime was rejected because updates must preserve state independently. Upstream auth behavior is retained and exposed explicitly; no new technical auth sandbox is claimed. Runtime tests must distinguish source parity from model uptake.

## MCP capability fingerprint

- Name: API Anything; source and commit above; stdio only.
- Launch: `python3 <installed-work-management>/scripts/api_anything.py mcp`, which verifies the selected runtime and executes `node <runtime>/dist/cli.js mcp`.
- Version/hash: 0.1.0 plus pinned source manifest; compiled entrypoint hashes are recorded after setup.
- Environment: recipient-selected runtime and state; optional upstream browser/registry/GitHub executable overrides. No credential environment variables are requested by setup. Inherited NODE_OPTIONS and NODE_PATH are removed.
- Working directory: caller's directory; source and runtime paths are resolved explicitly.
- Tools: list_sites, list_operations, call_operation, login. Resources/prompts/sampling: none registered.
- Filesystem: selected runtime plus private state; login can access an explicitly authorized browser profile and OS credential store. CLI export writes its requested output path.
- Network: selected sites and redirects; optional registry GitHub reads and explicit GitHub CLI publication. No host-wide allowlist or network sandbox.
- Writes: state/spec/capture/profile updates can occur during reads; website mutations require allow-writes. Publishing is CLI-only and needs an unchanged preview plus --yes.
- Auth: no model API key. Website sessions may be imported or established in a browser and refreshed; stored locally with restrictive permissions. Public smoke checks use fresh state and no login.
- Output: JSON/stdout; errors/stderr; local runtime/session logs. No added telemetry or daemon.
- Updates: explicit source review, manifest refresh, new runtime build and provider synchronization. No network install on run/startup.

## Acceptance

Run `python3 -B -m unittest discover -s tests -p test_api_anything.py -v` from this package. It checks source completeness, missing-setup behavior, tamper/symlink/path refusal, private-state separation, nonempty-directory preservation Node version requirements, missing direct dependencies and failed CLI startup. Build the pinned runtime, run upstream type checking and relevant tests, initialize stdio MCP, list tools and make a public Hacker News search with fresh state. Check one returned record against the source endpoint. Preserve output and installation readbacks in the owning task's private work record.

Public packaging must retain this reference, runner, tests, snapshot and license as a complete closure. Keep author-host bindings and runtime/session data outside the public tree. A staged archive or provider source sync is not a public release or proof that an already-running model loaded it.

Final independent code review identified misleading ready status after dependency removal and an unpinned command suggestion in upstream MCP output. The helper now checks direct dependencies and CLI startup; MCP handoff guidance explicitly replaces that suggestion with the pinned runner. Upstream is preserved unchanged.
