# Hands at Work · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #F6F1E5 | :root --paper; reusable role derives from source variable and usage |
| Text | text | #173C31 | :root --ink; reusable role derives from source variable and usage |
| Primary | primary | #973F2E | :root --rust; reusable role derives from source variable and usage |
| Accent | accent | #7E3123 | Observed direct source color; this reusable accent role is an editorial choice, not an inferred original token. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 10.79:1 | Normal-size text contrast threshold met |
| Background / Primary | 6.08:1 | Normal-size text contrast threshold met |
| Background / Accent | 7.93:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Creative Workshop Offering: native colors](references/creative-workshop-offering/COLORS.md)
