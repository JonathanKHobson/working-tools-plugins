# Common Material · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Residency peach | background | #FAE6D4 | Native reference.docx peach page ground confirmed in rendered cover; word/document.xml repeats #FAE6D4 working surfaces. |
| Text | text | #302A3B | used style Normal explicit text color |
| Warm table ground | surface | #FFF7EE | Native reference.docx word/document.xml active shading/border value #FFF7EE; source visual and native-design-style-audit corroboration. |
| Olive rule | rule | #B8C26F | Native reference.docx word/document.xml active shading/border value #B8C26F; source visual and native-design-style-audit corroboration. |
| Residency plum | primary | #853D5A | Native reference.docx word/styles.xml: style Metadata, style Heading2; text. |
| Reversed table labels | reverse-text | #FFFFFF | Native reference.docx word/document.xml: paragraph: Test, paragraph: Method, paragraph: Decision it informs; text. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Residency peach / Text | 11.40:1 | Normal-size text contrast threshold met |
| Residency peach / Residency plum | 6.16:1 | Normal-size text contrast threshold met |
| Text / Warm table ground | 13.02:1 | Normal-size text contrast threshold met |
| Text / Olive rule | 7.23:1 | Normal-size text contrast threshold met |
| Text / Reversed table labels | 13.82:1 | Normal-size text contrast threshold met |
| Warm table ground / Residency plum | 7.04:1 | Normal-size text contrast threshold met |
| Residency plum / Reversed table labels | 7.47:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Artist Residency Proposal: native colors](references/artist-residency-proposal/COLORS.md)
