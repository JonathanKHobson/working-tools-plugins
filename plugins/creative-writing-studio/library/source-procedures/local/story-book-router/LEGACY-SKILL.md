---
name: story-book-router
description: Route and support book, fiction, screenplay, manuscript, story bible, character, worldbuilding, scene, dialogue, chapter, revision, continuity, storyboard, and long-form prose work while preserving authorial voice, canon, ambiguity, and provenance.
---

# Story Book Router

Use this skill for long-form story and manuscript work. It owns the story lane; it does not own public release, live app mutation, or marketing copy.

## Route By Need

- New or normalized project scaffold: use `creative-project-context`.
- Premise, theme, plot, arcs, scene purpose, setup/payoff, clue logic, continuity, or contradiction triage: use `story-architecture`.
- Show/tell balance, emotional dramatization, concrete evidence, over-showing,
  or line-level "show, don't just tell" revision: use `show-vs-tell-craft`.
- Source, influence, quotation, rights, privacy, or generated-media provenance: use `originality-rights-and-provenance`.
- Export, EPUB/PDF/print, metadata, accessibility, excerpts, serialization, or release approval: use `publishing-router`.
- Public pitch, blurb, launch copy, social post, or stakeholder-facing explainer: use `communication-story-crafter`, `marketing-strategy-operator`, or `social-content-studio`.
- Storyboard or visual sequence planning: use this skill for narrative sequence, then coordinate with `visual-asset-integration` or `html-presentation-builder` for visual artifacts.

## Story Project Shape

For Markdown-first projects, prefer a Story Skills-inspired model:

```text
story.md
characters/_index.md
worldbuilding/_index.md
worldbuilding/locations/
worldbuilding/systems/
worldbuilding/factions/
worldbuilding/artifacts/
plot/_index.md
plot/arcs/
plot/timeline.md
scenes/_index.md
continuity/state.md
continuity/questions/
continuity/promises/
glossary/_index.md
chapters/_index.md
```

Use this as a clean-room model. Do not install or run the Story Skills CLI unless the user explicitly approves that dependency.

## Drafting Workflow

1. Read the project brief/canon before generating prose.
2. Identify POV, tense, voice, scene purpose, current state, open questions, promises, and constraints.
3. Identify the scene's emotional target, which beats must be dramatized, and
   which connective tissue should be summarized.
4. Outline beats before drafting when the output changes plot or canon.
5. Preserve the user's voice and intentional choices. Do not flatten dialect, fragmentary style, repetition, nonlinear structure, unreliable narration, or deliberate ambiguity.
6. Treat missing facts as questions or placeholders, not inventions.
7. After drafting or revision, update or propose updates to continuity, timeline, character state, object state, knowledge state, questions, and promises/payoffs.

## Revision Workflow

Pick one pass:

- Developmental: premise, stakes, agency, causality, scene purpose, pacing, structure.
- Continuity: chronology, knowledge, locations, injuries, objects, money, promises, clues, unresolved questions.
- Line: clarity, rhythm, specificity, dialogue, POV, voice.
- Show/tell: diagnose first, then choose `rewrite_to_show`,
  `rewrite_to_tell`, or `blend_show_and_tell`; do not blindly expand simple
  factual prose.
- Proof: formatting, typos, repeated words, small inconsistencies.

For prose quality, use Better Writing patterns locally: preserve meaning, facts, voice samples, legal/technical wording, and intentional quirks; remove generic AI tells only when they harm the target genre and audience.

## Output Contract

```markdown
## Story Read
- Project:
- Stage:
- Pass:
- Fixed facts:
- Open questions:

## Work

## Canon / Continuity Updates

## Risks Or Author Decisions

## Next Drafting Step
```
