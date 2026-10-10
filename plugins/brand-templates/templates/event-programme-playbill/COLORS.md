# The Night Window · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #000000 | used style Normal explicit text color |
| Programme paper | surface | #F2E8DC | Native reference.docx word/document.xml active shading/border value #F2E8DC; source visual and native-design-style-audit corroboration. |
| Programme rule | rule | #B5AAA2 | Native reference.docx word/document.xml active shading/border value #B5AAA2; source visual and native-design-style-audit corroboration. |
| Programme burgundy | primary | #713B4B | Native reference.docx word/styles.xml: style ProgrammeLabel; text. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 21.00:1 | Normal-size text contrast threshold met |
| Background / Programme burgundy | 8.64:1 | Normal-size text contrast threshold met |
| Text / Programme paper | 17.35:1 | Normal-size text contrast threshold met |
| Text / Programme rule | 9.24:1 | Normal-size text contrast threshold met |
| Programme paper / Programme burgundy | 7.14:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Event Programme Playbill: native colors](references/event-programme-playbill/COLORS.md)
