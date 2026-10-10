# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `923a51193c6260fc5a7a4ce1561de5066b94f34fbd9b6380126900b19162fb5b` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 26 paragraphs; base `None`): font `Helvetica Neue`, 12.0 pt, bold=False, italic=None; before=0.0 pt, after=8.0 pt, line=1.1×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 3 paragraphs; base `Normal`): font `Baskerville`, 32.0 pt, bold=False, italic=None; before=0.0 pt, after=10.0 pt, line=1.1×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 21 paragraphs; base `Normal`): font `Helvetica Neue`, 12.0 pt, bold=True, italic=None; before=0.0 pt, after=4.0 pt, line=1.1×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Portfolio Label** (`PortfolioLabel`, 6 paragraphs; base `None`): font `Helvetica Neue`, 10.5 pt, bold=True, italic=None; before=0.0 pt, after=8.0 pt, line=1.1×, keep-next=True; color=#38545F. Source: `word/styles.xml`.
- **Portfolio Note** (`PortfolioNote`, 8 paragraphs; base `None`): font `Helvetica Neue`, 10.5 pt, bold=False, italic=None; before=0.0 pt, after=8.0 pt, line=1.1×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Portfolio Excerpt** (`PortfolioExcerpt`, 2 paragraphs; base `None`): font `Baskerville`, 14.0 pt, bold=False, italic=None; before=0.0 pt, after=10.0 pt, line=1.1×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Portfolio Lead** (`PortfolioLead`, 1 paragraphs; base `None`): font `Baskerville`, 22.0 pt, bold=False, italic=None; before=0.0 pt, after=14.0 pt, line=1.1×, keep-next=False; color=#000000. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Helvetica Neue, Baskerville, Helvetica Neue, Helvetica Neue, Helvetica Neue, Baskerville, Baskerville. The local PDF (`office-pdf/portfolio-leave-behind.pdf`, SHA-256 `c11e6b2f09d9e114bb5ed92f283f6d928542e6b50ba3147e90baa262063056e1`) has font resources FrankRuhlHofshi-Bold, LinuxLibertineG; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
