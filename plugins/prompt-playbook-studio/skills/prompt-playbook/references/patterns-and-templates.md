# Select a useful pattern

Use the smallest scaffold that makes the request actionable. Fields are conditional. Do not force a seven-section packet onto routine work.

| Situation | Pattern | Decision that matters |
| --- | --- | --- |
| A draft already exists | Refine without changing intent | Preserve requirements and identify only material edits. |
| A messy brief contains many threads | Intent plus constraint sweep | Distinguish required outcomes, optional ideas, exclusions and approval limits. |
| Domain judgment is needed | Functional role | State the expertise needed, rather than inventing credentials or authority. |
| Many style adjectives compete | Ranked traits | Prioritize the few traits that affect the output; preserve explicit requirements. |
| Items need comparison across axes | Multi-axis organizer | Define primary axis, secondary axis, tie break and missing-data treatment. |
| A broad synthesis is requested | Evidence-led synthesis | Name the artifact, source scope, uncertainty and success criteria; do not fabricate personal history. |
| A previous answer nearly works | Targeted follow-up | Identify the exact failed condition; change that condition while keeping the accepted parts. |

## Reusable prompt shapes

**Refine:** “Revise the supplied prompt while preserving its goal, audience, required output and authorization limits. Fix the observed problem: [failure]. Return the revised prompt and the material changes. Source prompt: [quoted draft].”

**Build:** “Produce [deliverable] for [audience/use]. Use [supplied inputs] as [evidence/context]. Preserve [requirements]. Exclude [out-of-scope work]. Return [format]. Completion is verified by [observable check]. If [material input] is missing, [ask/mark missing/use stated assumption].”

**Compare:** “Compare [items] on [primary criterion], then [secondary criterion], using [source scope]. Mark missing evidence. Apply [tie break]. Return [table/list] with [supporting evidence]. Success means [decision-ready condition].”

**Repair:** “The previous result failed [specific requirement]. Keep [accepted facts/format/behavior]. Revise only [affected part] and verify [test]. Do not infer that this authorizes [unrelated external action].”

For structured output, specify field names, types, allowed values and missing-value behavior only when a consumer needs them. Example values must be clearly synthetic. Distinguish invalid input from an empty result. Validate syntax mechanically where possible; semantic correctness still needs evidence.

## Constraint preservation

Check each consequential source requirement against the revised text: scope, evidence, deliverable, audience, deadline, exclusions, permissions, success test and output shape. Preserve exact wording when precision matters; otherwise preserve meaning. Flag contradictory requirements instead of silently choosing one. A suggested next step is not evidence that the user approved it. For an auditable handoff with exact source fingerprints and constraint mappings, use the optional compiler documentation.

For a prompt involving persuasion or access to accounts, do not design deceptive impersonation, covert manipulation or credential theft; offer a transparent alternative. For medical, legal, financial, employment or similarly high-impact decisions, state uncertainty and include a proportionate qualified human review before the output is relied on. This review concerns consequential use of the output; it does not create a new approval step for an ordinary authorized prompt edit or task.
