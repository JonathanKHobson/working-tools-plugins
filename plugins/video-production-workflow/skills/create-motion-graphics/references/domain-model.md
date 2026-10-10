# Create Motion Graphics: Domain Model

## Purpose

Select the simplest licensed renderer that fits each animation slot, author deterministic motion, render a normalized asset, and integrate it without coupling the editorial timeline to one engine.

## Inputs

- Approved user intent and conversation context.
- Immutable source inventory and hashes.
- The current project manifest plus any analysis evidence.
- Current delivery, accessibility, rights, and toolchain constraints.

## Core artifacts

- `animation-brief.md` — a durable handoff artifact.
- `renderer-decision.md` — a durable handoff artifact.
- `slot-source/` — a durable handoff artifact.
- `render.mov-or-webm` — a durable handoff artifact.
- `alpha-check.png` — a durable handoff artifact.
- `slot-qa.json` — a durable handoff artifact.

## Decision boundary

This skill owns create motion graphics decisions. It does not silently take ownership of neighboring stages. Route to the neighboring skills named in `SKILL.md` when the primary problem changes.

## Evidence hierarchy

1. Direct source media and measured metadata.
2. User-provided intent, constraints, and feedback.
3. Cached transcript/scene/music/layout/QA evidence tied to the source hash.
4. Project-specific design system and prior approved renders.
5. General heuristics, clearly labeled as defaults rather than facts.

## Provenance model

Every generated or acquired asset should record stable ID, path, content hash, creator/provider, source URL or prompt, creation/acquisition date, license/rights status, model/tool/version, and parent inputs. A missing rights field is an unresolved production risk, not an empty administrative detail.
