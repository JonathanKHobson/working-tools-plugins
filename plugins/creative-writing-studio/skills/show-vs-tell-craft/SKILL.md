---
name: show-vs-tell-craft
description: Diagnose, teach, lint, and revise fiction, Story Atlas, player-facing TTRPG prose, GM sidebars, NPCs, emotions, clues, locations, factions, items, and live-table descriptions using show-vs-tell as a pacing, clarity, immersion, and emotional-focus choice. Use when drafting or revising prose for "show, don't just tell."
---

# Show vs Tell Craft

Use this skill when prose, table description, Story Atlas entries, NPCs, clues,
locations, factions, items, emotion beats, or revision notes need a nuanced
show/tell decision instead of a blanket "make it more descriptive" pass.

## Core Definition

```text
Showing = dramatization. The reader/player receives concrete evidence and infers the meaning.
Telling = summarization. The narrator/GM states the meaning, transition, fact, or conclusion directly.
Good prose uses both. Show important emotional, sensory, character, and dramatic moments. Tell when clarity, speed, compression, safety, or utility matters more than immersion.
```

The principle is **show, don't just tell**. Showing is not always better. Telling
is not bad. Strong writing chooses, blends, and compresses on purpose.

## Decision Model

Show when the moment should be felt: first impressions, character emotion,
atmosphere, awe, dread, humor, grief, tension, danger, wonder, intimacy, reveals,
clues, betrayals, emotional-cost decisions, NPC personality, relationship
dynamics, worldbuilding evidence, theme, motif, and anything the audience should
remember.

Tell when the moment should move quickly or clarify: transitions, travel
compression, repeated routines, unimportant logistics, safety reminders, rules
teaching, GM-only notes, sidebars, recaps, table procedure, accessibility
support, and places where showing would become awkward, bloated, or confusing.

Blend when a broad claim needs proof: tell the organizing idea, then immediately
show concrete evidence.

## TTRPG Rule

Player-facing prose should usually show first. GM-facing notes may tell plainly.

- Player-facing: concrete, sensory, read-aloud, describe before naming, no plot
  explanation, no "you feel" commands, no GM secrets.
- GM sidebar: plain function, tone, pacing role, real-world comparison, and
  table guidance. Do not become poetic.

## Revision Pass

Use `scripts/show_tell_revision_pass.py` when a deterministic lint/diagnosis
helps. Supported modes:

- `diagnose`
- `rewrite_to_show`
- `rewrite_to_tell`
- `blend_show_and_tell`
- `table_read_aloud`
- `gm_sidebar`
- `line_lint`
- `story_atlas_entry`

Do not automatically rewrite everything into showing. First decide the passage
purpose and audience.

## Internal Questions

1. What should the audience remember?
2. Should this moment be felt, understood quickly, or both?
3. Is this player-facing, GM-only, or mixed?
4. Is the current prose making a claim without evidence?
5. Is it using abstract labels instead of concrete proof?
6. Is it telling the reader/player what to feel?
7. Would showing waste time or improve immersion?
8. Is there a strong narrative voice that makes telling enjoyable?
9. Is the passage confusing because it shows too much and tells too little?
10. Is the passage flat because it tells too much and shows too little?

## Coordination

- Use with `story-architecture` for scene purpose, arcs, setup/payoff, clue
  logic, pacing, and thematic evidence.
- Use with `story-book-router` for line revision, developmental revision,
  drafting scenes, preserving narrative voice, and deciding what to dramatize.
- Use with `story-atlas-prep`, `ttrpg-router`, `gm-roleplay-router`,
  `npc-performance-director`, `improv-roleplay-coach`, and
  `live-table-director` for player-facing show-first prose and GM-only tell-clear
  sidebars.
- Use with `communication-story-crafter` when public prose needs proof, trust,
  audience inference, and compression.

## References

- `docs/show-vs-tell/README.md`
- `docs/show-vs-tell/decision-table.md`
- `docs/show-vs-tell/ttrpg-application.md`
- `docs/show-vs-tell/story-atlas-patterns.md`
- `docs/show-vs-tell/examples.md`
- `docs/show-vs-tell/lint-flags.md`
- `docs/show-vs-tell/evaluation-cases.md`
- `templates/show-vs-tell-templates.md`

For writing-template selection or purposeful variation in prose, use `writing-quality-studio:voice-and-style` and its shared Writing Voice Lab catalog. Useful scene/essay candidates include V04 Scene-led feature, V07 Lyrical concrete, V13 Marginal notebook, V14 Braided reflection and V21 Documentary collage. Honor explicit choices; otherwise choose compatible mechanics by scene purpose and audience. This creative owner retains canon, POV, character voice and deliberate ambiguity; do not turn every narrator into Kyle or randomize voice within a scene.

<!-- BEGIN PROFESSIONAL-AGENTS -->
## Professional roles

For an assignment needing a named owner, consult [this studio’s role contracts](../../references/professional-agents/README.md); this method supports Fiction Writer. Load only the selected contract. Work Management owns cross-studio routing. Role selection does not require delegation or expand authorization.
<!-- END PROFESSIONAL-AGENTS -->
