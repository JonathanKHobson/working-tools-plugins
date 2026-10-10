# 05 — Repository, Version Control, and Maintenance Guide

## Goal

A repository should be easy to understand, change, test, and recover.

## Required for expandable projects

```text
README.md
.gitignore
docs/project-map.md
```

Add when appropriate:

```text
AGENTS.md
CONTRIBUTING.md
CODEOWNERS
SECURITY.md
LICENSE
.github/
  workflows/
  pull_request_template.md
  ISSUE_TEMPLATE/
```

## README as front door

A README should answer:

- What is this project?
- Why does it exist?
- How do I run it?
- How do I test it?
- What are the important folders?
- What is the current phase?
- Where should future work go?

GitHub's README guidance frames the README as a way to explain project usefulness and usage. [S04](source-index.md)

## CODEOWNERS and branch protection

For team or multi-skill repos:

- use `CODEOWNERS` for critical directories,
- protect main branches,
- require reviews/status checks when appropriate.

GitHub supports CODEOWNERS review workflows and protected branch rules. [S05, S06](source-index.md)

## Repository size and large files

Keep source repos lean.

GitHub recommends repositories remain small, ideally under 1 GB and strongly under 5 GB. Individual Git objects are recommended under 1 MB and blocked at 100 MB; use Git LFS for large files. [S07](source-index.md)

This matters for games, media-heavy apps, generated builds, datasets, and AI/model projects.

## Change size

Small, coherent changes are easier to review and maintain. Google engineering practices emphasize small, self-contained changes for design quality, review speed, and lower blocking. [S08](source-index.md)

For agents:

- avoid giant all-at-once refactors,
- stage structural changes,
- run checks after each stage,
- summarize exactly what moved.

## Generated files

Do not mix generated outputs with source.

Common ignores:

```gitignore
node_modules/
dist/
build/
coverage/
.cache/
.DS_Store

# Vite/Next/etc.
.next/
.nuxt/
.svelte-kit/

# Unity
Library/
Temp/
Obj/
Build/
Builds/
Logs/
UserSettings/

# Unreal
Binaries/
DerivedDataCache/
Intermediate/
Saved/

# Python
__pycache__/
.pytest_cache/
.venv/
dist/
build/
*.egg-info/
```

## Monorepo structure

Use a monorepo when shared code/config and cross-project coordination outweigh the overhead.

```text
repo/
  apps/
    web/
    admin/
    game/
  packages/
    ui/
    config/
    utils/
  tools/
  docs/
  scripts/
```

Add boundaries:

- package-level README files,
- import rules,
- workspace config,
- separate tests per package,
- clear ownership.

## AGENTS.md integration

Codex reads `AGENTS.md` and related files before work. Use it to encode stable repo expectations such as layout, commands, conventions, constraints, and done criteria. [S01, S03](source-index.md)

Keep `AGENTS.md` concise. Link to deeper docs.

Example:

```md
# Agent Guidance

Before creating or expanding code, use the project-structure-architect skill.
Do not create monolithic app/game files unless the user explicitly asks for a one-file deliverable.

See:
- docs/project-map.md
- docs/architecture/adr/
```

## Repository hygiene checklist

- [ ] README exists and explains run/test commands.
- [ ] `.gitignore` covers generated outputs.
- [ ] Large media/data/build files are excluded or tracked with appropriate tooling.
- [ ] Entry points are thin.
- [ ] New features have obvious directories.
- [ ] Tests/checks are documented.
- [ ] Docs explain project structure.
- [ ] ADRs exist for major architecture decisions.
- [ ] Branch/CODEOWNERS rules are suggested for team settings.
