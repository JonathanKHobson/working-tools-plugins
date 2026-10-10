# Routes of Work · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #FFFFFF | body background in styles/site.css |
| Text | text | #161A23 | body color in styles/site.css |
| Primary | primary | #061CD1 | :root --blue; reusable role derives from source variable and usage |
| Surface | surface | #F3F4F7 | :root --sample; reusable role derives from source variable and usage |
| Rule | rule | #9DA6C2 | :root --rule; reusable role derives from source variable and usage |
| Secondary Text | secondary-text | #595F73 | :root --muted; reusable role derives from source variable and usage |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 17.41:1 | Normal-size text contrast threshold met |
| Background / Primary | 10.03:1 | Normal-size text contrast threshold met |
| Background / Secondary Text | 6.35:1 | Normal-size text contrast threshold met |
| Text / Surface | 15.83:1 | Normal-size text contrast threshold met |
| Text / Rule | 7.19:1 | Normal-size text contrast threshold met |
| Primary / Surface | 9.12:1 | Normal-size text contrast threshold met |
| Surface / Secondary Text | 5.77:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Audience Routed Portfolio: native colors](references/audience-routed-portfolio/COLORS.md)
