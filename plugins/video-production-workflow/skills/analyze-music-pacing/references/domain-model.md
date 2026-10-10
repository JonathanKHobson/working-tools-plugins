# Analyze Music Pacing: Domain Model

## Purpose

Translate audio features into a confidence-aware pacing map and editorial cut windows without reducing music to a raw waveform or cutting every beat.

## Inputs

- Approved user intent and conversation context.
- Immutable source inventory and hashes.
- The current project manifest plus any analysis evidence.
- Current delivery, accessibility, rights, and toolchain constraints.

## Core artifacts

- `music-analysis.json` — a durable handoff artifact.
- `waveform.png` — a durable handoff artifact.
- `energy-envelope.csv` — a durable handoff artifact.
- `section-map.md` — a durable handoff artifact.
- `cut-windows.json` — a durable handoff artifact.
- `pacing-recommendation.md` — a durable handoff artifact.

## Decision boundary

This skill owns analyze music pacing decisions. It does not silently take ownership of neighboring stages. Route to the neighboring skills named in `SKILL.md` when the primary problem changes.

## Evidence hierarchy

1. Direct source media and measured metadata.
2. User-provided intent, constraints, and feedback.
3. Cached transcript/scene/music/layout/QA evidence tied to the source hash.
4. Project-specific design system and prior approved renders.
5. General heuristics, clearly labeled as defaults rather than facts.

## Provenance model

Every generated or acquired asset should record stable ID, path, content hash, creator/provider, source URL or prompt, creation/acquisition date, license/rights status, model/tool/version, and parent inputs. A missing rights field is an unresolved production risk, not an empty administrative detail.
