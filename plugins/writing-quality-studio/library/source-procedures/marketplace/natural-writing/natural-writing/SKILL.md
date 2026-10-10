---
name: natural-writing
description: Draft or revise ordinary expository prose when the user asks for clearer, more concise, less formulaic, or audience-appropriate wording. Use for workplace messages, explanations, documentation, reports, and prose rewrites where wording and information order are central. Do not invoke automatically for code-only or machine-readable output, exact transcription or protected text, legal or specification wording, or creative and literary writing; use it there only when the user explicitly invokes the skill or asks to revise unprotected surrounding prose.
license: CC-BY-4.0; see LICENSE.md
metadata:
  version: "1.0.1"
  source: "Adapted from the Google Developer Documentation Style Guide"
---

# Natural writing

Write for the person who needs the answer, not for the appearance of completeness. Make the result sound considered: clear about the point, honest about uncertainty, and shaped for this reader and this moment.

This is a house style, not a claim that one style is objectively correct. Apply priorities in this order:

1. The user's request, including requested length, tone, format, and protected wording.
2. The facts, evidence, code, quotations, and authorization boundaries.
3. The author's established voice and the project's terminology and conventions.
4. This skill.

Depart from any guideline when doing so makes the result more accurate, clearer, safer, or more faithful to an intentional voice. Stay consistent after making that choice.

These instructions govern the prose you produce. They do not override required progress updates, citations, source attribution, safety information, verification results, limitations, approval requests, or a handoff summary. Keep those communications concise and useful.

## Start from the reader's job

Before writing, identify these points from the available context:

- What question must the response answer or what outcome must it produce?
- What does the reader probably know already?
- What decision or action, if any, comes next?
- Which details affect that decision, and which are merely related?
- What tone fits the relationship and the stakes?

Do not turn these checks into questions for the user when the context supports a reasonable answer. Ask only when a missing choice would materially change the result.

Choose the requested mode:

- **Draft:** Produce the requested prose from the supplied facts and context.
- **Rewrite:** Preserve meaning, evidence, exact items, and intentional voice unless the user authorizes a change.
- **Review:** Report specific findings and suggested repairs. Do not silently replace the entire artifact unless the user asks for a rewrite.

## Lead with the substance

Put the answer, outcome, recommendation, or important finding in the first useful sentence. If a condition changes the answer, include it early.

Do not delay the point with any of the following:

- Praise for the question.
- A generic acknowledgment of the request.
- A restatement of what the user just said.
- An announcement that a breakdown, deep dive, overview, or step-by-step answer follows.
- A broad scene-setting paragraph that does not change the reader's understanding.
- Process narration about how you approached the response.

A greeting, acknowledgment, or brief setup can be right when the social situation calls for it. It must earn its space.

## Make every sentence do work

Prefer subject-verb-object order. Keep the main subject and verb near the start. Use active voice when readers need to know who acts. Passive voice is useful when the actor is unknown, irrelevant, obvious, or better de-emphasized.

Use present tense for current behavior and general facts. Use past or future tense when time is part of the meaning, not to make ordinary behavior sound formal.

Put a condition first when it determines whether an instruction applies or lets the reader skip that instruction:

- Better: "If the request can be retried safely, use exponential backoff."
- Worse: "Use exponential backoff if the request can be retried safely."

A short trailing condition is fine when it is unambiguous and reads more naturally. Avoid creating a repetitive series of sentences that all begin with *if*.

Put the location or goal before an action when that order helps the reader orient themselves:

- "In **Settings**, select **API access**."
- "To keep the original data, return a copy."

Prefer common, precise words. Use *use* instead of *utilize*, *start* instead of *commence*, and *so* instead of *consequently* unless the less common word expresses a needed distinction.

Use common contractions such as *don't*, *can't*, and *you're* when they fit the voice. They often sound more natural and make a negative harder to miss. Avoid awkward or invented contractions.

Remove throat-clearing phrases such as *it is important to note*, *it is worth mentioning*, *in order to*, *at this point in time*, and *due to the fact that*. State the point they were delaying.

Keep helper words such as *that* and *then* when they prevent ambiguity. Concision means removing waste, not stripping out grammar that helps the reader.

## Build paragraphs around ideas

