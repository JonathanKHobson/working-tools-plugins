# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `821edbb65f940ede988d3f610dd0f48cd2341a2aefa4b7898bfdb3322580617e` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 82 paragraphs; base `None`): font `Arial`, 11.0 pt, bold=False, italic=None; before=0.0 pt, after=7.0 pt, line=1.1×, keep-next=None; color=#000000. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 5 paragraphs; base `Normal`): font `Rockwell`, 24.0 pt, bold=True, italic=None; before=0.0 pt, after=12.0 pt, line=1.1×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 8 paragraphs; base `Normal`): font `Rockwell`, 15.0 pt, bold=True, italic=None; before=10.0 pt, after=7.0 pt, line=1.1×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `Rockwell`, 34.0 pt, bold=True, italic=None; before=0.0 pt, after=13.0 pt, line=1.1×, keep-next=None; color=#000000. Source: `word/styles.xml`.
- **Field Label** (`FieldLabel`, 3 paragraphs; base `None`): font `Courier New`, 9.5 pt, bold=True, italic=None; before=0.0 pt, after=10.0 pt, line=1.1×, keep-next=None; color=#000000. Source: `word/styles.xml`.
- **Field Note** (`FieldNote`, 6 paragraphs; base `None`): font `Arial`, 9.5 pt, bold=False, italic=None; before=0.0 pt, after=9.0 pt, line=1.1×, keep-next=None; color=#000000. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Arial, Rockwell, Rockwell, Rockwell, Courier New, Arial. The local PDF (`office-pdf/discovery-opportunity-brief.pdf`, SHA-256 `73da2b3b3697bebc607302132b4cab26ef472112a2a1b48f071097a9e0e4b618`) has font resources FrankRuhlHofshi-Bold, LiberationMono, LiberationMono-Bold, LiberationSans, LiberationSans-Bold; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
