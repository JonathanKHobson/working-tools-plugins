# Artifact Caption Editor

## Purpose

Write captions and alt text that make artifacts function as proof.

## When To Use

- A case includes screenshots, diagrams, decks, prototypes, reports, maps, or worksheets.
- Captions are vague labels.
- The user needs a caption set for a case card, leave-behind, or deck.

## Inputs Needed

- Artifact name and type.
- What the artifact shows.
- Why it mattered.
- Decision influenced.
- Alt text needs.
- Confidentiality status.

## Output Shape

```markdown
## Artifact Caption Set

### [Artifact]
- Caption:
- Alt text:
- Use context:
- Redaction notes:
- Missing context:
```

## Red Flags

- Captions imply unsupported outcomes.
- Captions describe visuals but not decisions.
- Alt text is promotional instead of descriptive.
- Sensitive visual details are not redacted.

## Handoff Guidance

Hand off to `evidence-integrity-reviewer.md` if the caption makes a claim. Hand off to `confidentiality-auditor.md` if the artifact includes sensitive detail.
