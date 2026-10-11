# Independently hosted guide downloads

`catalog/external-products.json` records the actual public download products outside the Working Tools plugin registry. Its 22 frozen legacy products are historical evidence, not candidates for automatic versioning. Three active skill downloads are maintained in their owning guide repositories: Participatory Defense Assistant and Grounded Legal Research in Shareables, and Safe Install Review in What Is an MCP. Understanding AI in 2026 is an active page-only guide. Each product carries its own source commit so an update to one Shareables guide cannot rewrite another product's provenance.

The active source owner completes the authored change in its own repository first. Shareables is a public Pages mirror of a separate private authoring source, so the update note must state the reviewed authoring provenance. The public checkout must contain the final, committed download or page bytes at the exact registered paths. New paths require a separate source and rights review before they enter the ledger.

Routine local maintenance records pending changes with `scripts/complete_update.py`; its default is offline queue refresh. The commands below are explicit publication actions for a completed batch, not steps for every local edit.

For a changed product, the authoring agent writes `catalog/external-changes/<product-id>.json` with `product_id`, the full public `source_commit`, sorted exact `changed_files`, and specific `summary`, `why`, `compatibility`, `upgrade_guidance`, `validation`, `release_notes`, and `authoring_provenance` strings. No note is needed for an unchanged product. The agent then runs:

```sh
python3 scripts/complete_external_update.py \
  --product safe-install-review \
  --checkout /path/to/what-is-an-mcp \
  --notes-dir catalog/external-changes \
  --publish
```

The command checks the owning origin, committed registered paths, exact source commit, note, and fast-forward relationship with `origin/main`. It rejects malformed or unsafe installation archives and records SHA256 outside the archive. For downloads, it compares the prior committed bytes with the verified ledger digest and archives that snapshot in a revision-tagged GitHub release. It pushes the new source commit, publishes the new exact registered assets through the existing draft, byte-verification, publish sequence, waits for the original Pages download URLs to serve the new bytes, and atomically advances only that product's ledger pin and immutable release links. The original Pages URL stays in `original_url` for later verification. Revision tags derive from the exact source commits; they do not imply SemVer. The specific authored note and upgrade guidance remain in both the ledger and projected Site history. For the page-only guide it pushes and verifies the page bytes without creating an installation release.

If publication or Pages verification fails, retain the ledger and rerun the same command after the external condition is fixed. The publisher checks existing tags and assets for exact collisions, so recovery does not create a replacement version. After the ledger advances, run the normal catalog/Site reconciliation to include the new external history and verify the rendered guide card and live download. The native Sites source for each guide remains separately owned by its project; update it through that project's workflow when its text or links change. The Working Tools Site projection must read the updated external catalog before completion is claimed.

`plan_active_external_updates` in `scripts/release_manager/legacy.py` offers an optional read-only change/notes gate across registered source checkouts. It reports frozen source differences separately and never treats them as pending releases. A frozen product can move to an active lifecycle only through an explicit policy and source-lineage review.

## Preserved collection membership

[Historical collection manifests](../catalog/legacy-bundle-membership.json) record the exact member directories, declared versions and dependencies, and every file hash from both verified frozen collection ZIPs. This is a retrospective inspection of the original package bytes, not a new package release. The Writing and Design Enhancement Collection contains 46 skill directories and has no declared package/skill versions or machine-readable dependency manifest. Its recorded source revision and archive digest identify the exact edition. The Job Application Compass skills package contains four skills and declares package version `0.1.0-skills.1`. Individual skills do not declare separate versions. Neither archive is a bundle of the current Working Tools plugin ecosystem.

The manifest preserves missing declarations as null or explicit absence. It does not infer installed dependencies, runtime compatibility, or private authoring provenance from a public mirror. Original package bytes, tags and release identities remain unchanged.
