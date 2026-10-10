# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `13ffd209226534dd1ec2aed9f61d8453237b787bae989d77b0fcff795c779976` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 100 paragraphs; base `None`): font `Arial`, 12.0 pt, bold=False, italic=None; before=0.0 pt, after=7.0 pt, line=1.1208333333333333×, keep-next=None; color=#000000. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 5 paragraphs; base `Normal`): font `Georgia`, 23.0 pt, bold=False, italic=None; before=0.0 pt, after=13.0 pt, line=1.1208333333333333×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 7 paragraphs; base `Normal`): font `Georgia`, 15.0 pt, bold=False, italic=None; before=10.0 pt, after=5.0 pt, line=1.1208333333333333×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `Georgia`, 30.0 pt, bold=False, italic=None; before=0.0 pt, after=7.0 pt, line=1.1208333333333333×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Subtitle** (`Subtitle`, 1 paragraphs; base `Normal`): font `Georgia`, 18.0 pt, bold=False, italic=True; before=0.0 pt, after=7.0 pt, line=1.1208333333333333×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Caption** (`Caption`, 2 paragraphs; base `Normal`): font `Arial`, 9.0 pt, bold=False, italic=False; before=0.0 pt, after=0.0 pt, line=1.1208333333333333×, keep-next=None; color=#000000. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Arial, Georgia, Georgia, Georgia, Georgia, Arial. The local PDF (`office-pdf/learning-workshop-proposal.pdf`, SHA-256 `8fe1bd9daa6461db87a1c0fd973381f59329bfbe3624518748d159a6399d6c63`) has font resources LiberationSans, LiberationSans-Bold, LinuxLibertineG, LinuxLibertineGI; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
