# Demo Bench · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #EBECE6 | :root --paper; reusable role derives from source variable and usage |
| Text | text | #172937 | :root --ink; reusable role derives from source variable and usage |
| Primary | primary | #254DCC | :root --blue; reusable role derives from source variable and usage |
| Accent | accent | #BF421C | Observed direct source color; this reusable accent role is an editorial choice, not an inferred original token. |
| Rule | rule | #91A0AA | :root --rule; reusable role derives from source variable and usage |
| Support | support | #FFFFFF | Observed direct source color; this reusable accent role is an editorial choice, not an inferred original token. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 12.55:1 | Normal-size text contrast threshold met |
| Background / Primary | 5.87:1 | Normal-size text contrast threshold met |
| Text / Rule | 5.55:1 | Normal-size text contrast threshold met |
| Text / Support | 14.91:1 | Normal-size text contrast threshold met |
| Primary / Support | 6.97:1 | Normal-size text contrast threshold met |
| Accent / Support | 5.24:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Interactive Demo Companion: native colors](references/interactive-demo-companion/COLORS.md)
