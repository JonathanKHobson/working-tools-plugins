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
