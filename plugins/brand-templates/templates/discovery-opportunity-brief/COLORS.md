# Before the Journey · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #000000 | used style Normal explicit text color |
| Evidence header | primary | #653B21 | Native reference.docx word/document.xml active shading/border value #653B21; source visual and native-design-style-audit corroboration. |
| Evidence row | surface | #FAF0DB | Native reference.docx word/document.xml active shading/border value #FAF0DB; source visual and native-design-style-audit corroboration. |
| Fieldnote band | accent | #F4D69B | Native reference.docx word/document.xml active shading/border value #F4D69B; source visual and native-design-style-audit corroboration. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 21.00:1 | Normal-size text contrast threshold met |
| Background / Evidence header | 9.54:1 | Normal-size text contrast threshold met |
| Text / Evidence row | 18.55:1 | Normal-size text contrast threshold met |
| Text / Fieldnote band | 14.94:1 | Normal-size text contrast threshold met |
| Evidence header / Evidence row | 8.43:1 | Normal-size text contrast threshold met |
| Evidence header / Fieldnote band | 6.79:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Discovery Opportunity Brief: native colors](references/discovery-opportunity-brief/COLORS.md)
