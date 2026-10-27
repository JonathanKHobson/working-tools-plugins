# Changelog

## 0.3.0

2026-10-27 release review: Add optional inference usage recording and distinguish authentication status from CLI execution failures.

2026-10-27 release review: Allow configured hosts to record actual worker attempts without masking task failures or treating every failed auth command as sign-out.

2026-10-27 release review: Add a fail-open callback resolved from recipient usage-tracking configuration. Record one event around inference success, failure or timeout with available model/token metadata; authentication-only checks remain outside tracking. Accept explicit boolean loggedIn status even on a nonzero exit, reject unexpected JSON shapes and report sanitized command-failure categories without echoing provider text.

Compatibility: 2026-10-27 release review: Optional recording requires a separately configured recipient recorder; absent or disabled configuration is a no-op and recorder failure does not block work. Existing worker options and tool isolation remain; error wording becomes more precise.

Upgrade: 2026-10-27 release review: Refresh the package. Configure an optional recorder only if desired; diagnose auth command failures in the actual execution environment rather than assuming sign-out.

Validation: 2026-10-27 release review: Read-only scoped local_sync.plan found three changed reviewed paths and no conflicts. Eight canonical test_claude_worker.py tests passed with PYTHONDONTWRITEBYTECODE=1, covering worker isolation, requested effort/model receipts, success/failure/timeout recording, auth failure distinctions, malformed shapes, timeout termination and empty results. These mocked checks made no provider inference and do not establish live auth or recorder readiness.

## 0.2.0

Add Claude Toolkit as a standalone provider toolkit.

Expose provider-specific setup, CLI operation and task-fit guidance while keeping account data, credentials, machine paths and runtime state recipient-owned.

Initial public edition of Claude Toolkit. The package is CLI-first where a supported provider CLI exists, records readiness separately from successful inference, and includes recipient onboarding. Private account identifiers, host paths, model receipts and local state are excluded.

Compatibility: New standalone package; no existing package identifiers, hooks or runtime contracts are removed. Provider services and local operating-system capabilities remain external prerequisites.

Upgrade: Install this package, follow its recipient onboarding, configure the provider or host runtime yourself, then run its bounded readiness and task-fit checks before delegation.

Validation: Canonical source copied into the reviewed public checkout; portable and compatibility manifests checked; complete public file inventory generated; account, credential and machine-path scan returned no matches. Publication remains queued for the existing release workflow.

## 0.1.0

Initial provider toolkit with CLI-first operation, conditional interface alternatives, task-fit checks and recipient setup. Host credentials, private receipts and model downloads are excluded.
