---
name: ttrpg-router
description: "Design system-neutral tabletop RPG campaigns and table-ready material, including safety, rules and canon; separate player and GM content, with live VTT edits separately authorized."
---

# TTRPG Router

Use this skill for tabletop role-playing work: campaign design, adventure prep, session zero, GM improvisation, safety, recaps, consequences, canon updates, rules citations, and table-ready artifacts.

## Related Live GM Skills

- Use `gm-roleplay-router` when the request is multi-mode, live-table urgent,
  Story Atlas plus table facilitation, Daggerheart adapter work, public-GM
  operations, or post-session debrief routing.
- Use `live-table-director` when the GM needs one immediate under-140-word table
  intervention with exact speakable GM words, a signal to watch, a cut
  condition, and the next transition.
- Use `story-atlas-prep`, `pacing-scene-director`, `player-facilitator`,
  `npc-performance-director`, `rules-teaching-coach`,
  `safety-accessibility-facilitator`, `professional-public-gm`,
  `debrief-canon-maintainer`, `daggerheart-adapter`, or `personal-gm-style-adapter` when
  one of those narrower live/prep/debrief specialties owns the output.
- Use `show-vs-tell-craft` for boxed text, NPC reveals, factions, locations,
  clues, player-facing handouts, GM sidebars, and live description support.

## Core Boundaries

- Default to system-neutral methods unless the user names a ruleset and has rights to use the text.
- Do not ingest or reproduce commercial rulebooks, adventures, stat blocks, maps, art, or proprietary VTT content without explicit rights.
- Separate player-facing material from GM-only secrets.
- Treat player safety notes, feedback, contact details, and private table issues as sensitive.
- Do not mutate Foundry, Roll20, Obsidian, Kanka, VTTs, campaign managers, or live wikis without explicit scoped approval.

## Workflow

1. Identify system, edition, source rights, table tone, player count, session length, and prep target.
2. Classify the job:
   - campaign/adventure design
   - session zero/safety
   - session prep/run sheet
   - encounter/challenge design
   - NPC/faction/location design
   - recap/canon update
   - rules retrieval/citation
   - handout/player-facing artifact
3. Preserve agency:
   - create meaningful choices
   - support multiple outcomes
   - avoid single-solution bottlenecks
   - use clue redundancy for mysteries
4. Apply safety:
   - offer tools without coercion
   - allow consent to change
   - keep sensitive notes private and minimal
   - avoid using safety preferences as plot fodder
5. Update canon only from actual play, explicit prep decisions, or user-approved retcons.

## Coordination

- Use `creative-project-context` for campaign/project source-of-truth, canon
  logs, session records, milestones, backups, and inspectable local models.
- Use `story-architecture` for hooks, mysteries, factions, arcs, clues,
  setup/payoff, contradiction triage, and consequence design.
- Use `originality-rights-and-provenance` for licensed rules, third-party
  adventures, quotes, player privacy, attribution, and release permissions.
- Use `board-game-design` or `game-designer` when the task becomes system,
  mechanics, probability, balance, playtest, encounter economy, or game-loop
  design.
- Use `visual-asset-integration`, `communication-story-crafter`, or
  `publishing-router` for handouts, maps, campaign pages, public recaps,
  table-facing packets, and shareable artifacts.
- Use `show-vs-tell-craft` to split player-facing show-first prose from
  GM-only tell-clear notes. Do not make rules teaching, safety reminders, or
  table procedure poetic when direct telling is clearer.

## Table QA

- Is the hook clear?
- Do players have enough actionable information?
- Are at least three clue paths available where a clue is necessary?
- Are GM-only secrets separated?
- Does player-facing prose show concrete evidence without telling players what
  to feel, and do GM notes tell the table function plainly?
- Are rules citations edition/source-aware?
- Is accessibility addressed: sensory load, text size, color, pacing, breaks, online/offline constraints?
- Does the plan survive players choosing a different route?

## Output Contract

```markdown
## TTRPG Route
- System/source:
- Audience: player-facing / GM-only / mixed
- Safety/privacy:
- Session or artifact goal:

## Material

## Rules / Source Notes

## Canon Updates

## Table Risks
```

## Packaged routes and receiving-host inputs

Read [the recipient binding and companion-method map](../../docs/standalone-workflow-bindings.md) when a named companion method or adapter is unavailable. All local game/GM methods are included under this package. Optional external services and unreleased companion methods require recipient-owned access; their absence does not authorize invented tool calls or private-source copying.
