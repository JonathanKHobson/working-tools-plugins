# Structure and Formatting Patterns

Use this guide when organization and typography feel mechanically “helpful” or do not match the destination.

## Contents

- Heading case and hierarchy
- Mechanical emphasis
- Label-colon lists
- Em-dash audit
- Decorative emoji
- Tables that should be prose
- Quote-style consistency
- Repeated separators
- Structure as performance

## Heading case and hierarchy

### Title case everywhere

**Weak:** `## Challenges And Future Directions`

**Better for sentence-case systems:** `## Challenges and future directions`

Follow the publication’s house style. Title case is normal in many books, decks, and marketing pages; its presence is not a problem. The cue is automatic use that conflicts with the destination.

### Skipped levels

Do not jump from a page title directly to a third-level heading unless the format defines that hierarchy.

**Weak:** `# Field guide` followed by `### Examples`

**Better:** `# Field guide` followed by `## Examples`

Heading levels describe structure, not visual size. Use CSS or the platform’s styling tools for appearance.

### Excessive sectioning

A heading should orient the reader to a meaningful change of question, task, time, or topic.

**Weak structure:**

- Background
- Key background
- Important context
- Main considerations
- Key takeaways
- Conclusion

**Better structure:**

- What changed
- Who is affected
- Decision needed by Friday

## Mechanical emphasis

Watch for:

- every key noun in bold;
- the same term bolded every time it appears;
- bold labels carrying the structure of every paragraph;
- bold used where a heading, table header, or plain sentence would be clearer;
- emphasis added because the text calls something “key” rather than because the reader needs to find it.

**Weak:** The **primary benefit** is **increased efficiency** through **streamlined workflows**.

**Better:** Reviewers can approve the request from the notification instead of opening the dashboard.

Keep bold for scanning when the destination uses it consistently, such as a short form with field labels or an operational checklist.

## Label-colon lists

The recurring form is `- **Label:** description`, repeated for every point. It is useful for genuine mappings, glossaries, or parallel options. It becomes a problem when ordinary prose is broken into labeled fragments to simulate coverage.

**Weak:**

- **Efficiency:** The process saves time.
- **Clarity:** The process improves understanding.
- **Collaboration:** The process helps teams work together.

**Better:** The new form removes two approval fields. In testing, managers completed it 40 seconds faster.

**Useful:**

- **Owner:** Lena Ortiz
- **Deadline:** August 14
- **Blocker:** Finance has not approved the vendor rate

Check whether list markers match the destination. A literal bullet character, emoji, hash, or manually typed number may be wrong in systems with their own list syntax.

## Em-dash audit

Em dashes are valid punctuation. Review density, rhythm, spacing, and function.

Flag these uses:

- several dashes in one paragraph;
- a dash inserted in nearly every sentence for “punch”;
- repeated `X—not Y, but Z` frames;
- dashes where a period would reveal two separate claims;
- spaced and unspaced dashes mixed in one document;
- dashes that violate the house style.

**Weak:** The update is fast—really fast—and it changes everything—without changing how your team works.

**Better:** The update cuts the import from six minutes to 40 seconds. The workflow is unchanged.

**Keep:** I opened the envelope—and recognized my father’s handwriting.

The kept dash marks a genuine interruption in perception. Do not flatten an author’s rhythm merely to reduce a count.

Possible substitutions:

- period for a separate assertion;
- colon for an explanation or payoff;
- comma for a light interruption;
- parentheses for secondary information;
- no punctuation when the clause can be integrated directly.

## Decorative emoji

Emoji can be appropriate in social posts, informal communities, warnings, or established product patterns. They are distracting when every heading or bullet receives an icon unrelated to function.

**Weak:**

- 🚀 Key benefits
- 💡 Important insights
- 🎯 Next steps

**Better:**

- Benefits
- Evidence
- Next decision

In UX, an icon must have a semantic or navigational job and must not be the only carrier of meaning.

## Tables that should be prose

Use a table for repeated fields across multiple comparable items. Avoid a table for two facts, one short mapping, or narrative sequence.

**Weak table:**

| Metric | Value |
| --- | --- |
| Staff | 12 |
| Opened | 2023 |

**Better:** The office opened in 2023 with 12 staff members.

**Useful table:** compare five plans across price, storage, support, and cancellation terms.

Also check whether a tiny table duplicates an infobox, sidebar, or the preceding sentence.

## Quote-style consistency

Curly quotes and apostrophes are normal in professionally typeset work and on Apple or Microsoft devices. Straight quotes may be required in code, wikitext, data, or a house style. The cue is inconsistency or destination mismatch.

**Weak:** She called the draft “finished," but the editor's note said ‘incomplete'.

**Better for prose:** She called the draft “finished,” but the editor’s note said “incomplete.”

**Better for code:** `status == "finished"`

Do not normalize quotation marks inside code, identifiers, command examples, or data files without checking syntax.

## Repeated separators

Thematic breaks before every heading usually add noise and may reveal markup copied from another system.

**Weak:**

```markdown
---
## Background
...
---
## Results
...
```

**Better:** rely on headings and spacing unless the break marks a real change of scene, speaker, or document part.

## Structure as performance

Mechanical organization can hide thin thinking. Warning signs include:

- a “comprehensive” outline with one vague sentence per section;
- “Key takeaways” that repeat the headings;
- a numbered list whose natural order is unclear;
- exactly three sections regardless of the material;
- a conclusion that merely announces completion;
- questions to consider that the document never answers;
- a heading for a single sentence that belongs in the previous paragraph.

Test every section with three questions:

1. What reader question does this section answer?
2. What new evidence or decision appears here?
3. Would removing the heading make the prose more coherent?

If the answers are vague, combine, rename, or remove the section.
