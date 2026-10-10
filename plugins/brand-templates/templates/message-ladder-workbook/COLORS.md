# One Clear Message · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #000000 | used style Normal explicit text color |
| Ladder purple | primary | #673D74 | Native reference.docx word/document.xml active shading/border value #673D74; source visual and native-design-style-audit corroboration. |
| Ladder row | surface | #F2F5F7 | Native reference.docx word/document.xml active shading/border value #F2F5F7; source visual and native-design-style-audit corroboration. |
| Writing rule | rule | #C7BACB | Native reference.docx word/document.xml active shading/border value #C7BACB; source visual and native-design-style-audit corroboration. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 21.00:1 | Normal-size text contrast threshold met |
| Background / Ladder purple | 8.41:1 | Normal-size text contrast threshold met |
| Text / Ladder row | 19.18:1 | Normal-size text contrast threshold met |
| Text / Writing rule | 11.31:1 | Normal-size text contrast threshold met |
| Ladder purple / Ladder row | 7.68:1 | Normal-size text contrast threshold met |
| Ladder purple / Writing rule | 4.53:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Message Ladder Workbook: native colors](references/message-ladder-workbook/COLORS.md)
