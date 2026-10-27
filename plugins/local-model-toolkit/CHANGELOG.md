# Changelog

## 0.2.1

2026-10-27 release review: Document tested host adapters and opt-in usage recording for bounded local tasks.

2026-10-27 release review: Reuse verified host operation without reconstructing the lifecycle for every task.

2026-10-27 release review: Prefer a tested host-provided default adapter when available; resolve its private command through the host capability record and use opt-in metadata tracking through the adapter. Retain the existing raw lifecycle for hosts without that adapter.

Compatibility: 2026-10-27 release review: Documentation-only guidance; no bundled adapter, new default tracker, model call, polling or required configuration.

Upgrade: 2026-10-27 release review: Refresh the package. Hosts with a tested adapter can use their capability record; other hosts retain the existing CLI lifecycle.

Validation: 2026-10-27 release review: Read-only scoped local_sync.plan found one changed reviewed path and no conflicts. The reference diff was inspected; no model or recorder was executed.

## 0.2.0

Add recipient-agnostic local model operations and benchmark guidance.

Recipients need a bounded CLI-first method to measure local model usefulness without bundling weights or machine-specific setup.

Model weights, credentials, private receipts and host paths remain external.

Compatibility: Adds a new toolkit; existing packages are unaffected.

Upgrade: Install the toolkit and configure a supported local runner with recipient-selected models.

Validation: Catalog, source inventory, package build, privacy audit and full release tests.

## 0.1.0

Initial CLI-first local model toolkit with recipient onboarding, bounded model lifecycle, task-fit evaluation and comparative benchmark guidance.
