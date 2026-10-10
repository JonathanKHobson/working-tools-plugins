# Cover Letter Crafter Agents

These are prompt-role files, not executable agents. Use them when a cover-letter task benefits from a focused specialist lens.

## Available Roles

- `cover-letter-strategist.md`: overall arc, target fit, template choice, and paragraph plan.
- `hook-writer.md`: opening paragraph and hook options.
- `proof-editor.md`: compact proof paragraphs and evidence compression.
- `company-fit-auditor.md`: company research, mission fit, referral context, and values-claim safety.
- `evidence-integrity-reviewer.md`: unsupported claims, metrics, ownership, dates, and defensibility.

## Coordination Pattern

For a full cover letter:

1. Cover Letter Strategist chooses the template and paragraph arc.
2. Hook Writer drafts or repairs the opening.
3. Proof Editor builds the evidence paragraph.
4. Company Fit Auditor checks target-specific claims.
5. Evidence Integrity Reviewer blocks unsafe claims.

For an opening rewrite:

1. Hook Writer drafts options.
2. Company Fit Auditor checks whether the target signal is verified.

For a cover-letter audit:

1. Cover Letter Strategist checks the arc.
2. Company Fit Auditor checks target specificity.
3. Evidence Integrity Reviewer checks defensibility.

## Handoff Rule

Each role should return concise findings and specific edits. Do not create parallel full letters unless the user explicitly asks for variants.
