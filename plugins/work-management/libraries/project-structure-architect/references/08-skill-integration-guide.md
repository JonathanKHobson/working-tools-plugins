# 08 — Skill Integration Guide

## Goal

Make this skill available as a shared organizational policy across existing skills.

The user mentioned existing skills such as:

- Kyle's manager,
- game-related skills,
- game studio plugin,
- web app skills,
- Mac app skills,
- plugin skills,
- UX skills,
- database/data/project skills.

This guide explains how those should reference `project-structure-architect`.

## Why cross-reference instead of copying everything?

Official Codex skill guidance supports progressive disclosure: `SKILL.md` can be concise while supporting files live in `references/`, `scripts/`, `assets/`, and `agents/`. [S02](source-index.md)

Copying the entire organization policy into every skill would increase token cost and create drift. Instead:

- keep the deep policy here,
- add a short reference sentence in each existing skill,
- only duplicate a tiny decision rule if the skill frequently starts projects.

## Universal patch for existing skills

Add this to existing skill instructions:

```md
## Project organization guardrail

Before creating or expanding project files, consult the `project-structure-architect` skill. Do not create expandable games, apps, websites, plugins, UX systems, data systems, or repos as monolithic single-file implementations unless the user explicitly requests a one-off single-file deliverable.

When the user provides a north-star vision, roadmap, multi-phase goal, or future expansion hints, create a lightweight expansion-aware folder/file plan before implementation.
```

## Game skill patch

```md
## Game project structure guardrail

For browser/Three.js games, keep `src/main.js` thin. Separate core lifecycle, renderer, loop, scenes, entities, systems, UI/HUD, audio, config, assets, and docs. Use `project-structure-architect` before starting new game projects or refactoring monolithic game files.
```

## Web skill patch

```md
## Web structure guardrail

If the user explicitly requests a self-contained one-file HTML deliverable, single-file output is allowed. Otherwise, expandable websites/apps should separate HTML, CSS, JS, assets, components/features, docs, and tests according to framework conventions. Use `project-structure-architect` when starting or expanding the project.
```

## UX skill patch

```md
## UX organization guardrail

For UX/design-system work, organize research, synthesis, flows, wireframes, prototypes, content, design tokens, components, patterns, and guidelines into clear folders/docs. Use `project-structure-architect` when UX artifacts connect to implementation or future product expansion.
```

## Focus Ops Manager Patch

```md
## Project setup memory

When helping Kyle start, plan, or maintain a project, treat the first deliverable as a slice of a larger possible project unless he explicitly asks for a one-off artifact. Use `project-structure-architect` to propose expansion-aware folder/file structure, project-map docs, and staged refactor plans.
```

## Plugin/app skill patch

```md
## App/plugin structure guardrail

For app or plugin projects, separate entry points, commands/actions, UI, services, configuration, persistence, docs, tests, and assets. Do not store all plugin/app behavior in one file unless it is a tiny one-off proof of concept. Use `project-structure-architect` for setup and expansion planning.
```

## AGENTS.md companion

At repo root:

```md
# AGENTS.md

Before creating new project files or expanding features, use the `project-structure-architect` skill.

Do not create a monolithic single-file implementation unless the user explicitly asks for a one-off single-file deliverable. If the project is expected to grow, start with a lightweight folder/file structure and update `docs/project-map.md`.
```

## Skill dependency note

If your Codex/plugin packaging supports dependencies or explicit skill references, list this skill as a recommended companion for:

- game development,
- web app development,
- plugin development,
- UX/product work,
- project management,
- database/data work,
- repository refactoring.
