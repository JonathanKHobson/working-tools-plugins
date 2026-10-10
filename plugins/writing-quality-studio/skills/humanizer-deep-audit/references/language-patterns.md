# Language and Grammar Patterns

Use this guide for sentence construction, vocabulary clusters, repetitive rhetoric, and over-smoothed diction.

## Contents

- Vocabulary clusters
- Evasion of `is`, `are`, and `has`
- Contrast templates
- Automatic tricolons
- Synonym cycling
- Sentence-shape uniformity
- Hedging, intensifiers, and plain verbs
- Time- and model-sensitive cues

## Vocabulary clusters

Words observed at unusually high rates in some model outputs include:

`additionally`, `align with`, `boasts`, `bolstered`, `crucial`, `delve`, `emphasizing`, `enduring`, `enhance`, `fostering`, `garner`, `highlight`, `interplay`, `intricate`, `intricacies`, `key`, `landscape` used abstractly, `meticulous`, `pivotal`, `robust`, `showcase`, `tapestry` used abstractly, `testament`, `underscore`, `valuable`, and `vibrant`.

The editorial cue is density and co-occurrence, not the existence of a forbidden word.

**Weak cluster:** Additionally, the initiative showcases a robust framework that fosters collaboration across the evolving policy landscape.

**Better:** The initiative gives county planners and tribal water managers one shared permit calendar.

**Legitimate:** The unit tests exercise the library’s retry logic under packet loss; the suite is robust enough for release.

Context matters. `Landscape` may name visible terrain. `Underscore` may name a character. `Robust` may be a technical term with a defined criterion. Do not replace a precise word merely because it appears on a list.

### Repair method

1. Circle each abstract noun and evaluative adjective.
2. Keep terms required by the field.
3. Replace the rest with the actor, action, object, condition, or measured result.
4. Re-read for meaning; do not perform one-for-one synonym swaps.

## Evasion of `is`, `are`, and `has`

Over-edited prose often dodges plain copulas with `serves as`, `stands as`, `marks`, `functions as`, `operates as`, `represents`, `boasts`, `features`, `maintains`, `offers`, or `refers to`.

**Weak:** The annex serves as the organization’s exhibition space and features four galleries.

**Better:** The annex is the organization’s exhibition space. It has four galleries.

**Weak:** The term “red hour” refers to the last class period on Friday.

**Better:** “Red hour” is the last class period on Friday.

**Weak:** She began her career as the district’s records clerk.

**Better:** She was the district’s records clerk from 1998 to 2001.

Keep the richer verb when it carries extra meaning:

- `The pump functions as a check valve when pressure falls` describes behavior.
- `The hall serves as a shelter during storms` may emphasize temporary use.
- `The menu features six regional dishes` is acceptable in restaurant copy when selection is the point.

## Contrast templates

### Additive correction: “not just X, but also Y”

**Weak:** The delay was not just inconvenient; it also undermined trust and damaged morale.

**Better:** The delay moved training into exam week. Twelve instructors withdrew.

### Dramatic negation: “not X, but Y”

**Weak:** This is not merely a scheduling tool, but a catalyst for organizational transformation.

**Better:** The tool assigns shifts and alerts supervisors when a certification will expire.

### Staccato negation: “no X, no Y, just Z”

**Weak:** No jargon, no friction, just effortless collaboration.

**Better:** Guests can comment without creating an account.

### Reversed contrast: “X rather than Y”

**Weak:** The committee prioritized empirical consolidation rather than ideological purity.

**Better:** The committee funded the two proposals that already had pilot data.

### When contrast belongs

Keep a contrast when the reader has a real misconception, the source documents competing explanations, or the distinction drives a decision.

**Useful:** The sensor measures humidity, not temperature; installing it beside the oven will produce false alarms.

Do not make every paragraph argue against an imaginary reader.

## Automatic tricolons

Three-part sequences can create rhythm and memory. They become mechanical when nearly every claim arrives as three adjectives, three nouns, three examples, or three labeled bullets.

