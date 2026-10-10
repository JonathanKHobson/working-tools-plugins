# Plain-Text Export

## Best for

Email/plain-text review, archival, copy/paste, low-tech environments, and platform-specific TXT formats with documented syntax.

## Design

Use UTF-8, explicit question IDs, blank lines between items, unambiguous option markers, and plain labels for required/optional status. Avoid relying on indentation alone. Keep a separate codebook when values differ from labels.

Generate generic text:

```bash
python scripts/export_survey.py survey.yaml survey.txt --format text
```

Qualtrics Simple/Advanced TXT are not generic text exports; use their dedicated references and validator.

## QA

- identify encoding and reject UTF-16 for Qualtrics;
- inspect line endings and trailing whitespace;
- verify no smart punctuation breaks the target system;
- preserve question/choice order and IDs;
- ensure long lines wrap acceptably in the delivery channel;
- test import rather than assuming visually plausible text is valid.
