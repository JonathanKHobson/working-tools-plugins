# Used paragraph styles

Source: `assets/reference.docx` · SHA-256 `58d3741a213e93117d121a9e2b60ee5f640a03d0c883b42fc4db4ff2f925732a` (source file bytes). These are source observations; user-authorized changes may replace them.

A blank field inherits from the named base style or document defaults. Native point values are retained.

- **Normal** (`Normal`, 8 paragraphs; base `None`): font `Noto Sans`, 11.5 pt, bold=False, italic=False; before=0.0 pt, after=12.0 pt, line=1.1×, keep-next=False; color=#29251E. Source: `word/styles.xml`.
- **Heading 1** (`Heading1`, 2 paragraphs; base `Normal`): font `Rockwell`, 29.0 pt, bold=False, italic=False; before=0.0 pt, after=8.0 pt, line=1.1×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Heading 2** (`Heading2`, 6 paragraphs; base `Normal`): font `Noto Sans`, 13.0 pt, bold=True, italic=False; before=0.0 pt, after=12.0 pt, line=1.1×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Title** (`Title`, 1 paragraphs; base `Normal`): font `Rockwell`, 44.0 pt, bold=False, italic=False; before=0.0 pt, after=8.0 pt, line=1.1×, keep-next=True; color=#000000. Source: `word/styles.xml`.
- **Recipe Contents** (`RecipeContents`, 1 paragraphs; base `None`): font `Noto Sans`, 13.0 pt, bold=True, italic=False; before=0.0 pt, after=12.0 pt, line=1.1×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Recipe Label** (`RecipeLabel`, 4 paragraphs; base `None`): font `Noto Sans`, 10.0 pt, bold=True, italic=False; before=0.0 pt, after=12.0 pt, line=1.1×, keep-next=True; color=#80412B. Source: `word/styles.xml`.
- **Recipe Subtitle** (`RecipeSubtitle`, 1 paragraphs; base `None`): font `Noto Sans`, 16.0 pt, bold=False, italic=False; before=0.0 pt, after=10.0 pt, line=1.1×, keep-next=False; color=#29251E. Source: `word/styles.xml`.
- **Recipe Byline** (`RecipeByline`, 1 paragraphs; base `None`): font `Noto Sans`, 10.5 pt, bold=False, italic=False; before=0.0 pt, after=14.0 pt, line=1.1×, keep-next=False; color=#29251E. Source: `word/styles.xml`.
- **Recipe Description** (`RecipeDescription`, 2 paragraphs; base `None`): font `Noto Sans`, 12.0 pt, bold=False, italic=False; before=0.0 pt, after=9.0 pt, line=1.1×, keep-next=False; color=#29251E. Source: `word/styles.xml`.
- **Recipe Yield** (`RecipeYield`, 2 paragraphs; base `None`): font `Noto Sans`, 11.5 pt, bold=True, italic=False; before=0.0 pt, after=9.0 pt, line=1.1×, keep-next=False; color=#29251E. Source: `word/styles.xml`.
- **Recipe Equipment** (`RecipeEquipment`, 2 paragraphs; base `None`): font `Noto Sans`, 10.5 pt, bold=False, italic=False; before=0.0 pt, after=17.0 pt, line=1.1×, keep-next=False; color=#29251E. Source: `word/styles.xml`.
- **Recipe Note** (`RecipeNote`, 5 paragraphs; base `None`): font `Noto Sans`, 10.0 pt, bold=False, italic=False; before=0.0 pt, after=12.0 pt, line=1.1×, keep-next=False; color=#29251E. Source: `word/styles.xml`.
- **Recipe Link** (`RecipeLink`, 4 paragraphs; base `None`): font `Noto Sans`, 11.5 pt, bold=False, italic=False; before=0.0 pt, after=10.0 pt, line=1.1×, keep-next=False; color=#264E48. Source: `word/styles.xml`.
- **Recipe Cell** (`RecipeCell`, 24 paragraphs; base `None`): font `Noto Sans`, 10.5 pt, bold=False, italic=False; before=0.0 pt, after=0.0 pt, line=1.1×, keep-next=False; color=#29251E. Source: `word/styles.xml`.
- **Recipe Header** (`RecipeHeader`, 4 paragraphs; base `None`): font `Noto Sans`, 10.5 pt, bold=True, italic=False; before=0.0 pt, after=0.0 pt, line=1.1×, keep-next=False; color=#000000. Source: `word/styles.xml`.
- **Recipe Method** (`RecipeMethod`, 8 paragraphs; base `None`): font `Noto Sans`, 11.5 pt, bold=False, italic=False; before=0.0 pt, after=18.0 pt, line=1.1×, keep-next=False; color=#29251E. Source: `word/styles.xml`.
- **Recipe Folio** (`RecipeFolio`, 2 paragraphs; base `None`): font `Noto Sans`, 10.0 pt, bold=True, italic=False; before=0.0 pt, after=0.0 pt, line=1.1×, keep-next=False; color=#80412B. Source: `word/styles.xml`.

## Local PDF render comparison

The retained DOCX style fonts include Noto Sans, Rockwell, Noto Sans, Rockwell, Noto Sans, Noto Sans, Noto Sans, Noto Sans, Noto Sans, Noto Sans, Noto Sans, Noto Sans, Noto Sans, Noto Sans, Noto Sans, Noto Sans, Noto Sans. The local PDF (`office-pdf/recipe-collection.pdf`, SHA-256 `8aecebfa7371c744823b3244de6d3dd3d8937d9de07a4c8e24ce7e51fe5bd70b`) has font resources LinuxLibertineG, NotoSans-Bold, NotoSans-Regular; produced by LibreOfficeDev 26.8.0.0.alpha0 (AARCH64). Font resource names describe this renderer, not template tokens.
