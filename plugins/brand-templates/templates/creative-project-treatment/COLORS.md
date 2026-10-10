# The Last Key Studio · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #303030 | used style Normal explicit text color |
| Treatment table | surface | #F5F3EF | Native reference.docx word/document.xml active shading/border value #F5F3EF; source visual and native-design-style-audit corroboration. |
| Title ink | display-ink | #000000 | Native reference.docx word/styles.xml: style Title, style Heading2, style Heading1; text. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 13.20:1 | Normal-size text contrast threshold met |
| Background / Title ink | 21.00:1 | Normal-size text contrast threshold met |
| Text / Treatment table | 11.91:1 | Normal-size text contrast threshold met |
| Treatment table / Title ink | 18.95:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Creative Project Treatment: native colors](references/creative-project-treatment/COLORS.md)
