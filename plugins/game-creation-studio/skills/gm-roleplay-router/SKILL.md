---
name: gm-roleplay-router
description: Route live and prep-heavy TTRPG/GM work across roleplay, Story Atlas, rules teaching, table facilitation, safety, Daggerheart adapters, canon updates, and post-session debriefs to the smallest safe specialist set.
---

# GM Roleplay Router

Use this skill when a tabletop RPG request spans GM prep, live table direction,
roleplay coaching, Story Atlas work, rules teaching, player facilitation,
safety/accessibility, public-GM operations, or post-session canon maintenance.

## Route First

Classify:

- mode: `prep`, `live`, `teach`, `coach`, `write`, `debrief`, or `audit`
- urgency: `live-now`, `between-scenes`, `post-session`, or `planning`
- audience: `player-facing`, `GM-only`, or `mixed`
- privacy: `public`, `table-private`, `GM-private`, or `sensitive`
- system adapter: system-neutral by default, Daggerheart only when current
  official published SRD source status is known
- write permission: read-only unless the user explicitly approves a local patch or
  live tool mutation

In `live-now` mode, skip route narration and return the live card through
`live-table-director`. Use one reversible assumption instead of stopping play
for missing context.

Outside live play, name the chosen specialist and why it fits in one sentence
when that choice affects the deliverable. Skip a tour of the other skills.

## Specialist Handoff

- Use `live-table-director` for immediate table moves, scene cuts, spotlight,
  pacing, and exact GM words.
- Use `show-vs-tell-craft` for read-aloud text, live "show it at the table"
  cues, NPC/location/faction/item descriptions, clues, and GM sidebars.
- Use `story-atlas-prep` for Story Atlas preparation, scene compilation,
  player-safe/GM-only separation, and run-mode indexes.
- Use `improv-roleplay-coach` for practical roleplay exercises and low-pressure
  participation modes.
- Use `player-facilitator` for spotlight, collaboration, table conduct, and
  observable participation signals.
- Use `npc-performance-director` for memorable NPCs, performance handles,
  information tiers, and exit conditions.
- Use `pacing-scene-director` for scene cuts, clocks, clue movement, escalation,
  and finale protection.
- Use `rules-teaching-coach` for concise in-play rules teaching and ruling
  status labels.
- Use `safety-accessibility-facilitator` for consent, live edits, access needs,
  private check-ins, and dignified participation.
- Use `professional-public-gm` for paid/public tables, venue preflight, opening
  scripts, conduct ladders, and service recovery.
- Use `debrief-canon-maintainer` for actual-play recaps, canon patches,
  feedback themes, rulings, and next-session hypotheses.
- Use `daggerheart-adapter` only when Daggerheart current official SRD source status
  matters.
- Use `personal-gm-style-adapter` as a removable style layer after factual, source, safety,
  and agency constraints.
- Use `ttrpg-router` for campaign/adventure prep, system-neutral design,
  safety, handouts, rules citation, recaps, and canon boundaries.
- Use `creative-project-context` for Story Atlas, canon logs, session records,
  source-of-truth scaffolds, and provenance-friendly project models.
- Use `story-architecture` for hooks, clue webs, factions, arcs, dramatic
  stakes, NPC relationships, and consequence design.
- Use `originality-rights-and-provenance` for licensed rules, third-party
  material, player privacy, attribution, and release permissions.
- Use `board-game-design` or `game-designer` when the work becomes system,
  mechanics, balance, probability, or playtest analysis.
- Use `communication-story-crafter`, `publishing-router`, or
  `visual-asset-integration` for public event pages, player packets, handouts,
  shareables, or media-backed table materials.

## Live Retrieval Budget

Never load the full field guide during live play. Load only:

- current scene/run-state summary
- one relevant technique or reference card
- one system/rules card when needed
- one private safety/access note only when the user explicitly asks and the
  output remains GM-private

If a local MCP, compass, Story Atlas, or Knowledge Atlas adapter is unavailable,
say so briefly and use the Markdown fallback. Do not invent tool names or
schemas.

## Agency And Privacy

- Preserve player agency. Do not disguise forced outcomes as choices.
- Use observable participation signals rather than diagnosing or labeling
  players.
- Support third-person narration, brief answers, processing time, written
  responses, pass-and-return, and private check-ins.
- Separate established canon, actual-play updates, prep decisions, proposed
  lore, mysteries, contradictions, rulings, official rules, and uncertainty.
- Separate player-safe material from GM-only material and private safety/access
  notes.

## Output Contract

For planning or audit:

```markdown
## GM Route
- Mode:
- Urgency:
- Audience/privacy:
- System/source:
- Owning specialist:

## Immediate Output

## Source And Permission Notes

## Next Specialist
```

For live mode, return only the `live-table-director` card.

## References

- Read [the router map](references/router-map.md) when a request spans several
  specialists or the handoff boundary is unclear. A single obvious specialist
  does not need the full map.

## Packaged routes and receiving-host inputs

Read [the recipient binding and companion-method map](../../docs/standalone-workflow-bindings.md) when a named companion method or adapter is unavailable. All local game/GM methods are included under this package. Optional external services and unreleased companion methods require recipient-owned access; their absence does not authorize invented tool calls or private-source copying.
