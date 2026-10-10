# The Relevant Record · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #171B20 | used style Normal explicit text color |
| Forwarding scope | surface | #EDF2F4 | Native reference.docx word/document.xml active shading/border value #EDF2F4; source visual and native-design-style-audit corroboration. |
| Metadata gray | secondary-text | #565656 | Native reference.docx word/styles.xml: style Footer, style EMNotice, style EMMeta; text. |
| Name ink | display-ink | #000000 | Native reference.docx word/styles.xml: style Title, style Heading2, style Heading1; text. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 17.30:1 | Normal-size text contrast threshold met |
| Background / Metadata gray | 7.34:1 | Normal-size text contrast threshold met |
| Background / Name ink | 21.00:1 | Normal-size text contrast threshold met |
| Text / Forwarding scope | 15.33:1 | Normal-size text contrast threshold met |
| Forwarding scope / Metadata gray | 6.50:1 | Normal-size text contrast threshold met |
| Forwarding scope / Name ink | 18.61:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Recruiter Evidence Map: native colors](references/recruiter-evidence-map/COLORS.md)
