---
name: human-writing
description: Draft or revise prose so it sounds natural, specific, and individually voiced while preserving the writer's meaning. Use for humanizing AI-assisted text, matching a supplied voice sample, or improving fiction and narrative structure; do not use as an AI-detector or for proofreading that should preserve every stylistic choice.
license: MIT
---

# Human writing

Help the writer make deliberate choices at two levels:

- Surface prose: diction, rhythm, sentence structure, specificity, formatting, and conversational residue.
- Narrative design: character agency, causality, theme, time, revelation, perspective, setting, and reader relationship.

The goal is strong writing with a discernible voice. Do not add mistakes, random slang, choppy fragments, fake memories, or arbitrary quirks to simulate a person. Do not promise to bypass AI detectors or treat any pattern as proof of authorship.

## Choose the mode

Identify the mode from the request and source:

- **Draft:** Write new prose from the user's facts, intent, audience, format, and tone.
- **Revise:** Rebuild existing prose while preserving its claims and purpose.
- **Voice match:** Treat a sample of the user's writing as the main style authority.
- **Narrative revise:** For fiction, memoir, anecdotes, case studies, or other prose with characters and events, review narrative choices before polishing sentences.
- **Review:** Diagnose the strongest problems and recommend edits without rewriting unless asked.

Use the narrative mode only when the text actually tells a story. StoryScope's findings come from long-form fiction and should not be generalized to product copy, reference prose, emails, or technical documentation.

## Protect the source

Before drafting or revising, identify the non-negotiable content: facts, names, figures, dates, quotations, citations, promises, qualifications, technical terms, and the writer's actual position.

- Do not invent or strengthen factual claims.
- Preserve meaningful uncertainty, disagreement, mixed feelings, and unresolved questions.
- Keep quotations and citation targets accurate.
- Fiction may introduce details as part of the creative task, but follow the user's world, continuity, boundaries, and requested level of invention.
- If a necessary factual detail is missing, use a less specific sentence or flag the gap. Do not fill it with a plausible guess.

## Establish the voice

When the user supplies a writing sample, infer its tendencies: sentence-length range, cadence, vocabulary, contractions, punctuation, paragraph shape, humor, directness, transitions, and deliberate quirks. Match the combination rather than copying isolated phrases. A sample overrides generic preferences in this skill unless doing so would alter meaning or violate the requested format.

Without a sample, use a neutral human baseline: direct verbs, concrete nouns, varied but controlled rhythm, context-appropriate formality, and no performance of personality that the material has not earned.

Specificity must come from the source or the writer. Never invent a personal anecdote, named reference, sensory detail, opinion, or cultural marker merely to make the prose feel human.

## Revise at the right level

Do not perform a synonym swap over the original structure. Find the point of each paragraph, then merge, split, reorder, or rebuild as needed.

For all prose, read [references/prose-patterns.md](references/prose-patterns.md) when the text is AI-assisted, generic, over-polished, or explicitly being humanized. Use its patterns as an audit, not a blacklist.

For narrative prose, first read [references/narrative-choices.md](references/narrative-choices.md). Address structural defaults before sentence polish. Do not mechanically add every human-associated feature; choose what serves this particular story.

## Working pass

1. State the piece's job in one sentence: what should the reader understand, feel, decide, or do?
2. Preserve the content inventory and identify the intended voice.
3. In narrative mode, audit the underlying choices and revise only the ones that weaken this story.
4. Draft or rebuild paragraphs around concrete meaning. Let sentence length and emphasis follow the ideas.
5. Run the prose-pattern audit. Remove clusters of stock phrasing, empty emphasis, uniform structure, and chatbot residue while retaining intentional usage.
6. Read the result for rhythm and continuity. Repair paragraphs, not just flagged words.
7. Compare the result with the source inventory. Restore any claim, caveat, citation, or purposeful detail that was lost.

## Final checks

Before returning the text, verify:

- Every factual claim is supported by the source or user.
- The rewrite preserves the writer's position and level of certainty.
- The voice fits the audience and format; it does not merely sound casual.
- Specific details do real work instead of decorating the piece.
- Sentence and paragraph shapes vary for a reason, not randomly.
- No repeated rhetorical template dominates the piece.
- Fiction does not over-explain its meaning or default to an overly tidy, single-track structure unless that is intentional.
- Formatting, punctuation, and spelling follow the writer's sample or target publication, not a universal ban.

## Return the result

- For a draft or rewrite, return the finished text first. Add a brief note only when the user asked for analysis or when a missing detail or tradeoff needs attention.
- For review mode, report a small number of high-impact findings with precise examples and suggested changes.
- When editing a file, change only the prose in scope. Preserve frontmatter, code, data, links, identifiers, and document structure unless the user asks to change them.
- When embedded in another task, return only the text that task needs.

## Basis

This skill combines the prose-level editing patterns in [blader/humanizer](https://github.com/blader/humanizer) with narrative-level findings from [StoryScope](https://github.com/jenna-russell/storyscope) and its [paper](https://arxiv.org/abs/2604.03136). Both repositories are MIT-licensed; the StoryScope paper is CC0. The guidance is adapted for writing assistance, not authorship classification.
