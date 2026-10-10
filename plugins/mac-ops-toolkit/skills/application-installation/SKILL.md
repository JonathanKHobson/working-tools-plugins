---
name: application-installation
description: "Choose placement and verify an authorized Mac application installation, including external-runtime and login-item dependencies."
---

# Application installation

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


Choose placement and verify an authorized Mac application installation, including external-runtime and login-item dependencies.

## Complete procedures to load

Select by the triggers below. Read the complete chosen procedure and its required support; skip unrelated variants. These links preserve the full methods.

- [Install targets](../mac-environment-conventions/references/install-targets.md) — When choosing where an app or runtime should live; concrete placement roots.
- [Symlink constraints](../mac-environment-conventions/references/symlink-rules.md) — Before adding or changing a redirect; native-path and consumer constraints.
- [Login race](../../references/recovery/login-item-launch-race.md) — When startup depends on an external mount or login item; launch-order diagnosis.
- For first-run setup under storage pressure or removal of developer components: [Managed components](../../references/recovery/storage-cleanup-and-migration.md#xcode-and-other-managed-components).

## Workflow

1. Verify source/release and route an unreviewed executable to Master Security before running it.
2. Choose the established app/runtime location and preserve macOS-managed paths. Follow the complete placement and mount rules.
3. Before first launch, account for setup downloads and offered optional components; omit unrelated downloads when capacity is constrained. Launch through the intended path and check window/function state; verify external dependency availability at launch.

## Deliver and verify

Report installed, launched and verified states separately. Do not silently grant OS permissions or add startup persistence.

## Example boundary

Good: verify a relocatable bundle through its intended native launch path. Bad: assume copying an app also validates its MCPs.

Use current host facts rather than assuming historical absolute paths apply elsewhere. Work Management owns task coordination; Master Security owns software/permission threat review. Existing authorization carries through routine reversible steps.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports IT Operations Specialist. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
