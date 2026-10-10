# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `3115e0a323a47beae01521f2ab4c2e3bed5e4f82c7a4e3c4ef7c7fe8624fd89c` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 4 paragraphs; base `None`): font `Arial`, 11.5 pt, bold=False, italic=None; before=0.0 pt, after=5.0 pt, line=1.05×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 3 paragraphs; base `Normal`): font `Arial`, 17.0 pt, bold=True, italic=None; before=0.0 pt, after=5.0 pt, line=1.05×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `Arial`, 38.0 pt, bold=True, italic=None; before=0.0 pt, after=12.0 pt, line=0.9708333333333333×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Proof Index** (`ProofIndex`, 2 paragraphs; base `None`): font `Arial`, 44.0 pt, bold=True, italic=None; before=0.0 pt, after=0.0 pt, line=1.05×, keep-next=False; color=#B33525. Source: `word/styles.xml`.
- **Proof Meta** (`ProofMeta`, 6 paragraphs; base `None`): font `Arial`, 9.5 pt, bold=False, italic=None; before=0.0 pt, after=5.0 pt, line=1.05×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Proof Label** (`ProofLabel`, 4 paragraphs; base `None`): font `Arial`, 9.5 pt, bold=True, italic=None; before=0.0 pt, after=7.0 pt, line=1.05×, keep-next=True; color=#B33525. Source: `word/styles.xml`.
- **Proof Intro** (`ProofIntro`, 1 paragraphs; base `None`): font `Arial`, 12.5 pt, bold=False, italic=None; before=0.0 pt, after=12.0 pt, line=1.05×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Proof Name** (`ProofName`, 1 paragraphs; base `None`): font `Arial`, 14.0 pt, bold=True, italic=None; before=0.0 pt, after=2.0 pt, line=1.05×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Proof Contact** (`ProofContact`, 1 paragraphs; base `None`): font `Arial`, 15.0 pt, bold=True, italic=None; before=0.0 pt, after=6.0 pt, line=1.05×, keep-next=False; color=#000000. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Arial, Arial, Arial, Arial, Arial, Arial, Arial, Arial, Arial. The local PDF (`office-pdf/capability-proof-sheet.pdf`, SHA-256 `3b78a9061698ccb5e2032bf13b243ae1645ee890af0658dd316c62e20e103cbe`) has font resources LiberationSans, LiberationSans-Bold; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
