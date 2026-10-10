# 09 — Checklists

## New project setup checklist

- [ ] Classified deliverable as one-off, prototype, expandable project, existing monolith, or monorepo.
- [ ] If ambiguous, asked whether the user wants one-file or expandable structure.
- [ ] Created or proposed folder/file map before implementation.
- [ ] Created `README.md`.
- [ ] Created `docs/project-map.md` for expandable projects.
- [ ] Separated source, assets, docs, tests, config, and generated outputs.
- [ ] Kept entry files thin.
- [ ] Added `.gitignore` if repo/project.
- [ ] Documented run/test/check commands.
- [ ] Noted future expansion slots.

## Game checklist

- [ ] `main`/entry file is thin.
- [ ] Core lifecycle separated from rendering.
- [ ] Input, physics/collision, spawning, audio, UI/HUD, and entities are separated where present.
- [ ] Game constants/balancing values live in config/data.
- [ ] Assets are organized by type/use.
- [ ] Levels/scenes have clear homes.
- [ ] Project map explains where to add enemies, levels, controls, UI, audio, and assets.

## Web checklist

- [ ] Single-file exception justified or modular structure used.
- [ ] HTML, CSS, JS split for expandable projects.
- [ ] Components/features/pages organized.
- [ ] CSS has tokens/base/layout/components or equivalent.
- [ ] Assets separated into `public/` vs `src/assets/` where framework expects it.
- [ ] Framework conventions followed.
- [ ] README has run/build/test commands.

## Database checklist

- [ ] `db/migrations/` exists if schema changes are expected.
- [ ] Seeds separate from schema.
- [ ] Tables/entities documented.
- [ ] Relationships/foreign keys considered.
- [ ] Data files classified and sensitive data excluded.
- [ ] Denormalization documented.
- [ ] Queries/repositories separated from UI/business logic.

## Refactor checklist

- [ ] Identified mixed concerns.
- [ ] Wrote staged plan.
- [ ] Moved structure without behavior changes first.
- [ ] Updated imports.
- [ ] Ran tests/build/checks after each stage when available.
- [ ] Updated project map.
- [ ] Summarized changed files and rationale.

## Documentation checklist

- [ ] README is useful as front door.
- [ ] Project map explains directory roles.
- [ ] Roadmap/north-star exists if project is multi-phase.
- [ ] ADRs capture major structure decisions.
- [ ] UX/design artifacts have organized homes.
- [ ] Docs are not all dumped into a single giant notes file.

## Final response checklist for Codex

When done, Codex should tell the user:

- what structure was created/changed,
- why it was organized that way,
- what files are entry points,
- where future changes should go,
- what checks/tests ran,
- what remains uncertain or future work.
