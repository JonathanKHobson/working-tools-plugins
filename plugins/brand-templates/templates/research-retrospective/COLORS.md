# The Dated Record · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Reading ground | background | #F5F3EC | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Reading ink | text | #242B28 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Identity emphasis | primary | #923B2B | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Secondary | secondary | #365145 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Supporting field | surface | #DCE4DA | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Evidence panel | surface-white | #FFFFFF | Native ppt/slides/slide3.xml shape solidFill. Structural role corroborated at the native OOXML element, not assigned by palette order. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Reading ground / Reading ink | 13.03:1 | Normal-size text contrast threshold met |
| Reading ground / Identity emphasis | 6.56:1 | Normal-size text contrast threshold met |
| Reading ground / Secondary | 7.82:1 | Normal-size text contrast threshold met |
| Reading ink / Supporting field | 11.13:1 | Normal-size text contrast threshold met |
| Reading ink / Evidence panel | 14.47:1 | Normal-size text contrast threshold met |
| Identity emphasis / Supporting field | 5.60:1 | Normal-size text contrast threshold met |
| Identity emphasis / Evidence panel | 7.28:1 | Normal-size text contrast threshold met |
| Secondary / Supporting field | 6.68:1 | Normal-size text contrast threshold met |
| Secondary / Evidence panel | 8.68:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Research Retrospective: native colors](references/research-retrospective/COLORS.md)
