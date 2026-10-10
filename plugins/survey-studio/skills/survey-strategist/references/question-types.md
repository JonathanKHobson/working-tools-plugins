# Question Types

Choose a type because it matches the construct and analysis—not because the platform offers it. Availability and behavior vary by platform and device.

## Common types

| Type | Strong use | Advantages | Main risks |
|---|---|---|---|
| Single choice | One mutually exclusive category | fast, clear, simple coding | false exclusivity; missing category |
| Multiple choice | Any applicable categories | captures co-occurrence | ambiguous “select all”; order effects |
| Yes/No | genuine binary state | minimal effort | hides uncertainty and nuance |
| Dropdown | long, familiar list such as country | compact | poor discoverability/accessibility; hard comparison |
| Text entry | brief verbatim fact | flexible | inconsistent spelling/format; PII |
| Open-ended/essay | explanation, unknown category, diagnostic | respondent language and nuance | high burden and coding cost |
| Text/graphic/descriptive | instructions, consent, stimulus | provides context | can persuade or overload |
| Rating/Likert item | ordered intensity/frequency/agreement | easy comparison | scale interpretation and acquiescence |
| Likert matrix | same construct/scale across related statements | space efficient | straightlining, mobile/accessibility burden |
| Bipolar semantic differential | position between meaningful opposites | captures connotative perception | “opposites” may not be true endpoints |
| Slider/graphical slider | continuous-feeling judgment | engaging in some contexts | inaccessible, imprecise, hidden default |
| Star rating | familiar lightweight evaluation | fast and recognizable | platform/cultural conventions vary |
| NPS | 0–10 recommendation item in an established program | trend continuity and familiar reporting | weak diagnosis; arbitrary category compression |
| Rank order | force relative priority | reveals ordering | cognitively demanding; no distance between ranks |
| Constant sum | allocate a fixed budget/importance | expresses tradeoffs | arithmetic burden and validation errors |
| MaxDiff/best–worst | discriminate relative importance among many items | reduces scale-use bias | requires experimental design/modeling |
| Side by side | compare related item groups | compact comparisons | complexity and mobile burden |
| Form fields | structured identity/contact/attributes | operationally organized | tedious; nested PII risk |
| Drill-down/cascading choice | hierarchical geography/product selection | manages long taxonomy | inaccessible or fragile hierarchy |
| Pick, group, and rank | classify then prioritize | rich preference structure | very high cognitive/interface burden |
| File upload | documents, images, evidence | direct artifact collection | malware, storage, accessibility, privacy |
| Signature | attestation or consent workflow | explicit acknowledgement | identity/legal implications; not universal consent proof |
| Heat map/hotspot | select image regions | spatial feedback | image interpretation and accessibility |
| Highlight | mark words/passages | precise content feedback | needs accessible alternative and coding plan |
| Screen capture | visual bug/context evidence | diagnostic richness | captures unrelated private information |
| Video/audio response | rich expressive feedback | tone/context | bandwidth, moderation, consent, transcription |
| Timing | measure page/item time | diagnostic metadata | not equivalent to attention or quality |
| CAPTCHA/verification | deter automation | improves some fraud resistance | accessibility and legitimate-user friction |
| Metadata | device, browser, source, timestamps | operational context and QA | notice, consent, accuracy, fingerprinting |

## Matrix variants

- **Single-answer matrix:** one column per row; use only when all rows share a valid scale.
- **Multiple-answer matrix:** independent selections across columns; often harder to interpret than separate items.
- **Rank-order matrix:** ranks within rows/columns; high burden.
- **Constant-sum matrix:** allocations across dimensions; use sparingly.
- **Text-entry matrix:** structured verbatims; creates many sparse fields.

Avoid matrices with long row labels, more than roughly 5–7 rows, many columns, mixed constructs, or mobile-first audiences. The exact threshold depends on content and testing.

## Type selection questions

1. Is the construct categorical, ordinal, interval-like, continuous, textual, spatial, or behavioral?
2. Must categories be exclusive, or can several be true?
3. Does the respondent know the answer at the requested precision?
4. What analysis will be performed?
5. Can the control be completed with keyboard, screen reader, touch, and low bandwidth?
6. Does the platform export stable codes?
7. What happens when no option fits?

## Creative formats

Use sliders, stars, images, games, cards, or conversational forms only when they improve comprehension or motivation for the target population and have an accessible equivalent. Novelty is not evidence quality.

## Source inventory

The historical user-provided QuestionTypes.txt inventory is excluded because its author/source grant is unverified. Common format names are taxonomy labels; this reference retains the complete original construct, analysis, accessibility and burden safeguards. Bring authorized source material when a particular proprietary or validated instrument is needed.
