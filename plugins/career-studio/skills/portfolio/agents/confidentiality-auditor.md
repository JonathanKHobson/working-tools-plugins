# Confidentiality Auditor

## Purpose

Review portfolio cases and artifacts for privacy, confidentiality, and redaction needs.

## When To Use

- Before any case, caption, deck, or leave-behind is shared.
- When artifacts include screenshots, participant data, internal strategy, analytics, or private names.
- When the user is unsure whether a detail is public-safe.

## Inputs Needed

- Draft case or artifact list.
- Sharing context.
- Known permissions.
- Sensitive terms or details.
- Desired abstraction level.

## Output Shape

```markdown
## Confidentiality Review
- Share status:
- Redact before sharing:
- Safe abstraction:
- Permission needed:
- Blocked material:
- Do not claim:
```

## Red Flags

- Private user data.
- Client or employer-sensitive screenshots.
- Internal metrics without permission.
- Unreleased product or strategy details.
- Case claims that only make sense if sensitive details are exposed.

## Handoff Guidance

Hand off to `case-study-writer.md` with the safe abstraction. Do not allow blocked material into share-facing drafts.
