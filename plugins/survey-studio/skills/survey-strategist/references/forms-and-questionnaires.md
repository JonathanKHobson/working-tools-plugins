# Forms and Questionnaires

## Distinguish form work from research

A form primarily collects information required to complete a transaction, determine eligibility, register, apply, consent, or deliver a service. A research questionnaire measures constructs to answer a study question. They may share controls, but the legal basis, voluntariness, required fields, and success criteria differ.

## Form design workflow

1. Define the user goal and organizational action.
2. Remove fields that are not required for that action.
3. Use known data only when users can verify/correct it and reuse is appropriate.
4. Ask one coherent thing per page or section when it reduces complexity.
5. Reveal conditional fields only when relevant.
6. Explain why sensitive or unusual information is needed.
7. Validate at the right time with specific recovery guidance.
8. Provide review/confirmation for consequential submissions.
9. Preserve entered data after errors when safe.
10. Confirm submission, next steps, deadlines, and contact channel.

## Labels and instructions

Use persistent visible labels, not placeholder-only labels. Group related controls with fieldset/legend or equivalent semantics. Put format hints before input and error text beside the field plus an error summary. Do not use an asterisk as the only indication of required/optional status.

## Field types

- Use text inputs for identifiers whose leading zeros or formatting matter.
- Use email/telephone input modes for device convenience, but validate flexibly.
- Use date controls only when they work across browsers/locales; offer clear typed format.
- Avoid dropdowns for very short lists and avoid free text for a stable small taxonomy.
- Provide address flexibility for international users.
- Do not split names into first/last when the task does not require that model.
- Allow copy/paste and password managers; do not block them for “security theater.”

## Required fields

A field is required when the service cannot proceed without it, not because analysts prefer completeness. Mark optional fields explicitly. Sensitive fields need a proportionate necessity statement and an alternate path when feasible.

## Error handling

Good error messages state:

- what is wrong;
- where it is;
- how to fix it;
- whether data was preserved.

Avoid blame (“You entered an invalid…”), generic red banners, clearing fields, and validation that fires before the user has had a chance to answer.

## Intake forms

Separate operational contact data from research responses when possible. If staff will triage free text, state expected response time and emergencies policy. Do not invite confidential, health, financial, or account information into an unprotected generic comment box.

## Form QA

Test completion with keyboard and screen reader, zoom/reflow, mobile, slow connection, autofill, unusual names/addresses, copy/paste, browser back, session expiry, duplicate submission, file upload, validation boundaries, and confirmation delivery.
