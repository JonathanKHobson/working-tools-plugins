# Trial Ledger · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #102820 | :root --paper; reusable role derives from source variable and usage |
| Text | text | #D9F4DF | :root --ink; reusable role derives from source variable and usage |
| Primary | primary | #B8DC92 | :root --accent; reusable role derives from source variable and usage |
| Surface | surface | #19392C | :root --panel; reusable role derives from source variable and usage |
| Rule | rule | #66806C | :root --rule; reusable role derives from source variable and usage |
| Secondary Text | secondary-text | #F1C989 | :root --meta; reusable role derives from source variable and usage |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 13.34:1 | Normal-size text contrast threshold met |
| Background / Primary | 10.17:1 | Normal-size text contrast threshold met |
| Background / Secondary Text | 9.99:1 | Normal-size text contrast threshold met |
| Text / Surface | 10.80:1 | Normal-size text contrast threshold met |
| Primary / Surface | 8.23:1 | Normal-size text contrast threshold met |
| Surface / Secondary Text | 8.09:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Evaluation Log Notebook: native colors](references/evaluation-log-notebook/COLORS.md)
