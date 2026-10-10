# 06 — Database and Data Organization Guide

## Goal

Make data decisions explicit, versioned, and findable.

## Default project database scaffold

```text
db/
  migrations/
  schema/
  seeds/
  queries/
  docs/
    erd.md
    data-dictionary.md
```

For app-specific projects:

```text
src/
  data/
    repositories/
    services/
    mappers/
db/
  migrations/
  seeds/
  docs/
```

## Migrations

Use migrations for schema changes.

```text
db/migrations/
  0001_initial_schema.sql
  0002_add_user_profiles.sql
  0003_add_game_save_slots.sql
```

Rules:

- migrations should be ordered,
- each migration should be purposeful,
- avoid hiding schema changes in app startup code,
- document destructive migrations,
- keep seed/demo data separate.

## Schemas/namespaces

PostgreSQL schemas can organize database objects into logical groups, reduce collisions, and support multiple users/third-party applications in one database. [S21](source-index.md)

Use schemas when boundaries are meaningful:

```sql
CREATE SCHEMA game;
CREATE SCHEMA analytics;
CREATE SCHEMA auth;
```

Avoid schemas when they add complexity without real ownership or domain separation.

## Normalization and relationships

Microsoft describes normalization as organizing data into tables and relationships to protect data, improve flexibility, and reduce redundancy/inconsistent dependency. [S23](source-index.md)

PostgreSQL constraints and foreign keys protect relational integrity; many-to-many relationships need a linking structure. [S22](source-index.md)

Agent rule:

- design relationships explicitly,
- do not use a giant catch-all table unless it is intentional,
- document denormalization,
- name constraints/indexes when useful,
- keep database docs with the project.

## Data science / research projects

For data-heavy projects, use a data project structure:

```text
project/
  data/
    raw/
    interim/
    processed/
    external/
  docs/
  models/
  notebooks/
  reports/
    figures/
  src/
  references/
```

Cookiecutter Data Science promotes logical, flexible, standardized structures for data-science work. [S24](source-index.md)

## Data files

Do not casually commit large or sensitive data.

Classify data:

| Type | Location | Git? |
|---|---|---|
| Tiny sample data | `data/samples/` | Usually yes |
| Raw source data | `data/raw/` | Maybe no |
| Processed output | `data/processed/` | Maybe no |
| Generated reports | `reports/` | Sometimes |
| Secrets/credentials | never in repo | No |
| Large models/assets | external storage or LFS | Usually not normal Git |

## Data dictionary template

```md
# Data Dictionary

## Table: users

| Column | Type | Required | Description | Notes |
|---|---|---:|---|---|
| id | uuid | yes | Primary key | generated |
| email | text | yes | User email | unique |

## Relationships

- `profiles.user_id` → `users.id`
```

## Database done checklist

- [ ] Schema changes are migration-based.
- [ ] Seeds are separate from schema.
- [ ] Relationships are documented.
- [ ] Constraints/foreign keys are considered.
- [ ] Data files are classified.
- [ ] Large/sensitive data is not committed casually.
- [ ] Denormalization decisions are documented.
- [ ] `db/docs/` explains tables, relationships, and important queries.
