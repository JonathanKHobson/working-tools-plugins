# Packaging and Signing

## Project identity

- Keep bundle identifiers stable and environment-specific when needed.
- Align target names, schemes, and build configurations early.
- Avoid last-minute renames because they often break signing, provisioning, or helper targets.

## Targets and configurations

- Confirm the app target, test targets, helper targets, and extensions all have the correct signing context.
- Keep debug and release configuration differences intentional.
- Verify deployment targets across the app, packages, and embedded frameworks.

## Entitlements and sandbox

- Add only the entitlements the app actually needs.
- Treat sandbox access as a product constraint, not a technical afterthought.
- Prefer user-selected file access patterns for sandboxed apps.
- Re-check entitlements whenever file access, networking, notifications, or automation features are added.

## Distribution paths

### Direct download

- Use Developer ID signing.
- Enable hardened runtime unless a concrete dependency blocks it.
- Plan for notarization and stapling.
- Be explicit about any broader access model that differs from Mac App Store expectations.

### Mac App Store

- Use sandbox-compatible workflows.
- Expect tighter entitlement and behavior constraints.
- Avoid assuming unrestricted filesystem or background access.

## Notarization checklist

- Archive a release build from the correct scheme and configuration.
- Confirm signing identities are applied consistently.
- Verify hardened runtime for direct-download builds.
- Check entitlements before export.
- Submit the exported app for notarization.
- Staple the notarization ticket to the shipped artifact when required.
- Re-test launch, file access, and helper behavior on a clean machine when possible.

## Common failure modes

- bundle identifier mismatch between target and signing setup
- wrong signing identity for the intended distribution path
- helper target or embedded framework not signed consistently
- missing hardened runtime on direct-download builds
- incorrect or over-broad entitlements
- stale provisioning or account configuration in Xcode
- exported artifact differs from the build that was validated

## Packaging defaults

- Ask whether the app is for development, internal use, direct download, or the Mac App Store.
- Pick the simplest release path that matches the user’s target.
- Surface signing and notarization decisions early in implementation plans, not at release time.