Give each paragraph one main job. Put its distinguishing information in the first sentence, then supply the evidence, reason, limitation, or consequence.

Split a paragraph that hides several decisions or requires the reader to retain too much context. A paragraph longer than five or six sentences deserves review, not automatic division.

Do not isolate every sentence for drama. A one-sentence paragraph is useful when it has a distinct role. Repeated one-line paragraphs make ordinary prose feel staged.

Use transitions only when the relationship between ideas is not already clear. Vary sentence length and openings naturally. Do not begin a run of sentences with the same frame.

## Choose exact actors, terms, and claims

Name the actor when responsibility matters: the reader, application, server, administrator, team, or another party. Do not use *we* to mean people in general or *the user* to mean the reader. Address the reader as *you* when direct address helps.

Use *I* when the assistant must own an action, limitation, judgment, or uncertainty. Do not hide behind passive voice or invent a collective *we*.

Use one term for one concept. Do not cycle through synonyms for variety when readers might infer a technical distinction. Define an unfamiliar abbreviation or necessary term on first use. Keep an established technical term when replacing it would reduce accuracy; explain it briefly if the audience might not know it.

Avoid vague anthropomorphism when it obscures behavior. A service can *return*, *detect*, or *reject* something. It usually does not *want*, *believe*, or *know* something.

State requirements, options, expectations, and uncertainty precisely:

- Use *must* or an imperative for a requirement.
- Use *can* for an option or capability.
- Use *might* for a possible outcome.
- State an expected outcome directly.
- Replace ambiguous *should* when readers could mistake advice for a requirement or an expectation for a possibility.

Match the strength of a claim to the evidence. Avoid unsupported superlatives, absolutes, and guarantees such as *best*, *fastest*, *always*, *never*, *ensures*, and *prevents*. Give the measurement, source, scope, condition, or design intent that makes the claim useful. If the evidence is missing, say what would be needed instead of inventing support.

When the evidence supports a recommendation, make it and name the condition that would reverse it. Do not manufacture balance between options that the available facts do not support.

In durable material, avoid empty time markers such as *currently*, *now*, *new*, and *latest*. Use time-based language when time is real: release notes, announcements, histories, deadlines, and state changes.

## Sound human without performing humanity

Aim for the voice of a knowledgeable person speaking to another person: conversational, respectful, calm, and specific. Match the user's altitude. Do not explain elementary background to an expert or use unexplained shorthand with a newcomer.

Keep personality that belongs to the author or situation. Humor, fragments, rhetorical questions, idioms, and unusual rhythm can work when they are deliberate and suitable for the audience. Do not add them as decoration.

Treat the following patterns as review signals, not forbidden forms. Do not replace one stock phrase with another or damage good prose merely to remove a recognizable marker.

Do not manufacture intimacy, enthusiasm, or authority. Avoid the following patterns unless the content genuinely calls for them:

- "Great question," "Absolutely," or "You're exactly right."
- "Let's dive in," "Let's unpack this," or "Here's the thing."
- "This isn't just X; it's Y" and other slogan-like reversals.
- "Think of it as..." followed by an analogy that adds no precision.
- Fake quotations around a position nobody actually stated.
- Repeated intensifiers, exclamation marks, and sales language.
- Stock adjectives such as *robust*, *seamless*, *powerful*, *elegant*, and *game-changing* without an observable fact.
- Clusters of em dashes, parenthetical asides, or rhetorical questions used as a house rhythm.
- A neat three-part list chosen for cadence instead of content.
- A generic closing offer to do more when the answer is already complete.

Do not overcorrect into sterile manual prose. Make each choice responsive to meaning rather than habit.

## Use structure in proportion to the task

Default to connected prose for a short answer. Add structure when it helps the reader scan, compare, decide, or act.

### Headings

Use headings for distinct sections in a longer response or document. Make them descriptive and use sentence case. Do not add a heading that merely labels a single sentence as *Answer*, *Overview*, *Key takeaway*, or *Conclusion*.

Start task headings with a base-form verb when natural, such as *Create an access token*. Use a noun phrase for a concept, such as *Token lifetime*.

### Lists

Use numbered lists for sequences and rankings. Use bullets for genuine sets of options, requirements, examples, or independent facts. Use a table only when readers need to compare the same fields across several items.

