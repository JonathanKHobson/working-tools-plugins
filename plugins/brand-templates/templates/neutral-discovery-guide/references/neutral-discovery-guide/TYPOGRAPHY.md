# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `91b836ca3cb180d7f0dad1748d0615d3446da096895862e8e7b71795b7cd67fd` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 42 paragraphs; base `None`): font `Calibri`, 11.5 pt, bold=None, italic=None; before=None pt, after=7.0 pt, line=1.1416666666666666×, keep-next=None; color=#000000. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 4 paragraphs; base `Normal`): font `Calibri`, 18.0 pt, bold=True, italic=None; before=13.0 pt, after=7.0 pt, line=1.1416666666666666×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 16 paragraphs; base `Normal`): font `Calibri`, 13.0 pt, bold=True, italic=None; before=13.0 pt, after=7.0 pt, line=1.1416666666666666×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `Calibri`, 25.0 pt, bold=None, italic=None; before=None pt, after=14.0 pt, line=1.1416666666666666×, keep-next=None; color=#000000. Source: `word/styles.xml`.
- **Subtitle** (`Subtitle`, 1 paragraphs; base `Normal`): font `Calibri`, 12.0 pt, bold=None, italic=False; before=None pt, after=7.0 pt, line=1.1416666666666666×, keep-next=None; color=#000000. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Calibri, Calibri, Calibri, Calibri, Calibri. The local PDF (`office-pdf/neutral-discovery-guide.pdf`, SHA-256 `acb0965f30e9a00cd3d3ac57cd9a3bdc7e413a5b767e38f1b29da9c59e4fa616`) has font resources Carlito, Carlito-Bold; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
