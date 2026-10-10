# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `7fa724c4d7cc6ac260dfdc20ab3607f2be76ae29a132370a46ecd569264d565c` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 12 paragraphs; base `None`): font `Arial`, 11.0 pt, bold=False, italic=None; before=0.0 pt, after=7.0 pt, line=1.0791666666666666×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 2 paragraphs; base `Normal`): font `Arial Rounded MT Bold`, 32.0 pt, bold=False, italic=None; before=0.0 pt, after=5.0 pt, line=1.0791666666666666×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 4 paragraphs; base `Normal`): font `Arial Rounded MT Bold`, 15.0 pt, bold=False, italic=None; before=0.0 pt, after=5.0 pt, line=1.0791666666666666×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Calendar Label** (`CalendarLabel`, 5 paragraphs; base `None`): font `Arial`, 9.5 pt, bold=True, italic=None; before=0.0 pt, after=5.0 pt, line=1.0791666666666666×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Calendar Note** (`CalendarNote`, 4 paragraphs; base `None`): font `Arial`, 9.5 pt, bold=False, italic=None; before=0.0 pt, after=5.0 pt, line=1.0791666666666666×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Calendar Date** (`CalendarDate`, 42 paragraphs; base `None`): font `Arial`, 12.0 pt, bold=True, italic=None; before=0.0 pt, after=1.0 pt, line=1.0791666666666666×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Calendar Prompt** (`CalendarPrompt`, 42 paragraphs; base `None`): font `Arial`, 9.5 pt, bold=False, italic=None; before=0.0 pt, after=0.0 pt, line=1.0791666666666666×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Calendar Day** (`CalendarDay`, 7 paragraphs; base `None`): font `Arial`, 10.0 pt, bold=True, italic=None; before=0.0 pt, after=0.0 pt, line=1.0791666666666666×, keep-next=False; color=#000000. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Arial, Arial Rounded MT Bold, Arial Rounded MT Bold, Arial, Arial, Arial, Arial, Arial. The local PDF (`office-pdf/creative-practice-calendar.pdf`, SHA-256 `5bb5cea4cc3b6302ee8f27ccf00648aa56e169df18e5daa0c37789a500ef322b`) has font resources LiberationSans, LiberationSans-Bold, LinuxLibertineG; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
