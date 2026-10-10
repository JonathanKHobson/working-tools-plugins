# The Technical Record · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #171B20 | used style Normal explicit text color |
| Technical focus | primary | #142D41 | Native word/styles.xml Heading2 and TSHeadline. Structural role corroborated at the native OOXML element, not assigned by palette order. |
| Contact metadata | secondary-text | #47535D | Native word/styles.xml TSNotice/TSDates/TSContext. Structural role corroborated at the native OOXML element, not assigned by palette order. |
| Name ink | display-ink | #000000 | Native word/styles.xml Title/Heading1. Structural role corroborated at the native OOXML element, not assigned by palette order. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 17.30:1 | Normal-size text contrast threshold met |
| Background / Technical focus | 14.18:1 | Normal-size text contrast threshold met |
| Background / Contact metadata | 7.89:1 | Normal-size text contrast threshold met |
| Background / Name ink | 21.00:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Technical Signal: native colors](references/technical-signal/COLORS.md)
