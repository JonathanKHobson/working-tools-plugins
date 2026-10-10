# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `509bcb3256c5c3837ff2123c9e29d08a8e51fc71e509ab8f8efa97c1f17c5477` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 5 paragraphs; base `None`): font `Arial`, 11.0 pt, bold=False, italic=None; before=0.0 pt, after=2.0 pt, line=1.0291666666666666×, keep-next=False; color=#171B20. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 5 paragraphs; base `Normal`): font `Arial`, 11.5 pt, bold=True, italic=None; before=8.0 pt, after=4.0 pt, line=1.0291666666666666×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 2 paragraphs; base `Normal`): font `Arial`, 11.5 pt, bold=True, italic=None; before=5.0 pt, after=2.0 pt, line=1.0291666666666666×, keep-next=True; color=#142D41. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `Arial`, 28.0 pt, bold=True, italic=None; before=0.0 pt, after=2.0 pt, line=1.0291666666666666×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **TS Notice** (`TSNotice`, 1 paragraphs; base `None`): font `Arial`, 10.0 pt, bold=False, italic=None; before=0.0 pt, after=4.0 pt, line=1.0291666666666666×, keep-next=True; color=#47535D. Source: `word/styles.xml`.
- **TS Headline** (`TSHeadline`, 1 paragraphs; base `None`): font `Arial`, 12.0 pt, bold=True, italic=None; before=0.0 pt, after=3.0 pt, line=1.0291666666666666×, keep-next=True; color=#142D41. Source: `word/styles.xml`.
- **TS Contact** (`TSContact`, 1 paragraphs; base `None`): font `Arial`, 10.0 pt, bold=False, italic=None; before=0.0 pt, after=1.0 pt, line=1.0291666666666666×, keep-next=False; color=#47535D. Source: `word/styles.xml`.
- **TS Context** (`TSContext`, 2 paragraphs; base `None`): font `Courier New`, 10.0 pt, bold=False, italic=None; before=0.0 pt, after=3.0 pt, line=1.0291666666666666×, keep-next=True; color=#47535D. Source: `word/styles.xml`.
- **TS Evidence** (`TSEvidence`, 10 paragraphs; base `None`): font `Arial`, 11.0 pt, bold=False, italic=None; before=0.0 pt, after=2.0 pt, line=1.0291666666666666×, keep-next=False; color=#171B20. Source: `word/styles.xml`.
- **TS Dates** (`TSDates`, 3 paragraphs; base `None`): font `Arial`, 10.0 pt, bold=False, italic=None; before=0.0 pt, after=2.0 pt, line=1.0291666666666666×, keep-next=True; color=#47535D. Source: `word/styles.xml`.
- **TS Role** (`TSRole`, 2 paragraphs; base `None`): font `Arial`, 11.0 pt, bold=True, italic=None; before=4.0 pt, after=1.0 pt, line=1.0291666666666666×, keep-next=True; color=#171B20. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Arial, Arial, Arial, Arial, Arial, Arial, Arial, Courier New, Arial, Arial, Arial. The local PDF (`office-pdf/technical-signal.pdf`, SHA-256 `7eb4d1d7b93c6401990e670bbf309a5577e8d088fea7f86a0adbbbd83003d91f`) has font resources LiberationMono, LiberationSans, LiberationSans-Bold; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
