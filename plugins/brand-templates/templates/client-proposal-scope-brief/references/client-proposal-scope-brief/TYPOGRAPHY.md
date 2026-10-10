# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `7fb7ae4b82e339ff6178340a6f5d46ae9ad7f9c5e9301b94b4fd958ea5b6f76c` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 69 paragraphs; base `None`): font `Arial`, 12.0 pt, bold=None, italic=None; before=0.0 pt, after=4.0 pt, line=1.0×, keep-next=None; color=#000000. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 3 paragraphs; base `Normal`): font `Arial`, 18.0 pt, bold=True, italic=None; before=0.0 pt, after=4.0 pt, line=1.0×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 8 paragraphs; base `Normal`): font `Arial`, 14.0 pt, bold=True, italic=None; before=8.5 pt, after=4.0 pt, line=1.0×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `Arial`, 36.0 pt, bold=True, italic=None; before=0.0 pt, after=17.0 pt, line=1.0×, keep-next=True; color=#000000. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Arial, Arial, Arial, Arial. The local PDF (`office-pdf/client-proposal-scope-brief.pdf`, SHA-256 `313e826c05a6f1da9086ed451b1c51e229c36623742450fd14100cd93ddc187f`) has font resources LiberationSans, LiberationSans-Bold; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
