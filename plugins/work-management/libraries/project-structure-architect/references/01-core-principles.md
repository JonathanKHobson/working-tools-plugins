# 01 — Core Principles

## 1. Expansion-first, not architecture-first

Prepare for future expansion without burying the project in speculative architecture.

Good expansion-first structure:

- creates obvious homes for future work,
- keeps entry files thin,
- separates unrelated reasons to change,
- documents the project map,
- avoids needless abstractions.

Bad architecture-first structure:

- creates dozens of empty folders,
- invents patterns before there is a problem,
- hides simple work behind indirection,
- optimizes for "looking professional" rather than being editable.

## 2. Edit locality

A good structure makes likely future edits local.

Ask:

- Where would I change player movement?
- Where would I add a new enemy?
- Where would I edit HUD text?
- Where would I add a second page?
- Where would I change database schema?
- Where would I update design tokens?
- Where would I add onboarding docs?

If the answer is "search the 5,000-line file," the structure failed.

## 3. Thin entry points

Entry files should compose and initialize.

Examples:

- `main.js` starts the app/game and hands off.
- `index.html` hosts the page but does not contain the entire long-term app.
- `App.tsx` routes/composes, not every component and business rule.
- `Game.js` coordinates systems, not every entity behavior.
- `server.ts` wires middleware/routes, not every route implementation.

## 4. One reason to change

Group things that change together. Separate things that change for different reasons.

Examples:

- Player controls and HUD rendering should not live in the same function.
- CSS tokens and component-specific CSS should not be mixed randomly.
- Database migration files should not be mixed with runtime query helpers.
- UX research notes should not be mixed with implementation TODOs.

## 5. Names are navigation

Names should answer "what is this?" without opening the file.

Use:

- stable domain words,
- clear suffixes/prefixes where useful,
- consistent casing per platform/language,
- predictable folder names.

Avoid:

- `misc`,
- `stuff`,
- `new_new_final`,
- ambiguous duplicate names,
- over-clever abstractions like `EngineThing` or `Manager2`.

## 6. Framework conventions come first

Do not fight the framework or engine. Framework conventions reduce surprise.

Then adapt:

- React can group by feature or file type.
- Next.js has routing conventions and private folders.
- Vite has source assets and `public/` assets.
- Unity/Godot/Unreal each have engine-specific directories/naming rules.
- Python installable packages often benefit from `src/` layout.

## 7. Documentation is part of the structure

Documentation should help future agents and humans avoid re-reading the whole project.

Minimum docs for expandable projects:

- `README.md`
- `docs/project-map.md`

Add when needed:

- `docs/roadmap.md`
- `docs/architecture/adr/`
- `docs/how-to/`
- `docs/reference/`
- `docs/research/`
- `docs/data/`

## 8. Generated files are not source

Generated, cached, vendored, build, and binary-heavy files need clear separation.

Examples:

- `dist/`, `build/`, `.next/`, `coverage/`, `node_modules/`
- Unreal `DerivedDataCache/`, `Intermediate/`, `Saved/`
- Unity `Library/`, temporary build directories
- database dumps and large model files

Use `.gitignore` and Git LFS where appropriate.

## 9. Small moves beat big-bang refactors

When refactoring:

1. Split one concern.
2. Update imports.
3. Run checks.
4. Confirm behavior.
5. Repeat.

Structure-only changes should avoid behavior changes unless necessary.

## 10. The project map is the agent memory anchor

A `docs/project-map.md` should explain:

- what each directory does,
- where to add new features,
- what not to edit manually,
- where assets/data/docs live,
- current phase vs north-star direction,
- known planned modules.