Do not turn an ordinary sentence into bullets for visual weight. A one-item list is rarely useful, but it can fit a required template or set off a single action, warning, or checklist item. Introduce a list with a complete sentence when the heading or preceding text does not make its purpose clear. Keep list items parallel in grammar and consistent in punctuation.

### Emphasis

Use bold, italics, block quotes, and callouts sparingly. Words should carry most emphasis. Do not bold every label in a bullet list or use block quotes for text that is not quoted.

Format code identifiers, commands, filenames, literal values, and text the reader enters as code when the medium supports it. Preserve the exact spelling and case of technical items.

### Summaries

Do not append a recap to a short response. In a long document, a summary should synthesize several sections, expose a decision, or support a different reading path. It should not repeat every heading in shorter form.

## Write instructions people can follow

State the goal and necessary prerequisites before the procedure. Give the shortest accessible path that fits the common case. If several methods matter, recommend a default and separate the alternatives clearly.

Write steps in the order the reader performs them. Start each step with an imperative action. Prefer one decision or substantial action per step. Put an immediate result after the action when the result helps the reader confirm or continue.

Mark an optional step with `Optional:` at the start. Put warnings before the action that creates the risk.

For a command, say what it accomplishes when that context adds information. *Run this command* can be clear when the purpose is already established. Explain placeholders close to the command. Show output only when readers need it to verify the result or take the next step.

For a long or structurally complex document, tutorial, runbook, code explanation, or interface procedure, read [references/technical-writing.md](references/technical-writing.md). Do not load it for a short answer merely because that answer contains code.

## Write for more than one kind of reader

When writing for a broad, translated, or accessibility-sensitive audience, prefer literal, unambiguous language. Avoid culture-specific references, unexplained idioms, jokes that depend on local knowledge, and phrasal verbs that have a clearer single-word equivalent. Use unambiguous dates, times, and units.

Use inclusive, precise terms. Avoid ableist, gendered, violent, or socially charged metaphors when a neutral description is clearer. If a community's preferred terminology matters, use the terms its members prefer. Keep exact keywords and code names even when their wording is dated; format and explain them rather than silently changing code.

Do not rely on color, position, images, sound, or punctuation alone to carry an essential distinction. Use descriptive link text rather than *click here* or a bare URL. Refer to an interface control by its label or accessible name, not only by its color, shape, or position. Supply text equivalents for meaningful visuals and audio.

## Edit without changing the author

When revising existing text:

1. Identify what the passage must preserve: facts, stance, uncertainty, rhythm, humor, terminology, formatting, quotations, and deliberate roughness.
2. Fix meaning and information order before polishing sentences.
3. Cut repetition, filler, and generic framing.
4. Repair ambiguous actors, modifiers, pronouns, and requirements.
5. Replace inflated claims with evidence or an explicit limitation.
6. Read for rhythm and voice. Restore any personality the edit flattened.

Never silently change a quotation, code, URL, measurement, product name, legal clause, or cited claim. Do not "improve" poetry, marketing copy, fiction, or a distinctive personal voice into this house style unless the user asks for that kind of edit.

If a passage is formulaic and the right repair is not obvious, or if the user asks for an explanation of the edits, read [references/editing-patterns.md](references/editing-patterns.md). Do not load it for a straightforward light edit or text that may already be good.

## Finish silently

Before returning the result, check the following:

- The first useful sentence contains the answer, outcome, or necessary condition.
- Each paragraph, heading, and list has a distinct job.
- No adjacent sentence repeats the same point in different words.
- Actors, conditions, sequence, requirements, and uncertainty are clear.
- Claims match the available evidence.
- Facts, code, quotations, links, and protected wording are unchanged.
- Formatting helps the reader rather than displaying effort.
- The tone fits the author, reader, medium, and stakes.
- The result works for readers who use translation or assistive technology when that matters.
- A silent read-through sounds natural: sentence openings vary, transitions are earned, and the rhythm is neither choppy nor ceremonially polished.

Return only the requested artifact unless the user asks for an edit log, alternatives, rationale, or a conversation about the choices. Include any workflow communication, evidence, safety information, or handoff details required by the surrounding agent environment.

For provenance and attribution, see [references/sources.md](references/sources.md). The skill does not require network access at runtime.
