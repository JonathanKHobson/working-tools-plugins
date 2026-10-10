# Conform Video Delivery: Domain Model

## Purpose

Create verified delivery variants from a high-quality master without treating stale platform presets or one-size-fits-all crops as truth.

## Inputs

- Approved user intent and conversation context.
- Immutable source inventory and hashes.
- The current project manifest plus any analysis evidence.
- Current delivery, accessibility, rights, and toolchain constraints.

## Core artifacts

- `delivery-matrix.md` — a durable handoff artifact.
- `variants/` — a durable handoff artifact.
- `captions/` — a durable handoff artifact.
- `posters/` — a durable handoff artifact.
- `delivery-manifest.json` — a durable handoff artifact.
- `checksums.sha256` — a durable handoff artifact.

## Decision boundary

This skill owns conform video delivery decisions. It does not silently take ownership of neighboring stages. Route to the neighboring skills named in `SKILL.md` when the primary problem changes.

## Evidence hierarchy

1. Direct source media and measured metadata.
2. User-provided intent, constraints, and feedback.
3. Cached transcript/scene/music/layout/QA evidence tied to the source hash.
4. Project-specific design system and prior approved renders.
5. General heuristics, clearly labeled as defaults rather than facts.

## Provenance model

Every generated or acquired asset should record stable ID, path, content hash, creator/provider, source URL or prompt, creation/acquisition date, license/rights status, model/tool/version, and parent inputs. A missing rights field is an unresolved production risk, not an empty administrative detail.
