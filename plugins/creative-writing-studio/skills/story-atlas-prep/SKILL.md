---
name: story-atlas-prep
description: Compile story, module, campaign, and one-shot material into a durable Story Atlas with scenes, nodes, clocks, NPCs, clues, continuity, player-safe text, and GM-only material.
---

# Story Atlas Prep

Use this skill when TTRPG or story material needs to become an inspectable
Story Atlas, one-shot run sheet, scene graph, canon patch, or player-safe/GM-only
packet.

## Workflow

1. Inspect the current project context and any existing Story Atlas schema.
2. Extract promise, situation, actors, pressures, revelations, locations, clocks,
   finale, and alternate routes.
3. Build scene cards with purpose, timing, entry, exits, clues, compression,
   spotlight note, and failure-forward movement.
4. Separate established canon, actual-play updates, prep decisions, proposed
   Atlas lore, mysteries, contradictions, rulings, official rules, and
   unresolved uncertainty.
5. Separate player-safe text from GM-only material and private safety/access
   notes.
6. Emit reviewable Markdown/YAML/JSON patch sets when the real adapter is
   unavailable; do not mutate a live Story Atlas without approval.

For a mystery or investigation with required revelations or next steps, read the complete [clue-path audit](references/clue-path-audit.md) and selected original procedure. Check clue count, independent access routes, shared gates, orphan conclusions and dead ends before treating the scenario as robust. This does not impose a three-clue rule on optional lore or non-investigative fiction.

## Writing Rules

- Use `show-vs-tell-craft` for every location, NPC, faction, artifact,
  creature, encounter, clue, and boxed-text revision.
- Player-facing description shows first: short, sensory, concrete, read aloud,
  describe before naming, no GM secrets, no "you feel" commands.
- GM sidebar tells clearly: function, tone, pacing role, real-world comparison,
  what it resembles, and how to use it at the table.
- Include a concrete detail bank, interaction prompts, reveal ladder, and what
  not to reveal yet when building durable Atlas entries.
- Describe concrete sensory and social facts before naming abstractions.
- Flag thin canon instead of silently inventing.
- Do not bury plot instructions inside player-facing prose.
- Preserve agency by giving situations, pressures, and consequences rather than
  a single required solution.

## Output Contract

```markdown
## Atlas Scope
- Source/status:
- Audience/privacy:
- Adapter:

## Run-Mode Index

## Scene Or Node Cards

## Player-Safe Material

## GM-Only Material

## Canon / Mystery / Contradiction Notes

## Reviewable Patches
```

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports TTRPG Game Master. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
