# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `9da71d8ed9d641d7478043293b3034f78cf65acddc57aa9e666be07078292d0d` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 23 paragraphs; base `None`): font `IBM Plex Sans`, 11.5 pt, bold=False, italic=False; before=0.0 pt, after=6.0 pt, line=15.0 pt, keep-next=None; color=#172D47. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 8 paragraphs; base `Normal`): font `IBM Plex Mono SmBld`, 16.0 pt, bold=False, italic=False; before=15.0 pt, after=9.0 pt, line=20.0 pt, keep-next=True; color=#172D47. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 1 paragraphs; base `Normal`): font `IBM Plex Sans`, 12.5 pt, bold=True, italic=False; before=12.0 pt, after=7.0 pt, line=16.0 pt, keep-next=True; color=#172D47. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `IBM Plex Mono SmBld`, 24.0 pt, bold=False, italic=False; before=0.0 pt, after=14.0 pt, line=28.0 pt, keep-next=None; color=#172D47. Source: `word/styles.xml`.
- **Subtitle** (`Subtitle`, 1 paragraphs; base `Normal`): font `IBM Plex Mono`, 10.5 pt, bold=False, italic=False; before=0.0 pt, after=10.0 pt, line=13.0 pt, keep-next=None; color=#172D47. Source: `word/styles.xml`.
- **Caption** (`Caption`, 3 paragraphs; base `Normal`): font `IBM Plex Sans`, 10.5 pt, bold=False, italic=False; before=0.0 pt, after=8.0 pt, line=13.0 pt, keep-next=None; color=#172D47. Source: `word/styles.xml`.
- **Table Body** (`TableBody`, 82 paragraphs; base `None`): font `IBM Plex Sans`, 11.5 pt, bold=False, italic=False; before=0.0 pt, after=0.0 pt, line=15.0 pt, keep-next=None; color=#172D47. Source: `word/styles.xml`.
- **Diagram** (`Diagram`, 18 paragraphs; base `None`): font `IBM Plex Mono`, 11.0 pt, bold=False, italic=False; before=0.0 pt, after=6.0 pt, line=14.0 pt, keep-next=None; color=#172D47. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include IBM Plex Sans, IBM Plex Mono SmBld, IBM Plex Sans, IBM Plex Mono SmBld, IBM Plex Mono, IBM Plex Sans, IBM Plex Sans, IBM Plex Mono. The local PDF (`office-pdf/applied-ai-workflow-case.pdf`, SHA-256 `9bab247b278e56575b9a72d2e351d208e1b1b8b9f4c7e8b9a280ebbb7e243fb6`) has font resources IBMPlexMono, IBMPlexMono-SmBld, IBMPlexSans, IBMPlexSans-Bold; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
