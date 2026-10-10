# Response Options and Scales

Response design is part of measurement. Labels, order, number of points, coding, and missing options can change results.

## Choice-set quality

A closed list should be:

- **mutually exclusive** for single-choice items;
- **collectively sufficient** for the target population;
- expressed at one conceptual level;
- ordered logically when an order exists;
- free of overlapping ranges;
- coded with stable, non-semantic IDs or deliberate numeric values;
- paired with a legitimate escape route when needed.

Bad age bands: `18–25`, `25–34`.

Better: `18–24`, `25–34`, or a validated numeric field if exact age is necessary and proportionate.

## “Other,” “none,” “not applicable,” and refusal

- **Other (please specify):** use when the taxonomy is long-tail and the text will be reviewed/coded. Do not use it to compensate for a poorly researched list.
- **None of these:** use when zero categories can apply; make exclusive in multi-select.
- **Not applicable:** use when the construct legitimately does not apply.
- **Don’t know/not sure:** use when knowledge uncertainty is meaningful.
- **Prefer not to answer:** use for sensitive disclosure; distinguish it from missing/no response.

## Ordered scales

### Choose the construct before the scale

Agreement, satisfaction, ease, importance, frequency, likelihood, confidence, trust, and quality are not interchangeable. Ask directly about the construct rather than converting every statement into agree/disagree.

### Label points

Fully labeled scales reduce ambiguity, especially for accessibility and translation. At minimum, label endpoints and any meaningful midpoint, but test whether unlabeled intermediate points will be interpreted consistently.

### Balanced scales

Use comparable positive and negative range when both are plausible. A scale from “good” to “excellent” cannot measure poor experience.

### Midpoints

Include a midpoint when a substantively neutral position exists and respondents can hold it. Removing a midpoint does not create a genuine opinion; it forces classification. Keep “not applicable” separate from neutral.

### Number of points

There is no universal optimum. Use enough points to capture meaningful distinctions that respondents can make, maintain continuity with a valid trend measure, and support the analysis. Five- or seven-point verbal/ordered scales are common; 0–10 may be appropriate for established measures or fine-grained judgments.

### Direction

Keep low-to-high direction consistent across the instrument. Reverse-scored items may reduce some response patterns but increase mistakes and method effects; use them only when required by a validated measure or supported design.

## Frequency response options

Prefer numeric or behaviorally defined categories over vague adverbs. “Often” means different things across respondents and behaviors.

Example for a 30-day window:

- 0 days
- 1–2 days
- 3–5 days
- 6–10 days
- 11–20 days
- 21–30 days
- Not sure

Set boundaries based on expected distribution and analytical needs, not aesthetics.

## Multi-select

“Select all that apply” is easy but can undercount options later in a list. Consider forced yes/no grids, randomized options, or a follow-up “main reason” item when priority matters. Keep exclusive options programmatically exclusive.

## Ranking and allocation

Ranking indicates order, not magnitude. Constant-sum indicates allocation under an artificial budget. Both are cognitively demanding and should have few items, clear instructions, and validation. Use MaxDiff only with an appropriate experimental design and model.

## Coding rules

- Preserve labels and machine values separately.
- Do not encode meaning solely in column position.
- Reserve explicit missing codes and document them.
- Keep “prefer not,” “not applicable,” “don’t know,” skipped by logic, and technical missing distinct when analysis requires it.
- For multi-select, choose a documented representation: one binary column per choice, delimited values with escaping rules, or normalized response table.
- Freeze codes once fielding begins; version any change.

## Scale QA

Check that minimum is below maximum, step divides the range as intended, anchors correspond to actual values, NPS is 0–10 when called NPS, no hidden default is preselected, and visual control behavior matches exported values.
