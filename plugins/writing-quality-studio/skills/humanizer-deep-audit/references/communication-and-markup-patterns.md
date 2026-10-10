# Communication and Markup Patterns

Use this guide when text still contains the conversation, prompt, workflow, or interface that produced it.

## Contents

- Prompt-recipient residue
- Model limitation residue
- Unsupported absence claims
- Unfilled scaffolds
- Destination syntax mismatch
- Internal tool artifacts
- Institutional overperformance
- Summary proportionality
- Profile and reviewer templates
- Historical residue and truncation

## Prompt-recipient residue

Common phrases include `Of course`, `Certainly`, `You're absolutely right`, `I hope this helps`, `Would you like`, `Let me know`, `Is there anything else`, `Here is a detailed breakdown`, and `Below is an overview`.

These may be perfectly natural in correspondence. They are residue when pasted into an article, report, lesson, product page, proposal, or database field.

**Residue:** Here is a detailed overview of the proposed policy. I hope this helps clarify the key issues.

**Deliverable:** The proposal changes the review period from 30 days to 14.

**Residue:** In this section, we will discuss the relevant literature and provide a comprehensive understanding of the topic.

**Deliverable:** Three studies tested the intervention; none followed participants beyond six months.

Also remove advice addressed to the prompt user:

- “You can copy and paste this into…”
- “Customize the placeholders below.”
- “If you plan to submit this…”
- “Would you like me to convert this to…”
- “Delete this section before publishing.”
- “Final important tip…”

If the document genuinely is a how-to, rewrite the advice for its actual reader and verify every step.

## Model limitation residue

Watch for `as of my last knowledge update`, `up to my training cutoff`, `I don't have access to`, `based on the provided search results`, and `as an AI language model`.

**Residue:** As of my last knowledge update, I do not have specific information about the clinic’s current status.

**Deliverable:** The supplied sources end in March 2023; current status is unverified.

The repair names the evidence boundary, not the model’s biography.

## Unsupported absence claims

Retrieval failure is not evidence that information does not exist.

Watch for:

- “not widely documented”;
- “details remain scarce”;
- “specific information is limited”;
- “the person maintains a low profile”;
- “the company has not publicly disclosed”;
- “likely due to limited mainstream exposure.”

**Weak:** Details of Chen’s early life are not widely documented because she maintains a private profile.

**Better:** The supplied sources do not describe Chen’s early life.

**Weak:** Lyrics are unavailable, likely because the release had little mainstream exposure; the themes can be inferred from the track titles.

**Better:** No lyrics were supplied. Do not infer lyrical themes from titles alone.

## Unfilled scaffolds

Scan for square-bracket prompts, fake values, generic tokens, and partial template prose:

- `[Your Name]`, `[Company]`, `[insert detail]`, `[link]`;
- `2025-XX-XX`, `YYYY-MM-DD`;
- `URL`, `SOURCE_PUBLISHER`, `INSERT_SOURCE_URL_30`;
- `PASTE_*_HERE`;
- `lorem ipsum`, `TBD`, `TK`, `XXX`;
- empty fields followed by comments such as “Add if available with citation.”

**Before:** Contact [Your Name] at [Email Address] to schedule a consultation.

**After:** Contact information missing. Do not publish until the owner supplies it.

Do not silently guess a date, link, employer, award, title, or citation.

## Destination syntax mismatch

Identify the destination before formatting:

- Markdown uses `#` headings, `**bold**`, `[label](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)`, and fenced code blocks.
- MediaWiki uses equals-sign headings, apostrophe emphasis, and bracket-based links.
- HTML uses elements and attributes.
- Plain-text forms may reject all three.
- Rich-text editors may convert typography automatically.

