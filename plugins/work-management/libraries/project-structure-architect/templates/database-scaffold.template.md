# Database Scaffold

```text
db/
  migrations/
    0001_initial_schema.sql
  schema/
    current.sql
  seeds/
    dev_seed.sql
  queries/
    users.sql
  docs/
    erd.md
    data-dictionary.md
```

## App integration

```text
src/
  data/
    repositories/
    mappers/
    validators/
  services/
```

## Notes

- Use migrations for schema evolution.
- Keep seeds separate.
- Document relationships.
- Do not bury schema decisions in app startup code.
