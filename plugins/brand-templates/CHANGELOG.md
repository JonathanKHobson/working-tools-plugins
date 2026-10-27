# Changelog

## 0.2.1

2026-10-24 font rights repair: give 50 static derivatives distinct Atlas names and resolve the exact-hash RFN review.

2026-10-27 release review: Add shared backend transport while retaining the font-rights repairs recorded earlier.

Retain the original OFL and authors while making generated static derivative identities distinct and keeping typography tables unchanged.

2026-10-27 release review: Share SDK imports across callers while preserving independent MCP sessions and the existing tool contract.

Atlas Reading Serif replaces the generated Lora identity; Atlas Book Serif replaces the generated Libre Baskerville identity across 24 kits. Primary, full, PostScript, unique and variation-prefix names plus current paths/catalog/source metadata are consistent. Original author/copyright/trademark/OFL notices, glyphs, metrics, shaping tables, original native specifications and embedded PDF documents are retained. Earlier Atlas Editorial Serif naming repair remains included. Existing published assets and versions are unchanged.

2026-10-27 release review: Add an injectable FastMCP server class, version/binding-separated shared backend, stdio proxy and transport tests. POSIX no-argument launch uses the proxy; direct CLI/export, non-POSIX operation and BRAND_TEMPLATES_TRANSPORT=direct retain the direct route. A backend retires after its last client disconnects. This review explicitly includes the transport changes excluded from the earlier font-only note; the transport adaptation credits Activities Templates.

Compatibility: Install the supplied Atlas-named derivatives when using the portable kits. Typography instructions and guide rebuild inputs use those names. Original source-family/native-template specifications remain separately recorded.

2026-10-27 release review: Existing tool names and outputs remain; no catalog or UI content change is intended. The direct transport remains a rollback option. Runtime sharing is local to the recipient.

Upgrade: Review the staged candidates and allocate a new immutable release only under separate publication authorization. Existing published archives must not be overwritten. The SHA-bound review accepts only the exact repaired font bytes; later changes require fresh review.

2026-10-27 release review: Refresh the package and use a fresh connection to load the new transport. Use BRAND_TEMPLATES_TRANSPORT=direct if direct stdio is required.

Validation: Four unique font outputs reproduce offline from retained original variable inputs; all 50 canonical/public copies pass metadata, notice and raw SFNT table equality checks. All 35 public scope checks and public source inventory pass. Current Brand development ZIP passes integrity/legal closure. Forty-nine website candidates (24 Brand, 25 Design) preserve unrelated original/native/PDF bytes and pass complete asset-manifest/CRC closure. Live canonical source inventory has six unrelated preexisting changed files and four excluded-source additions; none is exported or admitted by this repair.

2026-10-27 release review: The release scope record and current public/canonical source differences were reviewed read-only for this note. Applicable added specialist policy files were checked for allow_implicit_invocation: false. Package structural, provenance/license closure, focused runtime tests, privacy checks and publication readback remain release-gate checks; this note does not claim those checks passed or establish live runtime readiness. Read-only local_sync.reviewed_additions passed for all 4 listed exact-canonical additions, checking public/canonical byte equality, source-inventory membership, provenance hashes and license coverage. This does not establish full package or runtime validation.

## 0.2.0

Add reusable logo-family galleries to brand-kit previews and exports.

A brand kit can include several logo variants without giving users a usable way to inspect them together.

Adds a generic serialized logo-family gallery with variant labels, source-aware local paths, modal inspection and keyboard focus return. Native chooser and exported page share one JavaScript module and one style block; duplicate embedded copies were removed. The public projection retains104 eligible kits and excludes private brand data, assets and contextual defaults.

Compatibility: Compatible chooser/gallery addition. Existing kit IDs, handoff contracts and external host bindings remain.

Upgrade: Update Brand Templates. Existing authorized kits with logo-family data gain the preview; no private kit is added to the public distribution.

Validation: Five catalog tests pass. Assembled104-kit export contains one module/style definition and excludes the private kit. Existing desktop/narrow, selection, modal Escape/focus-return and native-export visual checks were reused for unchanged gallery behavior; in-host MCP expansion and screen-reader narration remain untested.

## 0.1.4 · 2026-10-10

Source-first reconciliation of complete eligible runtime/method improvements, private collection continuity, environment precedence and exact distributable inventories. Existing held corpus bodies and original grants remain excluded and preserved privately.

## 0.1.3

Clarify the included 104-kit first run, optional external fixtures and recipient configuration.

## 0.1.2

Apply the Compass license model to this new edition of first-party contributions. Preserve all earlier grants and unchanged upstream notices. Add explicit file scopes, attribution and reserved-mark boundaries. Operative method, helper and runtime bodies are unchanged.

## 0.1.1

Export complete original first-party runtime with explicit external data bindings, native and portable manifests, reproducible synthetic fixture and isolated protocol checks. Private collection files and reference assets are excluded.
