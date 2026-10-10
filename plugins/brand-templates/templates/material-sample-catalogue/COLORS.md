# The Material Register · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #000000 | used style Normal explicit text color |
| Specimen header | primary | #333B3D | Native reference.docx word/document.xml active shading/border value #333B3D; source visual and native-design-style-audit corroboration. |
| Specimen row | surface | #F1F3F2 | Native reference.docx word/document.xml active shading/border value #F1F3F2; source visual and native-design-style-audit corroboration. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 21.00:1 | Normal-size text contrast threshold met |
| Background / Specimen header | 11.45:1 | Normal-size text contrast threshold met |
| Text / Specimen row | 18.84:1 | Normal-size text contrast threshold met |
| Specimen header / Specimen row | 10.28:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Material Sample Catalogue: native colors](references/material-sample-catalogue/COLORS.md)
