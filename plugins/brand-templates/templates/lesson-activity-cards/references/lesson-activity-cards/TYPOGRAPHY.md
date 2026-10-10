# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `e5e7d3bbb5efb1a9fa4c375bba2a293f997a55863fc2991252cf92e00b42f16f` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 25 paragraphs; base `None`): font `Trebuchet MS`, 11.0 pt, bold=False, italic=None; before=0.0 pt, after=6.0 pt, line=1.05×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 9 paragraphs; base `Normal`): font `Chalkboard`, 27.0 pt, bold=True, italic=None; before=0.0 pt, after=9.0 pt, line=1.05×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 20 paragraphs; base `Normal`): font `Trebuchet MS`, 11.5 pt, bold=True, italic=None; before=0.0 pt, after=4.0 pt, line=1.05×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `Chalkboard`, 32.0 pt, bold=True, italic=None; before=0.0 pt, after=8.0 pt, line=1.05×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Card Lead** (`CardLead`, 4 paragraphs; base `None`): font `Trebuchet MS`, 13.0 pt, bold=True, italic=None; before=0.0 pt, after=9.0 pt, line=1.05×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Card Label** (`CardLabel`, 17 paragraphs; base `None`): font `Trebuchet MS`, 9.0 pt, bold=True, italic=None; before=0.0 pt, after=7.0 pt, line=1.05×, keep-next=True; color=#185E65. Source: `word/styles.xml`.
- **Card Note** (`CardNote`, 13 paragraphs; base `None`): font `Trebuchet MS`, 10.0 pt, bold=False, italic=None; before=0.0 pt, after=7.0 pt, line=1.05×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Card Body** (`CardBody`, 24 paragraphs; base `None`): font `Trebuchet MS`, 12.0 pt, bold=False, italic=None; before=0.0 pt, after=9.0 pt, line=1.05×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Card Pattern** (`CardPattern`, 12 paragraphs; base `None`): font `Apple Symbols`, 28.0 pt, bold=False, italic=None; before=0.0 pt, after=15.0 pt, line=1.05×, keep-next=False; color=#185E65. Source: `word/styles.xml`.
- **Card Number** (`CardNumber`, 8 paragraphs; base `None`): font `Chalkboard`, 40.0 pt, bold=True, italic=None; before=0.0 pt, after=2.0 pt, line=1.05×, keep-next=True; color=#000000. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Trebuchet MS, Chalkboard, Trebuchet MS, Chalkboard, Trebuchet MS, Trebuchet MS, Trebuchet MS, Trebuchet MS, Apple Symbols, Chalkboard. The local PDF (`office-pdf/lesson-activity-cards.pdf`, SHA-256 `cd9e5280ba661cbb2c642937c71776b8fdd1034c2db59c300a298309baa86581`) has font resources FrankRuhlHofshi-Bold, LinuxLibertineG; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
