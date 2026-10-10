# Existing Skill Patch Snippets

## Universal snippet

```md
## Project organization guardrail

Before creating or expanding project files, consult the `project-structure-architect` skill. Do not create expandable games, apps, websites, plugins, UX systems, data systems, or repos as monolithic single-file implementations unless the user explicitly requests a one-off single-file deliverable.

When the user provides a north-star vision, roadmap, multi-phase goal, or future expansion hints, create a lightweight expansion-aware folder/file plan before implementation.
```

## Game skill snippet

```md
For browser/Three.js games, keep `src/main.js` thin. Separate core lifecycle, renderer, loop, scenes, entities, systems, UI/HUD, audio, config, assets, and docs. Use `project-structure-architect` before starting new game projects or refactoring monolithic game files.
```

## Web skill snippet

```md
If the user explicitly requests a self-contained one-file HTML deliverable, single-file output is allowed. Otherwise, expandable websites/apps should separate HTML, CSS, JS, assets, components/features, docs, and tests according to framework conventions. Use `project-structure-architect` when starting or expanding the project.
```

## UX skill snippet

```md
For UX/design-system work, organize research, synthesis, flows, wireframes, prototypes, content, design tokens, components, patterns, and guidelines into clear folders/docs. Use `project-structure-architect` when UX artifacts connect to implementation or future product expansion.
```

## Focus Ops Manager Snippet

```md
When helping Kyle start, plan, or maintain a project, treat the first deliverable as a slice of a larger possible project unless he explicitly asks for a one-off artifact. Use `project-structure-architect` to propose expansion-aware folder/file structure, project-map docs, and staged refactor plans.
```
