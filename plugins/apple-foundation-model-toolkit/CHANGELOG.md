# Changelog

## 0.2.0

Add Apple Foundation Model Toolkit as a standalone provider toolkit.

Expose provider-specific setup, CLI operation and task-fit guidance while keeping account data, credentials, machine paths and runtime state recipient-owned.

Initial public edition of Apple Foundation Model Toolkit. The package is CLI-first where a supported provider CLI exists, records readiness separately from successful inference, and includes recipient onboarding. Private account identifiers, host paths, model receipts and local state are excluded.

Compatibility: New standalone package; no existing package identifiers, hooks or runtime contracts are removed. Provider services and local operating-system capabilities remain external prerequisites.

Upgrade: Install this package, follow its recipient onboarding, configure the provider or host runtime yourself, then run its bounded readiness and task-fit checks before delegation.

Validation: Canonical source copied into the reviewed public checkout; portable and compatibility manifests checked; complete public file inventory generated; account, credential and machine-path scan returned no matches. Publication remains queued for the existing release workflow.

## 0.1.0

Initial provider toolkit with CLI-first operation, conditional interface alternatives, task-fit checks and recipient setup. Host credentials, private receipts and model downloads are excluded.
