---
name: project-structure-architect
description: Choose or repair a maintainable file layout before creating expandable project files, adding features, or refactoring mixed responsibilities. Use existing conventions first; explicit one-off single-file artifacts do not need scaffolding.
---

# Project Structure Architect

Give the current deliverable an obvious home and make the next likely edit
local. Do not build architecture for hypothetical future features.

## Existing project

1. Identify the owning checkout and read its applicable instructions and
   `docs/project-map.md` if present. Similarly named mounted roots are not
   interchangeable. Inspect branch, dirty state and active writers before edits.
2. Follow the framework and repository's existing organization. Separate only
   responsibilities that already change independently or obscure behavior.
3. Preserve behavior in small moves. Check affected imports and the actual
   workflow; run relevant tests when code behavior or integration can change.
4. Update the existing map when paths, ownership, entrypoints, or runtime
   assumptions change. Avoid a second map or a parallel documentation system.

## New files or project

- An explicitly requested one-off file may stay self-contained.
- A prototype likely to grow needs a few real boundaries, not empty folders:
  entry/setup, domain behavior, presentation, and supporting assets/config as
  needed. Follow framework conventions rather than imposing one universal tree.
- Keep entry files focused on startup and composition. Do not put all UI,
  persistence, rules and assets in one expandable implementation file.
- For an expandable project, create a short `docs/project-map.md`: purpose,
  entrypoints, important folders, data flow, safe verification command, and
  where the next likely change belongs. Add a README only if needed to run it.
- Keep generated output, caches and third-party assets distinct from source.
  Document required mounts, localhost servers or external services explicitly.

## Decide whether a split earns its cost

A useful module hides real complexity behind a small interface. Prefer a
feature change in one obvious area to a web of tiny forwarding modules.
Length is a review signal, not an automatic split rule. Do not create adapters
for one hypothetical integration or a multi-file change packet when a short
checklist is enough.

For a large refactor, identify the risky workflow, preserve a recoverable
snapshot, and sequence behavior-preserving changes. Add an architecture
decision only for a consequential boundary or tradeoff. A static project map
comes before an interactive codebase graph unless the graph answers a specific
unresolved question.

For skills/plugins, use `skill-authoring`: keep discovery and shared constraints
in `SKILL.md`, conditional detail in references, and deterministic work in
scripts. For a creative project with unclear ownership, use
`creative-project-router`. Load domain instructions only when the deliverable
requires them.

Done means the current slice works, its home is clear, and affected checks pass.
Report the result and evidence, not the amount of structure created.
