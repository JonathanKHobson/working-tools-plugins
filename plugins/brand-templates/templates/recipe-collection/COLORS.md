# The Shared Table · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | Native Office page/sheet white ground; explicit design choice retaining the reading surface. |
| Text | text | #29251E | used style Normal explicit text color |
| Recipe working row | surface | #E8E8E8 | Native reference.docx word/document.xml active shading/border value #E8E8E8; source visual and native-design-style-audit corroboration. |
| Recipe rust | primary | #80412B | Native reference.docx word/styles.xml: style RecipeLabel, style RecipeFolio; text. |
| Recipe green | link | #264E48 | Native reference.docx word/styles.xml: style RecipeLink; text. |
| Recipe title ink | display-ink | #000000 | Native reference.docx word/styles.xml: style Title, style RecipeHeader, style RecipeContents; text. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 15.24:1 | Normal-size text contrast threshold met |
| Background / Recipe rust | 7.75:1 | Normal-size text contrast threshold met |
| Background / Recipe green | 9.27:1 | Normal-size text contrast threshold met |
| Background / Recipe title ink | 21.00:1 | Normal-size text contrast threshold met |
| Text / Recipe working row | 12.44:1 | Normal-size text contrast threshold met |
| Recipe working row / Recipe rust | 6.33:1 | Normal-size text contrast threshold met |
| Recipe working row / Recipe green | 7.56:1 | Normal-size text contrast threshold met |
| Recipe working row / Recipe title ink | 17.14:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Recipe Collection: native colors](references/recipe-collection/COLORS.md)
