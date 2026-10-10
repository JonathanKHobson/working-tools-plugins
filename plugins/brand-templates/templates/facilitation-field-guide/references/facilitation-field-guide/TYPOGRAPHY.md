# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `3ad0c2d819ddd0aaeb6d533f9f0bf6c5e35f2559993607381fa74401f09f515b` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 48 paragraphs; base `None`): font `Arial`, 12.0 pt, bold=None, italic=None; before=None pt, after=7.0 pt, line=1.1416666666666666×, keep-next=None; color=#000000. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 3 paragraphs; base `Normal`): font `Arial`, 20.0 pt, bold=True, italic=None; before=13.0 pt, after=7.0 pt, line=1.1416666666666666×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 13 paragraphs; base `Normal`): font `Arial`, 13.0 pt, bold=True, italic=None; before=13.0 pt, after=7.0 pt, line=1.1416666666666666×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `Arial`, 26.0 pt, bold=None, italic=None; before=None pt, after=14.0 pt, line=1.1416666666666666×, keep-next=None; color=#000000. Source: `word/styles.xml`.
- **Subtitle** (`Subtitle`, 1 paragraphs; base `Normal`): font `Arial`, 12.0 pt, bold=None, italic=False; before=None pt, after=7.0 pt, line=1.1416666666666666×, keep-next=None; color=#000000. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Arial, Arial, Arial, Arial, Arial. The local PDF (`office-pdf/facilitation-field-guide.pdf`, SHA-256 `e5b36b6ccfc0b2526568cbe41b114760535bbe4a150b48020e50fa2b9fb907c4`) has font resources Carlito, Carlito-Bold, LiberationSans, LiberationSans-Bold; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
