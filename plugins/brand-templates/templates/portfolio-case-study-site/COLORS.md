# Case Notes · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #F5F2EC | :root --paper; reusable role derives from source variable and usage |
| Text | text | #292923 | :root --ink; reusable role derives from source variable and usage |
| Primary | primary | #973B2B | :root --accent; reusable role derives from source variable and usage |
| Surface | surface | #E9E5DC | :root --surface; reusable role derives from source variable and usage |
| Rule | rule | #B8B4AA | :root --rule; reusable role derives from source variable and usage |
| Secondary Text | secondary-text | #5D5C53 | :root --muted; reusable role derives from source variable and usage |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 13.09:1 | Normal-size text contrast threshold met |
| Background / Primary | 6.31:1 | Normal-size text contrast threshold met |
| Background / Secondary Text | 6.02:1 | Normal-size text contrast threshold met |
| Text / Surface | 11.64:1 | Normal-size text contrast threshold met |
| Text / Rule | 7.07:1 | Normal-size text contrast threshold met |
| Primary / Surface | 5.61:1 | Normal-size text contrast threshold met |
| Surface / Secondary Text | 5.35:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Portfolio Case Study: native colors](references/portfolio-case-study-site/COLORS.md)
