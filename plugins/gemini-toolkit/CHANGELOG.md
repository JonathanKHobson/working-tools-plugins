# Changelog

## 0.3.0

2026-10-27 release review: Add a bounded tracked Gemini worker and explicit Antigravity source synchronization.

2026-10-27 release review: Reuse authenticated CLI work with inspectable results and conflict-safe synchronization.

2026-10-27 release review: Bundle gemini_worker.py and sync_antigravity.py with focused tests and operation guidance. The worker performs a bounded supplied-text CLI task and invokes optional fail-open usage recording; the sync helper reconciles configured source links explicitly. Direct CLI diagnostics remain available outside the tracker.

Compatibility: 2026-10-27 release review: Recipient CLI authentication, model readiness, configured source roots and optional usage recorder remain external. Installation does not authenticate Gemini, run inference or synchronize a host.

Upgrade: 2026-10-27 release review: Refresh the package, verify the recipient CLI/account/model, and use the bundled worker for a bounded task. Review the sync helper configuration before explicitly running synchronization.

Validation: 2026-10-27 release review: The release scope record and current public/canonical source differences were reviewed read-only for this note. Applicable added specialist policy files were checked for allow_implicit_invocation: false. Package structural, provenance/license closure, focused runtime tests, privacy checks and publication readback remain release-gate checks; this note does not claim those checks passed or establish live runtime readiness. Read-only local_sync.reviewed_additions passed for all 4 listed exact-canonical additions, checking public/canonical byte equality, source-inventory membership, provenance hashes and license coverage. This does not establish full package or runtime validation.

## 0.2.0

Add Gemini Toolkit as a standalone provider toolkit.

Expose provider-specific setup, CLI operation and task-fit guidance while keeping account data, credentials, machine paths and runtime state recipient-owned.

Initial public edition of Gemini Toolkit. The package is CLI-first where a supported provider CLI exists, records readiness separately from successful inference, and includes recipient onboarding. Private account identifiers, host paths, model receipts and local state are excluded.

Compatibility: New standalone package; no existing package identifiers, hooks or runtime contracts are removed. Provider services and local operating-system capabilities remain external prerequisites.

Upgrade: Install this package, follow its recipient onboarding, configure the provider or host runtime yourself, then run its bounded readiness and task-fit checks before delegation.

Validation: Canonical source copied into the reviewed public checkout; portable and compatibility manifests checked; complete public file inventory generated; account, credential and machine-path scan returned no matches. Publication remains queued for the existing release workflow.

## 0.1.0

Initial provider toolkit with CLI-first operation, conditional interface alternatives, task-fit checks and recipient setup. Host credentials, private receipts and model downloads are excluded.
