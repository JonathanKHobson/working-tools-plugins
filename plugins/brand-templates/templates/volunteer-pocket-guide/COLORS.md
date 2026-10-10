# First Shift · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #213D38 | used style Normal explicit text color |
| Route green | primary | #426257 | Native reference.docx word/document.xml active shading/border value #426257; source visual and native-design-style-audit corroboration. |
| Route panel | surface | #DCE6DE | Native reference.docx word/document.xml active shading/border value #DCE6DE; source visual and native-design-style-audit corroboration. |
| Stage ink | display-ink | #000000 | Native reference.docx word/styles.xml: style Title, style Heading1; text. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 11.74:1 | Normal-size text contrast threshold met |
| Background / Route green | 6.74:1 | Normal-size text contrast threshold met |
| Background / Stage ink | 21.00:1 | Normal-size text contrast threshold met |
| Text / Route panel | 9.18:1 | Normal-size text contrast threshold met |
| Route green / Route panel | 5.27:1 | Normal-size text contrast threshold met |
| Route panel / Stage ink | 16.42:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Volunteer Pocket Guide: native colors](references/volunteer-pocket-guide/COLORS.md)
