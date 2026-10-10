# Little Lunch · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #F8EFDA | ppt/slides/slide1.xml p:bg |
| Text | text | #173D34 | Dominant text-run color in source richSlides |
| Primary | primary | #A84324 | slide 2 / header-divider fill |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 10.46:1 | Normal-size text contrast threshold met |
| Background / Primary | 5.25:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Food Enterprise Story: native colors](references/food-enterprise-story/COLORS.md)
