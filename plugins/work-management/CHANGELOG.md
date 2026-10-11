# Changelog

## 0.4.0

Finish authorized public updates with versioned publication and catalog deployment.

A local edit or Git push could previously finish without producing a versioned download or updating the public catalog. Plugin maintenance now routes completed public updates through the owning repository's executable release workflow.

- Adds the completed-update event and the catalog-only recovery command to the maintained plugin maintenance route.
- Requires instruction, reference and shared-template changes to participate in release detection.
- Preserves reviewed private exclusions, historical package bytes and independent product versions.
- Distinguishes prepared packages, GitHub publication and verified Site deployment so a partial failure can resume without another version.

Compatibility: Compatible optional completion workflow. Existing plugin and skill IDs, invocation names, installation layout and provider requirements remain unchanged. Publication still requires existing user authorization and repository access.

Upgrade: Install this version through the existing Codex or Claude marketplace route, or replace the prior plugin directory with this exact-version ZIP. Maintainers configure the release repository's private host adapter; end users need no publication setup.

Validation: Release completion helpers are covered by repository fixtures. The exact package inventory and supported manifest versions are checked before publication. This release does not assert that every plugin workflow or external provider was executed.

## 0.3.2

Unify fourteen complete methods, coordination helpers and licensed support. Make optional hooks and provider bindings explicit, preserve author-host configuration privately, and keep recipient defaults conditional on current user instructions.

## 0.3.1

Apply the Compass license model to this new edition of first-party contributions. Preserve all earlier grants and unchanged upstream notices. Add explicit file scopes, attribution and reserved-mark boundaries. Operative method, helper and runtime bodies are unchanged.

## 0.3.0

Retain complete standalone methods, references and helpers under their existing owner; replace originating private bindings with explicit recipient configuration. Existing procedures and versions remain independently recorded.

