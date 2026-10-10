# Return to One Place · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #263C32 | used style Normal explicit text color |
| Observation panel | surface | #E4EEDC | Native reference.docx word/document.xml active shading/border value #E4EEDC; source visual and native-design-style-audit corroboration. |
| Field rule | primary | #49614A | Native reference.docx word/document.xml active shading/border value #49614A; source visual and native-design-style-audit corroboration. |
| Writing rule | rule | #8B998A | Native reference.docx word/document.xml active shading/border value #8B998A; source visual and native-design-style-audit corroboration. |
| Title ink | display-ink | #000000 | Native reference.docx word/styles.xml: style Title, style Heading2, style Heading1; text. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 11.83:1 | Normal-size text contrast threshold met |
| Background / Field rule | 6.79:1 | Normal-size text contrast threshold met |
| Background / Title ink | 21.00:1 | Normal-size text contrast threshold met |
| Text / Observation panel | 9.90:1 | Normal-size text contrast threshold met |
| Observation panel / Field rule | 5.68:1 | Normal-size text contrast threshold met |
| Observation panel / Title ink | 17.56:1 | Normal-size text contrast threshold met |
| Writing rule / Title ink | 7.02:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Nature Observation Journal: native colors](references/nature-observation-journal/COLORS.md)
