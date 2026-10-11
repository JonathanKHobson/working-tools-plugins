# Incorporated-method acceptance

`complete_update.validate_committed` applies the existing package, canonical source-inventory and exact-build checks. Before remote publication it also invokes `release_manager.method_acceptance` for affected incorporated methods. This adds no model call to a routine edit, save or no-op update.

The reviewed manifest in `catalog/method-acceptance.json` covers the eight retired instruction packs through eight task capabilities. It names the full native procedures, relevant support, reviewed local reference edges, support-directory layouts and actual execution requirements. An added/removed support file, changed method requirement or new local method link needs a reviewed manifest change. The manifest never licenses excluded provider bodies or represents all a Studio's methods as provider clones.

Changes to the selected full source, capability contract or fictional fixture invalidate acceptance for that capability. Exact unchanged receipts can be reused; unrelated products and changes outside covered method paths pass through. The gate checks source evidence and real output review, not the presence of topic words or a successful link.

## Prepare a real trial

From the repository root:

```sh
python3 scripts/release_manager/method_acceptance.py snapshot > /tmp/method-review-snapshot.json
python3 scripts/release_manager/method_acceptance.py input-bundle > /tmp/method-trial-input.json
```

`--product <id>` scopes either command. The input bundle contains the full current selected procedures/support and the fictional requests; it omits reviewer criteria. Run that bundle with an actual available model through its authorized execution owner. Record the exact resolved model, not only a CLI alias. Preserve the invocation output/metadata and SHA-256. This helper performs only source reads and does not invoke an AI or install anything.

The response contract is a JSON object keyed by the selected case IDs. Each value contains the complete requested artifact/response; there are no self-grades. Keep the reviewer criteria out of the generating model's context. A lead reviews actual output against each functional criterion, retaining exact output excerpts and limitations. Source-method completeness and output success are distinct reviews.

## Trial receipt

Configure `method_acceptance_receipt` with the real receipt JSON path. It requires:

- `schema_version: 1`, `kind: executed-model-trial`, `run_id`, `observed_at`, `provider`, `exact_model`, and `invocation_evidence_sha256`.
- Exact `source_hashes`, `case_hashes` and `contract_hashes` from the current snapshot, plus `method_only_providers_invoked: false`.
- `reviewer` with `identity`, `method: source-and-output-review`, and honest `limitations`.
- `outputs` keyed by case ID, and `output_hashes` computed with `method_acceptance.value_hash` from those actual values.
- `evaluations` keyed by case ID: `status: pass`, explicit `limitations`, and all expected criterion IDs. Each criterion has `status: pass`, a `reason`, and `output_evidence` with exact excerpts of at least 12 characters from that case's actual response.
- `procedure_reviews` for each declared full procedural source: current `sha256`, `kind: complete-procedure`, `status: pass`, and `inputs`, `sequence`, `edge_cases`, `output`, `verification`, each listing source-anchor IDs.
- `procedure_source_evidence` keyed by source path. Each anchor records `id`, one-based `start` and `end`, and the exact full lines as `quote`. The gate matches these to the current source. A routing shell or unresolved handoff is not a complete procedure.

A source-only checklist, empty response, invented model invocation, failed criterion, absent output quote or unreviewed procedure cannot satisfy this contract. An accepted representative set remains bounded evidence; it does not prove universal method reliability.

## Host agreement

Configure `method_acceptance_host_receipts` with a JSON list of actual installation/readback receipts. Each required host has `kind: verified-host-method-readback`, `host`, `status: pass`, current `source_hashes` and `contract_hashes`, `observed_at`, `evidence_sha256`, explicit `limitations`, and true `checks` for `package_source_agreement`, `loaded_method_agreement` and `retired_prerequisites_absent`.

The existing source-inventory/package checks establish canonical and public distribution agreement; host receipts must come from the actual host installation/loading checks. Do not infer them from copied files or manifests alone. Codex is currently required. Add another required host only with its actual verification and supported-host claim; otherwise retain the host's unverified boundary. Host source disagreement or a reintroduced retired prerequisite blocks release.

The receipt binds relevant content rather than a Git commit, avoiding a receipt/commit self-reference cycle. No automatic release, installation, model selection or new prompt/method catalog is created here.
