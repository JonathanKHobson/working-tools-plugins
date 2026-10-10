# 03 — Web, App, and Frontend Structure Guide

## Goal

Prevent expandable websites and apps from becoming one giant HTML/CSS/JS blob.

## Single HTML exception

A single HTML file is fine when the user explicitly requests a self-contained deliverable.

Examples:

- "Make me a one-file HTML prototype."
- "Give me a pasteable demo."
- "I need a shareable artifact."
- "Make a quick mockup I can save as HTML."

For these, keep internal sections clear:

```html
<!-- Metadata -->
<!-- Styles -->
<!-- Markup -->
<!-- Templates/Data -->
<!-- Scripts -->
<!-- Initialization -->
```

## Expandable web default

When the request implies a larger website/app, split structure:

```text
project/
  README.md
  index.html
  package.json
  src/
    main.js
    app/
      App.js
      router.js
    components/
      Header.js
      Button.js
    pages/
      HomePage.js
    styles/
      tokens.css
      base.css
      layout.css
      components/
    assets/
      images/
      icons/
    data/
    config/
    utils/
  docs/
    project-map.md
  tests/
```

## Vite-style browser app

```text
project/
  index.html
  package.json
  vite.config.js
  public/
    robots.txt
    favicon.svg
  src/
    main.js
    App.js
    assets/
    components/
    features/
    styles/
```

Use `public/` for files that must be served as-is or keep exact names. Use `src/assets/` for assets imported by source code. [S13](source-index.md)

## React structure options

React does not mandate one structure. Two common choices are feature grouping and file-type grouping. [S12](source-index.md)

### Feature grouping

Best when future edits are feature/domain-oriented.

```text
src/
  features/
    auth/
      LoginForm.tsx
      authApi.ts
      auth.test.ts
    dashboard/
      DashboardPage.tsx
      widgets/
  shared/
    components/
    hooks/
    utils/
```

### File-type grouping

Best for tiny apps or when framework conventions are simple.

```text
src/
  components/
  hooks/
  pages/
  services/
  styles/
  utils/
```

## Next.js notes

Follow Next.js routing rules first. Use private folders when helpful to separate UI logic from routing logic, keep organization consistent, and avoid future naming conflicts. [S11](source-index.md)

Example:

```text
src/
  app/
    page.tsx
    layout.tsx
    _components/
    _lib/
  components/
  lib/
  styles/
```

## CSS organization

MDN recommends organizing CSS into logical sections to make scanning and maintenance easier. [S10](source-index.md)

For expandable projects, do not bury all styling in random inline styles. Prefer:

```text
src/styles/
  tokens.css
  base.css
  layout.css
  utilities.css
  components/
    button.css
    card.css
```

For component-driven frameworks, colocated styles are fine when they improve edit locality:

```text
components/
  Button/
    Button.tsx
    Button.css
    Button.test.tsx
```

## App/service layers

For small apps, keep this light:

```text
src/
  components/
  services/
  data/
  config/
  utils/
```

For larger apps:

```text
src/
  app/
  features/
  shared/
  services/
  stores/
  api/
  config/
  styles/
```

## Monorepo/multi-app structure

Use when there are multiple apps/packages or shared design/code.

```text
repo/
  apps/
    web/
    docs/
    admin/
  packages/
    ui/
    config/
    utils/
  tools/
  docs/
  package.json
  pnpm-workspace.yaml
  turbo.json / nx.json
```

Turborepo commonly separates `apps/` and `packages/`; pnpm workspaces use `pnpm-workspace.yaml`; Nx supports intentional project/folder organization for evolving workspaces. [S14, S15, S16](source-index.md)

## Web done checklist

- [ ] Single-file vs expandable decision made.
- [ ] CSS/JS split unless single-file requested.
- [ ] Entry file is thin.
- [ ] Components/features have obvious homes.
- [ ] Assets are separated from source where appropriate.
- [ ] README explains how to run.
- [ ] `docs/project-map.md` explains where new features go.
- [ ] Tests/check commands documented or added.
