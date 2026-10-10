---
name: creative-project-context
description: Create, inspect, validate, and maintain plain-text creative project scaffolds for books, stories, TTRPG campaigns, board/card games, game concepts, publishing projects, canon, provenance, milestones, decisions, feedback, playtests, builds, releases, backups, and archives.
---

# Creative Project Context

Use this skill when a creative project needs a durable source of truth before drafting, revising, publishing, playtesting, or integrating with apps. The default model is inspectable Markdown, YAML, and JSONL. It must work without Scrivener, Obsidian, Foundry, Zotero, or a vector database.

## When To Use

- Start or normalize a creative project.
- Create `creative-project.yaml`, canon folders, provenance ledgers, decision logs, feedback logs, playtest logs, build/release logs, or archive notes.
- Audit whether a creative project has enough context for story, publishing, TTRPG, or board/card work.
- Check project boundaries before a skill writes or exports anything.
- Prepare a project for future MCP/app integration without enabling that integration.

## Canonical Model

Every project should make these inspectable:

- Identity: title, type, owners, collaborators, audience, format, status, privacy class, canonical source.
- Brief: intent, promise, constraints, anti-goals, definition of done.
- Canon: entities, relationships, timeline, locations, objects, factions, systems, knowledge state.
- Voice: style examples, anti-flattening rules, deliberate quirks, dialect/register notes.
- Sources: claims, quotations, uncertainty, citations, transformations.
- Rights: influences, licenses, permissions, attribution, trademarks, platform terms, generated-media provenance.
- Boundaries: privacy, consent, safety, accessibility, redaction rules.
- Operations: milestones, WIP, decisions, assumptions, questions, risks, issues.
- Evidence: feedback, playtests, builds, exports, release hashes, archives, restore tests.

## Default Folders

```text
creative-project.yaml
brief.md
canon/
drafts/
research/
feedback/
provenance/
playtests/
builds/
releases/
logs/
tests/
archive/
```

For story projects, `story-book-router` may add a Story Skills-inspired story bible shape with `characters/`, `worldbuilding/`, `plot/`, `scenes/`, `chapters/`, and `continuity/`.

## Local Scripts

Resolve scripts relative to this skill folder:

- `scripts/create_creative_project.py`: create a small plain-text scaffold.
- `scripts/check_creative_project.py`: validate required files, privacy/rights fields, TODOs, and obvious secret patterns.

Examples:

```shell
python3 scripts/create_creative_project.py --root /path/to/projects --title "Project Title" --type book --privacy confidential
python3 scripts/check_creative_project.py /path/to/projects/project-title
```

Do not run these scripts against private or licensed roots unless the user has approved that root for the current task.

## Workflow

1. Identify project type, privacy class, canonical source, and desired operation.
2. Inspect existing files before creating anything.
3. If a scaffold is missing and the user asked to create one, generate the smallest local scaffold that preserves future growth.
4. Add or update ledgers rather than burying decisions in chat:
   - `logs/decisions.jsonl`
   - `logs/assumptions.jsonl`
   - `logs/questions.jsonl`
   - `provenance/provenance-ledger.jsonl`
   - `releases/release-ledger.jsonl`
5. Run the local check script after creation or meaningful edits.

## Guardrails

- Do not migrate, restructure, delete, overwrite, or import an existing manuscript/campaign/world without explicit approval.
- Do not write player safety notes, private feedback, journals, licensed text, credentials, or paid platform details into general ledgers.
- Do not turn KSB or another memory store into the canonical source. Durable memory can point to the project; the project remains the source of truth.
- Do not enable live app, VTT, browser, publication, or vector-store MCPs from this skill.

## Output Contract

```markdown
## Project Context
- Root:
- Type:
- Privacy/rights:
- Canonical source:

## Changes

## Checks

## Open Questions

## Next Safe Action
```

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Producer, TTRPG Game Master. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
