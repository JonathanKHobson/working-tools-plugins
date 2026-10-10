# 00 — Research Brief: Low-Maintenance Project Organization

## Executive synthesis

The strongest cross-domain pattern is this:

> Organize by **future change**, not just by current output.

Across software repositories, web apps, game engines, databases, data-science projects, documentation systems, and design systems, the maintainable structures are the ones that make likely future edits obvious and localized.

This packet turns that into an agent rule:

> When a project is likely to grow, Codex should create an expansion-aware structure before implementation and avoid monolithic all-in-one files.

## What the research consistently supports

### 1. Durable guidance belongs in agent/repo instructions

Codex can use reusable guidance through `AGENTS.md` and skills. Official Codex guidance emphasizes reusable project instructions, concise skill descriptions, and support files for deeper guidance. [S01, S02, S03](source-index.md)

**Implication:** This organization guidance should be both a standalone skill and referenced from existing game, web, UX, app, plugin, and project-manager skills.

### 2. Repositories need a readable front door

GitHub describes README files as a way to explain why a project is useful, what people can do with it, and how to use it. [S04](source-index.md)

**Implication:** Every expandable project should get a `README.md`, and most should get `docs/project-map.md`.

### 3. Small, coherent changes reduce maintenance cost

Google engineering practices emphasize small, self-contained changes because they are easier to design, review, and maintain. [S08](source-index.md)

**Implication:** Agents should prefer staged setup/refactors over giant rewrites and should structure files so future changes can touch one area instead of scanning a massive file.

### 4. Framework conventions matter, but they are not enough

React does not mandate one file structure; common options include grouping by feature/route or by file type. Next.js supports colocation and private folders for separating UI logic from routing logic. Vite distinguishes `public/` assets from source-referenced assets. [S11, S12, S13](source-index.md)

**Implication:** Codex should follow framework conventions, then add project-specific organization where future edits need it.

### 5. Game projects need asset and system boundaries early

Unity says there is no single correct project structure, but teams should document naming conventions and folder structure. Godot recommends consistent case conventions. Unreal recommends establishing asset naming early for large projects. [S17, S18, S19](source-index.md)

**Implication:** Game skills should scaffold entities, systems, scenes, assets, config, and UI rather than placing everything inside `main.js`.

### 6. Databases need explicit structure, not hidden app logic

PostgreSQL schemas organize objects into logical groups and reduce collisions. Constraints and foreign keys protect relational integrity. Microsoft describes normalization as organizing tables/relationships to protect data and reduce redundancy. [S21, S22, S23](source-index.md)

**Implication:** Projects with persistence need `db/` folders, migrations, seed data, relationship docs, and explicit schema decisions.

### 7. Documentation should be separated by user need

Diátaxis separates documentation into tutorials, how-to guides, reference, and explanation. ADRs capture architectural decisions with context and consequences. [S27, S28, S29](source-index.md)

**Implication:** A project should not mix roadmap, reference, setup, and decision history into one confused doc. Use purpose-specific docs.

### 8. Design/UX systems scale through reusable decisions

Design systems rely on reusable components, patterns, styles, guidelines, variables, and tokens. [S33, S34, S35, S36](source-index.md)

**Implication:** UX-related skills should treat design tokens, components, research artifacts, prototypes, and content standards as organized project materials rather than scattered files.

## Core anti-patterns

- One giant `main.js` containing rendering, game loop, input, physics, UI, assets, levels, and entity logic.
- One HTML file for a website that is clearly going to become multi-page or app-like.
- CSS embedded everywhere with no style system or sections.
- Database tables created ad hoc in app code without migrations.
- Assets dumped into a single folder.
- Docs, decisions, and roadmap stored in one long "notes" file.
- Empty enterprise folders created with no near-term purpose.
- New project with no README, no map, and no obvious place for future work.
- Refactor that changes structure and behavior at the same time without staging.

## The balanced standard

This skill should **not** overcorrect into bureaucracy.

Use modular structure when it lowers future edit cost. Avoid building layers, abstractions, and folders that do not yet earn their keep.

The agent's decision should be based on:

1. Is this one-off or expandable?
2. Is there a north-star vision?
3. What parts are likely to change independently?
4. What framework or engine conventions apply?
5. What docs would make future editing cheaper?
6. What structure keeps the current slice easy to finish?
