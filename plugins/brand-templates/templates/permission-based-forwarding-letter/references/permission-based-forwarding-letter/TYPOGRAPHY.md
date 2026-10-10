# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `81833526b09e6ba9acffb30fcfb0cb958fd0b80bbede200a92ff6848471762f4` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 4 paragraphs; base `None`): font `Arial`, 11.5 pt, bold=False, italic=None; before=0.0 pt, after=8.0 pt, line=1.05×, keep-next=False; color=#171B20. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `Georgia`, 24.0 pt, bold=False, italic=None; before=0.0 pt, after=9.0 pt, line=1.05×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **PF Notice** (`PFNotice`, 1 paragraphs; base `None`): font `Arial`, 10.5 pt, bold=True, italic=None; before=0.0 pt, after=6.0 pt, line=1.05×, keep-next=True; color=#47535D. Source: `word/styles.xml`.
- **PF Sender** (`PFSender`, 1 paragraphs; base `None`): font `Arial`, 10.5 pt, bold=False, italic=None; before=0.0 pt, after=3.0 pt, line=1.05×, keep-next=True; color=#171B20. Source: `word/styles.xml`.
- **PF Date** (`PFDate`, 1 paragraphs; base `None`): font `Arial`, 10.5 pt, bold=False, italic=None; before=0.0 pt, after=9.0 pt, line=1.05×, keep-next=True; color=#171B20. Source: `word/styles.xml`.
- **PF Recipient** (`PFRecipient`, 1 paragraphs; base `None`): font `Arial`, 10.5 pt, bold=False, italic=None; before=0.0 pt, after=0.0 pt, line=1.05×, keep-next=True; color=#171B20. Source: `word/styles.xml`.
- **PF Organization** (`PFOrganization`, 1 paragraphs; base `None`): font `Arial`, 10.5 pt, bold=False, italic=None; before=0.0 pt, after=9.0 pt, line=1.05×, keep-next=True; color=#171B20. Source: `word/styles.xml`.
- **PF Subject** (`PFSubject`, 1 paragraphs; base `None`): font `Arial`, 11.5 pt, bold=True, italic=None; before=0.0 pt, after=9.0 pt, line=1.05×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **PF Greeting** (`PFGreeting`, 1 paragraphs; base `None`): font `Arial`, 11.5 pt, bold=False, italic=None; before=0.0 pt, after=8.0 pt, line=1.05×, keep-next=True; color=#171B20. Source: `word/styles.xml`.
- **PF Scope** (`PFScope`, 4 paragraphs; base `None`): font `Arial`, 10.5 pt, bold=False, italic=None; before=0.0 pt, after=5.0 pt, line=1.05×, keep-next=False; color=#354653. Source: `word/styles.xml`.
- **PF Closing** (`PFClosing`, 1 paragraphs; base `None`): font `Arial`, 11.5 pt, bold=False, italic=None; before=7.0 pt, after=3.0 pt, line=1.05×, keep-next=True; color=#171B20. Source: `word/styles.xml`.
- **PF Signature** (`PFSignature`, 1 paragraphs; base `None`): font `Arial`, 10.5 pt, bold=True, italic=None; before=0.0 pt, after=0.0 pt, line=1.05×, keep-next=False; color=#171B20. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Arial, Georgia, Arial, Arial, Arial, Arial, Arial, Arial, Arial, Arial, Arial, Arial. The local PDF (`office-pdf/permission-based-forwarding-letter.pdf`, SHA-256 `7ff30d1e09cdd6f6adb668e48c56d9ef0c37d1a6a7a00716eb7345e45e6803f4`) has font resources LiberationSans, LiberationSans-Bold, LinuxLibertineG; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
