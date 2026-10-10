# Across Practice · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #25302B | used style Normal explicit text color |
| Section green | primary | #254B40 | Native reference.docx word/styles.xml: style Heading2, style Heading1, style CBTarget; text. |
| Metadata green | secondary-text | #44534C | Native reference.docx word/styles.xml: style CBRelevance, style CBNotice, style CBDates; text. |
| Name ink | display-ink | #000000 | Native reference.docx word/styles.xml: style Title; text. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 13.67:1 | Normal-size text contrast threshold met |
| Background / Section green | 9.73:1 | Normal-size text contrast threshold met |
| Background / Metadata green | 8.12:1 | Normal-size text contrast threshold met |
| Background / Name ink | 21.00:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Career Bridge: native colors](references/career-bridge/COLORS.md)
