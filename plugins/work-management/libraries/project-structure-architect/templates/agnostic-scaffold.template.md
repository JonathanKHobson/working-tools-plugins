# Generic Expandable Project Scaffold

```text
project/
  README.md
  AGENTS.md                    # optional, for repo-level agent rules
  docs/
    project-map.md
    roadmap.md
    architecture/
      adr/
    research/
    reference/
  src/
    main.*
    core/
    features/
    services/
    data/
    config/
    utils/
  assets/
  tests/
  scripts/
  tools/
  db/                          # if persistence exists
    migrations/
    seeds/
    docs/
```

## Use this when

- the project type is not yet specific,
- future expansion is likely,
- the user provided a north-star vision,
- multiple concerns will grow independently.
