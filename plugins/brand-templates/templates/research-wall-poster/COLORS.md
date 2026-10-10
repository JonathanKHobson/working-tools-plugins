# Studio Field Atlas · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #000000 | used style Normal explicit text color |
| Evidence header | header | #24232B | Native reference.docx word/document.xml active shading/border value #24232B; source visual and native-design-style-audit corroboration. |
| Evidence row | surface | #F2F5F7 | Native reference.docx word/document.xml active shading/border value #F2F5F7; source visual and native-design-style-audit corroboration. |
| Cyan strip | primary | #72C4CA | Native reference.docx word/media/image1.png exact repeated pixels; visible source geometric/illustrative strip. Artwork color, not a body-text color. |
| Plum shape | accent | #8B355A | Native reference.docx word/media/image1.png exact repeated pixels; visible source geometric/illustrative strip. Artwork color, not a body-text color. |
| Mint shape | secondary | #CDEBE5 | Native reference.docx word/media/image1.png exact repeated pixels; visible source geometric/illustrative strip. Artwork color, not a body-text color. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 21.00:1 | Normal-size text contrast threshold met |
| Background / Evidence header | 15.55:1 | Normal-size text contrast threshold met |
| Background / Plum shape | 7.62:1 | Normal-size text contrast threshold met |
| Text / Evidence row | 19.18:1 | Normal-size text contrast threshold met |
| Text / Cyan strip | 10.46:1 | Normal-size text contrast threshold met |
| Text / Mint shape | 16.61:1 | Normal-size text contrast threshold met |
| Evidence header / Evidence row | 14.20:1 | Normal-size text contrast threshold met |
| Evidence header / Cyan strip | 7.75:1 | Normal-size text contrast threshold met |
| Evidence header / Mint shape | 12.30:1 | Normal-size text contrast threshold met |
| Evidence row / Plum shape | 6.96:1 | Normal-size text contrast threshold met |
| Plum shape / Mint shape | 6.03:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Research Wall Poster: native colors](references/research-wall-poster/COLORS.md)
