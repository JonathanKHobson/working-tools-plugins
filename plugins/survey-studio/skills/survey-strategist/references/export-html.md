# HTML Export

## Best for

Standalone instrument review and local control/required-answer checks, plus a starting point for a web implementation. The export explicitly identifies itself as a preview: it does not send/save answers, apply branching, or validate destination-specific rules. Test actual respondent flow in the destination platform.

## Production caution

A static HTML file does not provide secure storage, authentication, consent records, rate limiting, server-side validation, anti-fraud controls, privacy governance, or a compliant data pipeline. Treat it as a prototype unless integrated into an approved application.

Generate:

```bash
python scripts/export_survey.py survey.yaml survey.html --format html
```

The generated file uses semantic headings, labels, fieldsets/legends, native inputs, required indicators, and notes about unsupported behavior. Extend with server-side processing only after security/privacy review.

## Required implementation qualities

- valid document language/title/viewport;
- unique IDs and label associations;
- fieldset/legend for grouped choices;
- keyboard-visible focus and logical order;
- inline instructions and error association;
- no placeholder-only labels;
- mobile reflow and sufficient touch targets;
- progressive enhancement rather than JavaScript-only basics;
- safe escaping of survey content;
- Content Security Policy and secure transport in production;
- explicit handling of logic, save/resume, submission, and confirmation.

## QA

Validate HTML, run automated accessibility checks, then manually test keyboard, screen reader, zoom/reflow, mobile, error states, logic, and submission. Inspect DOM IDs, required state, option values, and hidden content. Never inject untrusted respondent or survey text as raw HTML.