**Weak:** The workshop is engaging, practical, and transformative. Participants gain clarity, confidence, and connection.

**Better:** Participants leave with a revised opening and a five-minute practice they can use before the next class.

**Weak:** The redesign improves speed, simplicity, and satisfaction.

**Better:** The redesign removes the confirmation screen, cutting checkout from five steps to four.

Audit a page for:

- repeated `X, Y, and Z` endings;
- three adjectives before one noun;
- three short sentences with identical syntax;
- three bold label-colon bullets created only to appear complete;
- escalating abstract nouns such as `identity, authenticity, and dignity`.

Vary the count only when the material has a natural count. Two facts are enough. Four steps may be correct. One exact example often beats a decorative three.

## Synonym cycling

Some prose avoids repeating the clearest noun by rotating near-synonyms. This can blur reference and sound unnaturally ornate.

**Weak:** The clinic opened in May. The facility added weekend hours in June. The center hired two nurses in July. The institution now serves four neighborhoods.

**Better:** The clinic opened in May, added weekend hours in June, and hired two nurses in July. It serves four neighborhoods.

**Weak:** Rivera wrote the report. The analyst’s document argued for consolidation. The researcher’s paper reached the board in April.

**Better:** Rivera wrote the report arguing for consolidation. The board received it in April.

Repeat the exact technical or legal term when consistency prevents ambiguity. Use a pronoun only when its referent is unmistakable.

## Sentence-shape uniformity

Watch for paragraphs in which every sentence:

- begins with a transition;
- contains one comma plus a trailing `-ing` phrase;
- has nearly the same length;
- opens with the subject’s name;
- ends with an abstract significance claim;
- uses the same `While X, Y` or `By doing X, Y` frame.

**Weak:** Additionally, the lab expanded its facilities, enhancing research capacity. Furthermore, it recruited specialists, fostering interdisciplinary collaboration. Moreover, it launched a fellowship, supporting future innovation.

**Better:** The lab added a wet room and hired two soil chemists. Its new fellowship funds one graduate researcher each year.

Do not manufacture variation for its own sake. Let emphasis determine length: a short sentence can land a decision; a longer one can hold related conditions.

## Hedging, intensifiers, and plain verbs

Human writing includes hedges, intensifiers, awkward phrases, and strong claims. The goal is calibrated language, not antiseptic prose.

### Stacked hedges

**Weak:** It may perhaps be possible that the change could reduce delays.

**Better:** The change may reduce delays; the pilot did not measure wait time.

### Ceremonial hedges

**Weak:** I would like to suggest that we consider moving the deadline.

**Better:** Move the deadline to Friday so the finance team can review the estimate.

### Empty intensifiers

**Weak:** The outage had a very significant impact on users.

**Better:** The outage blocked password resets for 47 minutes.

### Stiff synonyms

Prefer `wrote` to `authored`, `used` to `utilized`, `moved` to `relocated`, `tried` to `attempted`, and `died` to euphemism when the plain verb fits the genre. Keep the formal term when it has legal, technical, or tonal value.

## Time- and model-sensitive cues

Observed model habits change. Earlier systems were associated with clusters around `delve`, `tapestry`, `testament`, and overt didactic disclaimers. Later systems may reduce those words while increasing source-performance language, shallow attribution, or `highlighting` and `showcasing` constructions. Different model families also have different syntactic and formatting habits.

Therefore:

- never build the edit around a frozen blacklist;
- prefer structural diagnosis over word replacement;
- inspect the destination and date before interpreting a cue;
- do not assume a pattern generalizes from informational prose to fiction, chat, code comments, or academic writing;
- update this guide and the linter when evidence changes.

## Agency and grammatical compression

When nominalization, passive voice or a chain of clauses hides responsibility or conditions, apply [the grammar check and keep examples](../../natural-prose-editor/references/research-pattern-review.md#inspect-grammar-beyond-fashionable-words). Restore only known actors and preserve technical terms, accurate nonhuman subjects and useful passive focus. The relevant studies compare specific models/registers; they do not make a construction a defect by itself.
