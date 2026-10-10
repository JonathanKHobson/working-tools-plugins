# Refactor Plan: Split Monolithic File

## Target

`<path/to/large-file>`

## Problem

- Current size: `<lines>`
- Mixed concerns:
  - `<concern>`
  - `<concern>`

## Goals

- Preserve behavior.
- Improve edit locality.
- Keep entry point thin.
- Update project docs.

## Proposed extraction map

| Concern | New file/folder | Notes |
|---|---|---|
| Bootstrap | `src/main.*` | Entry only |
| Config/constants | `src/config/` | |
| UI | `src/ui/` | |
| Domain/game systems | `src/systems/` | |
| Entities/components | `src/entities/` or `src/components/` | |

## Stages

1. Create folders and empty files.
2. Move constants/config.
3. Move pure utility functions.
4. Move independent systems/components.
5. Move UI/presentation.
6. Thin entry file.
7. Update imports.
8. Run tests/build/manual smoke test.
9. Update `docs/project-map.md`.

## Safety checks

- [ ] No behavior changes in stage 1.
- [ ] Imports updated after each move.
- [ ] Build/test command run.
- [ ] Manual smoke test described.
