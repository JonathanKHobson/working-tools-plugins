# The Session Field Guide · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #000000 | used style Normal explicit text color |
| Session header | header | #444444 | Native reference.docx word/document.xml active shading/border value #444444; source visual and native-design-style-audit corroboration. |
| Session row | surface | #F2F5F7 | Native reference.docx word/document.xml active shading/border value #F2F5F7; source visual and native-design-style-audit corroboration. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 21.00:1 | Normal-size text contrast threshold met |
| Background / Session header | 9.74:1 | Normal-size text contrast threshold met |
| Text / Session row | 19.18:1 | Normal-size text contrast threshold met |
| Session header / Session row | 8.90:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Facilitation Field Guide: native colors](references/facilitation-field-guide/COLORS.md)
