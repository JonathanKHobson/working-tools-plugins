# Verify a plugin's release surfaces

Use only when changing packaging, generated/distribution copies or installer modes, or when source-to-installed parity is disputed. Reuse the owning project map, change inventory, native install flow and Master Security Toolkit admission. No new registry, hook, app or script is required.

1. Identify the canonical source revision and actual release surfaces: generated package, unpacked dist, nested archives and installed cache. Record exact paths, version/tag/commit and applicable artifact hashes. Preserve concurrent active work; do not infer ownership from a similarly named folder.
2. Compare both directions: modified files, newly introduced source files omitted from dist, dist-only generated files and unsupported/binary members. Check archives as data with a trusted extractor: reject unsafe paths/links and apply size/resource bounds before writing into task-local inspection storage. Do not execute packaged tests or metadata flags to establish parity.
3. Preserve raw hashes. For text mismatches, explicitly compare with a named normalization such as CRLF-to-LF and report newline-only equivalence separately from byte identity. Do not normalize away meaningful code, JSON values, encoding changes or binary bytes. Trace semantic differences to an intended adaptation; missing required modules or stale entrypoints block parity.
4. Check version/manifest consistency across source, generated and installed files; keep hashes tied to the exact reviewed revision. Verify executable modes and archive link handling where a launcher depends on them. A matching version string alone does not prove equivalent contents.
5. Confirm package-wide licensing and carried notices cover the code/assets actually distributed; one third-party notice does not license unrelated original code. Verify required notices/assets are included in packaging rules. Keep missing rights or redistributed-runtime source obligations explicit and route specialized questions to software provenance/security; do not infer permission from public availability.
6. Trace declared mode behavior through helpers before claiming no change: dry-run, settings-only and check modes must honor the stated write/download/execute boundary on every applicable branch. Limit claims to verified branches; retain privacy/redaction and established runtime paths. Prefer a trusted static check during admission; runtime mode verification is separate authorized work.
7. Promote only reviewed staged hashes, use the native install/update flow, and compare installed paths/hashes against the approved surface. Re-run relevant source and staged security checks when behavior changes. Report prepared, generated, installed and verified separately, with unresolved surfaces listed.

Acceptance scenarios:

- ZIP and unpacked scripts differ only in CRLF/LF: retain differing byte hashes and report normalized-text equivalence, not stale semantics or byte parity.
- Source gains a required helper absent from dist: identify the caller and missing module, rebuild the affected release, and withhold a parity claim until the surface matches.
- README points to a missing package license or the manifest omits it: report the specific gap and repair the release inputs instead of adopting the nearest dependency license.
- A script loses its executable bit or a settings-only branch unpacks runtime archives: verify/fix that declared surface; do not claim the mode passed from a clean scan or copied source alone.

Method provenance: original local release-check refinement prompted by Bloom Studio's source/dist and installer-mode discrepancies, reviewed 2026-10-02. No upstream implementation imported; existing owner and admission procedures remain authoritative.


## Complete an authorized public update

Separate local maintenance from public release. After a requested local update, run its focused checks, install through the native manager and verify the changed source/cache paths. Then refresh the owning distribution's pending-change record. Routine completion does not publish, allocate versions or deploy the website. An explicit request to publish the current batch supplies the release event; existing access and standing approval remove repeated permission questions, not this batching boundary. Urgent security, data-loss or broken-install fixes may use an explicitly requested immediate scoped release.

For Working Tools, `catalog/packages.json` owns released plugin versions and `catalog/source-inventory.json` owns reviewed shipped paths and exclusions. In its maintained checkout, `.venv/bin/python scripts/complete_update.py --config <maintainer-config>` records the local queue. The queue is private, ignored state rather than a release record. It tracks differences and review needs without requiring GitHub, an AI session, version bumps or a Site deployment. For routine maintenance, repeat `--package <id>` for the plugins just changed so the command scans only those owners and preserves the rest of the queue. `--status` refreshes the same record for inspection; omit package selectors for a full ecosystem scan. Changes made outside Codex are discovered on the next command; no watcher, schedule or background AI job is installed.

Use `.venv/bin/python scripts/complete_update.py --config <maintainer-config> --publish` when publishing a completed batch. Repeat `--package <id>` to release only the intended plugins. Resolve all affected shared-resource members before choosing that scope. The publisher reconciles reviewed public files, synchronizes manifests, creates specific version records, validates exact-commit packages, publishes GitHub assets, then updates the catalog once for the batch. The current Site deployment adapter still requires its authenticated Codex connection. Do not describe the entire publisher as AI-free.

The authoring agent accumulates diff-grounded change notes in the existing `catalog/changes/<product-id>.json`, preserving earlier pending additions and checks instead of replacing them with only the last edit. Missing notes may remain a queue review item until the batch is prepared; the user does not need to write them. Review compatibility against the aggregate difference from the last public version at release time. One batch assigns one appropriate version per changed product. Include shipped instructions, references and templates. Website-only edits do not bump unrelated products, and unchanged inputs do not create releases. A logo belongs in a plugin release only if that asset is part of its downloaded package.

Prefer a useful public milestone over a raw file count or version-number threshold: a coherent capability, a correction users need, or a set of small improvements worth announcing. A weekly or fortnightly review can be a manual habit if requested; it is not a scheduled job or an automatic publishing threshold. Keep GitHub packages and the public catalog together by default so current downloads remain consistent. Reuse unchanged verification receipts where the implementation proves the same bytes and source identity.

Use `--publish --reconcile-only` with the original package scope to recover an already started publication without another version. Retain the published package and prior working Site if deployment fails; report the pending catalog step accurately. Never widen private export boundaries, rewrite historical assets or remove upstream notices to make a batch pass. New files, removals, conflicting contributions and redistribution changes require their specific review before release. A queued update is a completed local update, not a completed public release.


## Keep reusable release methods separate from private setup

Work Management owns this portable release method. A maintainer may add a
private companion plugin or user-global release skill for their configuration
and publication tools. Public users do not need that private setup. Keep it
outside public packages, export allowlists and distribution cleanup inputs;
private native installation caches are permitted.

Treat local maintained plugins as canonical. Publication only reads them and
builds a portable projection. Adapt machine-specific paths through relative
paths, environment variables or documented setup while retaining full approved
functionality. Generated manifests never overwrite canonical manifests.
Preserve skills, scripts, hooks and their host registrations, agents, MCP
configuration, references and assets. Missing capabilities block the affected
release; portability alone does not authorize removing them. Independently
verify the hook interface supported by each host, and detect missing or duplicate
handlers. Keep any separately authorized source reconciliation outside the
publisher.

Offer collection as a flow within release management, not another plugin or
skill. Track in-progress and completed edits with their reason, affected owner,
compatibility and actual checks. Merge earlier pending notes rather than
replacing them with the last edit. Collection updates only the existing local
notes and queue; it does not allocate versions or prepare release records.
A read-only status request computes fresh observations without writing the
queue. Explicit publication batches the accumulated net changes and deploys the
catalog once. Never start publication from a timer or a raw change-count threshold.
