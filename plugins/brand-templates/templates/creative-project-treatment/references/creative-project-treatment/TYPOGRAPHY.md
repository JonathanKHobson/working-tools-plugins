# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `947f3e25f7c959876976cbaccf64f1f0fdcad43d74f24d982c10cb5d20f3f1be` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 35 paragraphs; base `None`): font `Source Sans 3`, 11.5 pt, bold=False, italic=False; before=0.0 pt, after=7.0 pt, line=15.0 pt, keep-next=False; color=#303030. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 9 paragraphs; base `Normal`): font `Source Serif 4 Display`, 23.0 pt, bold=False, italic=False; before=15.0 pt, after=9.0 pt, line=27.0 pt, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 3 paragraphs; base `Normal`): font `Source Sans 3`, 13.0 pt, bold=True, italic=False; before=12.0 pt, after=8.0 pt, line=17.0 pt, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `Source Serif 4 Display`, 42.0 pt, bold=False, italic=False; before=0.0 pt, after=12.0 pt, line=46.0 pt, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Subtitle** (`Subtitle`, 1 paragraphs; base `Normal`): font `Source Sans 3`, 12.0 pt, bold=False, italic=False; before=0.0 pt, after=8.0 pt, line=15.0 pt, keep-next=True; color=#303030. Source: `word/styles.xml`.
- **Caption** (`Caption`, 5 paragraphs; base `Normal`): font `Source Sans 3`, 10.5 pt, bold=False, italic=False; before=0.0 pt, after=9.0 pt, line=13.0 pt, keep-next=False; color=#303030. Source: `word/styles.xml`.
- **Table Body** (`TableBody`, 166 paragraphs; base `None`): font `Source Sans 3`, 11.0 pt, bold=False, italic=False; before=0.0 pt, after=0.0 pt, line=14.0 pt, keep-next=False; color=#303030. Source: `word/styles.xml`.
- **Metadata** (`Metadata`, 1 paragraphs; base `None`): font `Source Sans 3`, 10.5 pt, bold=False, italic=False; before=0.0 pt, after=9.0 pt, line=13.0 pt, keep-next=False; color=#303030. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Source Sans 3, Source Serif 4 Display, Source Sans 3, Source Serif 4 Display, Source Sans 3, Source Sans 3, Source Sans 3, Source Sans 3. The local PDF (`office-pdf/creative-project-treatment.pdf`, SHA-256 `c2201b5d86d903460ec8b5cd4b060c3e6199b0481ae715c6cac524ba735e8fe9`) has font resources SourceSans3-Bold, SourceSans3-Regular, SourceSerif4Display-Regular; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
