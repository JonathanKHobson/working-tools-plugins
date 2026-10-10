# Project structure reviewer lenses

Read only the lens relevant to a substantial structure decision. These preserve the useful checks from the legacy project-structure agent briefs without requiring separate agents or reports.

## Initial or revised layout

Inspect the goal, existing tree, framework conventions, large or mixed-purpose files, data/assets/docs, and build/test commands. Classify the work as one-off, prototype, expandable project, monolith refactor, or monorepo. Propose only the current slice's folder/file ownership, with a reason tied to edit locality, files to create or move, material risks, and a done check. Keep entrypoints thin, avoid speculative layers, and update the concise project map when structure changes.

## Behavior-preserving refactor

Inspect mixed concerns, global state, import/export boundaries, available tests, and risky behavior. Make an extraction map, then stage small structure moves apart from behavior changes. Identify the first low-risk patch, a verification check for each meaningful stage, and a recoverable rollback point. Update docs after the structure is real.

## Repository hygiene

Check whether README and project-map guidance help the next editor find the entrypoint and safe commands. Review `.gitignore`, generated/build/cache files, large assets or data, documentation layout, and ownership or branch rules when relevant. Return the few quick wins that prevent a concrete maintenance problem; avoid a generic cleanup backlog.

## Data layer

Inspect schema creation and mutation in app code, migrations, seeds/demo data, queries/repositories, data documentation, and sensitive or large files. Keep schema, migrations, seeds, queries, and data notes distinguishable where the project actually needs them. Name relationship documentation and data-safety gaps that affect this change; do not prescribe a `db/` tree for an app that has no data layer.
