# 02 — Decision Rules: Single File vs Modular Project

## The central decision

Before writing files, decide whether the user wants:

1. a one-off deliverable,
2. a tiny prototype,
3. an expandable project,
4. a refactor of an existing project.

Do not assume "small first version" means "single file forever."

## Decision tree

```text
Did the user explicitly request one self-contained file?
├─ Yes → single-file allowed.
│   └─ Add logical sections, comments, and mention modular option if future growth is likely.
└─ No
   ├─ Is this a game/app/site/plugin/database/project repo?
   │   ├─ Yes → create an expansion-aware scaffold.
   │   └─ No
   ├─ Did the user mention future features, north star, roadmap, phases, or expansion?
   │   ├─ Yes → create a stronger modular scaffold.
   │   └─ No
   ├─ Is this likely to exceed ~300–500 lines quickly?
   │   ├─ Yes → split now.
   │   └─ No → lightweight structure or single file with a clear split plan.
```

## When single-file is appropriate

Use single-file output when the user asks for:

- a pasteable HTML prototype,
- a quick mockup,
- a CodePen-style demo,
- a self-contained file to share,
- a small reproduction case,
- a one-shot script,
- a minimal snippet.

Even then, structure the file internally:

```html
<!-- Structure -->
<!-- Styles -->
<!-- Data -->
<!-- Logic -->
<!-- Initialization -->
```

## When modular structure is required

Use modular structure when:

- the user asks for a game, app, website, plugin, or tool,
- there is any mention of future expansion,
- a north-star vision exists,
- multiple systems/features are implied,
- editing a small thing later would otherwise require scanning a long file,
- a repo already exists,
- tests/build/deployment are expected,
- assets/data/database/design docs are involved.

## Minimal modular scaffold

For small but expandable work:

```text
project/
  README.md
  src/
    main.*
    config/
    utils/
  docs/
    project-map.md
```

Add only what the project needs.

## Moderate scaffold

For clear multi-feature projects:

```text
project/
  README.md
  package.json / pyproject.toml / project config
  src/
    main.*
    app/ or core/
    features/
    components/ or entities/
    systems/ or services/
    config/
    utils/
  assets/
  docs/
    project-map.md
    roadmap.md
  tests/
```

## Strong scaffold

For north-star projects, plugins, games, web apps, or multi-phase builds:

```text
project/
  README.md
  AGENTS.md
  docs/
    project-map.md
    roadmap.md
    architecture/
      adr/
    reference/
    research/
  src/
    core/
    features/
    components/ or entities/
    systems/ or services/
    data/
    config/
    utils/
  assets/
  tests/
  tools/
  scripts/
  db/                 # if persistence exists
  packages/ or apps/  # if monorepo/multi-project
```

## One clarifying question

Ask only when the distinction changes the deliverable:

> Should this be a single-file deliverable, or should I structure it as an expandable project?

Do not ask if the user clearly indicates expansion. Proceed modularly.

## Practical file-size guardrails

Use these as agent warnings:

| File size | Action |
|---:|---|
| <300 lines | Usually fine. |
| 300–500 lines | Check if it has mixed concerns. |
| 500–800 lines | Consider splitting by concern. |
| 800–1,500 lines | Refactor plan recommended unless there is a reason. |
| 1,500+ lines | Treat as likely monolith. |
| 5,000+ lines | High-priority refactor target unless generated/data-only. |

## Do not split blindly

A file can be large because it is generated, declarative data, a lookup table, or a single coherent reference. Do not split just to hit a number.

Split when a file has multiple reasons to change.
