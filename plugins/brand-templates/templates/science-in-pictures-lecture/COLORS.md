# Light and Viewpoint · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Reading ground | background | #FBFBF9 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Reading ink | text | #404040 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Identity emphasis | primary | #1F6F5F | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Heading | heading | #171717 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Structural rule | rule | #B6B6B0 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Supporting field | surface | #E7E9E6 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Table light rule | rule-light | #D8D8D4 | Native ppt/slides/slide5.xml Cause table lower border. Structural role corroborated at the native OOXML element, not assigned by palette order. |
| Table dark rule | rule-dark | #8D8D88 | Native ppt/slides/slide5.xml Feature table upper border. Structural role corroborated at the native OOXML element, not assigned by palette order. |
| Diagram rule | rule | #999D99 | Native ppt/slides/slide3.xml shape line. Structural role corroborated at the native OOXML element, not assigned by palette order. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Reading ground / Reading ink | 10.01:1 | Normal-size text contrast threshold met |
| Reading ground / Identity emphasis | 5.80:1 | Normal-size text contrast threshold met |
| Reading ground / Heading | 17.30:1 | Normal-size text contrast threshold met |
| Reading ink / Structural rule | 5.09:1 | Normal-size text contrast threshold met |
| Reading ink / Supporting field | 8.49:1 | Normal-size text contrast threshold met |
| Reading ink / Table light rule | 7.25:1 | Normal-size text contrast threshold met |
| Identity emphasis / Supporting field | 4.92:1 | Normal-size text contrast threshold met |
| Heading / Structural rule | 8.80:1 | Normal-size text contrast threshold met |
| Heading / Supporting field | 14.68:1 | Normal-size text contrast threshold met |
| Heading / Table light rule | 12.54:1 | Normal-size text contrast threshold met |
| Heading / Table dark rule | 5.38:1 | Normal-size text contrast threshold met |
| Heading / Diagram rule | 6.52:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Science in Pictures Lecture: native colors](references/science-in-pictures-lecture/COLORS.md)
