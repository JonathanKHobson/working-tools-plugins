# The Comparison Lab · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Background | background | #F1F3F2 | ppt/slides/slide1.xml p:bg |
| Text | text | #182D34 | Dominant text-run color in source richSlides |
| Primary | primary | #026B69 | slide 1 / rail-accent fill |
| Accent | accent | #8A4B13 | Observed direct source color; this reusable accent role is an editorial choice, not an inferred original token. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Background / Text | 12.87:1 | Normal-size text contrast threshold met |
| Background / Primary | 5.69:1 | Normal-size text contrast threshold met |
| Background / Accent | 6.09:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Product Comparison Lab: native colors](references/product-comparison-lab/COLORS.md)
