# A Quieter Practice · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #000000 | used style Normal explicit text color |
| Reflection label | primary | #574936 | Native reference.docx word/styles.xml: style JournalLabel; text. |
| Journal link | link | #304D4A | Native reference.docx word/styles.xml: style JournalLink; text. |
| Journal rule | rule | #A99E8D | Native reference.docx word/styles.xml: style JournalRule; border. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 21.00:1 | Normal-size text contrast threshold met |
| Background / Reflection label | 8.71:1 | Normal-size text contrast threshold met |
| Background / Journal link | 9.19:1 | Normal-size text contrast threshold met |
| Text / Journal rule | 7.96:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Project Reflection Journal: native colors](references/project-reflection-journal/COLORS.md)
