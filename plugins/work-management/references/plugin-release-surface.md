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

Use the owning public distribution repository and its executable completion command after the requested update and focused checks are finished. Individual saves and work-in-progress commits do not start publication. Public release authorization remains distinct from local-only maintenance; a request to publish or a standing public-update instruction supplies it. Never widen reviewed export boundaries to make a release pass.

For Working Tools, `catalog/packages.json` owns each plugin version; `catalog/source-inventory.json` owns reviewed shipped paths and exclusions. `.venv/bin/python scripts/complete_update.py --config <maintainer-config>` is the completion event. It reconciles reviewed paths, detects changed distributions, synchronizes host manifests, records evidence-based notes, validates exact-commit packages, resumes GitHub drafts and rebuilds the catalog. Its configured Site adapter finishes the same existing Site through the host's supported save/deploy tools. Do not claim completion from its prepared-site receipt; require verified deployment.

Changes made outside Codex reach the same event by running that command once the update is complete. Use `--reconcile-only` with the same config to retry publication/catalog synchronization after a partial failure without another version. No schedule, per-save watcher or repository-wide Latest pointer chooses product versions.

The authoring agent supplies a change record when a semantic explanation or compatibility classification is needed; derive it from the actual diff and checks, without asking the user to write release notes. Existing recorded notes feed the package changelog, GitHub release and catalog. Include changed instructions, references and templates; website-only and unchanged inputs do not bump unrelated products. Shared shipped resources must map to every affected distribution.

When a newly included file, removed invocation, contributor conflict, private scope or redistribution requirement needs review, resolve that specific evidence before its dependent release. Preserve independent completed releases and prior working deployments. Keep older tags/assets fixed, use draft then complete assets then publish, and verify asset bytes and exact version links. Do not recreate a package version after publication merely to retry the Site.
