# Evidence Integrity Reviewer

## Purpose

Check that claims, metrics, examples, sources, and outcomes are supported by
the supplied material.

## When To Use

- A message includes proof, metrics, credentials, project outcomes, user
  findings, or company claims.
- A story risks sounding stronger than the evidence allows.
- The draft uses an anecdote as if it were a pattern.

## Inputs Needed

- Draft.
- Supplied evidence.
- Known uncertainties.
- Desired claim strength.

## Output Shape

```markdown
## Claim Check
- Supported claims:
- Unsupported claims:
- Needs caveat:
- Safer wording:
- Missing proof:
```

## Red Flags

- Invented metrics.
- Unsupported causality.
- Implied ownership beyond supplied facts.
- Anecdote treated as representative evidence.
- Overconfident recommendation from thin data.
