# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `0d61f0bb50a8e836f5ada26f3a3462bc58c34d9ac995a32711ae7971dd52f1ff` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 32 paragraphs; base `None`): font `Georgia`, 13.5 pt, bold=False, italic=None; before=0.0 pt, after=10.0 pt, line=1.1208333333333333×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 1 paragraphs; base `Normal`): font `Baskerville`, 46.0 pt, bold=True, italic=None; before=0.0 pt, after=8.0 pt, line=1.1208333333333333×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 4 paragraphs; base `Normal`): font `Baskerville`, 29.0 pt, bold=True, italic=None; before=0.0 pt, after=9.0 pt, line=1.1208333333333333×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 3** (`Heading3`, 10 paragraphs; base `Normal`): font `Baskerville`, 19.0 pt, bold=True, italic=None; before=0.0 pt, after=7.0 pt, line=1.1208333333333333×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **News Label** (`NewsLabel`, 6 paragraphs; base `None`): font `Arial`, 10.5 pt, bold=True, italic=None; before=0.0 pt, after=7.0 pt, line=1.1208333333333333×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **News Deck** (`NewsDeck`, 3 paragraphs; base `None`): font `Georgia`, 16.0 pt, bold=False, italic=None; before=0.0 pt, after=11.0 pt, line=1.1208333333333333×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **News Note** (`NewsNote`, 8 paragraphs; base `None`): font `Arial`, 11.5 pt, bold=False, italic=None; before=0.0 pt, after=10.0 pt, line=1.1208333333333333×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **News Issue** (`NewsIssue`, 2 paragraphs; base `None`): font `Arial`, 11.5 pt, bold=True, italic=None; before=0.0 pt, after=11.0 pt, line=1.1208333333333333×, keep-next=False; color=#000000. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Georgia, Baskerville, Baskerville, Baskerville, Arial, Georgia, Arial, Arial. The local PDF (`office-pdf/community-newspaper.pdf`, SHA-256 `093a18bfdb5e028de1fdf206f1d4c7511c337ec7ab66caa0cb27ef2006613f62`) has font resources FrankRuhlHofshi-Bold, LiberationSans, LiberationSans-Bold, LinuxLibertineG; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
