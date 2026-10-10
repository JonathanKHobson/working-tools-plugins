# Show the Work · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #202327 | used style Normal explicit text color |
| Cue paper | surface | #F4F1E9 | Native reference.docx word/document.xml active shading/border value #F4F1E9; source visual and native-design-style-audit corroboration. |
| Cue amber | primary | #72500C | Native reference.docx word/styles.xml: style Heading2; text. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 15.78:1 | Normal-size text contrast threshold met |
| Background / Cue amber | 7.32:1 | Normal-size text contrast threshold met |
| Text / Cue paper | 13.98:1 | Normal-size text contrast threshold met |
| Cue paper / Cue amber | 6.49:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Demo Cue Cards: native colors](references/demo-cue-cards/COLORS.md)
