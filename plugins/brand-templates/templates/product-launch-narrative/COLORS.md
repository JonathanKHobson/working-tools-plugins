# Slotline · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Reading ground | background | #FFFFFF | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Reading ink | text | #171A21 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Identity emphasis | primary | #194BB7 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Secondary Text | secondary-text | #545D6D | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Supporting field | surface | #F4F5F7 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Secondary Surface | secondary-surface | #E4ECFA | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Prototype panel | surface-blue | #B6CAE9 | Native ppt/slides/slide2.xml shape solidFill. Structural role corroborated at the native OOXML element, not assigned by palette order. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Reading ground / Reading ink | 17.41:1 | Normal-size text contrast threshold met |
| Reading ground / Identity emphasis | 7.69:1 | Normal-size text contrast threshold met |
| Reading ground / Secondary Text | 6.64:1 | Normal-size text contrast threshold met |
| Reading ink / Supporting field | 15.96:1 | Normal-size text contrast threshold met |
| Reading ink / Secondary Surface | 14.66:1 | Normal-size text contrast threshold met |
| Reading ink / Prototype panel | 10.46:1 | Normal-size text contrast threshold met |
| Identity emphasis / Supporting field | 7.05:1 | Normal-size text contrast threshold met |
| Identity emphasis / Secondary Surface | 6.47:1 | Normal-size text contrast threshold met |
| Identity emphasis / Prototype panel | 4.62:1 | Normal-size text contrast threshold met |
| Secondary Text / Supporting field | 6.09:1 | Normal-size text contrast threshold met |
| Secondary Text / Secondary Surface | 5.59:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Product Launch Narrative: native colors](references/product-launch-narrative/COLORS.md)
