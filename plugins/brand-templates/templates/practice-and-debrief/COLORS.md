# Try and Reflect · colors

| Name | Role | sRGB hex | Source evidence |
| --- | --- | --- | --- |
| Reading ground | background | #FFFFFF | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Reading ink | text | #1E2933 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Identity emphasis | primary | #214BC4 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Supporting field | surface | #FFFDF7 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Secondary Text | secondary-text | #626A79 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Cover Field | cover-field | #214BC4 | Exact value observed in native source/foundations or CSS. This semantic role is a deliberate editorial identity decision after reviewing native usage; alternate cover and reading grounds are distinguished. |
| Worked example ink | secondary-text | #222B3D | Native ppt/slides/slide2.xml text A complete brief. Structural role corroborated at the native OOXML element, not assigned by palette order. |


## Reading pairs

| Pair | Computed ratio | Use |
| --- | --- | --- |
| Reading ground / Reading ink | 14.79:1 | Normal-size text contrast threshold met |
| Reading ground / Identity emphasis | 7.32:1 | Normal-size text contrast threshold met |
| Reading ground / Secondary Text | 5.44:1 | Normal-size text contrast threshold met |
| Reading ground / Cover Field | 7.32:1 | Normal-size text contrast threshold met |
| Reading ground / Worked example ink | 14.18:1 | Normal-size text contrast threshold met |
| Reading ink / Supporting field | 14.54:1 | Normal-size text contrast threshold met |
| Identity emphasis / Supporting field | 7.20:1 | Normal-size text contrast threshold met |
| Supporting field / Secondary Text | 5.35:1 | Normal-size text contrast threshold met |
| Supporting field / Cover Field | 7.20:1 | Normal-size text contrast threshold met |
| Supporting field / Worked example ink | 13.94:1 | Normal-size text contrast threshold met |

Ratios use WCAG relative luminance in sRGB. They test flat color pairs, not every rendered component. Use 4.5:1 for normal-size text and 3:1 for large text or meaningful non-text boundaries where applicable. Do not put information in color alone. For translucent layers or imagery, check the actual composited result.

The source palette is preserved; percentage usage, CMYK and Pantone equivalents are not inferred. Convert for the actual printer and paper profile, then proof. Accent colors that fail reading contrast remain decorative or need a tested background.

Machine values: [tokens.json](tokens.json). Detailed source usage:

- [Practice and Debrief: native colors](references/practice-and-debrief/COLORS.md)
