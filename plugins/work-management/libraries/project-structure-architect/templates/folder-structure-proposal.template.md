# Folder Structure Proposal

## Classification

- [ ] One-off artifact
- [ ] Prototype likely to grow
- [ ] Expandable project
- [ ] Existing monolith refactor
- [ ] Multi-project/monorepo

## Reasoning

Why this structure fits the user request:

- `<reason>`

## Proposed structure

```text
project/
  README.md
  src/
  docs/
```

## Responsibility boundaries

| Area | Responsibility | Why separate? |
|---|---|---|
| `src/main.*` | Entry/bootstrap | Keeps startup thin |
| `src/config/` | Constants/settings | Makes tuning easy |
| `docs/project-map.md` | Structure guide | Reduces future rediscovery |

## Single-file exception?

- [ ] Yes — user explicitly requested a self-contained deliverable.
- [ ] No — project is expected to grow.

## Implementation stages

1. Create scaffold.
2. Implement current slice.
3. Add docs.
4. Run checks.
5. Summarize where future changes go.
