# Make Room to Try · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #000000 | used style Normal explicit text color |
| Weekday peach | primary | #FAD3C3 | Native reference.docx word/document.xml active shading/border value #FAD3C3; source visual and native-design-style-audit corroboration. |
| Weekday mint | secondary | #C6E5D7 | Native reference.docx word/document.xml active shading/border value #C6E5D7; source visual and native-design-style-audit corroboration. |
| Weekday lavender | accent | #DCD0EF | Native reference.docx word/document.xml active shading/border value #DCD0EF; source visual and native-design-style-audit corroboration. |
| Calendar grid | rule | #787878 | Native reference.docx word/document.xml active shading/border value #787878; source visual and native-design-style-audit corroboration. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 21.00:1 | Normal-size text contrast threshold met |
| Text / Weekday peach | 15.17:1 | Normal-size text contrast threshold met |
| Text / Weekday mint | 15.59:1 | Normal-size text contrast threshold met |
| Text / Weekday lavender | 14.31:1 | Normal-size text contrast threshold met |
| Text / Calendar grid | 4.76:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Creative Practice Calendar: native colors](references/creative-practice-calendar/COLORS.md)
