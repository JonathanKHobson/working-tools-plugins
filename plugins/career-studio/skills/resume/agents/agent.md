# Resume Crafter Agents

These are prompt-role files, not executable agents. Use them when a resume task benefits from a focused specialist lens.

## Available Roles

- `resume-strategist.md`: overall positioning, section order, target-role fit, and recruiter story.
- `bullet-editor.md`: bullet rewrites, verb choice, compression, and proof density.
- `ats-auditor.md`: parser-safe formatting, headings, keywords, and file hygiene.
- `evidence-integrity-reviewer.md`: unsupported claims, metrics, ownership, dates, and defensibility.
- `resume-design-advisor.md`: layout direction, visual hierarchy, and design tradeoffs.

## Coordination Pattern

For a full resume:

1. Resume Strategist sets positioning and section order.
2. Bullet Editor improves experience content.
3. ATS Auditor checks structure and formatting.
4. Evidence Integrity Reviewer blocks unsafe claims.
5. Resume Design Advisor suggests a submission-safe design direction.

For a single bullet:

1. Bullet Editor drafts options.
2. Evidence Integrity Reviewer checks truth and metric safety.

For a resume audit:

1. ATS Auditor checks parseability.
2. Resume Strategist checks target fit.
3. Evidence Integrity Reviewer checks defensibility.

## Handoff Rule

Each role should return concise findings and specific edits. Do not create parallel full resumes unless the user explicitly asks for variants.

## Truth Handoff Rule

Prior truth corrections travel forward. If the Evidence Integrity Reviewer or
the candidate softened, cut, or corrected a claim, later roles should preserve
that change unless new evidence supports a stronger version. Final audit passes
should list any strengthened claims and the evidence for each upgrade.
