# Analyze Video Content: Domain Model

## Purpose

Create compact, queryable evidence that lets an agent reason about what is said and shown without exhaustively loading every frame.

## Inputs

- Approved user intent and conversation context.
- Immutable source inventory and hashes.
- The current project manifest plus any analysis evidence.
- Current delivery, accessibility, rights, and toolchain constraints.

## Core artifacts

- `transcripts/` — a durable handoff artifact.
- `scenes.json` — a durable handoff artifact.
- `contact-sheets/` — a durable handoff artifact.
- `timeline-views/` — a durable handoff artifact.
- `subjects.json` — a durable handoff artifact.
- `quality-flags.json` — a durable handoff artifact.
- `analysis-index.md` — a durable handoff artifact.

## Decision boundary

This skill owns analyze video content decisions. It does not silently take ownership of neighboring stages. Route to the neighboring skills named in `SKILL.md` when the primary problem changes.

## Evidence hierarchy

1. Direct source media and measured metadata.
2. User-provided intent, constraints, and feedback.
3. Cached transcript/scene/music/layout/QA evidence tied to the source hash.
4. Project-specific design system and prior approved renders.
5. General heuristics, clearly labeled as defaults rather than facts.

## Provenance model

Every generated or acquired asset should record stable ID, path, content hash, creator/provider, source URL or prompt, creation/acquisition date, license/rights status, model/tool/version, and parent inputs. A missing rights field is an unresolved production risk, not an empty administrative detail.
