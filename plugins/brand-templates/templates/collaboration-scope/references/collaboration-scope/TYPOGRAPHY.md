# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `5b363251e4ed8cb3a836df7ae3eae5b82a4c1119e2f5b1efbd654a1e8b0213b5` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 64 paragraphs; base `None`): font `Calibri`, 11.5 pt, bold=None, italic=None; before=None pt, after=7.0 pt, line=1.1416666666666666×, keep-next=None; color=#000000. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 3 paragraphs; base `Normal`): font `Calibri`, 18.0 pt, bold=True, italic=None; before=13.0 pt, after=7.0 pt, line=1.1416666666666666×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 12 paragraphs; base `Normal`): font `Calibri`, 13.0 pt, bold=True, italic=None; before=13.0 pt, after=7.0 pt, line=1.1416666666666666×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `Calibri`, 25.0 pt, bold=None, italic=None; before=None pt, after=14.0 pt, line=1.1416666666666666×, keep-next=None; color=#000000. Source: `word/styles.xml`.
- **Subtitle** (`Subtitle`, 1 paragraphs; base `Normal`): font `Calibri`, 12.0 pt, bold=None, italic=False; before=None pt, after=7.0 pt, line=1.1416666666666666×, keep-next=None; color=#000000. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Calibri, Calibri, Calibri, Calibri, Calibri. The local PDF (`office-pdf/collaboration-scope.pdf`, SHA-256 `592b2080b27ae59bebb7d2553e1587726c81cefcea2f4996950dff7017f7e9e8`) has font resources Carlito, Carlito-Bold; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
