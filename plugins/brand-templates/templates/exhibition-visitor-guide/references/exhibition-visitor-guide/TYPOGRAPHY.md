# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `7397e3f64a90f2efb11b959ef0740a3d7bb2eba0da2c80984ef313e27fbec609` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 27 paragraphs; base `None`): font `Optima`, 11.5 pt, bold=False, italic=None; before=0.0 pt, after=9.0 pt, line=1.1×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 6 paragraphs; base `Normal`): font `Futura`, 28.0 pt, bold=False, italic=None; before=0.0 pt, after=10.0 pt, line=1.1×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 17 paragraphs; base `Normal`): font `Futura`, 11.5 pt, bold=True, italic=None; before=0.0 pt, after=5.0 pt, line=1.1×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `Futura`, 36.0 pt, bold=False, italic=None; before=0.0 pt, after=10.0 pt, line=1.1×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Gallery Lead** (`GalleryLead`, 5 paragraphs; base `None`): font `Optima`, 18.0 pt, bold=False, italic=None; before=0.0 pt, after=12.0 pt, line=1.1×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Gallery Label** (`GalleryLabel`, 6 paragraphs; base `None`): font `Futura`, 9.0 pt, bold=False, italic=None; before=0.0 pt, after=10.0 pt, line=1.1×, keep-next=True; color=#95482D. Source: `word/styles.xml`.
- **Gallery Note** (`GalleryNote`, 8 paragraphs; base `None`): font `Optima`, 9.5 pt, bold=False, italic=None; before=0.0 pt, after=9.0 pt, line=1.1×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Gallery Meta** (`GalleryMeta`, 3 paragraphs; base `None`): font `Optima`, 10.5 pt, bold=False, italic=None; before=0.0 pt, after=12.0 pt, line=1.1×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Gallery Route** (`GalleryRoute`, 11 paragraphs; base `None`): font `Optima`, 11.5 pt, bold=False, italic=None; before=0.0 pt, after=12.0 pt, line=1.1×, keep-next=False; color=#813A25. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Optima, Futura, Futura, Futura, Optima, Futura, Optima, Optima, Optima. The local PDF (`office-pdf/exhibition-visitor-guide.pdf`, SHA-256 `88316150c66d2e6bb193439cb6841102ce1a3d9ac8dc3b8bb4e722e067ffd93b`) has font resources FrankRuhlHofshi-Bold, LinuxLibertineG; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
