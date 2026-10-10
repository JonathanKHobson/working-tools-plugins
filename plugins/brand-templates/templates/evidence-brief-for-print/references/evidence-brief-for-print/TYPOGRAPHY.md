# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `edf2355109230e985edef623a4d68df077681c5f9efd7208a00b2be83d725f8b` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 43 paragraphs; base `None`): font `Cambria`, 12.0 pt, bold=None, italic=None; before=None pt, after=7.0 pt, line=1.1416666666666666×, keep-next=None; color=#000000. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 1 paragraphs; base `Normal`): font `Arial`, 20.0 pt, bold=True, italic=None; before=13.0 pt, after=7.0 pt, line=1.1416666666666666×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 7 paragraphs; base `Normal`): font `Arial`, 14.0 pt, bold=True, italic=None; before=13.0 pt, after=7.0 pt, line=1.1416666666666666×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `Arial`, 29.0 pt, bold=None, italic=None; before=None pt, after=14.0 pt, line=1.1416666666666666×, keep-next=None; color=#000000. Source: `word/styles.xml`.
- **Subtitle** (`Subtitle`, 2 paragraphs; base `Normal`): font `Cambria`, 12.0 pt, bold=None, italic=False; before=None pt, after=7.0 pt, line=1.1416666666666666×, keep-next=None; color=#000000. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Cambria, Arial, Arial, Arial, Cambria. The local PDF (`office-pdf/evidence-brief-for-print.pdf`, SHA-256 `01febfd0a802fbadc97c40ff1be7411f6e9c7c7143fc6da3b7cb79390e93bff9`) has font resources Caladea-Bold, Caladea-Regular, LiberationSans, LiberationSans-Bold; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
