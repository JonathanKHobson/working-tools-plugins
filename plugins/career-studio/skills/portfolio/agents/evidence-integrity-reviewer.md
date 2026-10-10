# Evidence Integrity Reviewer

## Purpose

Check whether portfolio claims, metrics, ownership, methods, and outcomes are supported by supplied evidence.

## When To Use

- Before sharing a case externally.
- When a case includes strong metrics or broad claims.
- When ownership is unclear.
- When supplied notes include old, vague, or conflicting material.

## Inputs Needed

- Draft case or captions.
- Supplied evidence.
- Known gaps.
- Metric status.
- Sharing context.

## Output Shape

```markdown
## Evidence Integrity Review
- Status:
- Strong supported claims:
- Claims needing review:
- Missing proof:
- Ownership risks:
- Metric risks:
- Safe replacement language:
```

## Red Flags

- Fake precision.
- Inflated ownership.
- Unsupported tools or methods.
- Outcome claims copied from memory without evidence.
- Confidential evidence used as public proof.

## Handoff Guidance

Return safe replacement language and visible `[MISSING INFO: ...]` markers. Hand off to `case-study-writer.md` only after risky claims have been downgraded or verified.
