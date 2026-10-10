# Metrics And Truth

Portfolio metrics must be more careful than marketing copy. A portfolio case can be questioned in an interview, so unsupported numbers create avoidable risk.

## Metric Statuses

Use:

- `verified`: exact number supplied by a reliable source.
- `estimated`: conservative range or calculation path supplied by the user.
- `needs_review`: plausible but not ready for external use.
- `missing`: no number should be used.
- `sensitive`: true or plausible, but permission or redaction is needed.

## Allowed Metric Language

Verified:

```text
Reduced [metric] by [value] after [action], based on [source supplied by user].
```

Estimated:

```text
Estimated [range] improvement based on [calculation path]. Verify before publishing.
```

Missing:

```text
Clarified the decision path and reduced ambiguity around [problem].
```

Sensitive:

```text
Improved a key internal workflow metric; exact numbers withheld pending permission.
```

## Do Not Invent

Do not create:

- fake percentages
- fake user counts
- fake revenue, time, cost, conversion, or satisfaction values
- fake precision from vague notes
- inflated scope from a prototype, recommendation, or draft

## Non-Numeric Impact

When a number is missing, use concrete non-numeric impact:

These are claim candidates, not automatic substitutes for missing metrics. Each
still needs evidence; otherwise describe the observed work or deliverable without
claiming its effect. "Produced a recommendation" does not prove it was adopted.

- clarified a decision
- reduced ambiguity
- exposed a risk
- created a reusable artifact
- aligned stakeholders
- improved handoff quality
- made a workflow testable
- documented tradeoffs
- produced a reviewable recommendation

## Portfolio Metric Audit

For every metric, ask:

- What exactly is being measured?
- Who measured it?
- When was it measured?
- Is it outcome, output, learning, or projection?
- Is it safe to share?
- Can the candidate defend it in an interview?

If not, mark it `needs_review` or replace it with non-numeric language.
