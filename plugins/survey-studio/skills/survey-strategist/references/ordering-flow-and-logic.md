# Ordering, Flow, and Logic

## Respondent journey

A typical research survey follows:

1. invitation/landing context;
2. consent and privacy essentials;
3. eligibility/screener;
4. recent behavior and concrete experience;
5. primary outcomes;
6. diagnostic drivers and open-ended follow-up;
7. concept or sensitive modules when applicable;
8. demographics/segmentation only as needed;
9. thank-you, support, withdrawal/contact, and incentive details.

This is a starting pattern, not a law. Eligibility must precede ineligible content; experimental exposure and validated instruments may require controlled ordering.

## Context and order effects

Earlier questions can teach terminology, prime concerns, anchor numbers, or make identity salient. Protect primary outcomes from unnecessary context. When order itself is not substantive, randomize blocks or items only if:

- dependencies remain valid;
- interpretation is stable in any order;
- scale scoring permits it;
- the analysis records the order;
- the platform implements randomization correctly.

## Branching

Use display/skip logic to reduce irrelevance. For every branch specify:

- source question and coded condition;
- destination or displayed block;
- behavior for missing/refused answers;
- back-button behavior;
- whether quotas or termination apply;
- how skipped values appear in exports.

Do not require an item that can be hidden. Do not reference a future question. Avoid loops and logic based on labels that may be translated; use stable codes.

## Pages and progress

Group a small coherent task per page. One question per page can reduce visual complexity but increase navigation and conceal length; long pages can create scrolling and loss. Test on target devices. Progress bars should reflect logic-aware remaining burden or be omitted if misleading.

## Screeners

- Ask only criteria required for eligibility or quotas.
- Conceal the desired answer by using balanced categories and indirect ordering when gaming risk matters.
- Terminate respectfully without revealing sensitive rationale.
- Preserve enough disposition data to report recruitment flow without retaining unnecessary personal data.

## Sensitive modules

Explain why the information is requested, make optional when possible, provide refusal, place after trust is established, and offer support resources when the topic can cause distress. Do not place sensitive disclosures immediately before an identifying contact form unless necessary and clearly explained.

## Randomization cautions

Randomize choice order when order could create primacy/recency bias and no inherent order exists. Keep fixed:

- ordinal ranges;
- chronological stages;
- “none/other/prefer not” anchors, usually at the end;
- response scales requiring consistent direction;
- validated measures when their protocol specifies order.

## Path testing

Test at least:

- eligible common path;
- each ineligible/terminate path;
- each branch condition, including multi-select combinations;
- missing/refusal and “none” paths;
- minimum/maximum validation;
- mobile/keyboard/screen reader path;
- language variants;
- save/resume and back navigation;
- randomization repetitions;
- quota full and duplicate invitation behavior;
- final export values for every path.

Create a path table with input choices, expected pages/questions, termination status, and exported fields. A preview alone is not a logic test.
