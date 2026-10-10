# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `51de73ffa809c805485616925e8f8370c931b3c150fe96f154567f768f2a61f1` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 56 paragraphs; base `None`): font `Calibri`, 11.5 pt, bold=None, italic=None; before=None pt, after=7.0 pt, line=1.1416666666666666×, keep-next=None; color=#000000. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 4 paragraphs; base `Normal`): font `Georgia`, 23.0 pt, bold=True, italic=None; before=13.0 pt, after=7.0 pt, line=1.1416666666666666×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 14 paragraphs; base `Normal`): font `Georgia`, 15.0 pt, bold=True, italic=None; before=13.0 pt, after=7.0 pt, line=1.1416666666666666×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `Georgia`, 34.0 pt, bold=None, italic=None; before=None pt, after=14.0 pt, line=1.1416666666666666×, keep-next=None; color=#000000. Source: `word/styles.xml`.
- **Subtitle** (`Subtitle`, 1 paragraphs; base `Normal`): font `Calibri`, 12.0 pt, bold=None, italic=False; before=None pt, after=7.0 pt, line=1.1416666666666666×, keep-next=None; color=#000000. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Calibri, Georgia, Georgia, Georgia, Calibri. The local PDF (`office-pdf/community-program-a4-edition.pdf`, SHA-256 `6af88f2b43347808069be0ec057358583c5fc0cf246bd79b2f73e21afdfbc5e9`) has font resources Carlito, Carlito-Bold, FrankRuhlHofshi-Bold, LinuxLibertineG; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
