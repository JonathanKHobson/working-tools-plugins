# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `8bf7ded45dbafa98547314d3079f0dd108d4107d8f18c4dd553f4f36f7b1ef04` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 26 paragraphs; base `None`): font `Arial`, 20.0 pt, bold=False, italic=None; before=0.0 pt, after=14.0 pt, line=1.1208333333333333×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 1 paragraphs; base `Normal`): font `Avenir Next`, 48.0 pt, bold=True, italic=None; before=0.0 pt, after=14.0 pt, line=1.1208333333333333×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 3 paragraphs; base `Normal`): font `Avenir Next`, 26.0 pt, bold=True, italic=None; before=0.0 pt, after=16.0 pt, line=1.1208333333333333×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 3** (`Heading3`, 9 paragraphs; base `Normal`): font `Avenir Next`, 20.0 pt, bold=True, italic=None; before=0.0 pt, after=7.0 pt, line=1.1208333333333333×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Poster Label** (`PosterLabel`, 2 paragraphs; base `None`): font `Arial`, 15.0 pt, bold=True, italic=None; before=0.0 pt, after=10.0 pt, line=1.1208333333333333×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Poster Lead** (`PosterLead`, 1 paragraphs; base `None`): font `Avenir Next`, 30.0 pt, bold=False, italic=None; before=0.0 pt, after=10.0 pt, line=1.1208333333333333×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Poster Note** (`PosterNote`, 4 paragraphs; base `None`): font `Arial`, 16.0 pt, bold=False, italic=None; before=0.0 pt, after=12.0 pt, line=1.1208333333333333×, keep-next=False; color=#000000. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Arial, Avenir Next, Avenir Next, Avenir Next, Arial, Avenir Next, Arial. The local PDF (`office-pdf/research-wall-poster.pdf`, SHA-256 `6fc35f85d21953bd7684e62097a9ae4062c19262a7b6e8386719afe243a91135`) has font resources FrankRuhlHofshi-Bold, LiberationSans, LiberationSans-Bold, LinuxLibertineG; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
