# Edit Dialogue Footage: Domain Model

## Purpose

Create a coherent dialogue edit that preserves meaning and performance while removing errors, choosing strong takes, smoothing audio, and supporting the story visually.

## Inputs

- Approved user intent and conversation context.
- Immutable source inventory and hashes.
- The current project manifest plus any analysis evidence.
- Current delivery, accessibility, rights, and toolchain constraints.

## Core artifacts

- `takes-packed.md` — a durable handoff artifact.
- `editorial-brief.md` — a durable handoff artifact.
- `edl.json` — a durable handoff artifact.
- `broll-plan.md` — a durable handoff artifact.
- `room-tone.wav` — a durable handoff artifact.
- `captions.srt` — a durable handoff artifact.
- `preview.mp4` — a durable handoff artifact.

## Decision boundary

This skill owns edit dialogue footage decisions. It does not silently take ownership of neighboring stages. Route to the neighboring skills named in `SKILL.md` when the primary problem changes.

## Evidence hierarchy

1. Direct source media and measured metadata.
2. User-provided intent, constraints, and feedback.
3. Cached transcript/scene/music/layout/QA evidence tied to the source hash.
4. Project-specific design system and prior approved renders.
5. General heuristics, clearly labeled as defaults rather than facts.

## Provenance model

Every generated or acquired asset should record stable ID, path, content hash, creator/provider, source URL or prompt, creation/acquisition date, license/rights status, model/tool/version, and parent inputs. A missing rights field is an unresolved production risk, not an empty administrative detail.
