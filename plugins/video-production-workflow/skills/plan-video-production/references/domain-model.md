# Plan Video Production: Domain Model

## Purpose

Turn an ambiguous request and available media into an approved production brief, acceptance criteria, beat sheet, and renderer-neutral project manifest.

## Inputs

- Approved user intent and conversation context.
- Immutable source inventory and hashes.
- The current project manifest plus any analysis evidence.
- Current delivery, accessibility, rights, and toolchain constraints.

## Core artifacts

- `creative-brief.md` — a durable handoff artifact.
- `asset-rights.csv` — a durable handoff artifact.
- `acceptance-criteria.md` — a durable handoff artifact.
- `beat-sheet.md` — a durable handoff artifact.
- `project.json` — a durable handoff artifact.

## Decision boundary

This skill owns plan video production decisions. It does not silently take ownership of neighboring stages. Route to the neighboring skills named in `SKILL.md` when the primary problem changes.

## Evidence hierarchy

1. Direct source media and measured metadata.
2. User-provided intent, constraints, and feedback.
3. Cached transcript/scene/music/layout/QA evidence tied to the source hash.
4. Project-specific design system and prior approved renders.
5. General heuristics, clearly labeled as defaults rather than facts.

## Provenance model

Every generated or acquired asset should record stable ID, path, content hash, creator/provider, source URL or prompt, creation/acquisition date, license/rights status, model/tool/version, and parent inputs. A missing rights field is an unresolved production risk, not an empty administrative detail.
