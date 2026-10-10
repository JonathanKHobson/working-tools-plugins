---
name: project-structure
description: Consult the owning architecture at the start of every new or continued project and when scope changes; choose or repair file boundaries only when the current work needs them. A requested one-off single-file artifact can stay single-file.
---

# Project Structure

When orientation helps, briefly name this skill’s outcome, needed input and expected result, then proceed. Broader help uses the [plugin introduction](../../README.md); skip maintainer notes unless needed.


Use this owner proactively for every new or continued project, including resuming an existing project. At the start, read the existing project map or applicable architecture instructions and locate the current change. Consult again when scope or ownership changes; do not reread guidance already in the current context. Consultation can confirm the existing layout without creating folders, a map, or a refactor. The older `project-structure-architect` name is a compatibility route to this owner.

Identify the owning checkout, branch, dirty state, applicable project instructions, and current conventions before editing. Similar mounted roots are not interchangeable. Find the existing entrypoints and project map; preserve the framework's organization. A useful module owns a responsibility that changes independently and exposes a small interface. Avoid folders, adapters, or layers for hypothetical growth.

**Storage on Kyle's Mac:** use the external **KyleSSD (`$PROJECT_VOLUME`) as primary project and bulk storage**. Put downloads, source media, renders, large datasets/models and substantial temporary production files in the owning project's organized folders there. Limit internal-SSD use to small working/configuration files or tool-required storage; keep any unavoidable internal scratch bounded and clean up task-owned copies after verifying the external result. Before a large write, resolve symlinks and verify the intended volume is mounted, writable and has room. A `<user-workspace>` workspace may already point to KyleSSD. If the SSD is unavailable, retain the queue and report the missing mount rather than silently downloading internally or creating an ordinary folder under `/Volumes`. Preserve existing source ownership and references; use Mac Ops storage-migration for an actual relocation instead of moving unrelated user files. On another host, verify its designated external root rather than copying this Mac's path.

For a Site with a new or updated downloadable package, keep page/render assets in the Site and apply the [download-hosting rule](../../references/operations/download-hosting.md) to substantial downloads. This is a delivery choice for the current artifact, not a request to migrate older files.

For a visual addition or change to an existing product, locate the related shipped screens and their source before setting a new direction. Pass the relevant component, token, type, layout and interaction conventions to the UX/design owner; a missing style document is not permission to invent a parallel system. If the related source or rendered artifact is inaccessible, state that evidence gap and proceed only with what can be checked. An explicit new visual direction can supersede the incumbent within the requested scope.

For a new expandable project, establish only boundaries the current deliverable uses: entry/setup, domain behavior, presentation, and assets or configuration as needed. Keep generated files and third-party assets distinct from source. For an existing project, split only where a current change is obscured or risky; move behavior in small steps and check imports and the affected path.

Maintain one concise `docs/project-map.md` for an expandable project: purpose, entrypoints, important folders, data flow, safe verification command, and where the next likely edit belongs. Update it when ownership or runtime assumptions change; do not build a second navigation system. A recoverable snapshot and staged moves matter for a large refactor. A one-off file may need no map.

For design artifacts and reusable visual templates, include or update a source-grounded `DESIGN.md` with the editable source. A template skill links it and the package builder retains its relative reference closure. UX Design Studio owns the detailed format and evidence method; Graphic Design owns graphic/print application. Use optional typography, colors, layouts, components and adaptation documents only where they add distinct value. Writing Templates owns the analogous `STYLE.md` entry backed by its authoritative guides. Keep build/maintenance instructions in `AGENTS.md` only when a repository needs them; do not add a duplicate persona to each template.

Use [structure decisions](../../references/structure-decisions.md) for a genuine boundary choice. Load the matching staged domain reference only when needed: [web/app](../../libraries/project-structure-architect/references/03-web-and-app-structures.md), [repository](../../libraries/project-structure-architect/references/05-repository-and-version-control.md), [data](../../libraries/project-structure-architect/references/06-database-and-data-organization.md), or [docs](../../libraries/project-structure-architect/references/07-docs-ux-information-architecture.md). The [templates](../../libraries/project-structure-architect/templates/project-map.template.md) and [scripts](../../libraries/project-structure-architect/scripts/README.md) are available for work that merits them. For skills/plugins, use the current skill-authoring owner; for creative projects, use their own router. Completion means the current slice works, its home is obvious, and the affected checks pass.

For a substantial structure review, read the conditional [reviewer lenses](references/reviewer-lenses.md) for initial layout, staged refactor, repository hygiene, or data-layer checks. They are checklists for the current owner, not a requirement to delegate or create four review artifacts.

For this workflow's full original method, **read and apply [project-structure-architect](../../libraries/project-structure-architect/SKILL.original.md)** when its trigger matches; follow its relevant support references. Preserve all applicable original steps and templates. Current user/host authorization and tool availability govern historical instructions, and existing narrowed routing remains the owner. Do not replace the loaded procedure with a synopsis.

When explaining a selected component using an existing graph or generated map, apply [graph-grounded explanation](references/graph-grounded-explanation.md): check project-scoped freshness, follow the selected neighborhood and verify actual source. Do not generate a graph for routine file-structure work.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Solutions Architect. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
