# Efficient implementation adoption

Source reviewed: Dietrich Gebert's **Ponytail v5.0.0**, commit
`b088b2df6e08d4306c6a3c3d575fe38c2d2d2989`, [repository](https://github.com/dietrichgebert/ponytail/tree/b088b2df6e08d4306c6a3c3d575fe38c2d2d2989).
MIT grant retained in [the source library](../libraries/efficient-implementation-v5/LICENSE).
Review date: 2026-10-20. This is a functionally named, security-hardened adaptation, not an unchanged upstream installation.

## Coverage and ownership

| Upstream utility | Integrated destination |
| --- | --- |
| Complete smallest-change procedure and three intensities | Existing `implement-software`, [full method](../references/efficient-implementation.md) |
| Session mode, off/default controls, resume and explicit child inheritance | [Runtime operations](../references/efficient-operations.md), `runtime/efficient-implementation/` |
| Status display | Read-only status badge; no host settings rewrite |
| Codebase reuse map | Bounded on-demand runtime map plus existing Code Intelligence |
| Complete diff review | Existing `review-and-release`, [review procedure](../references/quality-review.md) |
| Complete whole-repository audit | Same procedure, distinct audit scope and coverage limits |
| Shortcut debt ledger | Runtime `debt`, configurable marker and explicit legacy migration |
| Gain scoreboard and honesty boundary | Existing `evaluate-dev-workflows`, [evaluation](../references/implementation-evaluation.md) |
| Help | Existing implement/review/evaluate heads and operation table |
| All historical worked examples | [Complete example library](../libraries/efficient-implementation-v5/examples/README.md), labeled source evidence |
| Benchmark corpus, reports, adapters and maintainer assets | All 199 source files inventoried in [source dispositions](efficient-source-inventory.json); original checkout retained as evidence |

No new discovery skill or competing studio was added. Product readiness belongs to Work Management, applicable human expectations to UX Design, instruction refinement to Prompt Playbook, and implementation to Development. Companion methods are conditional, with a local fallback when unavailable.

## Deliberate adaptations

- Vague requests first establish the smallest complete outcome and applicable usability. The source's instruction to immediately build only a minimal core is replaced; unrequested features still remain out of scope.
- Full requested behavior, relevant accessibility, security, data integrity and error handling outrank code size. Test depth follows risk; one small test is not a universal ceiling.
- A shortcut marker never excuses a protected requirement or security defect. Divergent short command adapters resolve to the same complete guarded procedure.
- Session identity includes project and session. Startup does not automatically activate implementation rules, scan a repository, modify a statusline or launch workers.
- Filesystem utilities use bounded, descriptor-relative, no-follow operations on supported POSIX systems. Unsupported platforms fail closed; no universal Windows runtime claim is made.
- Hook control commands match complete explicit messages. Untrusted repository/contract text is not emitted into instructions, and the method pointer is anchored to the installed plugin.
- A staged native comparison found that root `plugin.json` suppresses hook discovery, while the compatibility layout exposes all three hooks with the same 22 skills, REA server and interface. Complete portable metadata is retained at `docs/portable-plugin-manifest.json`; root restoration requires a fresh native check. The matching [OpenAI loader branch](https://github.com/openai/codex/blob/e18a20d6eb6f5ede32a69fb56e3fe276d5e9d914/codex-rs/core-plugins/src/loader.rs#L972-L982) corroborates this host result. No global hook workaround is installed.
- Upstream publication, uninstall, auto-setup and alternate-host adapters are replaced by the current studio's native maintenance and scoped utilities. They are preserved in source evidence, not installed across unrelated hosts.
- The original benchmark harness is not trusted automation: it bypasses permissions and executes generated code. Its reported results and comparison capability are retained with explicit isolation and evidence requirements. Full numerical reproduction has not been performed.

## Security admission and evidence limits

Source inspection found no deliberate malicious payload or hidden core telemetry. Concrete defects included outside-root and unbounded map reads, source-comment prompt injection, unsafe shell construction in a publishing helper, broad benchmark execution/provider exposure, inherited configuration in tests, and cross-session state collisions. Publicity was not used as security evidence.

The adapted runtime resolved reviewed filesystem races and guidance-path shadowing. Its isolated suite covers state separation, contract freshness, invalid input, one-shot operations, bounded scans, symlink/directory-swap attacks, trusted guidance, and unsupported filesystems. Native hook registration/trust and installed byte parity are checked separately at installation. A synthetic hook test is not an actual model-session delivery trace.

The mode state records a caller assertion, not human acceptance or new access permission. If a native payload omits semantic scope, the agent must revalidate it. Concurrent writes within the same explicit session are last-writer-wins; other sessions remain isolated. Maps and debt scans remain regex approximations with stated limits.

## Review contributions

Claude Opus 5.5 supplied the readiness-boundary critique: adopted conditional ownership, routine-choice inference, complete behavior before minimization and scoped reopening. Rejected universal one-question-round and mandatory confirmation rules because task evidence and current authorization govern those decisions.

Gemini, requested as `gemini-4-argon-high`, supplied a benchmark-method critique. The wrapper reported success but did not expose a returned model ID. Key claims were checked against the pinned source. Statements based merely on files absent from its supplied packet were not promoted to repository-wide absence claims.

Local Gemma 4 12B MLX 4-bit extracted the six protected requirements, which were checked against the source and retained in the method. The first larger request timed out; a shorter bounded request completed and the owned model was unloaded. These are attributed worker contributions, not independent performance corroboration.

## Validation and rollback

Run `python3 -B scripts/validate_package.py` and
`python3 -B -m unittest discover -s tests -v` from the plugin root.
Validate changed skill frontmatter and routes, exercise readiness/bypass cases,
then install through the native manager and compare source/cache bytes.

The owning maintenance task retains source pins, pre-change files, worker outputs,
security findings and installation receipts outside the distributable package.
Rollback restores only the task-owned changed files from that snapshot, removes
its added files, reinstalls the prior source and restores only the hook keys this
change introduced. Preserve unrelated changes and existing host services.
