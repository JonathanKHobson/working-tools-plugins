# brand-templates project map

- `runtime/brand-library/`: complete original MCP catalog, source verification, handoff and chooser runtime. UI chrome stays package-owned. `ui/logo-gallery.js/.css` owns optional inline logo browsing in a selected brand detail; the Brand Library website uses the same component. Artwork comes from the selected external collection, with labels and fixed-field limits.
- `scripts/`: portable stdlib launch and explicit external synthetic-fixture creation.
- `skills/brand-templates/SKILL.md`: one discovery head for the complete external-collection workflow.
- `tests/`: real stdio, integrity and relocation checks; all data stays external.
- `PROVENANCE.json`, `PUBLIC_FILE_MANIFEST.json`: exact selected input/output hashes and public-file closure.

The original 104 fictional kits and previews are included with source closure and font notices. The additive Fresh Curiosity A2 kit and unrelated private materials are excluded. Public code does not expand their rights. User collections and feedback databases belong outside this package.

- `runtime/brand-library/stdio_proxy.py` and `shared_backend.py`: version/binding-separated sharing of SDK imports through private Unix sockets. Each caller has an independent MCP session. A backend retires 60 seconds after its last client disconnects; there is no timer that kills an active client. Native host still owns proxy lifetime. `BRAND_TEMPLATES_TRANSPORT=direct` retains the direct stdio fallback.
- `tests/test_shared_transport.py` checks protocol parity, concurrent isolation, private binding, crash failure and cold recovery. `BRAND_BASELINE_ROOT` optionally points to an earlier installed version for before/after parity. Transport code is adapted from the maintained Activities Templates 0.1.4 owner under the package's existing license. No UI or catalog source data changes.
