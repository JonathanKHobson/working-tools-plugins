# 07 — Documentation, UX, and Information Architecture Guide

## Goal

Organize project knowledge so future humans and agents do not have to rediscover the project from scratch.

## Documentation categories

Diátaxis separates documentation into four needs: tutorials, how-to guides, reference, and explanation. [S27](source-index.md)

Use that distinction:

```text
docs/
  tutorials/
  how-to/
  reference/
  explanation/
```

For most small projects, a lighter version works:

```text
docs/
  project-map.md
  roadmap.md
  how-to/
  reference/
  architecture/
    adr/
```

## Project map

The project map is the most important doc for agent maintainability.

It should say:

- current project phase,
- north-star vision,
- directory map,
- where to add new things,
- what not to edit manually,
- current known risks/debt,
- test/run commands,
- open expansion slots.

## ADRs

Lightweight Architecture Decision Records capture important architecture decisions with context and consequences. [S28](source-index.md)

Use an ADR when deciding:

- app architecture,
- framework/engine,
- folder structure,
- database schema approach,
- state management,
- asset pipeline,
- deployment model,
- plugin architecture,
- design system/token strategy.

MADR provides a structured markdown approach for architectural decision records. [S29](source-index.md)

## Work breakdown structure

PMI describes a Work Breakdown Structure as a product-oriented hierarchy that organizes and defines total project scope. [S25](source-index.md)

For agents, use WBS thinking to avoid "everything in one file":

```text
Game
  Core loop
  Player
  Enemies
  Levels
  UI
  Audio
  Save system
```

Each major deliverable should have a file/folder home.

## Technical data management

NASA frames technical data management as planning for acquiring, accessing, managing, protecting, and using technical data through the system life cycle. [S26](source-index.md)

For normal software projects, translate that to:

- store decisions intentionally,
- protect sensitive info,
- document how artifacts are generated,
- preserve important research/requirements,
- keep lifecycle docs discoverable.

## UX/design projects

Design systems include components, patterns, styles, and guidelines; they should be shaped by project scale and replicability. [S33](source-index.md)

For UX work:

```text
ux/
  research/
    interviews/
    surveys/
    synthesis/
  personas/
  journeys/
  flows/
  wireframes/
  prototypes/
  usability-testing/
  content/
  design-system/
    tokens/
    components/
    patterns/
    guidelines/
```

## Tokens and variables

Design tokens are small reusable design decisions; Figma variables store reusable values and support design systems/prototyping. [S34, S35, S36](source-index.md)

Organize tokens separately from one-off styling:

```text
design-system/
  tokens/
    color.md
    typography.md
    spacing.md
    motion.md
  components/
  patterns/
  content-guidelines.md
```

## UX-to-code bridge

When a project has both UX and implementation:

```text
docs/
  product/
    north-star.md
    requirements.md
  ux/
    research-summary.md
    flows.md
  design-system/
    tokens.md
  architecture/
    adr/
src/
  components/
  styles/
```

Rules:

- design decisions should not be buried only in code,
- code tokens and design tokens should map conceptually,
- research findings should inform roadmap/docs,
- design system components should have usage guidance.

## Documentation done checklist

- [ ] README explains project purpose and run/test commands.
- [ ] `docs/project-map.md` exists for expandable projects.
- [ ] ADRs capture structural decisions.
- [ ] UX research/design artifacts have their own homes.
- [ ] Design tokens/variables are separated from one-off styling.
- [ ] Roadmap/north-star vision is not mixed into implementation files.
- [ ] Docs are short enough for agents to use.