**Mixed residue:** a ` ```wikitext ` fenced block containing attempted MediaWiki syntax, surrounded by Markdown instructions.

**Repair:** deliver only valid destination syntax, validate it with the destination parser or preview, and remove explanatory wrappers unless requested.

Broken syntax is not merely cosmetic. It can hide links, misnumber sections, create phantom categories, or leave template parameters inert.

## Internal tool artifacts

These strings are high-confidence interface residue and should be removed only after recovering or verifying the intended citation or object:

### ChatGPT/OpenAI-style

- `contentReference`
- `oaicite` or `oai_citation`
- `turn0search0`, `turn1file0`, `turn0image0`, `turn0news0`
- `attributableIndex`
- private-use citation wrappers such as `cite…`
- short private-use markers such as `0`
- malformed aggregation labels such as `Source+3` or `Wikipedia+1`

### Gemini-style

- `[cite: 1]` or `[cite: 3, 12]`
- `[span_1][start_span]`
- `(start_span)` and `(end_span)` wrappers

### Grok-style

- `<grok-card ...>`
- `grok_render_citation_card_json`
- `referrer=grok.com`

### DeepSeek-style

- lenticular citations such as `【85†L261-269】`

### Perplexity-style

- `[attached_file:1]`
- `[web:1]`
- `ppl-ai-file-upload` URLs

### Other wrappers

- `:::writing{variant="document" id="12345"}`
- localized variants of the same wrapper

Never delete an artifact and leave an unsupported claim. Use it as a pointer to source recovery. If the original source cannot be recovered, mark the claim unverified.

## Destination object validation

In systems with templates, categories, fields, components, or workflow states, plausible names may still be nonexistent.

Check:

- category exists and is the correct canonical form;
- template/component exists;
- parameter/property name is supported;
- field value belongs to the accepted vocabulary;
- workflow state is valid for the current stage;
- protection, review, or maintenance tag reflects reality.

**Weak:** Add a plausible `Infobox ancient population` without checking that the template exists.

**Better:** Search the template registry, choose the closest valid template, and use only documented parameters.

## Institutional overperformance

A comment or proposal may recite policy language without demonstrating knowledge of the actual rule.

Watch for:

- made-up shortcuts or policy names;
- maintenance banners pasted where the writer meant to mention them;
- long titled comments for a minor disagreement;
- repeated assurances that text “adheres to,” “aligns with,” “complies with,” “follows,” or “meets” every standard;
- requests for other people to say exactly what must be fixed when the draft already claims full compliance;
- accusations that style concerns are invalid because no detector proof was offered.

**Weak:** I revised the section to ensure neutrality, verifiability, encyclopedic tone, and full compliance with all applicable guidelines.

**Better:** Removed “industry-leading” and attributed the 18 percent estimate to the regulator’s June report.

Demonstrate compliance through a specific change.

## Summary proportionality

Short change summaries should describe the change, not perform diligence.

**Weak:** I revised the content to provide a neutral and informative description while preserving all relevant details and ensuring compliance with style and sourcing requirements.

**Better:** Replaced the product claims with specifications from the June filing.

**Weak:** Expanded the article with sourced information, references, and internal and external links.

**Better:** Added the 2018 merger and 2021 plant closure.

Prompt-constraint residue often mentions what was `preserved`, `retained`, or `left unchanged`. Include that only when it matters to reviewers, such as a behavior-preserving code refactor or a legal redline.

## Profile and reviewer templates

### Canned profiles

Watch for `Welcome to my page`, `About me`, `My interests`, `What I'm working on`, `Let's connect`, `Happy editing`, a field of emoji, and vague claims about accuracy or collaboration.

**Weak:** I am passionate about technology, culture, history, and making a positive impact through accurate information.

**Better:** I edit Arizona transit history and photograph surviving bus depots built before 1960.

Specific interests and actual work make a profile useful.

### Reviewer-facing residue

Remove declarations that a draft is “neutral and well-sourced,” meets every policy, or should be accepted. Give reviewers the draft and the sources. In workflow systems, do not pre-place rejection, approval, protection, or maintenance states that only a reviewer can set.

## Historical residue and truncation

Older patterns include:

- `It is important/crucial to note`;
- `It is worth remembering`;
- a safety or jurisdiction disclaimer addressed to an imagined reader;
- `In summary` and `In conclusion` restatements;
- `I'm sorry, but as an AI language model…`;
- abrupt cutoffs at the end of a sentence or section;
- access dates much older than the document’s creation date.

**Weak:** It is important to note that laws may vary by jurisdiction, so readers should consult a professional.

**Better:** Arizona requires notice within 30 days. This draft does not address other jurisdictions.

Inspect abrupt endings before editing; truncation may also come from copy/paste failure, file corruption, or a source excerpt.
